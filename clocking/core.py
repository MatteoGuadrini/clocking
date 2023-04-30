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
from prettytable import from_db_cursor
from .util import build_dateid, split_dateid
from .exception import WorkingDayError

# endregion

# region globals
__version__ = '0.0.5'


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


def delete_database(database):
    """Delete all data into database
    
    :param database: database file path
    :return: None
    """
    # Create the database connection
    with sqlite3.connect(database) as conn:
        # Create cursor
        cur = conn.cursor()

        # Get all tables into database
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
        tables = [row[0] for row in cur.fetchall()]

        # Drop all tables
        for table in tables:
            cur.execute(f"DROP TABLE IF EXISTS {table};")


def update_version(database):
    """Update clocking version into database

    :param database: database file path
    :return: bool
    """
    # Create the database connection
    with sqlite3.connect(database) as conn:
        # Create cursor
        cur = conn.cursor()

        # Delete version table
        cur.execute("DROP TABLE IF EXISTS version;")
        # Create new version table
        cur.execute("CREATE TABLE IF NOT EXISTS version (version_id TEXT PRIMARY KEY, name TEXT NOT NULL);")
        # Insert version into properly table
        cur.execute(f"INSERT INTO version (version_id, name) VALUES ('{__version__}', 'clocking');")

        result = False if cur.rowcount <= 0 else True

    return result


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
                    r"permit_hours FLOAT NOT NULL,"
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
                      permit_hours,
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
    :param permit_hours: minimum permit value
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
                    "permit_hours, disease, holiday, currency, hour_reward, extraordinary_reward,"
                    "food_ticket, other_hours, other_reward) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);",
                    (active, user, location, empty_value, daily_hours,
                     working_days, extraordinary, permit_hours, disease,
                     holiday, currency, hour_reward, extraordinary_reward,
                     food_ticket, other_hours, other_reward))

        result = False if cur.rowcount <= 0 else True

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

        # Check if configuration is already enabled
        cur.execute(r"SELECT active FROM configuration "
                    r"WHERE id = ?;", (row_id,))
        active = cur.fetchone()[0]
        if not active:

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

            result = False if cur.rowcount <= 0 else True
        else:
            result = True

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

        result = False if cur.rowcount <= 0 else True

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
                    (user,))
        result = cur.fetchone()

        return result if result else ()


def get_working_hours(database, 
                      user, 
                      date=None, 
                      day=None, 
                      month=None, 
                      year=None, 
                      holiday=False, 
                      disease=False,
                      extraordinary=False,
                      permit_hours=False,
                      other_hours=False):
    """Get working day from database

    :param database: database file path
    :param user: user in configuration table
    :param date: date for insert values
    :param day: day of the date
    :param month: month of the date
    :param year: year of the date
    :param holiday: select only holiday values
    :param disease: select only disease values
    :param extraordinary: select only extraordinary values
    :param permit_hours: select only permit hour values
    :param other_hours: select only other hour values
    :return: Cursor
    """
    # Create the database connection
    with sqlite3.connect(database) as conn:
        # Create cursor
        cur = conn.cursor()

        # Get date_id
        date_id = build_dateid(date, year, month, day)

        # Get working day
        query = f"SELECT * FROM {user} WHERE date_id='{date_id}'"
        # Check if return only holiday
        if holiday:
            query += " AND holiday IS NOT NULL"
        elif disease:
            query += " AND disease IS NOT NULL"
        elif extraordinary:
            query += " AND (extraordinary IS NOT 0 AND extraordinary IS NOT NULL)"
        elif permit_hours:
            query += " AND (permit_hours IS NOT 0 AND permit_hours IS NOT NULL)"
        elif other_hours:
            query += " AND (other_hours IS NOT 0 AND other_hours IS NOT NULL)"
        cur.execute(query)

    return cur


