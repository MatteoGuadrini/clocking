#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# vim: se ts=4 et syn=python:

# created by: matteo.guadrini
# cli -- clocking
#
#     Copyright (C) 2022 Matteo Guadrini <matteo.guadrini@hotmail.it>
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

# endregion

# region globals
__version__ = '0.0.1'


# endregion

# region functions
def get_args():
    """Get command-line arguments

    :return: ArgumentParser
    """
    # Principal parser
    parser = argparse.ArgumentParser(description='tracking or monitoring worked hours',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     prog='clocking'
                                     )
    parser.add_argument('-v', '--verbose', help='enable verbosity', action='store_true')
    parser.add_argument('-V', '--version', help='print version', action='version', version=__version__)
    subparser = parser.add_subparsers(dest='command', help='commands to run', required=True)
    # Config subparser
    config = subparser.add_parser('config', help="default's configuration")
    print_group = config.add_argument_group('print')
    print_group.add_argument('-p', '--print',
                             help='print current configuration',
                             action='store_true')
    print_group.add_argument('-a', '--print-all',
                             help='print all configurations',
                             action='store_true')
    set_group = config.add_argument_group('set')
    set_group.add_argument('-D', '--daily-hours',
                           help='daily work hours',
                           default=8.0,
                           type=float,
                           metavar='HOURS')
    set_group.add_argument('-N', '--day-name',
                           help="working day's name",
                           nargs=argparse.ONE_OR_MORE,
                           default={"Mon", "Tue", "Wed", "Thu", "Fri"},
                           choices={"Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"},
                           type=str,
                           metavar='STR')
    set_group.add_argument('-E', '--extraordinary',
                           help="extraordinary hour value",
                           default=1.0,
                           type=float,
                           metavar='HOURS')
    set_group.add_argument('-P', '--permit-hour',
                           help="permit work hour value",
                           default=1.0,
                           type=float,
                           metavar='HOURS')
    set_group.add_argument('-S', '--disease',
                           help="disease value",
                           default='Disease',
                           type=str,
                           metavar='STR')
    set_group.add_argument('-H', '--holiday',
                           help="holiday value",
                           default='Holiday',
                           type=str,
                           metavar='STR')
    set_group.add_argument('-C', '--currency',
                           help="currency value",
                           default='$',
                           type=str,
                           metavar='SYMBOL')
    set_group.add_argument('-R', '--hour-reward',
                           help="hour reward",
                           default=10.0,
                           type=float,
                           metavar='NUMBER')
    set_group.add_argument('-W', '--extraordinary-reward',
                           help="extraordinary hour reward",
                           default=15.0,
                           type=float,
                           metavar='NUMBER')
    set_group.add_argument('-F', '--food-ticket',
                           help="food ticket reward",
                           default=7.0,
                           type=float,
                           metavar='NUMBER')
    set_group.add_argument('-U', '--other-hours',
                           help="other worked hours",
                           default=1.0,
                           type=float,
                           metavar='HOURS')
    set_group.add_argument('-O', '--other-reward',
                           help="other reward",
                           default=0,
                           type=float,
                           metavar='NUMBER')
    set_group.add_argument('-L', '--location',
                           help="current location",
                           default='Office',
                           type=str,
                           metavar='LOCATION')
    set_group.add_argument('-f', '--fill-empty',
                           help="fill empty date with value",
                           default=0,
                           metavar='VALUE')
    selection_group = config.add_argument_group('selection')
    selection_group.add_argument('-i', '--select-id', help="load configuration selecting id", type=int, metavar='ID')
    reset_group = config.add_argument_group('reset')
    reset_group.add_argument('-r', '--reset', help="reset with default values", action='store_true')

    # Set subparser
    setting = subparser.add_parser('set', help="Setting values")
    daily_value_group = setting.add_mutually_exclusive_group(required=True)
    daily_value_group.add_argument('-w', '--hours',
                                   help="worked hours",
                                   default=None,
                                   type=float)
    daily_value_group.add_argument('-s', '--disease',
                                   help="disease day",
                                   action='store_true')
    daily_value_group.add_argument('-H', '--holiday',
                                   help="holiday day",
                                   action='store_true')
    daily_value_group.add_argument('-u', '--uptime',
                                   help="calculate hours from uptime",
                                   action='store_true')
    daily_value_group.add_argument('-G', '--holidays-range',
                                   help="holiday days",
                                   metavar='DAYS')
    daily_value_group.add_argument('-c', '--custom',
                                   help="fill selected date with custom value",
                                   metavar='VALUE')
    daily_value_group.add_argument('-r', '--reset',
                                   help="reset current date with default fill empty value",
                                   action='store_true')
    daily_value_group.add_argument('-R', '--remove',
                                   help="remove date",
                                   metavar='DATE')
    setting.add_argument('-D', '--date',
                         help="setting date",
                         metavar='DATE')
    setting.add_argument('-d', '--day',
                         help="setting day",
                         metavar='DAY')
    setting.add_argument('-m', '--month',
                         help="setting month",
                         metavar='MONTH')
    setting.add_argument('-y', '--year',
                         help="setting year",
                         metavar='YEAR')
    setting.add_argument('-e', '--extraordinary',
                         help="extraordinary hours",
                         type=float,
                         metavar='HOURS')
    setting.add_argument('-o', '--other',
                         help="other hours",
                         type=float,
                         metavar='HOURS')
    setting.add_argument('-l', '--location',
                         help="current location",
                         type=str)
    setting.add_argument('-U', '--user',
                         help="user to track time",
                         type=str)
    # Remove subparser
    removing = subparser.add_parser('rm', help="Remove values")
    removing.add_argument('-D', '--date',
                          help="removing specific date",
                          metavar='DATE')
    removing.add_argument('-Y', '--year',
                          help="removing whole year",
                          type=int,
                          metavar='YEAR')
    removing.add_argument('-M', '--month',
                          help="removing whole month",
                          type=int,
                          metavar='MONTH')
    removing.add_argument('-U', '--user',
                          help="removing whole user data",
                          type=int,
                          metavar='USER')

    return parser.parse_args()


def main():
    """main function"""
    # Check if database is created
    # Check if configuration is created
    # Check subcommand
    # Check optional arguments
    args = get_args()


# endregion

# region main
if __name__ == '__main__':
    main()

# endregion
