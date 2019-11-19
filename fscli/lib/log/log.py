# -*- coding: utf-8 -*-

import click
import logging
from builtins import str as text


class LogObject:
    def __init__(self):
        self.logger = logging.getLogger()

    def debug(self, msg, *args, **kwargs):
        self.logger.debug(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        self.logger.info(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self.logger.warning(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self.logger.error(msg, *args, **kwargs)

    def exception(self, msg, *args, **kwargs):
        self.logger.exception(msg, *args, **kwargs)

    def format_message(self, msg):
        return text(msg)

    def style(self, msg, bg=None, fg=None):
        return click.style(u'%s' % msg, bg=bg, fg=fg)

    def information(self, msg):
        click.secho(self.style("[*]", bg="yellow") + self.style(u' %s' % self.format_message(msg), fg="yellow"))

    def process(self, msg):
        click.secho(self.style("[>]", bg="cyan") + self.style(u' %s' % self.format_message(msg), fg="cyan"))

LOG = LogObject()
