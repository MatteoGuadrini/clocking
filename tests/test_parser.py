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
    assert rv == 1
    assert out == "error: load configuration id 2 failed"


# --------------------------------------------------
def test_delete_configuration():
    """Delete configuration"""

    # Delete configuration
    rv, out = getstatusoutput(
        f"python3 {prg} config --database {TEMP_DB} --delete-id 1 --force"
    )
    assert rv == 0
    assert out == ""

    # Delete non-existent configuration
    rv, out = getstatusoutput(
        f"python3 {prg} config --database {TEMP_DB} --delete-id 2 --force"
    )
    assert rv == 4
    assert out == "error: delete configuration id 2 failed"


# --------------------------------------------------
def test_reset_configuration():
    """Reset configurations"""

    # Reset all configurations
    test_add_configuration()
    rv, out = getstatusoutput(
        f"python3 {prg} config --database {TEMP_DB} --reset --force"
    )
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
        "--reset --force"
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
        f"--date '10/09/2023' --reset --force"
    )
    assert rv == 0
    assert out == ""


# --------------------------------------------------
def test_set_remove():
    """remove value"""

    rv, out = getstatusoutput(
        f"python3 {prg} set --database {TEMP_DB} --user test "
        f"--date '10/09/2023' --remove --force"
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
        f"python3 {prg} delete --database {TEMP_DB} --user test --day 1 --force"
    )
    assert rv == 0
    assert out == ""

    rv, out = getstatusoutput(
        f"python3 {prg} delete --database {TEMP_DB} --user test --date 2/2/2021 --force"
    )
    assert rv == 0
    assert out == ""

    rv, out = getstatusoutput(
        f"python3 {prg} delete --database {TEMP_DB} --user test --date 3/2/2021 --force"
    )
    assert rv == 4
    assert out == "error: working day deletion failed"


# --------------------------------------------------
def test_delete_month():
    """delete month"""

    rv, out = getstatusoutput(
        f"python3 {prg} delete --database {TEMP_DB} --user test --month 12 --force"
    )
    assert rv == 0
    assert out == ""

    rv, out = getstatusoutput(
        f"python3 {prg} delete --database {TEMP_DB} --user test --month 12 --force"
    )
    assert rv == 4
    assert out == "error: working month deletion failed"


# --------------------------------------------------
def test_delete_year():
    """delete year"""

    rv, out = getstatusoutput(
        f"python3 {prg} delete --database {TEMP_DB} --user test --year 2022 --force"
    )
    assert rv == 0
    assert out == ""

    rv, out = getstatusoutput(
        f"python3 {prg} delete --database {TEMP_DB} --user test --year 1998 --force"
    )
    assert rv == 4
    assert out == "error: working year deletion failed"


# --------------------------------------------------
def test_delete_user():
    """delete user"""

    rv, out = getstatusoutput(
        f"python3 {prg} delete --database {TEMP_DB} --user test --clear --force"
    )
    assert rv == 0
    assert out == ""

    rv, out = getstatusoutput(
        f"python3 {prg} delete --database {TEMP_DB} --user test2 --clear --force"
    )
    assert rv == 4
    assert out == "error: working user data deletion failed"


# --------------------------------------------------
def test_print_usage():
    """print usage"""

    for flag in ["-h", "--help"]:
        rv, out = getstatusoutput(f"python3 {prg} print {flag}")
        assert rv == 0
        assert out.lower().startswith("usage: clocking print")


