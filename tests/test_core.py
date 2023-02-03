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
                           reset_configuration
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
