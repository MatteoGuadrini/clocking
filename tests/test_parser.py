#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# vim: se ts=4 et syn=python:

# created by: matteo.guadrini
# test_parser -- clocking-tests
#
#     Copyright (C) 2022 Matteo Guadrini <matteo.guadrini@hotmail.it>
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Unit testing module for arguments parser"""

import os
from subprocess import getstatusoutput

prg = 'clocking/cli.py'


# --------------------------------------------------
def test_exists():
    """exists cli"""

    assert os.path.isfile(prg)


# --------------------------------------------------
def test_usage():
    """usage"""

    for flag in ['-h', '--help']:
        rv, out = getstatusoutput(f'python3 {prg} {flag}')
        assert rv == 0
        assert out.lower().startswith('usage')


# --------------------------------------------------
def test_config_usage():
    """config usage"""

    for flag in ['-h', '--help']:
        rv, out = getstatusoutput(f'python3 {prg} config {flag}')
        assert rv == 0
        assert out.lower().startswith('usage: clocking config')


# --------------------------------------------------
def test_set_usage():
    """set usage"""

    for flag in ['-h', '--help']:
        rv, out = getstatusoutput(f'python3 {prg} set {flag}')
        assert rv == 0
        assert out.lower().startswith('usage: clocking set')


# --------------------------------------------------
def test_delete_usage():
    """delete usage"""

    for flag in ['-h', '--help']:
        rv, out = getstatusoutput(f'python3 {prg} delete {flag}')
        assert rv == 0
        assert out.lower().startswith('usage: clocking delete')


# --------------------------------------------------
def test_print_usage():
    """print usage"""

    for flag in ['-h', '--help']:
        rv, out = getstatusoutput(f'python3 {prg} print {flag}')
        assert rv == 0
        assert out.lower().startswith('usage: clocking print')
