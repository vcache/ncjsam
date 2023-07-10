from ncjsam.compiler import build
from ncjsam.compiler import BuildTargets
from ncjsam.io import fetch_sources
from ncjsam.io import write_outputs
from ncjsam.etc import inspect


def run_build(args, daemon_context=None):
    build_targets = [
        BuildTargets[i.upper()]
        for i in frozenset(args.build_targets)
    ]

    sources = fetch_sources(args.prefix)
    if args.dry_run:
        inspect.dump(sources)

    outputs = build(
        sources,
        build_targets,
        args.js_minification,
        daemon_context,
    )
    if args.dry_run:
        inspect.dump(outputs)
    else:
        write_outputs(
            outputs,
            args.prefix,
            args.destination,
        )