def get_whole_year(database, 
                   user, 
                   year, 
                   holiday=False, 
                   disease=False, 
                   extraordinary=False, 
                   permit_hours=False,
                   other_hours=False):
    """Get whole year's working days from database

    :param database: database file path
    :param user: user in configuration table
    :param year: year of the date
    :param holiday: select only holiday values
    :param disease: select only disease values
    :param extraordinary: select only extraordinary values
    :param permit_hours: select only permit hour values
    :param other_hours: select only other hour values
    :return: Cursor
    """
    # Create the database connection
    with sqlite3.connect(database) as conn:
        # Create cursor
        cur = conn.cursor()

        # Get working day from whole year
        query = f"SELECT * FROM {user} WHERE year = ?"
        # Check if return only holiday
        if holiday:
            query += " AND holiday IS NOT NULL"
        elif disease:
            query += " AND disease IS NOT NULL"
        elif extraordinary:
            query += " AND (extraordinary IS NOT 0 AND extraordinary IS NOT NULL)"
        elif permit_hours:
            query += " AND (permit_hours IS NOT 0 AND permit_hours IS NOT NULL)"
        elif other_hours:
            query += " AND (other_hours IS NOT 0 AND other_hours IS NOT NULL)"
        cur.execute(query, (year,))

    return cur


def get_whole_month(database, 
                    user, 
                    year, 
                    month, 
                    holiday=False, 
                    disease=False, 
                    extraordinary=False,
                    permit_hours=False,
                    other_hours=False):
    """Get whole month's working days from database

    :param database: database file path
    :param user: user in configuration table
    :param year: year of the date
    :param month: month of the date
    :param holiday: select only holiday values
    :param disease: select only disease values
    :param extraordinary: select only extraordinary values
    :param permit_hours: select only permit hour values
    :param other_hours: select only other hour values
    :return: Cursor
    """
    # Create the database connection
    with sqlite3.connect(database) as conn:
        # Create cursor
        cur = conn.cursor()

        # Get working day from whole month
        query = rf"SELECT * FROM {user} WHERE year = ? AND month = ?"
        # Check if return only holiday
        if holiday:
            query += " AND holiday IS NOT NULL"
        elif disease:
            query += " AND disease IS NOT NULL"
        elif extraordinary:
            query += " AND (extraordinary IS NOT 0 AND extraordinary IS NOT NULL)"
        elif permit_hours:
            query += " AND (permit_hours IS NOT 0 AND permit_hours IS NOT NULL)"
        elif other_hours:
            query += " AND (other_hours IS NOT 0 AND other_hours IS NOT NULL)"
        cur.execute(query, (year, month))

    return cur


def get_all_days(database, 
                 user, 
                 holiday=False, 
                 disease=False, 
                 extraordinary=False, 
                 permit_hours=False, 
                 other_hours=False):
    """Get all days from database
    
    :param database: database file path
    :param user: user in configuration table
    :param holiday: select only holiday values
    :param disease: select only disease values
    :param extraordinary: select only extraordinary values
    :param permit_hours: select only permit hour values
    :param other_hours: select only other hour values
    :return: Cursor
    """
    # Create the database connection
    with sqlite3.connect(database) as conn:
        # Create cursor
        cur = conn.cursor()

        # Get all working days
        query = rf"SELECT * FROM {user}"
        # Check if return only holiday
        if holiday:
            query += " WHERE holiday IS NOT NULL"
        elif disease:
            query += " WHERE disease IS NOT NULL"
        elif extraordinary:
            query += " WHERE (extraordinary IS NOT 0 AND extraordinary IS NOT NULL)"
        elif permit_hours:
            query += " WHERE (permit_hours IS NOT 0 AND permit_hours IS NOT NULL)"
        elif other_hours:
            query += " WHERE (other_hours IS NOT 0 AND other_hours IS NOT NULL)"
        cur.execute(query)

    return cur


def delete_configuration(database, row_id):
    """Delete specific configuration
    
    :param database: database file path
    :param row_id: row id
    :return: bool 
    """
    # Create the database connection
    with sqlite3.connect(database) as conn:
        # Create cursor
        cur = conn.cursor()

        # Delete specific configuration
        cur.execute(r"DELETE FROM configuration "
                    r"WHERE id = ?;", (row_id,))

        result = False if cur.rowcount <= 0 else True

    return result


