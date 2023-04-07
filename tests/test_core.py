#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# vim: se ts=4 et syn=python:

# created by: matteo.guadrini
# test_core -- clocking
#
#     Copyright (C) 2023 Matteo Guadrini <matteo.guadrini@hotmail.it>
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

"""Unit testing module for core logic"""
import datetime
import os
from pytest import raises
from sqlite3 import Cursor
from tempfile import gettempdir
from clocking.exception import WorkingDayError
from clocking.util import build_dateid
from clocking.core import (database_exists,
                           make_database,
                           create_configuration_table,
                           update_version,
                           add_configuration,
                           enable_configuration,
                           reset_configuration,
                           delete_configuration,
                           get_current_configuration,
                           create_working_hours_table,
                           insert_working_hours,
                           remove_working_hours,
                           delete_working_hours,
                           delete_whole_year,
                           delete_whole_month,
                           delete_user,
                           delete_database,
                           get_working_hours,
                           get_whole_year,
                           get_whole_month,
                           get_all_days,
                           print_working_table
                           )

TEMP_DB = os.path.join(gettempdir(), 'test_database.db')


# --------------------------------------------------
def test_create_database():
    """Check database creation"""
    assert make_database(TEMP_DB) is None


# --------------------------------------------------
def test_update_version():
    """Update version clocking database"""
    assert update_version(TEMP_DB)


# --------------------------------------------------
def test_database_exists():
    """Check if database exists"""
    assert database_exists(TEMP_DB)


# --------------------------------------------------
def test_configuration():
    """Operation on configuration table"""
    assert create_configuration_table(TEMP_DB)
    assert add_configuration(TEMP_DB,
                             active=True,
                             user='test',
                             location='Italy Office',
                             empty_value='X',
                             daily_hours=8.0,
                             working_days="Mon Tue Wed Thu Fri",
                             extraordinary=0.5,
                             permit_hour=1.0,
                             disease='disease',
                             holiday='holiday',
                             currency='€',
                             hour_reward=7.5,
                             extraordinary_reward=8.5,
                             food_ticket=0,
                             other_hours=0,
                             other_reward=8.0
                             )
    assert enable_configuration(TEMP_DB, row_id=1)
    assert isinstance(get_current_configuration(TEMP_DB, 'test'), tuple)
    assert get_current_configuration(TEMP_DB, 'test') == (1, 1, 'test', 'Italy Office',
                                                          'X', 8.0, 'Mon Tue Wed Thu Fri',
                                                          0.5, 1.0, 'disease',
                                                          'holiday', '€', 7.5, 8.5, 0.0,
                                                          0.0, 8.0)
    assert isinstance(get_current_configuration(TEMP_DB, 'unknown'), tuple)
    assert get_current_configuration(TEMP_DB, 'unknown') == ()
    assert reset_configuration(TEMP_DB)
    assert add_configuration(TEMP_DB,
                             active=False,
                             user='test',
                             location='Italy Office',
                             empty_value='X',
                             daily_hours=8.0,
                             working_days="Mon Tue Wed Thu Fri",
                             extraordinary=0.5,
                             permit_hour=1.0,
                             disease='disease',
                             holiday='holiday',
                             currency='€',
                             hour_reward=7.5,
                             extraordinary_reward=8.5,
                             food_ticket=0,
                             other_hours=0,
                             other_reward=8.0
                             )
    assert delete_configuration(TEMP_DB, row_id=1)


