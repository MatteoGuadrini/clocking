#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# vim: se ts=4 et syn=python:

# created by: matteo.guadrini
# cli -- clocking
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

# region imports
import argparse
import os.path
import sqlite3
from getpass import getuser

from __init__ import __version__
from clocking.core import (
    database_exists,
    make_database,
    get_current_version,
    update_version,
    create_configuration_table,
    add_configuration,
    get_current_configuration,
    enable_configuration,
    reset_configuration,
    delete_configuration,
    get_configurations,
    print_configurations,
    insert_working_hours,
    remove_working_hours,
    delete_working_hours,
    delete_whole_month,
    delete_whole_year,
    delete_user,
    get_working_hours,
    print_working_table,
    get_whole_month,
    get_whole_year,
    get_all_days,
)
from clocking.util import datetime


# endregion


# region functions
def get_args():
    """Get command-line arguments

    :return: ArgumentParser
    """
    # Principal parser
    parser = argparse.ArgumentParser(
        description="tracking or monitoring worked hours",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        prog="clocking",
    )
    common_parser = argparse.ArgumentParser(add_help=False)
    common_parser.add_argument(
        "-v", "--verbose", help="enable verbosity", action="store_true"
    )
    common_parser.add_argument(
        "-V", "--version", help="print version", action="version", version=__version__
    )
    common_parser.add_argument(
        "-B",
        "--database",
        help="select database file",
        metavar="FILE",
        type=str,
        default=os.path.expanduser("~/.clocking.db"),
    )
    common_parser.add_argument(
        "-u", "--user", help="change user", metavar="USER", default=getuser()
    )
    subparser = parser.add_subparsers(
        dest="command", help="commands to run", required=True
    )

    # Config subparser
    config = subparser.add_parser(
        "config",
        help="default's configuration",
        aliases=["cfg", "c"],
        parents=[common_parser],
    )
    print_group = config.add_argument_group("print")
    print_group.add_argument(
        "-p", "--print", help="print current configuration", action="store_true"
    )
    print_group.add_argument(
        "-t", "--print-user", help="print all user configurations", action="store_true"
    )
    print_group.add_argument(
        "-a", "--print-all", help="print all configurations", action="store_true"
    )
    set_group = config.add_argument_group("set")
    set_group.add_argument(
        "-D",
        "--daily-hours",
        help="daily work hours",
        default=None,
        type=float,
        metavar="HOURS",
    )
    set_group.add_argument(
        "-N",
        "--working-days",
        help="working day's name",
        nargs=argparse.ONE_OR_MORE,
        default={"Mon", "Tue", "Wed", "Thu", "Fri"},
        choices={"Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"},
        type=str,
        metavar="STR",
    )
    set_group.add_argument(
        "-E",
        "--extraordinary",
        help="extraordinary hour value",
        default=1.0,
        type=float,
        metavar="HOURS",
    )
    set_group.add_argument(
        "-P",
        "--permit-hours",
        help="permit work hour value",
        default=1.0,
        type=float,
        metavar="HOURS",
    )
    set_group.add_argument(
        "-S",
        "--disease",
        help="disease value",
        default="Disease",
        type=str,
        metavar="STR",
    )
    set_group.add_argument(
        "-H",
        "--holiday",
        help="holiday value",
        default="Holiday",
        type=str,
        metavar="STR",
    )
    set_group.add_argument(
        "-C",
        "--currency",
        help="currency value",
        default="$",
        type=str,
        metavar="SYMBOL",
    )
    set_group.add_argument(
        "-R",
        "--hour-reward",
        help="hour reward",
        default=10.0,
        type=float,
        metavar="NUMBER",
    )
    set_group.add_argument(
        "-W",
        "--extraordinary-reward",
        help="extraordinary hour reward",
        default=15.0,
        type=float,
        metavar="NUMBER",
    )
    set_group.add_argument(
        "-F",
        "--food-ticket",
        help="food ticket reward",
        default=0,
        type=float,
        metavar="NUMBER",
    )
    set_group.add_argument(
        "-U",
        "--other-hours",
        help="other worked hours",
        default=0,
        type=float,
        metavar="VALUE",
    )
    set_group.add_argument(
        "-O",
        "--other-reward",
        help="other reward",
        default=0,
        type=float,
        metavar="NUMBER",
    )
    set_group.add_argument(
        "-L",
        "--location",
        help="current location",
        default="Office",
        type=str,
        metavar="LOCATION",
    )
    set_group.add_argument(
        "-e",
        "--empty-value",
        help="fill empty date with value",
        default="Not worked",
        metavar="VALUE",
    )
    selection_group = config.add_argument_group("selection")
    selection_group.add_argument(
        "-i",
        "--select-id",
        help="load configuration selecting id",
        type=int,
        metavar="ID",
    )
    reset_group = config.add_argument_group("reset")
    reset_group.add_argument(
        "-r", "--reset", help="reset all with default values", action="store_true"
    )
    delete_group = config.add_argument_group("delete")
    delete_group.add_argument(
        "-d",
        "--delete-id",
        help="delete configuration selecting id",
        type=int,
        metavar="ID",
    )
    delete_group.add_argument(
        "-f",
        "--force",
        help="force delete action without prompt confirmation",
        action="store_true",
    )

    # Set subparser
    set_parse = subparser.add_parser(
        "set", help="setting values", aliases=["st", "s"], parents=[common_parser]
    )
    daily_value_group = set_parse.add_mutually_exclusive_group(required=True)
    daily_value_group.add_argument(
        "-w", "--hours", help="set worked hours", default=None, type=float
    )
    daily_value_group.add_argument(
        "-s", "--disease", help="set disease day", action="store_true"
    )
    daily_value_group.add_argument(
        "-H", "--holiday", help="set holiday day", action="store_true"
    )
    daily_value_group.add_argument(
        "-G",
        "--holidays-range",
        help="set holiday days",
        metavar="DAY[1-31]",
        nargs="+",
        choices=range(1, 32),
        type=int,
    )
    daily_value_group.add_argument(
        "-c",
        "--custom",
        help="set fill selected date with custom value",
        metavar="VALUE",
    )
    daily_value_group.add_argument(
        "-r",
        "--reset",
        help="reset current date with default fill empty value",
        action="store_true",
    )
    daily_value_group.add_argument(
        "-R",
        "--remove",
        help="remove values date",
        action="store_true",
    )
    set_parse.add_argument(
        "-f",
        "--force",
        help="force delete action without prompt confirmation",
        action="store_true",
    )
    set_parse.add_argument("-D", "--date", help="set date", metavar="DATE")
    set_parse.add_argument(
        "-d",
        "--day",
        help="set day",
        choices=range(1, 32),
        metavar="DAY[1-31]",
        type=int,
    )
    set_parse.add_argument(
        "-m",
        "--month",
        help="set month",
        choices=range(1, 13),
        metavar="MONTH[1-12]",
        type=int,
    )
    set_parse.add_argument("-y", "--year", help="set year", metavar="YEAR", type=int)
    set_parse.add_argument(
        "-e",
        "--extraordinary",
        help="set extraordinary hours",
        type=float,
        metavar="HOURS",
    )
    set_parse.add_argument(
        "-o", "--other", help="set other hours", type=float, metavar="HOURS"
    )
    set_parse.add_argument("-l", "--location", help="set current location", type=str)
    set_parse.add_argument(
        "-p",
        "--permit",
        help="set permit work hour value",
        type=float,
        metavar="HOURS",
    )
    set_parse.add_argument("-t", "--description", help="set description", type=str)

    # Delete subparser
    deleting_parse = subparser.add_parser(
        "delete", help="remove values", aliases=["del", "d"], parents=[common_parser]
    )
    deleting_group = deleting_parse.add_mutually_exclusive_group(required=True)
    deleting_group.add_argument(
        "-D", "--date", help="delete specific date", metavar="DATE"
    )
    deleting_group.add_argument(
        "-d",
        "--day",
        help="delete whole month",
        type=int,
        choices=range(1, 32),
        metavar="DAY[1-31]",
    )
    deleting_group.add_argument(
        "-M",
        "--month",
        help="delete whole month",
        type=int,
        choices=range(1, 13),
        metavar="MONTH[1-12]",
    )
    deleting_group.add_argument(
        "-Y", "--year", help="delete whole year", type=int, metavar="YEAR"
    )
    deleting_group.add_argument(
        "-C", "--clear", help="clear all data for user", action="store_true"
    )
    deleting_parse.add_argument(
        "-f",
        "--force",
        help="force delete action without prompt confirmation",
        action="store_true",
    )

    # Print subparser
    printing_parse = subparser.add_parser(
        "print", help="print values", aliases=["prt", "p"], parents=[common_parser]
    )
    printing_parse.add_argument(
        "-D", "--date", help="print specific date", metavar="DATE"
    )
    printing_parse.add_argument(
        "-d",
        "--day",
        help="print specific day",
        choices=range(1, 32),
        metavar="DAY[1-31]",
        type=int,
    )
    printing_parse.add_argument(
        "-Y", "--year", help="print whole year", type=int, metavar="YEAR"
    )
    printing_parse.add_argument(
        "-M",
        "--month",
        help="print whole month",
        type=int,
        choices=range(1, 32),
        metavar="MONTH[1-12]",
    )
    printing_parse.add_argument(
        "-U", "--all", help="print whole user data", action="store_true"
    )
    printing_fmt_group = printing_parse.add_mutually_exclusive_group()
    printing_fmt_group.add_argument(
        "-c", "--csv", help="print in csv format", action="store_true"
    )
    printing_fmt_group.add_argument(
        "-j", "--json", help="print in json format", action="store_true"
    )
    printing_fmt_group.add_argument(
        "-m", "--html", help="print in html format", action="store_true"
    )
    printing_selection_group = printing_parse.add_mutually_exclusive_group()
    printing_selection_group.add_argument(
        "-H", "--holiday", help="print only holidays", action="store_true"
    )
    printing_selection_group.add_argument(
        "-s", "--disease", help="print only diseases", action="store_true"
    )
    printing_selection_group.add_argument(
        "-e",
        "--extraordinary",
        help="print only extraordinaries hours",
        action="store_true",
    )
    printing_selection_group.add_argument(
        "-o", "--other", help="print only other hours", action="store_true"
    )
    printing_selection_group.add_argument(
        "-p", "--permit-hour", help="print only permit hours", action="store_true"
    )
    printing_parse.add_argument(
        "-E",
        "--export",
        help="suppress output and export value into file",
        metavar="FILE",
    )
    printing_parse.add_argument(
        "-r", "--rewards", help="print rewards", action="store_true"
    )

    args = parser.parse_args()
    return args


