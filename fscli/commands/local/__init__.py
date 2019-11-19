# -*- coding: utf-8 -*-

"""
Local command
"""
from fscli.lib.log.log import LOG
import click

from fscli.cli.main import pass_context, common_options


@click.command(
    "local",
    short_help="Run an JD Cloud Serverless application locally.",
    context_settings=dict(help_option_names=["-h", "--help"]),
)

@common_options
@pass_context
def cli(ctx):
    LOG.debug("JD Cloud Serverless Local Command")
    pass
