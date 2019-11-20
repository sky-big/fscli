# -*- coding: utf-8 -*-

"""
Package command
"""
from fscli.lib.log.log import LOG
import click

from fscli.cli.main import pass_context, common_options


@click.command(
    "package",
    short_help="Package an JD Cloud Serverless application.",
    context_settings=dict(help_option_names=["-h", "--help"]),
)

@common_options
@pass_context
def cli(ctx):
    LOG.debug("JD Cloud Serverless Package Command")
    pass