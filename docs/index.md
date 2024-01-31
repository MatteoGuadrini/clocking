# Welcome to clocking documentation

This site contains the full documentation of `clocking` python library.

## What is clocking?

`clocking` is a Python library that allows you to store and tracking for your working hours, in general or on a specific
project.

## Why clocking?

`clocking` is useful for creating your own scripts for tracking hours spent at work. Furthermore, clocking has its own
cli to do this in a simple and intuitive way.

The use cases are as follows:

- creation of scripts to track jobs
- integration with git to create pre-scripts for each commit
- use of the cli to track working days
- use of time conversion and tracking utilities

## Testing

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

## Start here

Now that clocking is installed, you can start using it.
Let's start with version control and help.

```commandline
clocking --version
clocking --help
```