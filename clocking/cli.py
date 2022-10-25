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
    parser = argparse.ArgumentParser(description='Use this tool to tracking or monitoring worked hours',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     prog='clocking'
                                     )
    parser.add_argument('-v', '--verbose', help='Enable verbosity', action='store_true')
    parser.add_argument('-V', '--version', help='Print version', version=__version__)
    subparser = parser.add_subparsers(dest='command', help='Commands to run', required=True)
    # Config subparser
    config = subparser.add_parser('config', help="Database's configuration")
    print_group = config.add_argument_group('print')
    print_group.add_argument('-p', '--print', help='Print current configurations', action='store_true')

    return parser.parse_args()


def main():
    """main function"""
    # Check if database is created
    # Check if configuration is created
    # Check subcommand
    # Check optional arguments
    pass


# endregion

# region main
if __name__ == '__main__':
    main()

# endregion
