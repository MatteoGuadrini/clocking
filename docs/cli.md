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
clocking config -h
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