# --------------------------------------------------
def test_insert_daily_value():
    """Setting value on a user table value"""
    assert create_configuration_table(TEMP_DB)
    assert add_configuration(TEMP_DB,
                             active=True,
                             user='test',
                             location='Italy Office',
                             empty_value='X',
                             daily_hours=8.0,
                             working_days="Mon Tue Wed Thu Fri",
                             extraordinary=0.5,
                             permit_hour=1.0,
                             disease='disease',
                             holiday='holiday',
                             currency='€',
                             hour_reward=7.5,
                             extraordinary_reward=8.5,
                             food_ticket=0,
                             other_hours=0,
                             other_reward=8.0
                             )
    assert enable_configuration(TEMP_DB, row_id=1)
    (rowid, active, user, location, empty_value,
     daily_hours, working_days, extraordinary,
     permit_hour, disease, holiday, currency,
     hour_reward, extraordinary_reward, food_ticket,
     other_hours, other_reward) = get_current_configuration(TEMP_DB, 'test')
    assert create_working_hours_table(TEMP_DB, user)
    # Today inserting
    assert insert_working_hours(TEMP_DB, user, 8)
    assert insert_working_hours(TEMP_DB, user, 8, extraordinary=2)
    assert insert_working_hours(TEMP_DB, user, holiday=holiday)
    assert insert_working_hours(TEMP_DB, user, disease=disease)
    assert insert_working_hours(TEMP_DB, user, 6, permit_hour=2)
    assert insert_working_hours(TEMP_DB, user, 7, permit_hour=permit_hour)
    assert insert_working_hours(TEMP_DB, user, 8, other_hours=4.5)
    assert insert_working_hours(TEMP_DB, user, empty_value)
    # Selecting date
    assert insert_working_hours(TEMP_DB, user, 8, date='2023-02-08')
    assert insert_working_hours(TEMP_DB, user, 8, date='2023/08/02')
    assert insert_working_hours(TEMP_DB, user, 8, date='2023-08-02')
    assert insert_working_hours(TEMP_DB, user, 8, date='2023/02/08')
    assert insert_working_hours(TEMP_DB, user, 8, date='8-2-2023')
    assert insert_working_hours(TEMP_DB, user, 8, date='8/2/2023')
    assert insert_working_hours(TEMP_DB, user, 8, date='20230208', location=location)
    assert insert_working_hours(TEMP_DB, user, 8, day='8',
                                month='2', year='2023')
    assert insert_working_hours(TEMP_DB, user, 8, day=8, month=2, year=2023)


# --------------------------------------------------
def test_get_values():
    """Get values from database"""
    user = get_current_configuration(TEMP_DB, 'test')[2]
    assert insert_working_hours(TEMP_DB, user, 8, date='2023.22.08')
    assert insert_working_hours(TEMP_DB, user, 8, date='2023.23.08')
    assert isinstance(get_working_hours(TEMP_DB, user, date='2023.22.08'), Cursor)