# --------------------------------------------------
def test_print_day():
    """print day"""

    rv, out = getstatusoutput(
        f"python3 {prg} set --database {TEMP_DB} --user test --hours 9 --date '01/25/2022'"
    )
    assert rv == 0
    assert out == ""

    rv, out = getstatusoutput(
        f"python3 {prg} print --database {TEMP_DB} --user test --date '01/25/2022'"
    )
    assert rv == 0
    assert (
            out
            == """+----------+------+-------+-----+-------+-------------+----------+---------------+--------------+-------------+---------+---------+
| date_id  | year | month | day | hours | description | location | extraordinary | permit_hours | other_hours | holiday | disease |
+----------+------+-------+-----+-------+-------------+----------+---------------+--------------+-------------+---------+---------+
| 20220125 | 2022 |   1   |  25 |  8.0  |     None    |  Milan   |      1.0      |     0.0      |     0.0     |    0    |    0    |
+----------+------+-------+-----+-------+-------------+----------+---------------+--------------+-------------+---------+---------+"""
    )

    rv, out = getstatusoutput(
        f"python3 {prg} print --database {TEMP_DB} --user test --day 25 --month 1 --year 2022"
    )
    assert rv == 0
    assert (
            out
            == """+----------+------+-------+-----+-------+-------------+----------+---------------+--------------+-------------+---------+---------+
| date_id  | year | month | day | hours | description | location | extraordinary | permit_hours | other_hours | holiday | disease |
+----------+------+-------+-----+-------+-------------+----------+---------------+--------------+-------------+---------+---------+
| 20220125 | 2022 |   1   |  25 |  8.0  |     None    |  Milan   |      1.0      |     0.0      |     0.0     |    0    |    0    |
+----------+------+-------+-----+-------+-------------+----------+---------------+--------------+-------------+---------+---------+"""
    )


# --------------------------------------------------
def test_print_month():
    """print month"""

    rv, out = getstatusoutput(
        f"python3 {prg} set --database {TEMP_DB} --user test --hours 8 --date '01/24/2022'"
    )
    assert rv == 0
    assert out == ""

    rv, out = getstatusoutput(
        f"python3 {prg} print --database {TEMP_DB} --user test --year 2022 --month 1"
    )
    assert rv == 0
    assert (
            out
            == """+----------+------+-------+-----+-------+-------------+----------+---------------+--------------+-------------+---------+---------+
| date_id  | year | month | day | hours | description | location | extraordinary | permit_hours | other_hours | holiday | disease |
+----------+------+-------+-----+-------+-------------+----------+---------------+--------------+-------------+---------+---------+
| 20220124 | 2022 |   1   |  24 |  8.0  |     None    |  Milan   |      0.0      |     0.0      |     0.0     |    0    |    0    |
| 20220125 | 2022 |   1   |  25 |  8.0  |     None    |  Milan   |      1.0      |     0.0      |     0.0     |    0    |    0    |
+----------+------+-------+-----+-------+-------------+----------+---------------+--------------+-------------+---------+---------+"""
    )


# --------------------------------------------------
def test_print_year():
    """print year"""

    rv, out = getstatusoutput(
        f"python3 {prg} set --database {TEMP_DB} --user test --hours 8 --date '03/01/2022'"
    )
    assert rv == 0
    assert out == ""

    rv, out = getstatusoutput(
        f"python3 {prg} print --database {TEMP_DB} --user test --year 2022"
    )
    assert rv == 0
    assert (
            out
            == """+----------+------+-------+-----+-------+-------------+----------+---------------+--------------+-------------+---------+---------+
| date_id  | year | month | day | hours | description | location | extraordinary | permit_hours | other_hours | holiday | disease |
+----------+------+-------+-----+-------+-------------+----------+---------------+--------------+-------------+---------+---------+
| 20220103 | 2022 |   1   |  3  |  8.0  |     None    |  Milan   |      0.0      |     0.0      |     0.0     |    0    |    0    |
| 20220124 | 2022 |   1   |  24 |  8.0  |     None    |  Milan   |      0.0      |     0.0      |     0.0     |    0    |    0    |
| 20220125 | 2022 |   1   |  25 |  8.0  |     None    |  Milan   |      1.0      |     0.0      |     0.0     |    0    |    0    |
+----------+------+-------+-----+-------+-------------+----------+---------------+--------------+-------------+---------+---------+"""
    )


