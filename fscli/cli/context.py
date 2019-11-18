"""
Context information passed to each CLI command
"""

import uuid
import logging
import click


class Context:
    """
    Top level context object for the CLI. Exposes common functionality required by a CLI, including logging,
    environment config parsing, debug logging etc.

    This object is passed by Click to every command that adds the proper annotation.
    Read this for more details on Click Context - http://click.pocoo.org/5/commands/#nested-handling-and-contexts
    Each command gets its own context object, but linked to both parent and child command's context, like a Linked List.

    This class itself does not rely on how Click works. It is just a plain old Python class that holds common
    properties used by every CLI command.
    """

    def __init__(self):
        """
        Initialize the context with default values
        """
        self._debug = False
        self._aws_region = None
        self._aws_profile = None
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
        return self._aws_region

    @region.setter
    def region(self, value):
        """
        Set AWS region
        """
        self._aws_region = value
        self._refresh_session()

    @property
    def profile(self):
        return self._aws_profile

    @profile.setter
    def profile(self, value):
        """
        Set AWS profile for credential resolution
        """
        self._aws_profile = value
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
        Returns the full path of the command as invoked ex: "fs local generate-event s3 put". Wrapper to
        https://click.palletsprojects.com/en/7.x/api/#click.Context.command_path

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
        Get the current Context object from Click's context stacks. This method is safe to run within the
        actual command's handler that has a ``@pass_context`` annotation. Outside of the handler, you run
        the risk of creating a new Context object which is entirely different from the Context object used by your
        command.
         .. code:
            @pass_context
            def my_command_handler(ctx):
                 # You will get the right context from within the command handler. This will also work from any
                # downstream method invoked as part of the handler.
                 this_context = Context.get_current_context()
                assert ctx == this_context
         Returns
        -------
        fscli.cli.context.Context
            Instance of this object, if we are running in a Click command. None otherwise.
        """

        # Click has the concept of Context stacks. Think of them as linked list containing custom objects that are
        # automatically accessible at different levels. We start from the Core Click context and discover the
        # SAM CLI command-specific Context object which contains values for global options used by all commands.
        #
        # https://click.palletsprojects.com/en/7.x/complex/#ensuring-object-creation
        #

        click_core_ctx = click.get_current_context()
        if click_core_ctx:
            return click_core_ctx.find_object(Context) or click_core_ctx.ensure_object(Context)

        return None