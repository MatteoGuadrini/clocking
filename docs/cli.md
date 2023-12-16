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