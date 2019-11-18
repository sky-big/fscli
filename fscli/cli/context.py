# -*- coding: utf-8 -*-

"""
Context information passed to each CLI command
"""

import uuid
import logging
import click


class Context:
    def __init__(self):
        """
        Initialize the context with default values
        """
        self._debug = False
        self._region = None
        self._session_id = str(uuid.uuid4())

    @property
    def debug(self):
        return self._debug

    @debug.setter
    def debug(self, value):
        """
        Turn on debug logging if necessary.

        :param value: Value of debug flag
        """
        self._debug = value

        if self._debug:
            # Turn on debug logging
            logging.getLogger("fscli").setLevel(logging.DEBUG)
            logging.getLogger("aws_lambda_builders").setLevel(logging.DEBUG)

    @property
    def region(self):
        return self._region

    @region.setter
    def region(self, value):
        """
        Set AWS region
        """
        self._region = value
        self._refresh_session()

    @property
    def session_id(self):
        """
        Returns the ID of this command session. This is a randomly generated UUIDv4 which will not change until the
        command terminates.
        """
        return self._session_id

    @property
    def command_path(self):
        """
        Returns
        -------
        str
            Full path of the command invoked
        """

        # Uses Click's Core Context. Note, this is different from this class, also confusingly named `Context`.
        # Click's Core Context object is the one that contains command path information.
        click_core_ctx = click.get_current_context()
        if click_core_ctx:
            return click_core_ctx.command_path

        return None

    @staticmethod
    def get_current_context():
        """
        -------
        fscli.cli.context.Context
            Instance of this object, if we are running in a Click command. None otherwise.
        """

        click_core_ctx = click.get_current_context()
        if click_core_ctx:
            return click_core_ctx.find_object(Context) or click_core_ctx.ensure_object(Context)

        return None
