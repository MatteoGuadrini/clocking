#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# vim: se ts=4 et syn=python:

# created by: matteo.guadrini
# core -- clocking
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

"""Module that contains business logic of clocking command line tool"""

# region import
import os.path


# endregion

# region functions
def database_exists(database):
    """Check if database exists

    :param database: database file path
    :return: bool
    """
    # SQLite database path exists
    if not os.path.exists(database):
        return False

    # SQLite database is file
    if not os.path.isfile(database):
        return False

    # SQLite database file header is 100 bytes
    if os.path.getsize(database) < 100:
        return False

    # Is a SQLite database
    return True

# endregion
