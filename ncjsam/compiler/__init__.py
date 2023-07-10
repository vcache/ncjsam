import logging

from pathlib import Path
from typing import List, Dict

from ncjsam.model.module import Module
from ncjsam.compiler.build_targets import BuildTargets
from ncjsam.compiler.modules_compiler import compile_modules
from ncjsam.compiler.output_builder import make_output


def build(modules: Dict[Path, Module],
          build_targets: List[BuildTargets],
          minify_js: bool,
          daemon_context: dict,
          ) -> Dict[Path, Dict]:
    # Check preconditions
    if not modules:
        raise ValueError('no modules provide to build')
    if not build_targets:
        raise ValueError('no build targets to build')

    build_targets = frozenset(build_targets)

    # Annotate action to be performed
    logging.info(
        'building %s from %d module%s',
        '+'.join([i.name.lower() for i in build_targets]),
        len(modules),
        's' if len(modules) > 1 else '',
    )

    # Compile modules
    compiled_modules = compile_modules(modules)

    # Build final outputs
    return make_output(
        compiled_modules,
        build_targets,
        minify_js,
        daemon_context,
    )
