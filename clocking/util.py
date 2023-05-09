#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# vim: se ts=4 et syn=python:

# created by: matteo.guadrini
# util -- clocking
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

"""clocking module that contains some utility"""

# region imports
from datetime import datetime
from sqlite3 import Cursor
from prettytable import PrettyTable
from collections import namedtuple
from .exception import UserConfigurationError

# endregion

# region globals
UserConfiguration = namedtuple('UserConfiguration', [
    'rowid', 'active', 'user', 'location', 'empty_value',
    'daily_hours', 'working_days', 'extraordinary',
    'permit_hours', 'disease', 'holiday', 'currency',
    'hour_reward', 'extraordinary_reward', 'food_ticket',
    'other_hours', 'other_reward'
])
DataTable = namedtuple('DataTable', ['data', 'table'])


# endregion

# region functions
def datestring_to_datetime(date):
    """Convert any date-string format to datetime object
    
    :param date: date in string format
    :return: datetime
    :raise: ValueError
    """
    all_date_format = (
        '%d{0}%m{0}%Y', '%d{0}%Y{0}%m', '%m{0}%Y{0}%d',
        '%m{0}%d{0}%Y', '%Y{0}%d{0}%m', '%Y{0}%m{0}%d',
        '%d{0}%m{0}%y', '%d{0}%y{0}%m', '%m{0}%y{0}%d',
        '%m{0}%d{0}%y', '%y{0}%d{0}%m', '%y{0}%m{0}%d',
        '%Y%d%m', '%Y%m%d', '%d%m%Y', '%d%Y%m', '%m%Y%d', '%m%d%Y',
        '%y%d%m', '%y%m%d', '%d%m%y', '%d%y%m', '%m%y%d', '%m%d%y'
    )
    # Try converts string into datetime object
    for sep in r'-\/ .:;':
        for fmt in all_date_format:
            # Add separator into format
            fmt = fmt.format(sep)
            try:
                date = datetime.strptime(date, fmt)
                return date
            except ValueError:
                pass
    raise ValueError(f'{date} is not a valid date format')


def build_dateid(date=None, year=None, month=None, day=None, fmt='%Y%m%d'):
    """Build date_id for database
    
    :param date: datetime object
    :param year: number represents the year
    :param month: number represents the year
    :param day: number represents the year
    :param fmt: datetime string format
    :return: str
    """
    # Build date
    if date and (year or month or day):
        print('warning: date arguments is selected first')
    if date:
        date = datestring_to_datetime(date)
    elif year and month and day:
        year, month, day = [int(i) for i in (year, month, day) if i]
        date = datetime(year=year, month=month, day=day)
    else:
        date = datetime.today()

    return date.strftime(fmt)


def split_dateid(date_id, fmt='%Y%m%d'):
    """Split date_id to year, month and day 
    
    :param date_id: string date_id object
    :param fmt: date_id string format
    :return: tuple
    """
    date = datetime.strptime(date_id, fmt).date().timetuple()
    return date.tm_year, date.tm_mon, date.tm_mday


def make_printable_table(cursor: Cursor):
    """Create a PrettyTable object from sqlite3 Cursor object
    
    :param cursor: sqlite3 Cursor object
    :return: DataTable
    """
    # Create table
    working_data = cursor.fetchall()
    working_table = PrettyTable([col[0] for col in cursor.description])
    working_table.add_rows(working_data)
    return DataTable(data=working_data, table=working_table)


def sum_rewards(data, configuration: UserConfiguration):
    """Sum working hours rewards
    
    :param data: tuple of working hours
    :param configuration: UserConfiguration object
    :return: float
    """
    # Check data contains numbers
    if not all(isinstance(row[4], (int, float))
               for row in data):
        raise ValueError('not all hours contains numbers')
    # Check configuration
    if not isinstance(configuration, UserConfiguration):
        raise UserConfigurationError(f"{type(configuration)} is not an UserConfiguration object")
    # Calculate rewards
    rewards = [str(
        sum([
            row[4] * configuration.hour_reward,
            row[7] * configuration.extraordinary_reward,
            row[8] * configuration.hour_reward,
            row[9] * configuration.other_reward,
        ]) + configuration.food_ticket if row[4] > 0 else 0
    ) + configuration.currency for row in data]

    return rewards

# endregion