# --------------------------------------------------
def test_print_table(capsys):
    """Print tables"""
    user = get_current_configuration(TEMP_DB, 'test')[2]
    assert insert_working_hours(TEMP_DB, user, 8, date='2023.22.08')
    assert insert_working_hours(TEMP_DB, user, 8, date='2023.23.08')
    # Print date
    print_working_table(get_working_hours(TEMP_DB, user, date='2023.22.08'))
    captured = capsys.readouterr()
    assert captured.out == """+----------+------+-------+-----+-------+-------------+----------+---------------+-------------+-------------+---------+---------+
| date_id  | year | month | day | hours | description | location | extraordinary | permit_hour | other_hours | holiday | disease |
+----------+------+-------+-----+-------+-------------+----------+---------------+-------------+-------------+---------+---------+
| 20230822 | 2023 |   8   |  22 |  8.0  |     None    |   None   |      0.0      |     0.0     |     0.0     |   None  |   None  |
+----------+------+-------+-----+-------+-------------+----------+---------------+-------------+-------------+---------+---------+
"""
    # Print whole year
    print_working_table(get_whole_year(TEMP_DB, user, year=2023))
    captured = capsys.readouterr()
    today = datetime.datetime.now()
    today_bid = build_dateid()
    today_year = today.year
    today_month = today.month
    today_day = today.day
    assert captured.out == f"""+----------+------+-------+-----+-------+-------------+--------------+---------------+-------------+-------------+---------+---------+
| date_id  | year | month | day | hours | description |   location   | extraordinary | permit_hour | other_hours | holiday | disease |
+----------+------+-------+-----+-------+-------------+--------------+---------------+-------------+-------------+---------+---------+
| 20230208 | 2023 |   2   |  8  |  8.0  |     None    |     None     |      0.0      |     0.0     |     0.0     |   None  |   None  |
| {today_bid} | {today_year} |   {today_month}   |  {today_day}  |   X   |     None    |     None     |      0.0      |     0.0     |     0.0     |   None  |   None  |
| 20230802 | 2023 |   8   |  2  |  8.0  |     None    | Italy Office |      0.0      |     0.0     |     0.0     |   None  |   None  |
| 20230822 | 2023 |   8   |  22 |  8.0  |     None    |     None     |      0.0      |     0.0     |     0.0     |   None  |   None  |
| 20230823 | 2023 |   8   |  23 |  8.0  |     None    |     None     |      0.0      |     0.0     |     0.0     |   None  |   None  |
+----------+------+-------+-----+-------+-------------+--------------+---------------+-------------+-------------+---------+---------+
"""
    # Print whole month
    print_working_table(get_whole_month(TEMP_DB, user, year=2023, month=8))
    captured = capsys.readouterr()
    assert captured.out == """+----------+------+-------+-----+-------+-------------+--------------+---------------+-------------+-------------+---------+---------+
| date_id  | year | month | day | hours | description |   location   | extraordinary | permit_hour | other_hours | holiday | disease |
+----------+------+-------+-----+-------+-------------+--------------+---------------+-------------+-------------+---------+---------+
| 20230802 | 2023 |   8   |  2  |  8.0  |     None    | Italy Office |      0.0      |     0.0     |     0.0     |   None  |   None  |
| 20230822 | 2023 |   8   |  22 |  8.0  |     None    |     None     |      0.0      |     0.0     |     0.0     |   None  |   None  |
| 20230823 | 2023 |   8   |  23 |  8.0  |     None    |     None     |      0.0      |     0.0     |     0.0     |   None  |   None  |
+----------+------+-------+-----+-------+-------------+--------------+---------------+-------------+-------------+---------+---------+
"""
    # Print all
    print_working_table(get_all_days(TEMP_DB, user))
    captured = capsys.readouterr()
    assert captured.out == f"""+----------+------+-------+-----+-------+-------------+--------------+---------------+-------------+-------------+---------+---------+
| date_id  | year | month | day | hours | description |   location   | extraordinary | permit_hour | other_hours | holiday | disease |
+----------+------+-------+-----+-------+-------------+--------------+---------------+-------------+-------------+---------+---------+
| 20230208 | 2023 |   2   |  8  |  8.0  |     None    |     None     |      0.0      |     0.0     |     0.0     |   None  |   None  |
| {today_bid} | {today_year} |   {today_month}   |  {today_day}  |   X   |     None    |     None     |      0.0      |     0.0     |     0.0     |   None  |   None  |
| 20230802 | 2023 |   8   |  2  |  8.0  |     None    | Italy Office |      0.0      |     0.0     |     0.0     |   None  |   None  |
| 20230822 | 2023 |   8   |  22 |  8.0  |     None    |     None     |      0.0      |     0.0     |     0.0     |   None  |   None  |
| 20230823 | 2023 |   8   |  23 |  8.0  |     None    |     None     |      0.0      |     0.0     |     0.0     |   None  |   None  |
+----------+------+-------+-----+-------+-------------+--------------+---------------+-------------+-------------+---------+---------+
"""
    # Print all, but sorted by date
    print_working_table(get_all_days(TEMP_DB, user), sort=True)
    captured = capsys.readouterr()
    assert captured.out == f"""+----------+------+-------+-----+-------+-------------+--------------+---------------+-------------+-------------+---------+---------+
| date_id  | year | month | day | hours | description |   location   | extraordinary | permit_hour | other_hours | holiday | disease |
+----------+------+-------+-----+-------+-------------+--------------+---------------+-------------+-------------+---------+---------+
| 20230208 | 2023 |   2   |  8  |  8.0  |     None    |     None     |      0.0      |     0.0     |     0.0     |   None  |   None  |
| {today_bid} | {today_year} |   {today_month}   |  {today_day}  |   X   |     None    |     None     |      0.0      |     0.0     |     0.0     |   None  |   None  |
| 20230802 | 2023 |   8   |  2  |  8.0  |     None    | Italy Office |      0.0      |     0.0     |     0.0     |   None  |   None  |
| 20230822 | 2023 |   8   |  22 |  8.0  |     None    |     None     |      0.0      |     0.0     |     0.0     |   None  |   None  |
| 20230823 | 2023 |   8   |  23 |  8.0  |     None    |     None     |      0.0      |     0.0     |     0.0     |   None  |   None  |
+----------+------+-------+-----+-------+-------------+--------------+---------------+-------------+-------------+---------+---------+
"""
    # Print only holidays
    assert insert_working_hours(TEMP_DB, user, date='2022:09:16', holiday='Oktoberfest')
    assert insert_working_hours(TEMP_DB, user, date='2023:09:16', holiday='Oktoberfest')
    assert insert_working_hours(TEMP_DB, user, date='2023:09:17', holiday='Oktoberfest')
    assert insert_working_hours(TEMP_DB, user, date='2023:08:15', holiday='All at the beach!')
    print_working_table(get_working_hours(TEMP_DB, user,
                                          date='2023:09:16', holiday=True))
    captured = capsys.readouterr()
    assert captured.out == """+----------+------+-------+-----+-------+-------------+----------+---------------+-------------+-------------+-------------+---------+
| date_id  | year | month | day | hours | description | location | extraordinary | permit_hour | other_hours |   holiday   | disease |
+----------+------+-------+-----+-------+-------------+----------+---------------+-------------+-------------+-------------+---------+
| 20230916 | 2023 |   9   |  16 |  0.0  |     None    |   None   |      0.0      |     0.0     |     0.0     | Oktoberfest |   None  |
+----------+------+-------+-----+-------+-------------+----------+---------------+-------------+-------------+-------------+---------+
"""
    print_working_table(get_whole_year(TEMP_DB, user, year=2023, holiday=True))
    captured = capsys.readouterr()
    assert captured.out == """+----------+------+-------+-----+-------+-------------+----------+---------------+-------------+-------------+-------------------+---------+
| date_id  | year | month | day | hours | description | location | extraordinary | permit_hour | other_hours |      holiday      | disease |
+----------+------+-------+-----+-------+-------------+----------+---------------+-------------+-------------+-------------------+---------+
| 20230815 | 2023 |   8   |  15 |  0.0  |     None    |   None   |      0.0      |     0.0     |     0.0     | All at the beach! |   None  |
| 20230916 | 2023 |   9   |  16 |  0.0  |     None    |   None   |      0.0      |     0.0     |     0.0     |    Oktoberfest    |   None  |
| 20230917 | 2023 |   9   |  17 |  0.0  |     None    |   None   |      0.0      |     0.0     |     0.0     |    Oktoberfest    |   None  |
+----------+------+-------+-----+-------+-------------+----------+---------------+-------------+-------------+-------------------+---------+
"""
    print_working_table(get_whole_month(TEMP_DB, user, year=2023,
                                        month=9, holiday=True))
    captured = capsys.readouterr()
    assert captured.out == """+----------+------+-------+-----+-------+-------------+----------+---------------+-------------+-------------+-------------+---------+
| date_id  | year | month | day | hours | description | location | extraordinary | permit_hour | other_hours |   holiday   | disease |
+----------+------+-------+-----+-------+-------------+----------+---------------+-------------+-------------+-------------+---------+
| 20230916 | 2023 |   9   |  16 |  0.0  |     None    |   None   |      0.0      |     0.0     |     0.0     | Oktoberfest |   None  |
| 20230917 | 2023 |   9   |  17 |  0.0  |     None    |   None   |      0.0      |     0.0     |     0.0     | Oktoberfest |   None  |
+----------+------+-------+-----+-------+-------------+----------+---------------+-------------+-------------+-------------+---------+
"""
    print_working_table(get_all_days(TEMP_DB, user, holiday=True))
    captured = capsys.readouterr()
    assert captured.out == """+----------+------+-------+-----+-------+-------------+----------+---------------+-------------+-------------+-------------------+---------+
| date_id  | year | month | day | hours | description | location | extraordinary | permit_hour | other_hours |      holiday      | disease |
+----------+------+-------+-----+-------+-------------+----------+---------------+-------------+-------------+-------------------+---------+
| 20220916 | 2022 |   9   |  16 |  0.0  |     None    |   None   |      0.0      |     0.0     |     0.0     |    Oktoberfest    |   None  |
| 20230815 | 2023 |   8   |  15 |  0.0  |     None    |   None   |      0.0      |     0.0     |     0.0     | All at the beach! |   None  |
| 20230916 | 2023 |   9   |  16 |  0.0  |     None    |   None   |      0.0      |     0.0     |     0.0     |    Oktoberfest    |   None  |
| 20230917 | 2023 |   9   |  17 |  0.0  |     None    |   None   |      0.0      |     0.0     |     0.0     |    Oktoberfest    |   None  |
+----------+------+-------+-----+-------+-------------+----------+---------------+-------------+-------------+-------------------+---------+
"""


