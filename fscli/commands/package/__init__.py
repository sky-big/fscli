# -*- coding: utf-8 -*-

"""
Package command
"""
import click

from fscli.cli.main import pass_context

@click.command(
    "package",
    short_help="Package an JD Cloud Serverless application.",
    context_settings=dict(help_option_names=["-h", "--help"]),
)

@pass_context
def cli(ctx):
    print("JD Cloud Serverless Package Command")
    pass
