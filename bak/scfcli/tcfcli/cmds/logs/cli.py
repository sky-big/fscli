# -*- coding: utf-8 -*-

from datetime import datetime
from datetime import timedelta
from tcfcli.common.operation_msg import Operation
import tcfcli.common.base_infor as infor
from tcfcli.common import tcsam
from tcfcli.common.user_exceptions import *
from tcfcli.common.template import Template
from tcfcli.common.user_exceptions import InvalidEnvParameters
from tcfcli.common.scf_client.scf_log_client import ScfLogClient
from tcfcli.common.tcsam.tcsam_macro import TcSamMacro as tsmacro
from tcfcli.help.message import LogsHelp as help

TM_FORMAT = '%Y-%m-%d %H:%M:%S'
REGIONS = infor.REGIONS


@click.command(short_help=help.SHORT_HELP)
@click.option('-n', '--name', help=help.NAME)
@click.option('-ns', '--namespace', default="default", help=help.NAMESPACE)
@click.option('-r', '--region', default=None, help=help.REGION)
@click.option('-c', '--count', type=int, help=help.COUNT)
@click.option('-s', '--start-time', type=str, default=None, help=help.START_TIME)
@click.option('-e', '--end-time', type=str, default=None, help=help.END_TIMEE)
@click.option('-d', '--duration', type=int, default=None, help=help.DURATION)
@click.option('-f', '--failed', is_flag=True, default=False, help=help.FAILED)
@click.option('-t', '--tail', is_flag=True, default=False, help=help.TAIL)
@click.option('--no-color', '-nc', is_flag=True, default=False, help=help.NOCOLOR)
def logs(name, namespace, region, count, start_time, end_time, duration, failed, tail, no_color):
    """
    \b
    Scf cli can use the logs command to view historical or real-time logs generated by cloud functions.
    \b
    Common usage:
        \b
        * Fetch logs using the function's name
          $ scf logs -n(--name) function
        \b
        * Specify a namespace, the default value is 'default'
          $ scf logs -n function -ns(--namespace) nodefault
        \b
        * Specific time range using the -s (--starttime) and -e (--endtime) options
          $ scf logs -n function -s xxxx-xx-xx 00:00:00 -e xxxx-xx-xx 00:00:10
        \b
        * Specify a duration between starttime and current time(unit:second)
          $ scf logs -n function -d(--duration)  10
        \b
        * Fetch logs that was exceptional
          $ scf logs -n function  -f(--failed)
        \b
        * Specify region of service
          $ scf logs -n function --region ap-guangzhou
    """

    if region and region not in REGIONS:
        raise ArgsException("The region must in %s." % (", ".join(REGIONS)))
    else:
        if name is None:
            try:
                template_data = tcsam.tcsam_validate(Template.get_template_data("template.yaml"))
                resource = template_data.get(tsmacro.Resources, {})
                for ns in resource:
                    if not resource[ns]:
                        continue
                    for func in resource[ns]:
                        if func == tsmacro.Type:
                            continue
                        name = func
                        if name:
                            Operation("In this project, default function name is: %s" % func).information()
                            Operation(
                                "If you want to specify the function name, use --name, like: scf logs --name YourFunctionName").information()
                            break

            except:
                raise InvalidEnvParameters("Function name is unspecif")

        if name is None:
            raise InvalidEnvParameters("Function name is unspecif")

        if duration and (start_time or end_time):
            raise InvalidEnvParameters("Duration is conflict with (start_time, end_time)")

        if tail:
            start = datetime.now()
            end = start + timedelta(days=1)
            if count:
                end = start
                start = end - timedelta(days=1)
        else:
            start, end = _align_time(start_time, end_time, duration)
        client = ScfLogClient(name, namespace, region, failed)
        if tail and count:
            client.fetch_log_tail_c(start.strftime(TM_FORMAT), end.strftime(TM_FORMAT), count, tail)
            return
        if not count:
            count = 10000  # cloudapi limit
        client.fetch_log(start.strftime(TM_FORMAT), end.strftime(TM_FORMAT), count, tail)


def _align_time(_start, _end, _offset):
    start = end = None
    if _start:
        start = datetime.strptime(_start, TM_FORMAT)

    if _end:
        end = datetime.strptime(_end, TM_FORMAT)

    if _offset:
        end = datetime.now()
        start = end - timedelta(seconds=_offset)
    elif start and end:
        pass
    elif (not start) and (not end):
        end = datetime.now()
        start = end - timedelta(seconds=60)
    elif not start:
        raise InvalidEnvParameters("start-time name is unspecified")
    else:
        raise InvalidEnvParameters("end-time name is unspecified")

    if start >= end:
        raise InvalidEnvParameters("endtime must be greater than starttime")
    return start, end
