#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import subprocess
from re import search
from subprocess import STDOUT

import pwndbg.commands
import pwndbg.memoize
import pwndbg.wrappers

cmd_name = "checksec"

@pwndbg.wrappers.OnlyWithCommand(cmd_name)
@pwndbg.memoize.reset_on_objfile
def get_raw_out():
    local_path = pwndbg.file.get_file(pwndbg.proc.exe)
    try:
        version_output = subprocess.check_output([get_raw_out.cmd_path, "--version"], stderr=STDOUT).decode('utf-8')
        match = search('checksec v([\\w.]+),', version_output)
        if match:
            version = tuple(map(int, (match.group(1).split("."))))
            if version >= (2, 0):
                return pwndbg.wrappers.call_cmd([get_raw_out.cmd_path, "--file=" + local_path])
    except Exception:
        pass
    return pwndbg.wrappers.call_cmd([get_raw_out.cmd_path, "--file", local_path])

@pwndbg.wrappers.OnlyWithCommand(cmd_name)
def relro_status():
    relro = "No RELRO"
    out = get_raw_out()

    if "Full RELRO" in out:
        relro = "Full RELRO"
    elif "Partial RELRO" in out:
        relro = "Partial RELRO"

    return relro

@pwndbg.wrappers.OnlyWithCommand(cmd_name)
def pie_status():
    pie = "No PIE"
    out = get_raw_out()

    if "PIE enabled" in out:
        pie = "PIE enabled"

    return pie
