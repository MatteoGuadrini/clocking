# Examples

`clocking` opens up a world of possibilities for tracking your time over the various working days;
you can also use it to track your work and the time spent on it across various projects.
Below, you will find many real examples.

## Tracking my working time

Suppose you work for a company as an employee, so you want to track the days you worked on various projects.
Let's start creating a profile that reflects us.

```console
clocking config --daily-hours 8 \       # Max standard hours per day
                --extraordinary 1 \     # Min extraordinary hours per day
                --permit-hours 1 \      # Min permit hours per day
                --other-hours 1 \       # Min other hours per day
                --working-days Mon Tue Wed Thu Fri \     # Working days
                --disease "I have fever" \       # Standard text for disease
                --holiday "Wow! I'm in pause" \  # Standard text for holiday
                --currency "€" \        # Select currency
                --hour-reward 8 \       # Reward for one hour
                --extraordinary-reward 10 \ # Reward for one extraordinary hour
                --food-ticket 7 \       # Reward for one food ticket
                --location "Milan Office" \ # Standard location
                --other-reward 7 \      # Reward for one other hour
                --empty-value "I'm not worked today" # Standard empty value for no entry
```

We have now configured our profile in terms of hours and salary. Now just enable it.

!!! note

    It is possible to enable a profile at the time of insertion if you know the profile number.

First, we print all the profiles entered into our database.

```console
clocking config --print-user
+----+--------+-...
| id | active | ...
+----+--------+-...
| 1  |   0    | ...
+----+--------+-...
```

Catch the _id_ and enable it.

```console
clocking config --select-id 1
clocking config --print
+----+--------+-...
| id | active | ...
+----+--------+-...
| 1  |   1    | ...
+----+--------+-...
```

Now that we have an active setup, we can start tracking time spent on days worked.

```console
clocking set --hours 8
clocking print --all        # or simply "clocking print"
+----------+------+-------+-----+-------+-------------+--------------+---------------+...
| date_id  | year | month | day | hours | description |   location   | extraordinary |...
+----------+------+-------+-----+-------+-------------+--------------+---------------+...
| 20240109 | 2024 |   1   |  9  |  8.0  |     None    | Milan Office |      0.0      |...
+----------+------+-------+-----+-------+-------------+--------------+---------------+...
```

Suppose now that we go some days in to holidays resort.

```console
clocking set --holidays-range {12..15} --location "Cortina D'Ampezzo"
clocking print
+----------+------+-------+-----+----------------------+-------------------+-------------------+...
| date_id  | year | month | day |        hours         |    description    |      location     |...
+----------+------+-------+-----+----------------------+-------------------+-------------------+...
| 20240109 | 2024 |   1   |   9 |         8.0          |        None       |    Milan Office   |...
| 20240112 | 2024 |   1   |  12 | I'm not worked today | Wow! I'm in pause | Cortina D'Ampezzo |...
| 20240113 | 2024 |   1   |  13 | I'm not worked today | Wow! I'm in pause | Cortina D'Ampezzo |...
| 20240114 | 2024 |   1   |  14 | I'm not worked today | Wow! I'm in pause | Cortina D'Ampezzo |...
| 20240115 | 2024 |   1   |  15 | I'm not worked today | Wow! I'm in pause | Cortina D'Ampezzo |...
+----------+------+-------+-----+----------------------+-------------------+-------------------+...
```

And then the day will come when we won't be okay...

```console
clocking set --disease
clocking print --day 16
+----------+------+-------+-----+----------------------+--------------+...+---------+
| date_id  | year | month | day |        hours         | description  |...| disease |
+----------+------+-------+-----+----------------------+--------------+...+---------+
| 20240116 | 2024 |   1   |  16 | I'm not worked today | I have fever |...|    1    |
+----------+------+-------+-----+----------------------+--------------+...+---------+
```

However, if you have entered the hours of the day incorrectly, you can correct it by relaunching the command on the day;
or, it is possible to delete it or restore the defaults via the enabled configuration.

