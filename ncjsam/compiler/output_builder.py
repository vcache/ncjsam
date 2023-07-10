import os
import logging
from pprint import pformat
from datetime import datetime
from pathlib import Path
from typing import Dict, FrozenSet, Union

from jinja2 import Environment, PackageLoader
from jsmin import jsmin  # pip3 install jsmin
from pygments import highlight, lexers, formatters

from ncjsam import constants
from ncjsam.compiler.build_targets import BuildTargets
from ncjsam.compiler.modules_compiler import CompiledModules


CONTRIB_JS = [
    'es-module-shims.js',
    'three.module.js',
    'GLTFLoader.js',
    'BufferGeometryUtils.js',
    'OrbitControls.js',
    'CSS2DRenderer.js',
    'CSS3DRenderer.js',
]


def make_output(compiled_modules: CompiledModules,
                build_targets: FrozenSet[BuildTargets],
                minify_js: bool,
                daemon_context: dict,
                ) -> Dict[str, Union[str, Dict[str, str]]]:
    now = datetime.utcnow()
    outputs = {}

    jinja2_env = Environment(
        loader=PackageLoader('ncjsam.compiler'),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    jinja2_env.tests['ncjsam_dynamic_property'] = _ncjsam_dynamic_property

    assert compiled_modules.application
    cummon_dickt = {
        'ncjsam_meta_authors': compiled_modules.application.meta_info.authors,
        'ncjsam_meta_title': compiled_modules.application.meta_info.title,
        'ncjsam_meta_version': compiled_modules.application.meta_info.version,
        'ncjsam_window_title': compiled_modules.application.window.title,
        'ncjsam_version': constants.NCJSAM_VERSION,
        'ncjsam_build_datetime': now.isoformat() + 'Z',
        'ncjsam_build_year': now.year,
        'ncjsam_root_entities': compiled_modules.get_root_entities(),
        'ncjsam_assets': compiled_modules.assets,
    }

    if daemon_context:
        cummon_dickt.update({
            'ncjsam_daemon_context': daemon_context,
        })

    if BuildTargets.JS in build_targets:
        cummon_dickt.update({
            'ncjsam_entities': compiled_modules.flatten_classes,
        })
    logging.debug(
        'dict for template:\n%s',
        highlight(pformat(cummon_dickt),
                  lexers.PythonLexer(),
                  formatters.TerminalFormatter(bg='dark')))

    file_abs = os.path.abspath(__file__)
    file_dirname = os.path.dirname(file_abs)
    template_prefix = Path(file_dirname) / 'templates'

    if BuildTargets.HTML in build_targets:
        index_html = jinja2_env.get_template('index.html')
        outputs['index.html'] = index_html.render(**cummon_dickt)

    if BuildTargets.JS in build_targets:
        # Build JS templates
        main_js = jinja2_env.get_template('main.js')
        outputs['main.js'] = main_js.render(**cummon_dickt)

        # Minify generated templates
        if minify_js:
            outputs = {k: jsmin(v) for k, v in outputs.items()}

        # Minify and add contrib files
        for contrib in CONTRIB_JS:
            effective_minify_js = (
                minify_js and 'wasm' not in contrib
                and 'es-module-shims.js' not in contrib
            )
            minified_name = (
                _minified_name(contrib) if effective_minify_js else contrib
            )
            minified_path = template_prefix / minified_name
            contrib_path = template_prefix / contrib
            if (
                effective_minify_js and
                (not minified_path.exists()) or
                (_is_older(contrib_path, minified_path))
            ):
                nonmimified = contrib_path.read_text()
                minified = jsmin(nonmimified)
                minified_path.write_text(minified)
                logging.info(
                    f'minified "{minified_name}" to '
                    f'"{str(minified_path.absolute())}": '
                    f'{len(nonmimified)} bytes to {len(minified)} '
                    f'({len(minified) / len(nonmimified) * 100.0 : .2f}%)')
            outputs[contrib] = {'copy': minified_path}

    return outputs


def _minified_name(src):
    parts = src.split('.')
    return '.'.join(parts[:-1] + ['min'] + parts[-1:])


def _is_older(src: Path, dst: Path):
    src_stat = src.stat()
    dst_stat = dst.stat()
    return src_stat.st_mtime > dst_stat.st_mtime


# TODO: move it to a proper place
def _ncjsam_dynamic_property(pair):
    return type(pair[1]) == dict and 'expr' in pair[1]