# --------------------------------------------------
def test_print_holiday():
    """print holiday"""

    rv, out = getstatusoutput(
        f"python3 {prg} set --database {TEMP_DB} --user test --holiday --date '04/01/2022'"
    )
    assert rv == 0
    assert out == ""

    rv, out = getstatusoutput(
        f"python3 {prg} print --database {TEMP_DB} --user test --holiday --year 2022"
    )
    assert rv == 0
    assert (
            out
            == """+----------+------+-------+-----+------------+-------------+----------+---------------+--------------+-------------+---------+---------+
| date_id  | year | month | day |   hours    | description | location | extraordinary | permit_hours | other_hours | holiday | disease |
+----------+------+-------+-----+------------+-------------+----------+---------------+--------------+-------------+---------+---------+
| 20220104 | 2022 |   1   |  4  | Not worked |     None    |  Milan   |      0.0      |     0.0      |     0.0     |    1    |    0    |
+----------+------+-------+-----+------------+-------------+----------+---------------+--------------+-------------+---------+---------+"""
    )


# --------------------------------------------------
def test_print_disease():
    """print disease"""

    rv, out = getstatusoutput(
        f"python3 {prg} set --database {TEMP_DB} --user test --disease --date '05/01/2022'"
    )
    assert rv == 0
    assert out == ""

    rv, out = getstatusoutput(
        f"python3 {prg} print --database {TEMP_DB} --user test --disease --year 2022"
    )
    assert rv == 0
    assert (
            out
            == """+----------+------+-------+-----+------------+-------------+----------+---------------+--------------+-------------+---------+---------+
| date_id  | year | month | day |   hours    | description | location | extraordinary | permit_hours | other_hours | holiday | disease |
+----------+------+-------+-----+------------+-------------+----------+---------------+--------------+-------------+---------+---------+
| 20220105 | 2022 |   1   |  5  | Not worked |   Disease   |  Milan   |      0.0      |     0.0      |     0.0     |    0    |    1    |
+----------+------+-------+-----+------------+-------------+----------+---------------+--------------+-------------+---------+---------+"""
    )


# --------------------------------------------------
def test_print_extraordinary():
    """print extraordinary"""

    rv, out = getstatusoutput(
        f"python3 {prg} set --database {TEMP_DB} --user test --hours 8 --extraordinary 1 --date '11/01/2022'"
    )
    assert rv == 0
    assert out == ""

    rv, out = getstatusoutput(
        f"python3 {prg} print --database {TEMP_DB} --user test --extraordinary --year 2022"
    )
    assert rv == 0
    assert (
            out
            == """+----------+------+-------+-----+-------+-------------+----------+---------------+--------------+-------------+---------+---------+
| date_id  | year | month | day | hours | description | location | extraordinary | permit_hours | other_hours | holiday | disease |
+----------+------+-------+-----+-------+-------------+----------+---------------+--------------+-------------+---------+---------+
| 20220111 | 2022 |   1   |  11 |  7.0  |     None    |  Milan   |      1.0      |     0.0      |     0.0     |    0    |    0    |
| 20220125 | 2022 |   1   |  25 |  8.0  |     None    |  Milan   |      1.0      |     0.0      |     0.0     |    0    |    0    |
+----------+------+-------+-----+-------+-------------+----------+---------------+--------------+-------------+---------+---------+"""
    )


