#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# vim: se ts=4 et syn=python:

# created by: matteo.guadrini
# test_core -- clocking
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

"""Unit testing module for core logic"""

import os
from tempfile import gettempdir
from clocking.core import database_exists, make_database


# --------------------------------------------------
def test_database_exists():
    """Check if database exists"""
    assert database_exists(os.path.join(gettempdir(), 'test_database.db'))


# --------------------------------------------------
def test_create_database():
    """Check database creation"""
    database = os.path.join(gettempdir(), 'test_database.db')
    if database_exists(database):
        assert make_database(database) is not None
