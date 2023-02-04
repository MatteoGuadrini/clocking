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
    with sqlite3.connect(database) as conn:

        # Create cursor
        cur = conn.cursor()

        # Create clocking version table
        cur.execute(r"CREATE TABLE IF NOT EXISTS version (version_id TEXT PRIMARY KEY, name TEXT NOT NULL);")
        # Insert version into properly table
        cur.execute("SELECT version_id FROM version")
        if not cur.fetchone():
            cur.execute(f"INSERT INTO version (version_id, name) VALUES ('{__version__}', 'clocking');")


def create_configuration_table(database):
    """Create configuration table

    :param database: database file path
    :return: bool
    """
    # Create the database connection
    with sqlite3.connect(database) as conn:

        # Create cursor
        cur = conn.cursor()

        # Create configuration table
        cur.execute(r"CREATE TABLE IF NOT EXISTS configuration ("
                    r"id INTEGER PRIMARY KEY,"
                    r"active BOOL NOT NULL,"
                    r"user TEXT NOT NULL,"
                    r"location TEXT NOT NULL,"
                    r"empty_value TEXT NOT NULL,"
                    r"daily_hours FLOAT NOT NULL,"
                    r"working_days TEXT NOT NULL,"
                    r"extraordinary FLOAT NOT NULL,"
                    r"permit_hour FLOAT NOT NULL,"
                    r"disease TEXT NOT NULL,"
                    r"holiday TEXT NOT NULL,"
                    r"currency TEXT NOT NULL,"
                    r"hour_reward FLOAT NOT NULL,"
                    r"extraordinary_reward FLOAT NOT NULL,"
                    r"food_ticket FLOAT NOT NULL,"
                    r"other_hours FLOAT NOT NULL,"
                    r"other_reward FLOAT NOT NULL"
                    r");")

        # Return boolean if configuration table was created
        cur.execute("SELECT name FROM sqlite_master WHERE name='configuration'")
        result = True if cur.fetchone()[0] == 'configuration' else False

    return result


def add_configuration(database,
                      active,
                      user,
                      location,
                      empty_value,
                      daily_hours,
                      working_days,
                      extraordinary,
                      permit_hour,
                      disease,
                      holiday,
                      currency,
                      hour_reward,
                      extraordinary_reward,
                      food_ticket,
                      other_hours,
                      other_reward
                      ):
    """Add new configuration into database

    :param database: database file path
    :param active: configuration active boolean
    :param user: configuration user owner
    :param location: location name
    :param empty_value: replacement for empty value
    :param daily_hours: daily hours value
    :param working_days: working name's days
    :param extraordinary: minimum extraordinary value
    :param permit_hour: minimum permit value
    :param disease: disease string name
    :param holiday: holiday string name
    :param currency: currency char value
    :param hour_reward: total hour reward
    :param extraordinary_reward: total extraordinary hour reward
    :param food_ticket: food ticket reward
    :param other_hours: other hours value
    :param other_reward: other hours reward
    :return: int
    """
    # Create the database connection
    with sqlite3.connect(database) as conn:

        # Create cursor
        cur = conn.cursor()

        # Insert values into configuration table
        cur.execute("INSERT INTO configuration("
                    "active, user, location, empty_value, daily_hours, working_days, extraordinary,"
                    "permit_hour, disease, holiday, currency, hour_reward, extraordinary_reward,"
                    "food_ticket, other_hours, other_reward) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);",
                    (active, user, location, empty_value, daily_hours,
                     working_days, extraordinary, permit_hour, disease,
                     holiday, currency, hour_reward, extraordinary_reward,
                     food_ticket, other_hours, other_reward))

        result = cur.lastrowid

    return result


def enable_configuration(database, row_id):
    """Enable configuration to specific id.

    :param database: database file path
    :param row_id: row id
    :return: bool
    """
    # Create the database connection
    with sqlite3.connect(database) as conn:

        # Create cursor
        cur = conn.cursor()

        # Update active into configuration table
        cur.execute(r"UPDATE configuration "
                    r"SET active = ? "
                    r"WHERE id = ?;", (True, row_id))
        # Disable other configuration for user
        cur.execute(r"SELECT user FROM configuration "
                    r"WHERE id = ?;", (row_id,))
        user = cur.fetchone()[0]
        cur.execute(r"UPDATE configuration "
                    r"SET active = ? "
                    r"WHERE user = ? AND id != ?;", (False, user, row_id))
        result = bool(cur.rowcount) if cur.rowcount != 0 else True

    return result


def reset_configuration(database):
    """Reset configuration table with default values

    :param database: database file path
    :return: bool
    """
    # Create the database connection
    with sqlite3.connect(database) as conn:

        # Create cursor
        cur = conn.cursor()

        # Delete all rows from table
        cur.execute('DELETE FROM configuration;')

        # Insert values into configuration table
        cur.execute(r"INSERT INTO configuration("
                    r"active, user, location, empty_value, daily_hours, working_days, extraordinary,"
                    r"permit_hour, disease, holiday, currency, hour_reward, extraordinary_reward,"
                    r"food_ticket, other_hours, other_reward) "
                    r"VALUES (True, 'User', 'Office', 'not worked', "
                    r"8.0, 'Mon Tue Wed Thu Fri', 1.0, 1.0, 'Disease', 'Holiday', "
                    r"'$', 10.0, 15.0, 7.0, 0, 5.0);")
        result = bool(cur.rowcount)

    return result


def get_current_configuration(database, user):
    """Get current enabled configuration for user

    :param database: database file path
    :param user: user in configuration table
    :return: tuple
    """
    # Create the database connection
    with sqlite3.connect(database) as conn:

        # Create cursor
        cur = conn.cursor()

        # Get active configuration for user
        cur.execute(r"SELECT * FROM configuration "
                    r"WHERE user = ? AND active = 1;",
                    (user, ))
        result = cur.fetchone()

        return result if result else ()


# endregion
