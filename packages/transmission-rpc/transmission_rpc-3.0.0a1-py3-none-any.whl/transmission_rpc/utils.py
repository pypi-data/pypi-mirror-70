# Copyright (c) 2018-2020 Trim21 <i@trim21.me>
# Copyright (c) 2008-2014 Erik Svensson <erik.public@gmail.com>
# Licensed under the MIT license.

import datetime
from typing import Any, Tuple, NamedTuple

import transmission_rpc.constants as constants
from transmission_rpc.constants import LOGGER

UNITS = ['B', 'KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB']


def format_size(size: int) -> Tuple[float, str]:
    """
    Format byte size into IEC prefixes, B, KiB, MiB ...
    """
    s = float(size)
    i = 0
    while s >= 1024.0 and i < len(UNITS):
        i += 1
        s /= 1024.0
    return s, UNITS[i]


def format_speed(size: int) -> Tuple[float, str]:
    """
    Format bytes per second speed into IEC prefixes, B/s, KiB/s, MiB/s ...
    """
    (s, unit) = format_size(size)
    return s, unit + '/s'


def format_timedelta(delta: datetime.timedelta) -> str:
    """
    Format datetime.timedelta into <days> <hours>:<minutes>:<seconds>.
    """
    minutes, seconds = divmod(delta.seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return '%d %02d:%02d:%02d' % (delta.days, hours, minutes, seconds)


def format_timestamp(timestamp: int, utc=False) -> str:
    """
    Format unix timestamp into ISO date format.
    """
    if timestamp > 0:
        if utc:
            dt_timestamp = datetime.datetime.utcfromtimestamp(timestamp)
        else:
            dt_timestamp = datetime.datetime.fromtimestamp(timestamp)
        return dt_timestamp.isoformat(' ')
    else:
        return '-'


def rpc_bool(arg: Any) -> int:
    """
    Convert between Python boolean and Transmission RPC boolean.
    """
    if isinstance(arg, str):
        try:
            arg = bool(int(arg))
        except ValueError:
            arg = arg.lower() in ['true', 'yes']
    return 1 if bool(arg) else 0


TR_TYPE_MAP = {
    'number': int,
    'string': str,
    'double': float,
    'boolean': rpc_bool,
    'array': list,
    'object': dict,
}


def make_python_name(name):
    """
    Convert Transmission RPC name to python compatible name.
    """
    return name.replace('-', '_')


def make_rpc_name(name):
    """
    Convert python compatible name to Transmission RPC name.
    """
    return name.replace('_', '-')


def argument_value_convert(method, argument, value, rpc_version):
    """
    Check and fix Transmission RPC issues with regards to methods, arguments and values.
    """
    if method in ('torrent-add', 'torrent-get', 'torrent-set'):
        args = constants.TORRENT_ARGS[method[-3:]]
    elif method in ('session-get', 'session-set'):
        args = constants.SESSION_ARGS[method[-3:]]
    else:
        return ValueError('Method "%s" not supported' % (method))
    if argument in args:
        info = args[argument]
        invalid_version = True
        while invalid_version:
            invalid_version = False
            replacement = None
            if rpc_version < info[1]:
                invalid_version = True
                replacement = info[3]
            if info[2] and info[2] <= rpc_version:
                invalid_version = True
                replacement = info[4]
            if invalid_version:
                if replacement:
                    LOGGER.warning(
                        f'Replacing requested argument "{argument}" with "{replacement}".'
                    )
                    argument = replacement
                    info = args[argument]
                else:
                    raise ValueError(
                        f'Method "{method}" Argument "{argument}" does not exist in version {rpc_version:d}.'
                    )
        return argument, TR_TYPE_MAP[info[0]](value)
    else:
        raise ValueError('Argument "%s" does not exists for method "%s".', (argument, method))


def get_arguments(method, rpc_version):
    """
    Get arguments for method in specified Transmission RPC version.
    """
    if method in ('torrent-add', 'torrent-get', 'torrent-set'):
        args = constants.TORRENT_ARGS[method[-3:]]
    elif method in ('session-get', 'session-set'):
        args = constants.SESSION_ARGS[method[-3:]]
    else:
        return ValueError('Method "%s" not supported' % (method))
    accessible = []
    for argument, info in args.items():
        valid_version = True
        if rpc_version < info[1]:
            valid_version = False
        if info[2] and info[2] <= rpc_version:
            valid_version = False
        if valid_version:
            accessible.append(argument)
    return accessible


class Field(NamedTuple):
    value: Any
    dirty: bool
