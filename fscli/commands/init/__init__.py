# -*- coding: utf-8 -*-

"""
Init command to scaffold a project app from a template
"""
from fscli.lib.log.log import LOG
import click

from fscli.cli.main import pass_context, common_options
from fscli.lib.globals.runtimes import *

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
    short_help="Init an JD Cloud Serverless application.",
    context_settings=dict(help_option_names=["-h", "--help"]),
)

@common_options
@pass_context
def cli(ctx):
    LOG.debug("JD Cloud Serverless Init Command")
    pass