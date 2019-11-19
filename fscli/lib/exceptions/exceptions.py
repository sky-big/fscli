# -*- coding: utf-8 -*-

from click import ClickException


class UserException(ClickException):

    exit_code = -1
