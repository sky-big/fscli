# -*- coding: utf-8 -*-

"""
Local command
"""
import click

from fscli.cli.main import pass_context

@click.command(
    "local",
    short_help="Run an JD Cloud Serverless application locally.",
    context_settings=dict(help_option_names=["-h", "--help"]),
)

@pass_context
def cli(ctx):
    print("JD Cloud Serverless Local Command")
    pass