# --------------------------------------------------
def test_print_permit():
    """print permit hours"""

    rv, out = getstatusoutput(
        f"python3 {prg} set --database {TEMP_DB} --user test --hours 7 --permit 1 --date '21/01/2022'"
    )
    assert rv == 0
    assert out == ""

    rv, out = getstatusoutput(
        f"python3 {prg} print --database {TEMP_DB} --user test --permit-hours --year 2022"
    )
    assert rv == 0
    assert (
            out
            == """+----------+------+-------+-----+-------+-------------+----------+---------------+--------------+-------------+---------+---------+
| date_id  | year | month | day | hours | description | location | extraordinary | permit_hours | other_hours | holiday | disease |
+----------+------+-------+-----+-------+-------------+----------+---------------+--------------+-------------+---------+---------+
| 20220121 | 2022 |   1   |  21 |  7.0  |     None    |  Milan   |      0.0      |     1.0      |     0.0     |    0    |    0    |
+----------+------+-------+-----+-------+-------------+----------+---------------+--------------+-------------+---------+---------+"""
    )


# --------------------------------------------------
def test_print_other():
    """print other hours"""

    rv, out = getstatusoutput(
        f"python3 {prg} set --database {TEMP_DB} --user test --hours 8 --other 1 --date '22/01/2022'"
    )
    assert rv == 0
    assert out == ""

    rv, out = getstatusoutput(
        f"python3 {prg} print --database {TEMP_DB} --user test "
        "--other-hours --year 2022"
    )
    assert rv == 0
    assert (
            out
            == """+----------+------+-------+-----+-------+-------------+----------+---------------+--------------+-------------+---------+---------+
| date_id  | year | month | day | hours | description | location | extraordinary | permit_hours | other_hours | holiday | disease |
+----------+------+-------+-----+-------+-------------+----------+---------------+--------------+-------------+---------+---------+
| 20220122 | 2022 |   1   |  22 |  8.0  |     None    |  Milan   |      0.0      |     0.0      |     1.0     |    0    |    0    |
+----------+------+-------+-----+-------+-------------+----------+---------------+--------------+-------------+---------+---------+"""
    )


# --------------------------------------------------
def test_print_all():
    """print all"""

    rv, out = getstatusoutput(
        f"python3 {prg} set --database {TEMP_DB} --user test --hours 8 --date '03/02/2022'"
    )
    assert rv == 0
    assert out == ""

    rv, out = getstatusoutput(
        f"python3 {prg} print --database {TEMP_DB} --user test --all"
    )
    assert rv == 0
    assert (
            out
            == """+----------+------+-------+-----+------------+-------------+----------+---------------+--------------+-------------+---------+---------+
| date_id  | year | month | day |   hours    | description | location | extraordinary | permit_hours | other_hours | holiday | disease |
+----------+------+-------+-----+------------+-------------+----------+---------------+--------------+-------------+---------+---------+
| 20220103 | 2022 |   1   |  3  |    8.0     |     None    |  Milan   |      0.0      |     0.0      |     0.0     |    0    |    0    |
| 20220104 | 2022 |   1   |  4  | Not worked |     None    |  Milan   |      0.0      |     0.0      |     0.0     |    1    |    0    |
| 20220105 | 2022 |   1   |  5  | Not worked |   Disease   |  Milan   |      0.0      |     0.0      |     0.0     |    0    |    1    |
| 20220111 | 2022 |   1   |  11 |    7.0     |     None    |  Milan   |      1.0      |     0.0      |     0.0     |    0    |    0    |
| 20220121 | 2022 |   1   |  21 |    7.0     |     None    |  Milan   |      0.0      |     1.0      |     0.0     |    0    |    0    |
| 20220122 | 2022 |   1   |  22 |    8.0     |     None    |  Milan   |      0.0      |     0.0      |     1.0     |    0    |    0    |
| 20220124 | 2022 |   1   |  24 |    8.0     |     None    |  Milan   |      0.0      |     0.0      |     0.0     |    0    |    0    |
| 20220125 | 2022 |   1   |  25 |    8.0     |     None    |  Milan   |      1.0      |     0.0      |     0.0     |    0    |    0    |
| 20220203 | 2022 |   2   |  3  |    8.0     |     None    |  Milan   |      0.0      |     0.0      |     0.0     |    0    |    0    |
+----------+------+-------+-----+------------+-------------+----------+---------------+--------------+-------------+---------+---------+"""
    )


