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