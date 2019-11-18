# -*- coding: utf-8 -*-

"""
Logs command
"""
import click

from fscli.cli.main import pass_context, common_options

@click.command(
    "logs",
    short_help="Look up an JD Cloud Serverless application log.",
    context_settings=dict(help_option_names=["-h", "--help"]),
)

@common_options
@pass_context
def cli(ctx):
    print("JD Cloud Serverless Logs Command")
    pass