def vprint(*messages, verbose=False):
    """Print verbose messages

    :param messages: messages to print
    :param verbose: verbosity boolean
    :return: None
    """
    # Set level message
    level = "debug:"
    # Print level and all messages
    if verbose:
        print(level, *messages)


def confirm(message, default="n"):
    """
    Ask user to enter Y or N (case-insensitive).
    :message: message to print
    :default: default answer
    :return: True if the answer is Y.
    :rtype: bool
    """
    while answer := None not in ["y", "n"]:
        answer = input(
            "{0}\nTo continue? {1}".format(
                message, "[Y/n]" if default == "y" else "[y/N]"
            )
        ).lower()
        # Check if default
        if not answer:
            answer = default
            break
    return answer == "y"


def check_default_hours(hours, default, t=""):
    """Check if hours value is into defaults

    :param hours: hour values
    :param default: default hour values
    :param t: type of hours
    :return: float
    """
    if default:
        if hours / default < 1.0:
            hours = 0
            print(f"warning: {t} hours must be greater than default {default}")
    return hours


def find_extraordinary_hours(hours, default):
    """Find extraordinary hours into worked hours

    :param hours: hour values
    :param default: default hour values
    :return: float
    """
    extraordinary = 0
    if hours > default:
        extraordinary = hours - default
    return extraordinary