```console
clocking set --hours 8
clocking print --day 16
+----------+------+-------+-----+-------+-------------+--------------+...+---------+
| date_id  | year | month | day | hours | description |   location   |...| disease |
+----------+------+-------+-----+-------+-------------+--------------+...+---------+
| 20240116 | 2024 |   1   |  16 |  8.0  |     None    | Milan Office |...|    0    |
+----------+------+-------+-----+-------+-------------+--------------+...+---------+
clocking set --reset
Reset working day to defaults.
To continue? [y/N] y
clocking print --day 16                                                                                                                                           130 ↵
+----------+------+-------+-----+----------------------+-------------+...+---------+
| date_id  | year | month | day |        hours         | description |...| disease |
+----------+------+-------+-----+----------------------+-------------+...+---------+
| 20240116 | 2024 |   1   |  16 | I'm not worked today |     None    |...|    0    |
+----------+------+-------+-----+----------------------+-------------+...+---------+
clocking set --remove   # Or 'clocking delete --day 16'
Remove working day.
To continue? [y/N] y
clocking print --day 16
+---------+------+-------+-----+-------+-------------+----------+...+---------+
| date_id | year | month | day | hours | description | location |...| disease |
+---------+------+-------+-----+-------+-------------+----------+...+---------+
+---------+------+-------+-----+-------+-------------+----------+...+---------+

```

## Tracking project time for teams

Let's imagine we are a team manager who manages various projects for a specific objective.
Each person manages a certain project, and we need to quantify the hours spent on each individual project.
We need to create a fairly general configuration.

```console
id=1
for userdb in jack jessy james jerry; do
    clocking config --daily-hours 8 --currency "$" --hour-reward 8 --location "Damage Inc." --user $userdb --select-id $id
    id=$((id+1))
done
```

Today is the first day of work in the team;
at the end of the day, I have to assign how many hours were spent on each project and each person.

```console
clocking set --hours 2 --user jack --description "Project #1: build site"
clocking set --hours 3 --user jessy --description "Project #2: network firewall"
clocking set --hours 8 --user james --description "Project #3: human resource"
clocking set --hours 3 --user jerry --description "Project #4: database manager"
```

And now see all worked hours for our project.

```console
for userdb in jack jessy james jerry; do
    echo $userdb
    clocking print --user $userdb
    echo
done

jack
+----------+------+-------+-----+-------+------------------------+-------------+...+---------+
| date_id  | year | month | day | hours |      description       |   location  |...| disease |
+----------+------+-------+-----+-------+------------------------+-------------+...+---------+
| 20240119 | 2024 |   1   |  19 |  2.0  | Project #1: build site | Damage Inc. |...|    0    |
+----------+------+-------+-----+-------+------------------------+-------------+...+---------+

jessy
+----------+------+-------+-----+-------+------------------------------+-------------+...+---------+
| date_id  | year | month | day | hours |         description          |   location  |...| disease |
+----------+------+-------+-----+-------+------------------------------+-------------+...+---------+
| 20240119 | 2024 |   1   |  19 |  3.0  | Project #2: network firewall | Damage Inc. |...|    0    |
+----------+------+-------+-----+-------+------------------------------+-------------+...+---------+

james
+----------+------+-------+-----+-------+----------------------------+-------------+...+---------+
| date_id  | year | month | day | hours |        description         |   location  |...| disease |
+----------+------+-------+-----+-------+----------------------------+-------------+...+---------+
| 20240119 | 2024 |   1   |  19 |  8.0  | Project #3: human resource | Damage Inc. |...|    0    |
+----------+------+-------+-----+-------+----------------------------+-------------+...+---------+

jerry
+----------+------+-------+-----+-------+------------------------------+-------------+...+---------+
| date_id  | year | month | day | hours |         description          |   location  |...| disease |
+----------+------+-------+-----+-------+------------------------------+-------------+...+---------+
| 20240119 | 2024 |   1   |  19 |  3.0  | Project #4: database manager | Damage Inc. |...|    0    |
+----------+------+-------+-----+-------+------------------------------+-------------+...+---------+
```