# --------------------------------------------------
def test_print_table_disease(capsys):
    """Print tables with only disease"""
    user = get_current_configuration(TEMP_DB, 'test')[2]
    # Print only disease
    assert insert_working_hours(TEMP_DB, user, date='2022/09/16', disease='disease')
    assert insert_working_hours(TEMP_DB, user, date='2023/09/16', disease='fever!')
    assert insert_working_hours(TEMP_DB, user, date='2023/09/17', disease='disease')
    assert insert_working_hours(TEMP_DB, user, date='2023/08/15', disease='heachache')
    print_working_table(get_working_hours(TEMP_DB, user,
                                          date='2023:09:16', disease=True))
    captured = capsys.readouterr()
    assert captured.out == """+----------+------+-------+-----+-------+-------------+----------+---------------+-------------+-------------+---------+---------+
| date_id  | year | month | day | hours | description | location | extraordinary | permit_hour | other_hours | holiday | disease |
+----------+------+-------+-----+-------+-------------+----------+---------------+-------------+-------------+---------+---------+
| 20230916 | 2023 |   9   |  16 |  0.0  |     None    |   None   |      0.0      |     0.0     |     0.0     |   None  |  fever! |
+----------+------+-------+-----+-------+-------------+----------+---------------+-------------+-------------+---------+---------+
"""
    print_working_table(get_whole_year(TEMP_DB, user, year=2023, disease=True))
    captured = capsys.readouterr()
    assert captured.out == """+----------+------+-------+-----+-------+-------------+----------+---------------+-------------+-------------+---------+-----------+
| date_id  | year | month | day | hours | description | location | extraordinary | permit_hour | other_hours | holiday |  disease  |
+----------+------+-------+-----+-------+-------------+----------+---------------+-------------+-------------+---------+-----------+
| 20230815 | 2023 |   8   |  15 |  0.0  |     None    |   None   |      0.0      |     0.0     |     0.0     |   None  | heachache |
| 20230916 | 2023 |   9   |  16 |  0.0  |     None    |   None   |      0.0      |     0.0     |     0.0     |   None  |   fever!  |
| 20230917 | 2023 |   9   |  17 |  0.0  |     None    |   None   |      0.0      |     0.0     |     0.0     |   None  |  disease  |
+----------+------+-------+-----+-------+-------------+----------+---------------+-------------+-------------+---------+-----------+
"""
    print_working_table(get_whole_month(TEMP_DB, user, 
                                        year=2023, month=9, disease=True))
    captured = capsys.readouterr()
    assert captured.out == """+----------+------+-------+-----+-------+-------------+----------+---------------+-------------+-------------+---------+---------+
| date_id  | year | month | day | hours | description | location | extraordinary | permit_hour | other_hours | holiday | disease |
+----------+------+-------+-----+-------+-------------+----------+---------------+-------------+-------------+---------+---------+
| 20230916 | 2023 |   9   |  16 |  0.0  |     None    |   None   |      0.0      |     0.0     |     0.0     |   None  |  fever! |
| 20230917 | 2023 |   9   |  17 |  0.0  |     None    |   None   |      0.0      |     0.0     |     0.0     |   None  | disease |
+----------+------+-------+-----+-------+-------------+----------+---------------+-------------+-------------+---------+---------+
"""


