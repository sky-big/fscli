# -*- coding: utf-8 -*-

"""
Deploy command
"""
import click

from fscli.cli.main import pass_context

@click.command(
    "deploy",
    short_help="Deploy an JD Cloud Serverless application to the JD Cloud.",
    context_settings=dict(help_option_names=["-h", "--help"]),
)

@pass_context
def cli(ctx):
    print("JD Cloud Serverless Deploy Command")
    pass
