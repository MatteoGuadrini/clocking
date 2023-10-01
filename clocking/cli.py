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
        metavar="DAYS",
        nargs="+",
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
    set_parse.add_argument("-D", "--date", help="set date", metavar="DATE")
    set_parse.add_argument("-d", "--day", help="set day", metavar="DAY")
    set_parse.add_argument("-m", "--month", help="set month", metavar="MONTH")
    set_parse.add_argument("-y", "--year", help="set year", metavar="YEAR")
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
    deleting = subparser.add_parser(
        "delete", help="remove values", aliases=["del", "d"], parents=[common_parser]
    )
    deleting_group = deleting.add_mutually_exclusive_group(required=True)
    deleting_group.add_argument(
        "-D", "--date", help="delete specific date", metavar="DATE"
    )
    deleting_group.add_argument(
        "-Y", "--year", help="delete whole year", type=int, metavar="YEAR"
    )
    deleting_group.add_argument(
        "-M", "--month", help="delete whole month", type=int, metavar="MONTH"
    )
    deleting_group.add_argument(
        "-C", "--clear", help="clear all data", action="store_true"
    )
    # Print subparser
    printing = subparser.add_parser(
        "print", help="print values", aliases=["prt", "p"], parents=[common_parser]
    )
    printing_group = printing.add_mutually_exclusive_group(required=True)
    printing_group.add_argument(
        "-D", "--date", help="print specific date", metavar="DATE"
    )
    printing_group.add_argument(
        "-Y", "--year", help="print whole year", type=int, metavar="YEAR"
    )
    printing_group.add_argument(
        "-M", "--month", help="print whole month", type=int, metavar="MONTH"
    )
    printing_group.add_argument(
        "-U", "--all", help="print whole user data", type=str, metavar="USER"
    )
    printing_fmt_group = printing.add_mutually_exclusive_group()
    printing_fmt_group.add_argument(
        "-c", "--csv", help="print in csv format", action="store_true"
    )
    printing_fmt_group.add_argument(
        "-j", "--json", help="print in json format", action="store_true"
    )
    printing_fmt_group.add_argument(
        "-m", "--html", help="print in html format", action="store_true"
    )
    printing_selection_group = printing.add_mutually_exclusive_group()
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
    printing.add_argument(
        "-E",
        "--export",
        help="suppress output and export value into file",
        metavar="FILE",
    )
    printing.add_argument("-r", "--rewards", help="print rewards", action="store_true")

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


def configuration(**options):
    """Configuration function

    :param options: options dictionary
    :return: None
    """
    db = options.get("database")
    verbosity = options.get("verbose")
    user = options.get("user")
    vprint("check configuration table", verbose=verbosity)
    create_configuration_table(db)
    # Delete configuration
    if options.get("delete_id"):
        vprint(f"delete configuration id {options.get('delete_id')}", verbose=verbosity)
        if not delete_configuration(db, options.get("delete_id")):
            print(f"error: delete configuration id {options.get('delete_id')} failed")
    # Reset configurations
    if options.get("reset"):
        vprint("reset configuration table", verbose=verbosity)
        if not reset_configuration(db):
            print("error: reset configuration table failed or table is empty")
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
    """

    :param options: options dictionary
    :return: None
    """
    db = options.get("database")
    verbosity = options.get("verbose")
    user = options.get("user")
    vprint(f"insert data into database {db} for user {user}", verbose=verbosity)
    # Set filled daily values
    today = datetime.today()
    year = today.year if not options.get("year") else options.get("year")
    month = today.month if not options.get("month") else options.get("month")
    day = today.day if not options.get("day") else options.get("day")
    # Get current configuration
    user_configuration = get_current_configuration(db, user)
    if not user_configuration:
        print(f"error: no active configuration found for user '{user}'")
        return
    # Default configuration values
    empty_value = (
        options.get("empty_value")
        if options.get("empty_value")
        else user_configuration.empty_value
    )
    if options.get("hours"):
        hours_value = options.get("hours") if options.get("hours") else empty_value
    else:
        hours_value = options.get("custom") if options.get("custom") else empty_value
    # Insert day(s)
    holiday_days = options.get("holidays_range")
    print(options.get("permit"))
    if holiday_days:
        for hday in holiday_days:
            if not insert_working_hours(
                database=db,
                user=user,
                hours=0,
                description=options.get("description"),
                location=options.get("location"),
                extraordinary=options.get("extraordinary"),
                permit_hours=options.get("permit"),
                other_hours=options.get("other"),
                holiday=True,
                disease=options.get("disease"),
                date=options.get("date"),
                day=hday,
                month=month,
                year=year,
                empty_value=empty_value,
            ):
                print("error: working day insert failed")
    else:
        if not insert_working_hours(
            database=db,
            user=user,
            hours=hours_value,
            description=options.get("description"),
            location=options.get("location"),
            extraordinary=options.get("extraordinary"),
            permit_hours=options.get("permit"),
            other_hours=options.get("other"),
            holiday=options.get("holiday"),
            disease=options.get("disease"),
            date=options.get("date"),
            day=day,
            month=month,
            year=year,
            empty_value=empty_value,
        ):
            print("error: working day insert failed")
    # Remove values
    if options.get("reset"):
        remove_working_hours(
            database=db,
            user=user,
            date=options.get("date"),
            day=day,
            month=month,
            year=year,
            empty_value=empty_value,
        )
    elif options.get("remove"):
        delete_working_hours(
            database=db,
            user=user,
            date=options.get("date"),
            day=day,
            month=month,
            year=year,
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
        "delete": None,
        "print": None,
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
