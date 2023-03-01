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


# endregion

# region functions
def datestring_to_datetime(date):
    """Convert any date-string format to datetime object
    
    :param date: date in string format
    :return: datetime
    """
    all_date_format = (
        '%Y%m%d', '%m%Y%d', '%m%d%Y', '%d%Y%m', '%Y%d%m', '%d%m%Y',
        '%y%m%d', '%m%y%d', '%m%d%y', '%d%y%m', '%y%d%m', '%d%m%y'
    )
    # Remove separator date chars
    date = ''.join([char for char in date if char not in r'\/-.:;'])
    for fmt in all_date_format:
        try:
            date = datetime.strptime(date, fmt)
            return date
        except ValueError:
            pass
    raise ValueError(f'{date} is not a valid date format')


def build_dateid(date, year=None, month=None, day=None, fmt='%Y%m%d'):
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

# endregion
