import logging

import asyncio
from aiohttp import web
from asyncinotify import Inotify, Mask
from pathlib import Path

from ncjsam.io import eval_dist_path
from ncjsam.tool.builder import run_build


NCJSAM_HTTP_PREFIX = '__ncjsam__'


# TODO: add version to handle race conditions
class State:
    def __init__(self, contents):
        self._contents = contents

    def contents(self):
        return self._contents


class Watch:
    def __init__(self, watch, path):
        self._watch = watch
        self._path = path
        self._mtime = self._path.stat().st_mtime
        logging.info('start watching %s "%s"',
                     'directory' if path.is_dir() else 'file',
                     path)

    def watch(self):
        return self._watch

    def test_mtime(self):
        mtime = self._path.stat().st_mtime
        if mtime > self._mtime:
            self._mtime = mtime
            return True
        return False


class LiveServer:
    def __init__(self, args):
        self._states = {}
        self._watches = {}
        self._code_revision = 0
        self._args = args

        # TODO: implement via Websocket instead polling

        dist_prefix = eval_dist_path(args.prefix, args.destination)

        self._app = web.Application()
        self._app.add_routes([
            web.get('/', self._index),
            web.get(f'/{NCJSAM_HTTP_PREFIX}/code-revision',
                    self._get_code_revision),
            web.post(f'/{NCJSAM_HTTP_PREFIX}/rebuild-prefix',
                     self._post_rebuild_prefix),
            web.get(f'/{NCJSAM_HTTP_PREFIX}/states/{{id}}',
                    self._get_state),
            web.post(f'/{NCJSAM_HTTP_PREFIX}/states/{{id}}',
                     self._post_state),
            web.delete(f'/{NCJSAM_HTTP_PREFIX}/states/{{id}}',
                       self._delete_state),
            web.static('/', dist_prefix),
        ])

    def get_daemon_context(self):
        return {
            'endpoint': f'http://{self._args.bind_ip}:{self._args.bind_port}',
        }

    def run(self):
        self._app.cleanup_ctx.append(self._run__watch_files_task)
        web.run_app(self._app,
                    host=self._args.bind_ip,
                    port=self._args.bind_port,
                    print=logging.info)

    async def _run__watch_files_task(self, app):
        task = asyncio.create_task(self._watch_files())

        yield

        task.cancel()
        await task

    async def _watch_files(self):
        with Inotify() as inotify:
            self._start_watch(Path(self._args.prefix), inotify)
            async for event in inotify:
                full_filename = LiveServer._event_abs_path(event)
                if LiveServer._skip_watch(full_filename):
                    continue
                if event.mask & Mask.MODIFY:
                    self._advance_version()
                elif event.mask & Mask.CREATE:
                    self._start_watch(full_filename, inotify)
                    self._advance_version()
                elif event.mask & (Mask.DELETE | Mask.IGNORED):
                    if full_filename in self._watches:
                        logging.info('stop watching "%s"', full_filename)
                        watch = self._watches[full_filename]
                        if watch and (event.mask & Mask.DELETE):
                            # NOTE: will cause an error in case of Mask.IGNORED
                            inotify.rm_watch(watch.watch())
                        del self._watches[full_filename]
                        self._advance_version()
                elif event.mask & Mask.MOVE:
                    pass
                elif event.mask & Mask.ATTRIB:
                    watch = self._watches.get(full_filename)
                    if watch and watch.test_mtime():
                        self._advance_version()
                else:
                    logging.warning(f'unprocessed inotify-event: {event}')

    def _start_watch(self, path: Path, inotify: Inotify):
        if path in self._watches:
            return

        if LiveServer._skip_watch(path):
            return

        if path.is_dir():
            watch = inotify.add_watch(
                path,
                Mask.CREATE | Mask.DELETE | Mask.MOVE | Mask.IGNORED
            )
            self._watches[path] = Watch(watch=watch, path=path)

            for i in LiveServer._make_watch_list(path):
                self._start_watch(i, inotify)
        else:
            watch = inotify.add_watch(
                path,
                Mask.MODIFY | Mask.IGNORED | Mask.ATTRIB
            )
            self._watches[path] = Watch(watch=watch, path=path)

    def _advance_version(self):
        self._code_revision += 1
        logging.info('code revision advanced: %d', self._code_revision)

    @staticmethod
    def _skip_watch(path: Path) -> bool:
        # this is a hack for editors like vim, who creating temporary files,
        # but this won't work reliably due to possible races, should fix it
        # someday
        if path.parts[-1][0] == '.':
            return True
        if path.parts[-1][-1] == '~':
            return True
        if path.parts[-1] in ('4913', '5036', '5159'):  # vim-related hacks
            return True
        if not path.exists():
            return True
        return False

    @staticmethod
    def _event_abs_path(event):
        result = event.watch.path
        if event.name:
            result = result / event.name
        return result

    @staticmethod
    def _make_watch_list(root_dir: Path):
        if not root_dir.exists():
            raise ValueError(f'directory not exists: "{root_dir}"')
        if not root_dir.is_dir():
            raise ValueError(f'not a directory: "{root_dir}"')
        result = [root_dir]
        for child in root_dir.iterdir():
            if child.is_dir():
                result.extend(LiveServer._make_watch_list(child))
            elif child.is_file():
                result.append(child)
        return result

    async def _index(self, request):
        return web.Response(
            status=301,
            headers={'Location': f'/index.html?{request.query_string}'},
        )

    async def _get_code_revision(self, request):
        return web.json_response({
            'revision': self._code_revision,
            'polling_interval': self._args.revision_polling_interval,
        })

    async def _post_rebuild_prefix(self, request):
        run_build(
            self._args,
            daemon_context=self.get_daemon_context(),
        )
        return web.Response()

    async def _get_state(self, request):
        state_id = request.match_info['id']
        state = self._states.get(state_id)
        if state:
            return web.json_response({
                'contents': state.contents(),
            })
        else:
            return web.Response(status=404)

    async def _post_state(self, request):
        state_id = request.match_info['id']
        state = await request.json()
        new_state = State(
            contents=state['contents'],
        )
        self._states[state_id] = new_state
        return web.Response()

    async def _delete_state(self, request):
        state_id = request.match_info['id']
        if state_id in self._states:
            del self._states[state_id]
        return web.Response()
