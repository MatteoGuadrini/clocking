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

import os
from tempfile import gettempdir
from clocking.core import (database_exists,
                           make_database,
                           create_configuration_table,
                           add_configuration,
                           enable_configuration,
                           reset_configuration,
                           get_current_configuration,
                           insert_working_hours
                           )

TEMP_DB = os.path.join(gettempdir(), 'test_database.db')


# --------------------------------------------------
def test_create_database():
    """Check database creation"""
    assert make_database(TEMP_DB) is None


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


# --------------------------------------------------
def test_insert_daily_value():
    """Setting value on a user table value"""
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
    assert enable_configuration(TEMP_DB, row_id=2)
    (rowid, active, user, location, empty_value,
     daily_hours, working_days, extraordinary,
     permit_hour, disease, holiday, currency,
     hour_reward, extraordinary_reward, food_ticket,
     other_hours, other_reward) = get_current_configuration(TEMP_DB, 'test')
    # Today inserting
    assert insert_working_hours(TEMP_DB, 8, user=user)
    assert insert_working_hours(TEMP_DB, 8, user=user, extraordinary=2)
    assert insert_working_hours(TEMP_DB, holiday=holiday, user=user)
    assert insert_working_hours(TEMP_DB, disease=disease, user=user)
    assert insert_working_hours(TEMP_DB, 6, permit_hour=2)
    assert insert_working_hours(TEMP_DB, 7, permit_hour=permit_hour)
    assert insert_working_hours(TEMP_DB, 8, other_hours=4.5)
    assert insert_working_hours(TEMP_DB, empty_value=empty_value)
    # Selecting date
    assert insert_working_hours(TEMP_DB, 8, user=user, date='2023-02-08')
    assert insert_working_hours(TEMP_DB, 8, user=user, date='2023/08/02')
    assert insert_working_hours(TEMP_DB, 8, user=user, date='2023-08-02')
    assert insert_working_hours(TEMP_DB, 8, user=user, date='2023/02/08')
    assert insert_working_hours(TEMP_DB, 8, user=user, date='08-02-2023')
    assert insert_working_hours(TEMP_DB, 8, user=user, date='08/02/2023')
    assert insert_working_hours(TEMP_DB, 8, user=user, date='20230208')
    assert insert_working_hours(TEMP_DB, 8, user=user, day='08',
                                month='02', year='2023')
    assert insert_working_hours(TEMP_DB, 8, user=user, day=8, month=2, year=2023)
    assert insert_working_hours(TEMP_DB, 8, user=user, day=8)
    assert insert_working_hours(TEMP_DB, 8, user=user, month=2)
    assert insert_working_hours(TEMP_DB, 8, user=user, year=2023)
