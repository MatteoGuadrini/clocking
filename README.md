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

## Usage

`clocking` was born to be a python library that offers a command line utility.

### As a command line

Use the command line to track and take daily hours worked on projects or not.

```console
$ clocking -h
usage: clocking [-h] [-v] [-V] [-d FILE] {config,cfg,c,set,st,s,delete,del,d,print,prt,p} ...

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
  -v, --verbose         enable verbosity (default: False)
  -V, --version         print version
  -d FILE, --database FILE
                        select database file (default: None)
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
    # Prepare table for insert hours
    create_working_hours_table(mydb, user)

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