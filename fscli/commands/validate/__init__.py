# -*- coding: utf-8 -*-

"""
Validate command
"""
import click

from fscli.cli.main import pass_context

@click.command(
    "validate",
    short_help="Validate an JD Cloud Serverless application.",
    context_settings=dict(help_option_names=["-h", "--help"]),
)

@pass_context
def cli(ctx):
    print("JD Cloud Serverless Validate Command")
    pass
