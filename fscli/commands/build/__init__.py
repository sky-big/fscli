# -*- coding: utf-8 -*-

"""
Build command
"""
import click

from fscli.cli.main import pass_context

@click.command(
    "build",
    short_help="Build an JD Cloud Serverless application code.",
    context_settings=dict(help_option_names=["-h", "--help"]),
)

@pass_context
def cli(ctx):
    print("JD Cloud Serverless Build Command")
    pass