def create_working_hours_table(database, user):
    """Create working hours table

    :param database: database file path
    :param user: user 
    :return: bool
    """
    # Create the database connection
    with sqlite3.connect(database) as conn:
        # Create cursor
        cur = conn.cursor()

        # Create user table
        cur.execute(rf"CREATE TABLE IF NOT EXISTS {user} ("
                    r"date_id INTEGER PRIMARY KEY,"
                    r"year INTEGER NOT NULL,"
                    r"month INTEGER NOT NULL,"
                    r"day INTEGER NOT NULL,"
                    r"hours FLOAT NOT NULL,"
                    r"description TEXT,"
                    r"location TEXT,"
                    r"extraordinary FLOAT,"
                    r"permit_hours FLOAT,"
                    r"other_hours FLOAT ,"
                    r"holiday TEXT,"
                    r"disease TEXT"
                    r");")

        # Return boolean if user table was created
        cur.execute(f"SELECT name FROM sqlite_master WHERE name='{user}'")

    return bool(cur.fetchone())


def insert_working_hours(database,
                         user,
                         hours=0,
                         description=None,
                         location=None,
                         extraordinary=0,
                         permit_hours=0,
                         other_hours=0,
                         holiday=None,
                         disease=None,
                         date=None,
                         day=None,
                         month=None,
                         year=None,
                         empty_value=None):
    """Insert working day into database
 
    :param database: database file path
    :param hours: number of working hours
    :param user: user in configuration table
    :param description: description of working day
    :param location: name of location
    :param extraordinary: extraordinary hours
    :param permit_hours: permit hours
    :param other_hours: other working hours
    :param holiday: holiday value
    :param disease: disease value
    :param date: date for insert values
    :param day: day of the date
    :param month: month of the date
    :param year: year of the date
    :param empty_value: empty value if worked hours is 0
    :return: bool
    """
    # Create the database connection
    with sqlite3.connect(database) as conn:
        # Create cursor
        cur = conn.cursor()

        # Check if user table exists
        cur.execute(f"SELECT name FROM sqlite_master WHERE name='{user}'")
        if not cur.fetchone():
            create_working_hours_table(database, user)

        # Get date_id
        date_id = build_dateid(date, year, month, day)
        year, month, day = split_dateid(date_id)

        # Check empty hours
        hours = hours if hours else empty_value if empty_value else 0

        # Check if date_id exists
        cur.execute(f"SELECT date_id FROM {user} WHERE date_id='{date_id}'")
        if not cur.fetchone():

            # Insert into database
            cur.execute(rf"INSERT INTO {user} ("
                        r"date_id, year, month, day, hours, description, location, "
                        r"extraordinary, permit_hours, other_hours, holiday, disease) "
                        r"VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);",
                        (date_id, year, month, day, hours, description, location, extraordinary, permit_hours,
                         other_hours, holiday, disease))
        else:

            # Update into database
            cur.execute(rf"UPDATE {user} "
                        r"SET hours = ?, description = ?, "
                        r"location = ?, extraordinary = ?, permit_hours = ?, "
                        r"other_hours = ?, holiday = ?, disease = ? "
                        r"WHERE date_id = ?;",
                        (hours, description, location, extraordinary,
                         permit_hours, other_hours, holiday, disease, date_id))

        result = False if cur.rowcount <= 0 else True

    return result


def remove_working_hours(database, user, date=None, day=None, month=None, year=None, empty_value=None):
    """Remove working day into database
    
    :param database: database file path
    :param user: user in configuration table
    :param date: date for insert values
    :param day: day of the date
    :param month: month of the date
    :param year: year of the date
    :param empty_value: fill empty value
    :return: bool
    """
    # Create the database connection
    with sqlite3.connect(database) as conn:
        # Create cursor
        cur = conn.cursor()

        # Get date_id
        date_id = build_dateid(date, year, month, day)

        # Check empty value
        hours = empty_value if empty_value else 0

        # Check if date_id exists
        cur.execute(f"SELECT date_id FROM {user} WHERE date_id='{date_id}'")
        if cur.fetchone():

            # Update empty day into database
            cur.execute(rf"UPDATE {user} "
                        r"SET hours = ?, description = ?, location = ?, extraordinary = ?, permit_hours = ?, "
                        r"other_hours = ?, holiday = ?, disease = ? "
                        r"WHERE date_id = ?;", (hours, None, None, 0, 0, 
                                                0, None, None, date_id))

        else:
            raise WorkingDayError(f'date_id {date_id} not exists from table "{user}" into database {database}')

        result = False if cur.rowcount <= 0 else True

    return result


