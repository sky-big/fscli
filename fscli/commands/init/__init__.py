# -*- coding: utf-8 -*-

"""
Init command to scaffold a project app from a template
"""
import logging
import click

from fscli.cli.main import pass_context, common_options
from fscli.lib.globals.runtimes import *

LOG = logging.getLogger(__name__)

RUNTIMES_TEMPLATES = {
    RUNTIME_PYTHON27: "",
    RUNTIME_PYTHON36: "",
    RUNTIME_PYTHON37: "",
    RUNTIME_PHP7: "",
    RUNTIME_NODEJS6: "",
    RUNTIME_NODEJS8: "",
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