# --------------------------------------------------
def test_print_csv():
    """print date in csv"""

    rv, out = getstatusoutput(
        f"python3 {prg} print --database {TEMP_DB} --user test "
        "--date '01/25/2022' --csv"
    )
    assert rv == 0
    assert (
            out
            == """date_id,year,month,day,hours,description,location,extraordinary,permit_hours,other_hours,holiday,disease
20220125,2022,1,25,8.0,,Milan,1.0,0.0,0.0,0,0
"""
    )


# --------------------------------------------------
def test_print_json():
    """print date in json"""

    rv, out = getstatusoutput(
        f"python3 {prg} print --database {TEMP_DB} --user test "
        "--date '01/25/2022' --json"
    )
    assert rv == 0
    assert (
            out
            == """[
    [
        "date_id",
        "year",
        "month",
        "day",
        "hours",
        "description",
        "location",
        "extraordinary",
        "permit_hours",
        "other_hours",
        "holiday",
        "disease"
    ],
    {
        "date_id": 20220125,
        "day": 25,
        "description": null,
        "disease": "0",
        "extraordinary": 1.0,
        "holiday": "0",
        "hours": 8.0,
        "location": "Milan",
        "month": 1,
        "other_hours": 0.0,
        "permit_hours": 0.0,
        "year": 2022
    }
]"""
    )


# --------------------------------------------------
def test_print_html():
    """print date in html"""

    rv, out = getstatusoutput(
        f"python3 {prg} print --database {TEMP_DB} --user test "
        "--date '01/25/2022' --html"
    )
    assert rv == 0
    assert (
            out
            == """<table>
    <thead>
        <tr>
            <th>date_id</th>
            <th>year</th>
            <th>month</th>
            <th>day</th>
            <th>hours</th>
            <th>description</th>
            <th>location</th>
            <th>extraordinary</th>
            <th>permit_hours</th>
            <th>other_hours</th>
            <th>holiday</th>
            <th>disease</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>20220125</td>
            <td>2022</td>
            <td>1</td>
            <td>25</td>
            <td>8.0</td>
            <td>None</td>
            <td>Milan</td>
            <td>1.0</td>
            <td>0.0</td>
            <td>0.0</td>
            <td>0</td>
            <td>0</td>
        </tr>
    </tbody>
</table>"""
    )


# --------------------------------------------------
def test_print_rewards():
    """print date in rewards"""

    rv, out = getstatusoutput(
        f"python3 {prg} print --database {TEMP_DB} --user test --date '01/25/2022' --rewards"
    )
    assert rv == 0
    assert (
            out
            == """+----------+------+-------+-----+-------+-------------+----------+---------------+--------------+-------------+---------+---------+---------+
| date_id  | year | month | day | hours | description | location | extraordinary | permit_hours | other_hours | holiday | disease | rewards |
+----------+------+-------+-----+-------+-------------+----------+---------------+--------------+-------------+---------+---------+---------+
| 20220125 | 2022 |   1   |  25 |  8.0  |     None    |  Milan   |      1.0      |     0.0      |     0.0     |    0    |    0    |  81.0€  |
+----------+------+-------+-----+-------+-------------+----------+---------------+--------------+-------------+---------+---------+---------+"""
    )


# --------------------------------------------------
def test_print_export():
    """export data"""

    tmp_file = '/tmp/test.txt'

    rv, out = getstatusoutput(
        f"python3 {prg} set --database {TEMP_DB} --user test --hours 9 --date '01/25/2022'"
    )
    assert rv == 0
    assert out == ""

    rv, out = getstatusoutput(
        f"python3 {prg} print --database {TEMP_DB} --user test --date '01/25/2022' --export '{tmp_file}'"
    )
    print(out)
    assert rv == 0
    assert out == ""

    assert os.path.exists(tmp_file) is True
