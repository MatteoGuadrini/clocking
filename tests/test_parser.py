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
        "--other-hours 1 "
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
| 1  |   0    | test |  Milan   |  Not worked |     8.0     | Mon Tue Wed  |      1.0      |     1.0      | Disease | Holiday |    €     |     8.0     |         10.0         |     7.0     |     1.0     |     0.0      |
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
| 1  |   0    | test |  Milan   |  Not worked |     8.0     | Mon Tue Wed  |      1.0      |     1.0      | Disease | Holiday |    €     |     8.0     |         10.0         |     7.0     |     1.0     |     0.0      |
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
| 1  |   0    | test |  Milan   |  Not worked |     8.0     | Mon Tue Wed  |      1.0      |     1.0      | Disease | Holiday |    €     |     8.0     |         10.0         |     7.0     |     1.0     |     0.0      |
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
    assert rv == 0
    assert out == "error: load configuration id 2 failed"


# --------------------------------------------------
def test_delete_configuration():
    """Delete configuration"""

    # Delete configuration
    rv, out = getstatusoutput(
        f"python3 {prg} config --database {TEMP_DB} --delete-id 1"
    )
    assert rv == 0
    assert out == ""

    # Delete non-existent configuration
    rv, out = getstatusoutput(
        f"python3 {prg} config --database {TEMP_DB} --delete-id 2"
    )
    assert rv == 0
    assert out == "error: delete configuration id 2 failed"


# --------------------------------------------------
def test_reset_configuration():
    """Reset configurations"""

    # Reset all configurations
    test_add_configuration()
    rv, out = getstatusoutput(f"python3 {prg} config --database {TEMP_DB} --reset")
    assert rv == 0
    assert out == ""