# --------------------------------------------------
def test_remove_daily_value():
    """Remove value on a user table value"""
    user = get_current_configuration(TEMP_DB, 'test')[2]
    assert insert_working_hours(TEMP_DB, user, 8, date='2023-02-08')
    assert remove_working_hours(TEMP_DB, user, date='2023-02-08')
    assert insert_working_hours(TEMP_DB, user, 8, date='2023-02-08')
    assert remove_working_hours(TEMP_DB, user, date='2023-02-08')
    assert insert_working_hours(TEMP_DB, user, 8, date='2023-02-08')
    assert remove_working_hours(TEMP_DB, user, date='2023/08/02')
    assert insert_working_hours(TEMP_DB, user, 8, date='2023-02-08')
    assert remove_working_hours(TEMP_DB, user, date='2023-08-02')
    assert insert_working_hours(TEMP_DB, user, 8, date='2023-02-08')
    assert remove_working_hours(TEMP_DB, user, date='2023/02/08')
    assert insert_working_hours(TEMP_DB, user, 8, date='2023-02-08')
    assert remove_working_hours(TEMP_DB, user, date='8-2-2023')
    assert insert_working_hours(TEMP_DB, user, 8, date='2023-02-08')
    assert remove_working_hours(TEMP_DB, user, date='8/2/2023')
    assert insert_working_hours(TEMP_DB, user, 8, date='2023-02-08')
    assert remove_working_hours(TEMP_DB, user, date='20230208')
    assert insert_working_hours(TEMP_DB, user, 8, date='2023-02-08')
    assert remove_working_hours(TEMP_DB, user, day='8',
                                month='2', year='2023')
    assert insert_working_hours(TEMP_DB, user, 8, date='2023-02-08')
    assert remove_working_hours(TEMP_DB, user, day=8, month=2, year=2023)
    with raises(WorkingDayError):
        assert remove_working_hours(TEMP_DB, user, day=5, month=2, year=2023)


