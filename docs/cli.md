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