# --------------------------------------------------
def test_all_configuration():
    """Set, enable, delete and clean"""

    # Add twice configuration for reset
    test_add_configuration()
    test_add_configuration()

    # Test all options
    rv, out = getstatusoutput(
        f"python3 {prg} config "
        "--user test "
        f"--database {TEMP_DB} "
        "--daily-hours 8 "
        "--working-days Mon Tue Wed "
        "--hour-reward 8 "
        "--other-hours 1 "
        "--extraordinary-reward 10 "
        "--food-ticket 7 "
        "--location Milan "
        "--currency € "
        "--select-id 1 "
        "--delete-id 1 "
        "--reset "
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
def test_set_working_day():
    """set working day"""

    rv, out = getstatusoutput(
        f"python3 {prg} set --database {TEMP_DB} --user test --hours 8"
    )
    assert rv == 0
    assert out == ""

    rv, out = getstatusoutput(
        f"python3 {prg} set --database {TEMP_DB} --user test --hours 9 --date '01/25/2022'"
    )
    assert rv == 0
    assert out == ""


# --------------------------------------------------
def test_set_disease():
    """set disease"""

    rv, out = getstatusoutput(
        f"python3 {prg} set --database {TEMP_DB} --user test --disease"
    )
    assert rv == 0
    assert out == ""


# --------------------------------------------------
def test_set_holiday():
    """set holiday"""

    rv, out = getstatusoutput(
        f"python3 {prg} set --database {TEMP_DB} --user test --holiday"
    )
    assert rv == 0
    assert out == ""


# --------------------------------------------------
def test_set_holiday_range():
    """set holiday range days"""

    rv, out = getstatusoutput(
        f"python3 {prg} set --database {TEMP_DB} --user test --holidays-range 1 2 3 4"
    )
    assert rv == 0
    assert out == ""


# --------------------------------------------------
def test_set_custom():
    """set custom value"""

    rv, out = getstatusoutput(
        f"python3 {prg} set --database {TEMP_DB} --user test "
        f"--date '10/09/2023' --custom 'my custom value'"
    )
    assert rv == 0
    assert out == ""


# --------------------------------------------------
def test_set_reset():
    """set reset value"""

    rv, out = getstatusoutput(
        f"python3 {prg} set --database {TEMP_DB} --user test "
        f"--date '10/09/2023' --reset"
    )
    assert rv == 0
    assert out == ""


# --------------------------------------------------
def test_set_remove():
    """remove value"""

    rv, out = getstatusoutput(
        f"python3 {prg} set --database {TEMP_DB} --user test "
        f"--date '10/09/2023' --remove"
    )
    assert rv == 0
    assert out == ""


# --------------------------------------------------
def test_set_date():
    """set with date value"""

    rv, out = getstatusoutput(
        f"python3 {prg} set --database {TEMP_DB} --user test "
        f"--hours 8 --date '11/09/2023'"
    )
    assert rv == 0
    assert out == ""


# --------------------------------------------------
def test_set_day():
    """set with day value"""

    rv, out = getstatusoutput(
        f"python3 {prg} set --database {TEMP_DB} --user test --hours 8 --day 1"
    )
    assert rv == 0
    assert out == ""
    rv, out = getstatusoutput(
        f"python3 {prg} set --database {TEMP_DB} --user test --hours 8 --day 01"
    )
    assert rv == 0
    assert out == ""


# --------------------------------------------------
def test_set_month():
    """set with month value"""

    rv, out = getstatusoutput(
        f"python3 {prg} set --database {TEMP_DB} --user test "
        f"--hours 8 --day 1 --month 1"
    )
    assert rv == 0
    assert out == ""
    rv, out = getstatusoutput(
        f"python3 {prg} set --database {TEMP_DB} --user test --hours 8 --month 1"
    )
    assert rv == 0
    assert out == ""


# --------------------------------------------------
def test_set_year():
    """set with year value"""

    rv, out = getstatusoutput(
        f"python3 {prg} set --database {TEMP_DB} --user test "
        f"--hours 8 --day 1 --month 1 --year 2020"
    )
    assert rv == 0
    assert out == ""
    rv, out = getstatusoutput(
        f"python3 {prg} set --database {TEMP_DB} --user test --hours 8 --year 2020"
    )
    assert rv == 0
    assert out == ""


# --------------------------------------------------
def test_set_all_day_formats():
    """set with all values"""

    rv, out = getstatusoutput(
        f"python3 {prg} set --database {TEMP_DB} --user test "
        f"--hours 8 --day 1 --month 1 --year 2020 --date '11/09/2022'"
    )
    assert rv == 0
    assert out == ""


# --------------------------------------------------
def test_set_extraordinary():
    """set extraordinary hours"""

    rv, out = getstatusoutput(
        f"python3 {prg} set --database {TEMP_DB} --user test "
        "--hours 8 --extraordinary 1 --day 2 --month 2 --year 2021"
    )
    assert rv == 0
    assert out == ""

    rv, out = getstatusoutput(
        f"python3 {prg} set --database {TEMP_DB} --user test "
        "--hours 8 --extraordinary 1 --day 2 --month 2"
    )
    assert rv == 0
    assert out == ""

    rv, out = getstatusoutput(
        f"python3 {prg} set --database {TEMP_DB} --user test "
        "--hours 8 --extraordinary 1"
    )
    assert rv == 0
    assert out == ""

    rv, out = getstatusoutput(
        f"python3 {prg} set --database {TEMP_DB} --user test "
        "--hours 8 --extraordinary 0.5"
    )
    assert rv == 0
    assert out == "warning: extraordinary hours must be greater than default 1.0"


# --------------------------------------------------
def test_set_permit():
    """set permit hours"""

    rv, out = getstatusoutput(
        f"python3 {prg} set --database {TEMP_DB} --user test "
        "--hours 8 --permit 1 --day 4 --month 4 --year 2022"
    )
    assert rv == 0
    assert out == ""

    rv, out = getstatusoutput(
        f"python3 {prg} set --database {TEMP_DB} --user test "
        "--hours 8 --permit 1 --day 4 --month 4"
    )
    assert rv == 0
    assert out == ""

    rv, out = getstatusoutput(
        f"python3 {prg} set --database {TEMP_DB} --user test --hours 8 --permit 1"
    )
    assert rv == 0
    assert out == ""

    rv, out = getstatusoutput(
        f"python3 {prg} set --database {TEMP_DB} --user test --hours 8 --permit 0.5"
    )
    assert rv == 0
    assert out == "warning: permit hours must be greater than default 1.0"


# --------------------------------------------------
def test_set_other():
    """set other hours"""

    rv, out = getstatusoutput(
        f"python3 {prg} set --database {TEMP_DB} --user test "
        "--hours 8 --other 1 --day 2 --month 2 --year 2021"
    )
    assert rv == 0
    assert out == ""

    rv, out = getstatusoutput(
        f"python3 {prg} set --database {TEMP_DB} --user test "
        "--hours 8 --other 1 --day 2 --month 2"
    )
    assert rv == 0
    assert out == ""

    rv, out = getstatusoutput(
        f"python3 {prg} set --database {TEMP_DB} --user test --hours 8 --other 1"
    )
    assert rv == 0
    assert out == ""

    rv, out = getstatusoutput(
        f"python3 {prg} set --database {TEMP_DB} --user test --hours 8 --other 0.5"
    )
    assert rv == 0
    assert out == "warning: other hours must be greater than default 1.0"


# --------------------------------------------------
def test_set_location():
    """set with location value"""

    rv, out = getstatusoutput(
        f"python3 {prg} set --database {TEMP_DB} --user test "
        f"--hours 8 --day 3 --month 3 --year 2020 --location 'Praga Office'"
    )
    assert rv == 0
    assert out == ""
    rv, out = getstatusoutput(
        f"python3 {prg} set --database {TEMP_DB} --user test --holiday --location 'At home!'"
    )
    assert rv == 0
    assert out == ""
    rv, out = getstatusoutput(
        f"python3 {prg} set --database {TEMP_DB} --user test "
        f"--hours 8 --day 7 --month 7 --year 2020"
    )
    assert rv == 0
    assert out == ""


# --------------------------------------------------
def test_set_description():
    """set with description value"""
    rv, out = getstatusoutput(
        f"python3 {prg} set --database {TEMP_DB} --user test --hours 8 --description 'Project: #1'"
    )
    assert rv == 0
    assert out == ""


# --------------------------------------------------
def test_set_all():
    """set with all options"""

    rv, out = getstatusoutput(
        f"python3 {prg} set --database {TEMP_DB} --user test "
        "--hours 8 --day 5 --month 5 --year 2019 --location 'Milan Office' "
        "--description 'Study Programming Python' --permit 1 --other 1 "
        "--extraordinary 1"
    )
    assert rv == 0
    assert out == "warning: no permit and extraordinary hours in the same day"


# --------------------------------------------------
def test_delete_usage():
    """delete usage"""

    for flag in ["-h", "--help"]:
        rv, out = getstatusoutput(f"python3 {prg} delete {flag}")
        assert rv == 0
        assert out.lower().startswith("usage: clocking delete")


# --------------------------------------------------
def test_delete_day():
    """delete day"""

    rv, out = getstatusoutput(
        f"python3 {prg} delete --database {TEMP_DB} --user test --day 1"
    )
    assert rv == 0
    assert out == ""

    rv, out = getstatusoutput(
        f"python3 {prg} delete --database {TEMP_DB} --user test --date 2/2/2021"
    )
    assert rv == 0
    assert out == ""


# --------------------------------------------------
def test_delete_month():
    """delete month"""

    rv, out = getstatusoutput(
        f"python3 {prg} delete --database {TEMP_DB} --user test --month 10"
    )
    assert rv == 0
    assert out == ""


# --------------------------------------------------
def test_print_usage():
    """print usage"""

    for flag in ["-h", "--help"]:
        rv, out = getstatusoutput(f"python3 {prg} print {flag}")
        assert rv == 0
        assert out.lower().startswith("usage: clocking print")