The project continues and comes to an end.
At this point, we need to quantify the hours spent on each project by our team.

```console
clocking print --user jack --rewards
+----------+------+-------+-----+-------+------------------------+-------------+---------------+...+---------+
| date_id  | year | month | day | hours |      description       |   location  | extraordinary |...| rewards |
+----------+------+-------+-----+-------+------------------------+-------------+---------------+...+---------+
| 20240119 | 2024 |   1   |  19 |  2.0  | Project #1: build site | Damage Inc. |      0.0      |...|  16.0$  |
| 20240120 | 2024 |   1   |  20 |  4.0  | Project #1: build site | Damage Inc. |      0.0      |...|  32.0$  |
| 20240121 | 2024 |   1   |  21 |  3.5  | Project #1: build site | Damage Inc. |      0.0      |...|  28.0$  |
| 20240122 | 2024 |   1   |  22 |  7.0  | Project #1: build site | Damage Inc. |      0.0      |...|  56.0$  |
| 20240123 | 2024 |   1   |  23 |  8.0  | Project #1: build site | Damage Inc. |      1.5      |...|  86.5$  |
+----------+------+-------+-----+-------+------------------------+-------------+---------------+...+---------+
```

## Developing my tracking library

As a developers, we can develop a custom script or decorator function to track and dump time to database.
We start to create a simple custom script.

```python
import datetime

start_time = datetime.datetime.now()
# My code here
...
end_time = datetime.datetime.now()
hours_difference = abs(start_time - end_time).total_seconds() / 3600.0

# Calculate hours that has been passed
hours = float("{:.2f}".format(hours_difference))

from clocking.core import *

mydb = 'script.db'
user = 'script'

# Create configuration if not was created
if not get_current_configuration(mydb, user):
    # Update version
    update_version(mydb)
    # Create default configuration
    create_configuration_table(mydb)
    add_configuration(mydb,
                      active=True,
                      user=user,
                      location='My workstation',
                      empty_value='not run!',
                      daily_hours=8.0,
                      working_days="Mon Tue Wed Thu Fri Sat",
                      extraordinary=0,
                      permit_hours=0,
                      disease='',
                      holiday='',
                      currency='',
                      hour_reward=0,
                      extraordinary_reward=0,
                      food_ticket=0,
                      other_hours=0,
                      other_reward=0
                      )
    enable_configuration(mydb, row_id=1)

# Insert daily hours...
insert_working_hours(mydb, user, hours)

# ...and print it!
print_working_table(get_working_hours(mydb, user))
```

This creates a simple database that log any runs of the script and time spent to compute the job.

Another example, is to write a custom function decorator to track hours that run other functions.

```python
from clocking.core import *
from functools import wraps
import datetime

mydb = 'script.db'


@wraps
def clocking_decorator(func):
    user = func.__name__

    def decorate(*args, **kwargs):
        start_time = datetime.datetime.now()
        func(*args, **kwargs)
        end_time = datetime.datetime.now()
        hours_difference = abs(start_time - end_time).total_seconds() / 3600.0
        # Calculate hours that has been passed
        hours = float("{:.2f}".format(hours_difference))

        # Create configuration if not was created
        if not get_current_configuration(mydb, user):
            # Update version
            update_version(mydb)
            # Create default configuration
            create_configuration_table(mydb)
            add_configuration(mydb,
                              active=True,
                              user=user,
                              location=f'function: {user}',
                              empty_value='not run!',
                              daily_hours=8.0,
                              working_days="Mon Tue Wed Thu Fri Sat",
                              extraordinary=0,
                              permit_hours=0,
                              disease='',
                              holiday='',
                              currency='',
                              hour_reward=0,
                              extraordinary_reward=0,
                              food_ticket=0,
                              other_hours=0,
                              other_reward=0
                              )
            enable_configuration(mydb, row_id=1)

        # Insert daily hours...
        insert_working_hours(mydb, user, hours)

    return decorate


@clocking_decorator
def my_log_runs_function(arg1, arg2):
    print(arg1, arg2)


my_log_runs_function(1, 2)
```
