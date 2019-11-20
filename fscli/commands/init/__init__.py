# -*- coding: utf-8 -*-

"""
Init command to scaffold a project app from a template
"""
from fscli.lib.log.log import LOG
import click

from fscli.cli.main import pass_context, common_options
from fscli.lib.globals.runtimes import *
from fscli.lib.help.message import InitCommandHelp as help

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
    LOG.debug("JD Cloud Serverless Init Command")
    pass