# --------------------------------------------------
def test_delete_values():
    """Delete values on user table"""
    user = get_current_configuration(TEMP_DB, 'test')[2]
    assert insert_working_hours(TEMP_DB, user, 8, date='2023-02-08')
    assert delete_working_hours(TEMP_DB, user, date='2023-02-08')
    assert insert_working_hours(TEMP_DB, user, 8, date='2023-02-08')
    assert delete_working_hours(TEMP_DB, user, day='8',
                                month='2', year='2023')


# --------------------------------------------------
def test_delete_more_values():
    """Delete whole year and month values on user table"""
    user = get_current_configuration(TEMP_DB, 'test')[2]
    # Delete whole year
    assert insert_working_hours(TEMP_DB, user, 8, date='2023 22 08')
    assert insert_working_hours(TEMP_DB, user, 8, date='2023 23 08')
    assert delete_whole_year(TEMP_DB, user, year=2023)
    assert insert_working_hours(TEMP_DB, user, 8, date='2023 22 08')
    assert insert_working_hours(TEMP_DB, user, 8, date='2023 23 08')
    assert delete_whole_year(TEMP_DB, user, '2023')
    assert insert_working_hours(TEMP_DB, user, 8, date='2023 22 08')
    assert insert_working_hours(TEMP_DB, user, 8, date='2023 23 08')
    assert delete_whole_year(TEMP_DB, user, 2023)
    # Delete whole month of current year
    assert insert_working_hours(TEMP_DB, user, 8, date='2023 22 08')
    assert insert_working_hours(TEMP_DB, user, 8, date='2023 23 08')
    assert delete_whole_month(TEMP_DB, user, year=2023, month=8)
    assert insert_working_hours(TEMP_DB, user, 8, date='2023 22 08')
    assert insert_working_hours(TEMP_DB, user, 8, date='2023 23 08')
    assert delete_whole_month(TEMP_DB, user, '2023', '8')
    assert insert_working_hours(TEMP_DB, user, 8, date='2023 22 08')
    assert insert_working_hours(TEMP_DB, user, 8, date='2023 23 08')
    assert delete_whole_month(TEMP_DB, user, 2023, 8)
    # Delete all user data
    assert insert_working_hours(TEMP_DB, user, 8, date='2023 22 08')
    assert insert_working_hours(TEMP_DB, user, 8, date='2023 23 08')
    assert delete_user(TEMP_DB, user)
    # Delete all
    assert delete_database(TEMP_DB) is None