def configuration(**options):
    """Configuration function

    :param options: options dictionary
    :return: None
    """
    db = options.get("database")
    verbosity = options.get("verbose")
    user = options.get("user")
    # Get force for deletion
    force = options.get("force")
    vprint("check configuration table", verbose=verbosity)
    create_configuration_table(db)
    # Delete configuration
    if options.get("delete_id"):
        vprint(f"delete configuration id {options.get('delete_id')}", verbose=verbosity)
        if force or confirm(f"Delete configuration id {options.get('delete_id')}."):
            if not delete_configuration(db, options.get("delete_id")):
                print(
                    f"error: delete configuration id {options.get('delete_id')} failed"
                )
                exit(4)
    # Reset configurations
    if options.get("reset"):
        vprint("reset configuration table", verbose=verbosity)
        if force or confirm("Reset configuration table."):
            if not reset_configuration(db):
                print("error: reset configuration table failed or table is empty")
                exit(4)
    # Create new configuration
    if options.get("daily_hours"):
        vprint("create new configuration", verbose=verbosity)
        add_configuration(
            db,
            False,
            user,
            options.get("location"),
            options.get("empty_value"),
            options.get("daily_hours"),
            " ".join(day for day in options.get("working_days")),
            options.get("extraordinary"),
            options.get("permit_hours"),
            options.get("disease"),
            options.get("holiday"),
            options.get("currency"),
            options.get("hour_reward"),
            options.get("extraordinary_reward"),
            options.get("food_ticket"),
            options.get("other_hours"),
            options.get("other_reward"),
        )
    # Enable configuration
    if options.get("select_id"):
        vprint(
            f"enable configuration with id {options.get('select_id')}",
            verbose=verbosity,
        )
        if get_current_configuration(db, user) and get_current_configuration(db, user)[
            0
        ] == options.get("select_id"):
            print(
                f"warning: configuration id {options.get('select_id')} already enabled"
            )
        else:
            if not enable_configuration(db, options.get("select_id")):
                print(f"error: load configuration id {options.get('select_id')} failed")
                exit(1)
    # Print configuration
    if options.get("print"):
        vprint(
            f"print current enabled configuration for user: {user}", verbose=verbosity
        )
        print_configurations(get_configurations(db, user, enabled=True))
    if options.get("print_user"):
        vprint(f"print all configurations for user: {user}", verbose=verbosity)
        print_configurations(get_configurations(db, user))
    if options.get("print_all"):
        vprint("print all configurations", verbose=verbosity)
        print_configurations(get_configurations(db))


