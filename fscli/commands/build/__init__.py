# -*- coding: utf-8 -*-

"""
Build command
"""
import logging
import click

from fscli.cli.main import pass_context, common_options

LOG = logging.getLogger(__name__)

@click.command(
    "build",
    short_help="Build an JD Cloud Serverless application code.",
    context_settings=dict(help_option_names=["-h", "--help"]),
)

@common_options
@pass_context
def cli(ctx):
    LOG.debug("JD Cloud Serverless Build Command")
    pass
