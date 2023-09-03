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
from tempfile import gettempdir

prg = "clocking/cli.py"
TEMP_DB = os.path.join(gettempdir(), "test_database_cli.db")


# --------------------------------------------------
def test_exists():
    """exists cli"""

    assert os.path.isfile(prg)


# --------------------------------------------------
def test_usage():
    """usage"""

    for flag in ["-h", "--help"]:
        rv, out = getstatusoutput(f"python3 {prg} {flag}")
        assert rv == 0
        assert out.lower().startswith("usage")


# --------------------------------------------------
def test_config_usage():
    """config usage"""

    for flag in ["-h", "--help"]:
        rv, out = getstatusoutput(f"python3 {prg} config {flag}")
        assert rv == 0
        assert out.lower().startswith("usage: clocking config")


# --------------------------------------------------
def test_add_configuration():
    """Add configuration"""

    rv, out = getstatusoutput(
        f"python3 {prg} config "
        "--user test "
        f"--database {TEMP_DB} "
        "--daily-hours 8 "
        "--working-days Mon Tue Wed "
        "--hour-reward 8 "
        "--extraordinary-reward 10 "
        "--food-ticket 7 "
        "--location Milan "
        "--currency €"
    )
    assert rv == 0
    assert out == ""


# --------------------------------------------------
def test_print_configuration():
    """Print configuration"""

    # Print enabled configuration
    rv, out = getstatusoutput(
        f"python3 {prg} config --database {TEMP_DB} --user test --print"
    )
    assert rv == 0
    assert (
        out
        == """+----+--------+------+----------+-------------+-------------+--------------+---------------+--------------+---------+---------+----------+-------------+----------------------+-------------+-------------+--------------+
| id | active | user | location | empty_value | daily_hours | working_days | extraordinary | permit_hours | disease | holiday | currency | hour_reward | extraordinary_reward | food_ticket | other_hours | other_reward |
+----+--------+------+----------+-------------+-------------+--------------+---------------+--------------+---------+---------+----------+-------------+----------------------+-------------+-------------+--------------+
| 1  |   0    | test |  Milan   |  Not worked |     8.0     | Mon Tue Wed  |      1.0      |     1.0      | Disease | Holiday |    €     |     8.0     |         10.0         |     7.0     |     0.0     |     0.0      |
+----+--------+------+----------+-------------+-------------+--------------+---------------+--------------+---------+---------+----------+-------------+----------------------+-------------+-------------+--------------+"""
    )

    # Print all user configurations
    rv, out = getstatusoutput(
        f"python3 {prg} config --database {TEMP_DB} --user test --print-user"
    )
    assert rv == 0
    assert (
        out
        == """+----+--------+------+----------+-------------+-------------+--------------+---------------+--------------+---------+---------+----------+-------------+----------------------+-------------+-------------+--------------+
| id | active | user | location | empty_value | daily_hours | working_days | extraordinary | permit_hours | disease | holiday | currency | hour_reward | extraordinary_reward | food_ticket | other_hours | other_reward |
+----+--------+------+----------+-------------+-------------+--------------+---------------+--------------+---------+---------+----------+-------------+----------------------+-------------+-------------+--------------+
| 1  |   0    | test |  Milan   |  Not worked |     8.0     | Mon Tue Wed  |      1.0      |     1.0      | Disease | Holiday |    €     |     8.0     |         10.0         |     7.0     |     0.0     |     0.0      |
+----+--------+------+----------+-------------+-------------+--------------+---------------+--------------+---------+---------+----------+-------------+----------------------+-------------+-------------+--------------+"""
    )

    # Print all configurations
    rv, out = getstatusoutput(
        f"python3 {prg} config --database {TEMP_DB} --user test --print-all"
    )
    assert rv == 0
    assert (
        out
        == """+----+--------+------+----------+-------------+-------------+--------------+---------------+--------------+---------+---------+----------+-------------+----------------------+-------------+-------------+--------------+
| id | active | user | location | empty_value | daily_hours | working_days | extraordinary | permit_hours | disease | holiday | currency | hour_reward | extraordinary_reward | food_ticket | other_hours | other_reward |
+----+--------+------+----------+-------------+-------------+--------------+---------------+--------------+---------+---------+----------+-------------+----------------------+-------------+-------------+--------------+
| 1  |   0    | test |  Milan   |  Not worked |     8.0     | Mon Tue Wed  |      1.0      |     1.0      | Disease | Holiday |    €     |     8.0     |         10.0         |     7.0     |     0.0     |     0.0      |
+----+--------+------+----------+-------------+-------------+--------------+---------------+--------------+---------+---------+----------+-------------+----------------------+-------------+-------------+--------------+"""
    )


# --------------------------------------------------
def test_enable_configuration():
    """Enable configuration"""

    # Enable exists id
    rv, out = getstatusoutput(
        f"python3 {prg} config --database {TEMP_DB} --user test --select-id 1"
    )
    assert rv == 0
    assert out == ""

    # Enable non-existent id
    rv, out = getstatusoutput(
        f"python3 {prg} config --database {TEMP_DB} --user test --select-id 2"
    )
    print(out)
    assert rv == 0
    assert out == "error: load configuration id 2 failed"


# --------------------------------------------------
def test_reset_configuration():
    """Enable configuration"""

    # Reset all configuration
    rv, out = getstatusoutput(f"python3 {prg} config --database {TEMP_DB} --reset")
    assert rv == 0
    assert out == ""


# --------------------------------------------------
def test_delete_configuration():
    """Enable configuration"""

    # Reset all configuration
    rv, out = getstatusoutput(
        f"python3 {prg} config --database {TEMP_DB} --delete-id 1"
    )
    assert rv == 0
    assert out == ""


# --------------------------------------------------
def test_set_usage():
    """set usage"""

    for flag in ["-h", "--help"]:
        rv, out = getstatusoutput(f"python3 {prg} set {flag}")
        assert rv == 0
        assert out.lower().startswith("usage: clocking set")


# --------------------------------------------------
def test_delete_usage():
    """delete usage"""

    for flag in ["-h", "--help"]:
        rv, out = getstatusoutput(f"python3 {prg} delete {flag}")
        assert rv == 0
        assert out.lower().startswith("usage: clocking delete")


# --------------------------------------------------
def test_print_usage():
    """print usage"""

    for flag in ["-h", "--help"]:
        rv, out = getstatusoutput(f"python3 {prg} print {flag}")
        assert rv == 0
        assert out.lower().startswith("usage: clocking print")