def setting(**options):
    """Setting function

    :param options: options dictionary
    :return: None
    """
    db = options.get("database")
    verbosity = options.get("verbose")
    user = options.get("user")
    # Get force for deletion
    force = options.get("force")
    vprint(f"insert data into database {db} for user {user}", verbose=verbosity)
    # Set filled daily values
    today = datetime.today()
    year = today.year if not options.get("year") else options.get("year")
    month = today.month if not options.get("month") else options.get("month")
    day = today.day if not options.get("day") else options.get("day")
    if options.get("date"):
        vprint(f"setting date is {options.get('date')}", verbose=verbosity)
    else:
        vprint(
            f"setting date is day={day}, month={month}, year={year}", verbose=verbosity
        )
    # Get current configuration
    user_configuration = get_current_configuration(db, user)
    if not user_configuration:
        print(f"error: no active configuration found for user '{user}'")
        exit(1)
    # Default configuration values
    description = options.get("description")
    empty_value = (
        options.get("empty_value")
        if options.get("empty_value")
        else user_configuration.empty_value
    )
    # Default: check hours value
    hours_value = (
        options.get("hours") if options.get("hours") else options.get("custom")
    )
    if not hours_value:
        hours_value = empty_value
    # Default: check disease value
    if options.get("disease"):
        hours_value = 0
        description = user_configuration.disease
    # Default: check extraordinary value
    extraordinary = (
        check_default_hours(
            options.get("extraordinary", 0),
            user_configuration.extraordinary,
            "extraordinary",
        )
        if options.get("extraordinary")
        else 0
    )
    # Default: check permit value
    permit = (
        check_default_hours(
            options.get("permit"),
            user_configuration.permit_hours,
            "permit",
        )
        if options.get("permit")
        else 0
    )
    # Default: check other value
    other = (
        check_default_hours(
            options.get("other"),
            user_configuration.other_hours,
            "other",
        )
        if options.get("other")
        else 0
    )
    if isinstance(hours_value, (int, float)) and isinstance(
        extraordinary, (int, float)
    ):
        # Check if worked hours is less than of default
        if hours_value < user_configuration.daily_hours and extraordinary:
            print(
                "warning: no extraordinary because the hours worked are "
                f"lower than the default({user_configuration.daily_hours})"
            )
            extraordinary = 0
        # Check if worked hours is greater than of default
        elif hours_value > user_configuration.daily_hours and permit:
            print(
                "warning: no permit because the hours worked are "
                f"greater than the default({user_configuration.daily_hours})"
            )
            permit = 0
        # Check if hours value contains extraordinary hours
        else:
            extraordinary = extraordinary + find_extraordinary_hours(
                hours_value, user_configuration.daily_hours
            )
        # Check if permit and extraordinary are specified
        if permit and extraordinary:
            print("warning: no permit and extraordinary hours in the same day")
            permit = 0
            extraordinary = 0
        hours_value = hours_value - extraordinary
    # Default: check location value
    location = (
        options.get("location")
        if options.get("location")
        else user_configuration.location
    )
    vprint(
        f"setting hours={hours_value}, location={location}, "
        f"extraordinary={extraordinary}, permit={permit}, other={other}"
        f"description={description}",
        verbose=verbosity,
    )
    insert_err_msg = "error: working day insert failed"
    remove_err_msg = "error: working day deletion failed"
    # Insert day(s)
    holiday_days = options.get("holidays_range")
    if holiday_days:
        holiday_description = description if description else user_configuration.holiday
        for holiday_day in holiday_days:
            if not insert_working_hours(
                database=db,
                user=user,
                hours=0,
                description=holiday_description,
                location=options.get("location"),
                extraordinary=options.get("extraordinary"),
                permit_hours=options.get("permit"),
                other_hours=options.get("other"),
                holiday=True,
                date=options.get("date"),
                day=holiday_day,
                month=month,
                year=year,
                empty_value=empty_value,
            ):
                print(insert_err_msg)
                exit(2)
    else:
        if not insert_working_hours(
            database=db,
            user=user,
            hours=hours_value,
            description=description,
            location=location,
            extraordinary=extraordinary,
            permit_hours=permit,
            other_hours=other,
            holiday=options.get("holiday"),
            disease=options.get("disease"),
            date=options.get("date"),
            day=day,
            month=month,
            year=year,
            empty_value=empty_value,
        ):
            print(insert_err_msg)
            exit(2)
    # Remove values
    if options.get("reset"):
        if force or confirm("Reset working day to defaults."):
            if not remove_working_hours(
                database=db,
                user=user,
                date=options.get("date"),
                day=day,
                month=month,
                year=year,
                empty_value=empty_value,
            ):
                print(remove_err_msg)
                exit(3)
    elif options.get("remove"):
        if force or confirm("Remove working day."):
            if not delete_working_hours(
                database=db,
                user=user,
                date=options.get("date"),
                day=day,
                month=month,
                year=year,
            ):
                print(remove_err_msg)
                exit(4)


