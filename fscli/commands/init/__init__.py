# -*- coding: utf-8 -*-

"""
Init command to scaffold a project app from a template
"""
import os

import click
from cookiecutter.main import cookiecutter

from fscli.lib.log.log import LOG
from fscli.cli.main import pass_context, common_options
from fscli.lib.globals.runtimes import *
from fscli.lib.help.message import InitCommandHelp as help
from fscli.lib.exceptions.exceptions import UserException

RUNTIMES_TEMPLATES = {
    RUNTIME_PYTHON27: "fs-demo-python",
    RUNTIME_PYTHON36: "fs-demo-python",
    RUNTIME_PYTHON37: "fs-demo-python",
    RUNTIME_PHP7: "fs-demo-php",
    RUNTIME_NODEJS6: "fs-demo-nodejs6",
    RUNTIME_NODEJS8: "fs-demo-nodejs8",
}


@click.command(
    "init",
    short_help=help.SHORT_HELP,
    context_settings=dict(help_option_names=["-h", "--help"]),
)

@click.option('-n', '--name', default="hello_world", help=help.NAME)
@click.option('-r', '--runtime', type=str, default="python3.6", help=help.RUNTIME)
@click.option('-o', '--output-dir', default='.', type=click.Path(), help=help.OUTPUT_DIR)
@common_options
@pass_context
def cli(ctx, name, runtime, output_dir):

    _check_runtime(runtime)

    LOG.process("Initializing project...")
    template = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates", RUNTIMES_TEMPLATES[runtime])
    params = {
        "template": template,
        "output_dir": output_dir,
    }
    LOG.configuration("Project Name: %s" % name)
    LOG.configuration("Project Runtime: %s" % runtime)
    LOG.configuration("Output Dir: %s" % output_dir)
    LOG.configuration("Template Location: %s" % template)

    params["no_input"] = True
    params['extra_context'] = {'project_name': name, 'runtime': runtime}

    try:
        cookiecutter(**params)
    except Exception as e:
        raise UserException(e)

    LOG.process("Project initialization completed")


def _check_runtime(runtime):
    if runtime not in list(RUNTIMES_TEMPLATES.keys()):
        raise UserException("runtime {runtime} not support".format(runtime=runtime))