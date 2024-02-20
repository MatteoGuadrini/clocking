# Release notes

## 0.1.1

Feb 21, 2024

- Fix result into _get_current_version_ function
- Fix issue of wrong extraordinary calculations
- Fix _version_ argument

## 0.1.0

Jan 31, 2024

- Add _printing_ function
- Add _date_ common parser
- Add _docs_ to project
- Add check day name into **configuration**
- Fix default word into _description_ of configuration arguments

## 0.0.9

Nov 09, 2023

- Add _deleting_ function
- Add _confirm_ function
- Add _force_ argument on **delete** action
- Add _force_ arguments for **configuration** action
- Add _force_ arguments for **setting** action

## 0.0.8

Oct 20, 2023

- Add _setting_ function
- Add _check_default_hours_ function
- Add range choice for days and months

## 0.0.7

Sep 06, 2023

- Add _vprint_ function
- Add **pyproject.toml** file
- Add _get_current_version_ function
- Add _cli_select_command_ function
- Add _configuration_ function
- Add _common_parser_ parser
- Add _get_configurations_ function
- Add _print_configurations_ function
- Fix check **result** of _enable_configuration_ function
- Fix default values into _config_ subparser

## 0.0.6

May 12, 2023

- Add _get_working_hours_ function
- Add _print_working_table_ function
- Add _get_whole_year_ function
- Add _get_whole_month_ function
- Add _get_all_days_ function
- Add **holiday** argument on all get functions
- Add **disease** argument on all get functions
- Add **extraordinary** argument on all get functions
- Add **permit_hours** argument on all get functions
- Add **other_hours** argument on all get functions
- Add _save_working_table_ function
- Add **html** argument on print group
- Add **json** argument on save_working_table and print_working_table function
- Add **csv** argument on save_working_table and print_working_table function
- Add **html** argument on save_working_table and print_working_table function
- Add **UserConfiguration** namedtuple
- Add **DataTable** namedtuple
- Add **UserConfigurationError** class
- Add _make_printable_table_ function
- Add _sum_rewards_ function
- Fix **empty** column to user table

## 0.0.5

Mar 21, 2023

- Add _delete_working_hours_ function
- Add _delete-id_ argument
- Add _delete_configuration_ function
- Add _split_dateid_ function on **util** module
- Add _delete_whole_year_ function
- Add _delete_user_ function
- Add _delete_database_ function
- Add _update_version_ function
- Fix various separator format into _datestring_to_datetime_ function
- Fix check if _row_id_ is already active in **enable_configuration** function

## 0.0.4

Mar 4, 2023

- Add _core_ module
- Add _database_exists_ function
- Add _test_create_database_ function
- Add _make_database_ function
- Add _create_configuration_table_ function
- Add _add_configuration_ function
- Add _enable_configuration_ function
- Add _get_current_configuration_ function
- Add _insert_working_hours_ function
- Add _create_working_hours_table_ function
- Add _util_ module
- Add _datestring_to_datetime_ function
- Add _exception_ module
- Add _build_dateid_ function

## 0.0.3

Dec 23, 2022

- Add a mutually exclusive group for _daily_ value
- Add selection group on _config_ subparser
- Add _user_ on **config** subparser
- Add _printing_ subparser
- Add _database_ argument
- Add aliases to all commands

## 0.0.2

Nov 11, 2022

- Add _init_ subparser
- Add _print_ argument group
- Add _set_ argument group
- Add _delete_ argument and group

## 0.0.1

Oct 10, 2022

- Add _clocking_ package
- Add _cli_ module