def deleting(**options):
    """Delete function

    :param options: options dictionary
    :return: None
    """
    db = options.get("database")
    verbosity = options.get("verbose")
    user = options.get("user")
    vprint(f"delete data into database {db} for user {user}", verbose=verbosity)
    # Set filled daily values
    today = datetime.today()
    year = today.year if not options.get("year") else options.get("year")
    month = today.month if not options.get("month") else options.get("month")
    day = today.day if not options.get("day") else options.get("day")
    if options.get("date"):
        vprint(f"deleting date is {options.get('date')}", verbose=verbosity)
    else:
        vprint(
            f"deleting date is day={day}, month={month}, year={year}", verbose=verbosity
        )
    # Get force for deletion
    force = options.get("force")
    # Deleting day
    if options.get("date") or options.get("day"):
        if force or confirm("Delete day."):
            if not delete_working_hours(
                database=db,
                user=user,
                date=options.get("date"),
                day=day,
                month=month,
                year=year,
            ):
                print("error: working day deletion failed")
                exit(4)
    # Deleting whole month
    elif options.get("month"):
        if force or confirm("Delete whole month."):
            if not delete_whole_month(database=db, user=user, month=month, year=year):
                print("error: working month deletion failed")
                exit(4)
    # Deleting whole year
    elif options.get("year"):
        if force or confirm("Delete whole year."):
            if not delete_whole_year(database=db, user=user, year=year):
                print("error: working year deletion failed")
                exit(4)
    # Deleting whole data for user
    elif options.get("clear"):
        if force or confirm("Delete whole data for user."):
            try:
                delete_user(database=db, user=user)
            except sqlite3.OperationalError:
                print("error: working user data deletion failed")
                exit(4)


