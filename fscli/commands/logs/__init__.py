# -*- coding: utf-8 -*-

"""
Logs command
"""
import logging
import click

from fscli.cli.main import pass_context, common_options

LOG = logging.getLogger(__name__)

@click.command(
    "logs",
    short_help="Look up an JD Cloud Serverless application log.",
    context_settings=dict(help_option_names=["-h", "--help"]),
)

@common_options
@pass_context
def cli(ctx):
    LOG.debug("JD Cloud Serverless Logs Command")
    pass