def delete_working_hours(database, user, date=None, day=None, month=None, year=None):
    """Delete working day into database
    
    :param database: database file path
    :param user: user in configuration table
    :param date: date for insert values
    :param day: day of the date
    :param month: month of the date
    :param year: year of the date
    :return: bool
    """
    # Create the database connection
    with sqlite3.connect(database) as conn:
        # Create cursor
        cur = conn.cursor()

        # Get date_id
        date_id = build_dateid(date, year, month, day)

        # Check if date_id exists
        cur.execute(f"SELECT date_id FROM {user} WHERE date_id='{date_id}'")
        if cur.fetchone():
            # Delete day into database
            cur.execute(rf"DELETE FROM {user} "
                        r"WHERE date_id = ?;", (date_id,))

        result = False if cur.rowcount <= 0 else True

    return result


def delete_whole_year(database, user, year):
    """Delete whole year values into database
    
    :param database: database file path
    :param user: user in configuration table
    :param year: year of the date
    :return: bool
    """
    # Create the database connection
    with sqlite3.connect(database) as conn:
        # Create cursor
        cur = conn.cursor()

        # Delete whole year into database
        cur.execute(rf"DELETE FROM {user} "
                    r"WHERE year = ?;", (year,))

        result = False if cur.rowcount <= 0 else True

    return result


def delete_whole_month(database, user, year, month):
    """Delete whole month values into database
    
    :param database: database file path
    :param user: user in configuration table
    :param year: year of the date
    :param month: month of the date
    :return: bool
    """
    # Create the database connection
    with sqlite3.connect(database) as conn:
        # Create cursor
        cur = conn.cursor()

        # Delete whole month into database
        cur.execute(rf"DELETE FROM {user} "
                    r"WHERE year = ? "
                    r"AND month = ?;", (year, month))

        result = False if cur.rowcount <= 0 else True

    return result


def delete_user(database, user):
    """Delete all user data
    
    :param database: 
    :param user: 
    :return: 
    """
    # Create the database connection
    with sqlite3.connect(database) as conn:
        # Create cursor
        cur = conn.cursor()

        # Delete whole month into database
        cur.execute(rf"DELETE FROM {user};")

        result = False if cur.rowcount <= 0 else True

    return result


def print_working_table(cursor, sort=False, csv=False, json=False, html=False):
    """Print in stdout the working hours table 
     
    :param cursor: sqlite3 Cursor object
    :param sort: sort by date_id
    :param csv: CSV format
    :param json: Json format
    :param html: HTML format
    :return: None
    """
    working_table = from_db_cursor(cursor)
    # Sort form date_id
    if sort:
        working_table.sortby = 'date_id'
    # Check format to print
    if csv:
        print(working_table.get_csv_string())
    elif json:
        print(working_table.get_json_string())
    elif html:
        print(working_table.get_html_string())
    else:
        print(working_table)
    
    
def save_working_table(cursor, file, sort=False, csv=False, json=False):
    """Save into file the working hours table
    
    :param cursor: sqlite3 Cursor object
    :param file: file path where to save stdout
    :param sort: sort by date_id
    :param csv: CSV format
    :param json: Json format
    :return: None
    """
    working_table = from_db_cursor(cursor)
    # Sort form date_id
    if sort:
        working_table.sortby = 'date_id'
    # Write stdout into file
    with open(file, 'wt') as fh:
        # Check format to print
        if csv:
            fh.write(working_table.get_csv_string())
        elif json:
            fh.write(working_table.get_json_string())
        else:
            fh.write(working_table.get_string())
        
# endregion