def printing(**options):
    """Print function

    :param options: options dictionary
    :return: None
    """
    db = options.get("database")
    verbosity = options.get("verbose")
    user = options.get("user")
    vprint(f"print data from database {db} for user {user}", verbose=verbosity)
    # Set filled daily values
    today = datetime.today()
    year = today.year if not options.get("year") else options.get("year")
    month = today.month if not options.get("month") else options.get("month")
    day = today.day if not options.get("day") else options.get("day")
    # Print output options
    sort = options.get("sort")
    csv = options.get("csv")
    json = options.get("json")
    html = options.get("html")
    rewards = options.get("rewards")
    # Get current configuration
    user_configuration = get_current_configuration(db, user)
    if not user_configuration:
        print(f"error: no active configuration found for user '{user}'")
        exit(1)
    # Print selected data
    if options.get("date") or options.get("day"):
        print_working_table(
            get_working_hours(
                db, user, day=day, month=month, year=year, date=options.get("date")
            ),
            sort=sort,
            csv=csv,
            json=json,
            html=html,
            rewards=user_configuration if rewards else None,
        )
    elif options.get("month"):
        print_working_table(
            get_whole_month(db, user, year=year, month=month),
            sort=sort,
            csv=csv,
            json=json,
            html=html,
            rewards=user_configuration if rewards else None,
        )
    elif options.get("year"):
        print_working_table(
            get_whole_year(db, user, year=year),
            sort=sort,
            csv=csv,
            json=json,
            html=html,
            rewards=user_configuration if rewards else None,
        )
    elif options.get("all"):
        print_working_table(
            get_all_days(db, user),
            sort=sort,
            csv=csv,
            json=json,
            html=html,
            rewards=user_configuration if rewards else None,
        )


def cli_select_command(command):
    """
    Select command

    :param command: Sub-parser command
    :return: function
    """
    # Define action dictionary
    commands = {
        "config": configuration,
        "set": setting,
        "delete": deleting,
        "print": printing,
    }
    return commands.get(command)


def main():
    """main function"""
    args = get_args()
    verbosity = args.verbose
    db = args.database
    # Check database status
    if not database_exists(db):
        make_database(db)
        vprint(f"database {db} created", verbose=verbosity)
    # Check update version
    if get_current_version(db) != __version__:
        update_version(db)
    vprint(f"clocking version {__version__}", verbose=verbosity)
    # Select action
    options = vars(args)
    cmd = cli_select_command(args.command)
    if cmd:
        cmd(**options)


# endregion

# region main
if __name__ == "__main__":
    main()

# endregion
