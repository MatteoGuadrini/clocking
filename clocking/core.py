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
import sqlite3
import os.path

# endregion

# region globals
__version__ = '0.0.1'


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


def make_database(database):
    """Create a blank database

    :param database: database file path
    :return: None
    """
    # Create the database connection
    conn = sqlite3.connect(database)

    # Create cursor
    cur = conn.cursor()

    # Create clocking version table
    cur.execute(r"CREATE TABLE version (version_id TEXT PRIMARY KEY, name TEXT NOT NULL);")
    # Insert version into properly table
    cur.execute(rf"INSERT INTO version (version_id, name) VALUES ('{__version__}', 'clocking');")

    # Close connection of the database
    conn.commit()
    conn.close()

# endregion
