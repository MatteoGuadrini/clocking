# Cli

`clocking` has a CLI to work in a standard way; track the time.

## Common options

`clocking` has a common options to change environments.

| short | long       | description          | args                  |
|-------|------------|----------------------|-----------------------|
| -v    | --verbose  | Enable verbosity     |                       |
| -V    | --version  | Print version        |                       |
| -B    | --database | Select database file | Path of database file |
| -u    | --user     | Change user          | Username              |

## Config subparser

`clocking` has _config_ subparser to configure your personal settings.

```commandline
clocking config --help
clocking cfg -h
clocking c -h
```

All options are intended to default of empty values of _set_ subparser.
It is possible configure more than one configuration per user.

### Print group

Print options used to print the saved configurations.

| short | long         | description                   | args |
|-------|--------------|-------------------------------|------|
| -p    | --print      | Print current configuration   |      |
| -t    | --print-user | Print all user configurations |      |
| -a    | --print-all  | Print all configurations      |      |

```commandline
clocking config --print
clocking config --print-user
clocking config --print-all
```

### Set group

Set options used to add default configurations for the user.

| short | long                   | description                | args                        |
|-------|------------------------|----------------------------|-----------------------------|
| -D    | --daily-hours          | Daily work hours           | hours                       |
| -N    | --working-days         | Working day's name         | Mon,Tue,Wed,Thu,Fri,Sat,Sun |
| -E    | --extraordinary        | Extraordinary hour value   | hours                       |
| -P    | --permit-hours         | Permit work hour value     | hours                       |
| -U    | --other-hours          | Other hour                 | hours                       |
| -S    | --disease              | Disease value              | text                        |
| -H    | --holiday              | Holiday value              | text                        |
| -C    | --currency             | Currency value             | text/symbol                 |
| -R    | --hour-reward          | Hour reward                | float                       |
| -W    | --extraordinary-reward | Extraordinary hour reward  | float                       |
| -F    | --food-ticket          | Food ticket reward         | float                       |
| -O    | --other-reward         | Other reward               | float                       |
| -L    | --location             | Current location           | location                    |
| -e    | --empty-value          | Fill empty date with value | text                        |

```commandline
clocking config --daily-hours 8 --other-hours 1 --working-days Mon Tue Wed --hour-reward 8 --extraordinary-reward 10 --food-ticket 7 --location "Milan Office" --currency "€"
clocking config --daily-hours 8 --other-hours 1 --hour-reward 10 --extraordinary-reward 15 --location "Pasadina Office" --currency "$"
```

### Selection group

Selection options used to load a configurations for the user.

| short | long        | description                     | args |
|-------|-------------|---------------------------------|------|
| -i    | --select-id | Load configuration selecting id | id   |

```commandline
clocking config --select-id 1
```

### Reset group

Reset options used to reset all configurations for the user.

| short | long    | description              | args |
|-------|---------|--------------------------|------|
| -r    | --reset | Reset all configurations |      |

```commandline
clocking config --reset
```

### Delete group

Delete options used to permanently delete the configurations for the user.

| short | long        | description                                     | args |
|-------|-------------|-------------------------------------------------|------|
| -d    | --delete-id | Delete configuration selecting id               | id   |
| -z    | --delete-db | Delete whole database                           |      |
| -f    | --force     | Force delete action without prompt confirmation |      |

```commandline
clocking config --delete-id 1
clocking config --delete-db
clocking config --delete-id 1 --force
clocking config --delete-db --force
```

## Set subparser

`clocking` has _set_ subparser to insert/modify/reset data.

```commandline
clocking set --help
clocking st -h
clocking s -h
```

### Daily group

Daily group is exclusive. Choose one flag mode to set values.

| short | long             | description                                       | args  |
|-------|------------------|---------------------------------------------------|-------|
| -w    | --hours          | Set worked hours                                  | hours |
| -s    | --disease        | Set disease day                                   |       |
| -H    | --holiday        | Set holiday day                                   |       |
| -G    | --holidays-range | Set holiday days                                  | days  |
| -c    | --custom         | Set fill selected date with custom value          | value |
| -r    | --reset          | Reset selected date with default fill empty value |       |
| -R    | --remove         | Remove date value                                 |       |

```commandline
clocking set --hours 8
clocking set --disease
clocking set --holiday
clocking set --holidays-range 7 8 9 11 12 23
clocking set --custom "Today I am boring!"
clocking set --reset
clocking set --remove
```

### Other options

`set` subparser supports other options.

| short | long            | description                                     | args  |
|-------|-----------------|-------------------------------------------------|-------|
| -f    | --force         | force delete action without prompt confirmation |       |
| -e    | --extraordinary | Set extraordinary hours                         | hours |
| -o    | --other         | Set other hours                                 | hours |
| -l    | --location      | Set current location                            | text  |
| -p    | --permit        | Set permit hours                                | hours |
| -t    | --description   | Set description                                 | text  |

```commandline
clocking set --reset --force
clocking set --remove --force
clocking set --hours 8 --extraordinary 1
clocking set --hours 8 --other 1
clocking set --hours 8 --location "New York Office"
clocking set --hours 7 --permit 1
clocking set --hours 8 --description "New project"
```

### Date options

`set` subparser inheritance date options.

| short | long    | description        | args  |
|-------|---------|--------------------|-------|
| -D    | --date  | Set literally date | date  |
| -d    | --day   | Set day            | day   |
| -m    | --month | Set month          | month |
| -y    | --year  | Set year           | year  |

```commandline
clocking set --hours 8 --date "15/7/2023"
clocking set --hours 8 --date "7.15.2023"
clocking set --hours 8 --date "2023-7-15"
clocking set --hours 8 --day 31
clocking set --hours 8 --month 2
clocking set --hours 8 --year 2022
clocking set --hours 8 --day 31 --month 2 --year 2022
```

## Delete subparser

`clocking` has _delete_ subparser to delete data.

```commandline
clocking delete --help
clocking del -h
clocking d -h
```

| short | long    | description                                     | args |
|-------|---------|-------------------------------------------------|------|
| -C    | --clear | Clear all data for user                         |      |
| -f    | --force | Force delete action without prompt confirmation |      |

```commandline
clocking delete -C
clocking delete -C -f
```

### Date options

`delete` subparser inheritance date options.

| short | long    | description        | args  |
|-------|---------|--------------------|-------|
| -D    | --date  | Set literally date | date  |
| -d    | --day   | Set day            | day   |
| -m    | --month | Set month          | month |
| -y    | --year  | Set year           | year  |

```commandline
clocking delete -C --date "15/7/2023"
clocking delete -C --day 31
clocking delete -C --month 2
clocking delete -C --year 2022
clocking delete -C --day 31 --month 2 --year 2022
clocking delete -C --day 31 --month 2 --year 2022 -f
```

## Print subparser

`clocking` has _print_ subparser to print selected data.

```commandline
clocking print --help
clocking prt -h
clocking p -h
```

