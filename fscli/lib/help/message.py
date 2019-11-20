# -*- coding: utf-8 -*-

from fscli.lib.log.log import LOG
from fscli.lib.globals.runtimes import RUNTIMES

class CommonHelp:

    FUNCTION_NAME = "Function name."

    RUNTIME_STR = LOG.style("".join(RUNTIMES), bg="green")


class InitCommandHelp:

    NAME = CommonHelp.FUNCTION_NAME

    SHORT_HELP = "Initialize a JD Cloud serverless application with the template."

    RUNTIME = "Runtime of your app. Include %s." % (CommonHelp.RUNTIME_STR)

    OUTPUT_DIR = "Where to output the initialized app into"
