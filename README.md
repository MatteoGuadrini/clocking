# `clocking`

`clocking` is a command line utility to help you manage your worked hours, vacation, projects or whatever you need to
consider tracking time.

> This project is WIP!

## Testing

[![CircleCI](https://circleci.com/gh/MatteoGuadrini/clocking.svg?style=svg)](https://circleci.com/gh/MatteoGuadrini/clocking)

To test package before use it, follow this:

```commandline
pip install -U pytest
git clone https://github.com/MatteoGuadrini/clocking.git
cd clocking
pytest tests 
```

## Installing

To install package, follow below.

With `pip`:

```commandline
pip install clocking
```

With `git`:

```commandline
git clone https://github.com/MatteoGuadrini/clocking.git
cd clocking
pip install .
```

## Usage

`clocking` was born to be a python library that offers a command line utility.

### As a command line

Use the command line to track and take daily hours worked on projects or not.

```console
$ clocking -h
usage: clocking [-h] {config,cfg,c,set,st,s,delete,del,d,print,prt,p} ...

tracking or monitoring worked hours

positional arguments:
  {config,cfg,c,set,st,s,delete,del,d,print,prt,p}
                        commands to run
    config (cfg, c)     default's configuration
    set (st, s)         setting values
    delete (del, d)     remove values
    print (prt, p)      print values

options:
  -h, --help            show this help message and exit
```

### Configuration

`clocking` uses configurations to apply automatically determine information when insert data into database; these
configurations to creates in command line through `config` section.

```console
# Create configuration
$> clocking config --daily-hours 8 --hour-reward 10 --extraordinary-reward 12 --location "Milan Office" --currency €
# Print configuration
$> clocking config --print
...
# Enable/load configuration
$> clocking config --select-id 1
# Or all in one
$> clocking config --daily-hours 8 --hour-reward 10 --extraordinary-reward 12 --location "Milan Office" --currency € --select-id 1 --print
```

Use `config` action also to delete or clean configurations:

```console
# Delete configuration
$> clocking config --delete-id 1
# Clean all configurations
$> clocking config --reset
```

### Setting

`clocking` uses set mode to insert data into own database; insert data in command line through `set` section.

```console
# Set current working day
$> clocking set --hours 8
# Set other working day
$> clocking set --hours 9.5 --date '11/25/2022'
# Set disease
$> clocking set --disease
# Set holiday
$> clocking set --holiday
# Set custom value
$> clocking set --custom 'Today I not work! I play guitar!'
# Set custom day value: this month, this year but first day
$> clocking set --hours 8 --day 1
# Set custom month value: this day, this year but month november
$> clocking set --hours 8 --month 11
# Set custom year value: this day, this month but year 2022
$> clocking set --hours 8 --year 2021
# Set extraordinary hours
$> clocking set --hours 8 --extraordinary 1
# Set permit hours
$> clocking set --hours 7 --permit 1
# Set other hours
$> clocking set --hours 8 --other 0.5
# Set location
$> clocking set --hours 8 --location 'Milan Office, p.za Duomo'
# Set description
$> clocking set --hours 8 --description 'Project: #1'
# Set all
$> clocking set --hours 8 --day 5 --month 5 --year 2019 --location 'Milan Office' \
    --description 'Study Programming Python' --extraordinary 1 --other 1
# Reset a day, without prompt
$> clocking set --date '10/09/2023' --reset --force
# Delete a day, without prompt
$> clocking set --date '10/09/2023' --remove --force
```

### Deleting

`clocking` uses delete mode to delete data from own database; delete data in command line through `delete` section.

```console
# Delete working first day of month
$> clocking delete --day 1
Delete day.
To continue? [y/N]
# Delete working first day of month, without prompt
$> clocking delete --day 1 --force
# Delete precise date, without prompt
$> clocking delete --date 2/2/2021 --force
# Delete whole month (current year), without prompt
$> clocking delete --month 11 --force
# Delete whole year 2022, without prompt
$> clocking delete --year 2022 --force
# Delete whole user data, without prompt
$> clocking delete --clear --force
```

### Printing

`clocking` uses print mode to print data from own database; print data in command line through `print` section.

```console
# Print day
$> clocking print --date '01/25/2022'
+----------+------+-------+-----+-------+-------------+----------+---------------+--------------+-------------+---------+---------+
| date_id  | year | month | day | hours | description | location | extraordinary | permit_hours | other_hours | holiday | disease |
+----------+------+-------+-----+-------+-------------+----------+---------------+--------------+-------------+---------+---------+
| 20220125 | 2022 |   1   |  25 |  8.0  |     None    |  Milan   |      1.0      |     0.0      |     0.0     |    0    |    0    |
+----------+------+-------+-----+-------+-------------+----------+---------------+--------------+-------------+---------+---------+
$> clocking print --day 25 --month 1 --year 2022
+----------+------+-------+-----+-------+-------------+----------+---------------+--------------+-------------+---------+---------+
| date_id  | year | month | day | hours | description | location | extraordinary | permit_hours | other_hours | holiday | disease |
+----------+------+-------+-----+-------+-------------+----------+---------------+--------------+-------------+---------+---------+
| 20220125 | 2022 |   1   |  25 |  8.0  |     None    |  Milan   |      1.0      |     0.0      |     0.0     |    0    |    0    |
+----------+------+-------+-----+-------+-------------+----------+---------------+--------------+-------------+---------+---------+
# Print whole month
$> clocking print --year 2022 --month 1
+----------+------+-------+-----+-------+-------------+----------+---------------+--------------+-------------+---------+---------+
| date_id  | year | month | day | hours | description | location | extraordinary | permit_hours | other_hours | holiday | disease |
+----------+------+-------+-----+-------+-------------+----------+---------------+--------------+-------------+---------+---------+
| 20220124 | 2022 |   1   |  24 |  8.0  |     None    |  Milan   |      0.0      |     0.0      |     0.0     |    0    |    0    |
| 20220125 | 2022 |   1   |  25 |  8.0  |     None    |  Milan   |      1.0      |     0.0      |     0.0     |    0    |    0    |
+----------+------+-------+-----+-------+-------------+----------+---------------+--------------+-------------+---------+---------+
# Print whole year
$> clocking print --year 2022
+----------+------+-------+-----+-------+-------------+----------+---------------+--------------+-------------+---------+---------+
| date_id  | year | month | day | hours | description | location | extraordinary | permit_hours | other_hours | holiday | disease |
+----------+------+-------+-----+-------+-------------+----------+---------------+--------------+-------------+---------+---------+
| 20220103 | 2022 |   1   |  3  |  8.0  |     None    |  Milan   |      0.0      |     0.0      |     0.0     |    0    |    0    |
| 20220124 | 2022 |   1   |  24 |  8.0  |     None    |  Milan   |      0.0      |     0.0      |     0.0     |    0    |    0    |
| 20220125 | 2022 |   1   |  25 |  8.0  |     None    |  Milan   |      1.0      |     0.0      |     0.0     |    0    |    0    |
+----------+------+-------+-----+-------+-------------+----------+---------------+--------------+-------------+---------+---------+
# Print holiday in whole year
$> clocking print --holiday --year 2022
+----------+------+-------+-----+------------+-------------+----------+---------------+--------------+-------------+---------+---------+
| date_id  | year | month | day |   hours    | description | location | extraordinary | permit_hours | other_hours | holiday | disease |
+----------+------+-------+-----+------------+-------------+----------+---------------+--------------+-------------+---------+---------+
| 20220104 | 2022 |   1   |  4  | Not worked |     None    |  Home!   |      0.0      |     0.0      |     0.0     |    1    |    0    |
+----------+------+-------+-----+------------+-------------+----------+---------------+--------------+-------------+---------+---------+
# Print disease in whole month
$> clocking print --disease --month 1
+----------+------+-------+-----+------------+-------------+----------+---------------+--------------+-------------+---------+---------+
| date_id  | year | month | day |   hours    | description | location | extraordinary | permit_hours | other_hours | holiday | disease |
+----------+------+-------+-----+------------+-------------+----------+---------------+--------------+-------------+---------+---------+
| 20220105 | 2022 |   1   |  5  | Not worked |   Disease   |  Home!   |      0.0      |     0.0      |     0.0     |    0    |    1    |
+----------+------+-------+-----+------------+-------------+----------+---------------+--------------+-------------+---------+---------+
# Print disease in whole year
$> clocking print --disease --year 2022
+----------+------+-------+-----+-------+-------------+----------+---------------+--------------+-------------+---------+---------+
| date_id  | year | month | day | hours | description | location | extraordinary | permit_hours | other_hours | holiday | disease |
+----------+------+-------+-----+-------+-------------+----------+---------------+--------------+-------------+---------+---------+
| 20220111 | 2022 |   1   |  11 |  7.0  |     None    |  Milan   |      1.0      |     0.0      |     0.0     |    0    |    0    |
| 20220125 | 2022 |   1   |  25 |  8.0  |     None    |  Milan   |      1.0      |     0.0      |     0.0     |    0    |    0    |
+----------+------+-------+-----+-------+-------------+----------+---------------+--------------+-------------+---------+---------+
# Print in other format: csv, json, html
$> clocking print --date '01/25/2022' --csv
date_id,year,month,day,hours,description,location,extraordinary,permit_hours,other_hours,holiday,disease
20220125,2022,1,25,8.0,,Milan,1.0,0.0,0.0,0,0
$> clocking print --date '01/25/2022' --json
[
    [
        "date_id",
        "year",
        "month",
        "day",
        "hours",
        "description",
        "location",
        "extraordinary",
        "permit_hours",
        "other_hours",
        "holiday",
        "disease"
    ],
    {
        "date_id": 20220125,
        "day": 25,
        "description": null,
        "disease": "0",
        "extraordinary": 1.0,
        "holiday": "0",
        "hours": 8.0,
        "location": "Milan",
        "month": 1,
        "other_hours": 0.0,
        "permit_hours": 0.0,
        "year": 2022
    }
]
$> clocking print --date '01/25/2022' --html
<table>
    <thead>
        <tr>
            <th>date_id</th>
            <th>year</th>
            <th>month</th>
            <th>day</th>
            <th>hours</th>
            <th>description</th>
            <th>location</th>
            <th>extraordinary</th>
            <th>permit_hours</th>
            <th>other_hours</th>
            <th>holiday</th>
            <th>disease</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>20220125</td>
            <td>2022</td>
            <td>1</td>
            <td>25</td>
            <td>8.0</td>
            <td>None</td>
            <td>Milan</td>
            <td>1.0</td>
            <td>0.0</td>
            <td>0.0</td>
            <td>0</td>
            <td>0</td>
        </tr>
    </tbody>
</table>
# Print with rewards
$> clocking print --date '01/25/2022' --rewards
+----------+------+-------+-----+-------+-------------+----------+---------------+--------------+-------------+---------+---------+---------+
| date_id  | year | month | day | hours | description | location | extraordinary | permit_hours | other_hours | holiday | disease | rewards |
+----------+------+-------+-----+-------+-------------+----------+---------------+--------------+-------------+---------+---------+---------+
| 20220125 | 2022 |   1   |  25 |  8.0  |     None    |  Milan   |      1.0      |     0.0      |     0.0     |    0    |    0    |  81.0€  |
+----------+------+-------+-----+-------+-------------+----------+---------------+--------------+-------------+---------+---------+---------+
# Export data
$> clocking print --date '01/25/2022' --export my_hours.txt
$> cat my_hours.txt
+----------+------+-------+-----+-------+-------------+----------+---------------+--------------+-------------+---------+---------+
| date_id  | year | month | day | hours | description | location | extraordinary | permit_hours | other_hours | holiday | disease |
+----------+------+-------+-----+-------+-------------+----------+---------------+--------------+-------------+---------+---------+
| 20220125 | 2022 |   1   |  25 |  8.0  |     None    |  Milan   |      1.0      |     0.0      |     0.0     |    0    |    0    |
+----------+------+-------+-----+-------+-------------+----------+---------------+--------------+-------------+---------+---------+
```

### As a python module

All useful functions to create scripts or software to track time on projects or days worked, are found in the core
module: `clocking.core`

I create a simple script that tracks hours worked daily.

```python
from sys import argv
from clocking.core import *

mydb = 'mydb.db'
user = 'myuser'

# Create configuration if not was created
if not get_current_configuration(mydb, user):
    # Update version
    update_version(mydb)
    # Create default configuration
    create_configuration_table(mydb)
    add_configuration(mydb,
                      active=True,
                      user=user,
                      location='Italy Office',
                      empty_value='not work!',
                      daily_hours=8.0,
                      working_days="Mon Tue Wed Thu Fri",
                      extraordinary=0.5,
                      permit_hours=1.0,
                      disease='disease',
                      holiday='holiday',
                      currency='€',
                      hour_reward=7.5,
                      extraordinary_reward=8.5,
                      food_ticket=0,
                      other_hours=0,
                      other_reward=8.0
                      )
    enable_configuration(mydb, row_id=1)

# Insert daily hours...
insert_working_hours(mydb, user, argv[1])

# ...and print it!
print_working_table(get_working_hours(mydb, user))
```

## Open source

_clocking_ is an open source project. Any contribute, It's welcome.

**A great thanks**.

For donations, press this

For me

[![paypal](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)](https://www.paypal.me/guos)

For [Telethon](http://www.telethon.it/)

The Telethon Foundation is a non-profit organization recognized by the Ministry of University and Scientific and
Technological Research.
They were born in 1990 to respond to the appeal of patients suffering from rare diseases.
Come today, we are organized to dare to listen to them and answers, every day of the year.

[Adopt the future](https://www.ioadottoilfuturo.it/)

## Treeware

This package is [Treeware](https://treeware.earth). If you use it in production,
then we ask that you [**buy the world a tree**](https://plant.treeware.earth/matteoguadrini/clocking) to thank us for
our work.
By contributing to the Treeware forest you’ll be creating employment for local families and restoring wildlife habitats.

[![Treeware](https://img.shields.io/badge/dynamic/json?color=brightgreen&label=Treeware&query=%24.total&url=https%3A%2F%2Fpublic.offset.earth%2Fusers%2Ftreeware%2Ftrees)](https://treeware.earth)

## Acknowledgments

Thanks to Mark Lutz for writing the _Learning Python_ and _Programming Python_ books that make up my python foundation.

Thanks to Kenneth Reitz and Tanya Schlusser for writing the _The Hitchhiker’s Guide to Python_ books.

Thanks to Dane Hillard for writing the _Practices of the Python Pro_ books.

Special thanks go to my wife, who understood the hours of absence for this development.
Thanks to my children, for the daily inspiration they give me and to make me realize, that life must be simple.

Thanks Python!