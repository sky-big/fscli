# -*- coding: utf-8 -*-

"""
JD Cloud FS CLI
"""

import logging
import json
import click

from fscli import __version__
from fscli.lib.log.fs_logging import FSCliLogger
from .options import debug_option
from .context import Context
from .command import BaseCommand

# log
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

# context
pass_context = click.make_pass_decorator(Context)


def common_options(f):
    """
    Common CLI options used by all commands. Ex: --debug
    :param f: Callback function passed by Click
    :return: Callback function
    """
    f = debug_option(f)
    return f


def print_info(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return

    click.echo(json.dumps({"version": __version__}, indent=2))

    ctx.exit()


@click.command(cls=BaseCommand)
@common_options
@click.version_option(version=__version__, prog_name="FS CLI")
@click.option("--info", is_flag=True, is_eager=True, callback=print_info, expose_value=False)
@pass_context
def cli(ctx):
    fs_cli_logger = logging.getLogger("fscli")
    fs_cli_formatter = logging.Formatter("%(message)s")

    FSCliLogger.configure_logger(fs_cli_logger, fs_cli_formatter, logging.INFO)
