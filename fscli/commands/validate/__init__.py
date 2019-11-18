# -*- coding: utf-8 -*-

"""
Validate command
"""
import logging
import click

from fscli.cli.main import pass_context, common_options

LOG = logging.getLogger(__name__)

@click.command(
    "validate",
    short_help="Validate an JD Cloud Serverless application.",
    context_settings=dict(help_option_names=["-h", "--help"]),
)

@common_options
@pass_context
def cli(ctx):
    LOG.debug("JD Cloud Serverless Validate Command")
    pass
