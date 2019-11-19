# -*- coding: utf-8 -*-

"""
Deploy command
"""
from fscli.lib.log.log import LOG
import click

from fscli.cli.main import pass_context, common_options


@click.command(
    "deploy",
    short_help="Deploy an JD Cloud Serverless application to the JD Cloud.",
    context_settings=dict(help_option_names=["-h", "--help"]),
)

@common_options
@pass_context
def cli(ctx):
    LOG.debug("JD Cloud Serverless Deploy Command")
    pass
