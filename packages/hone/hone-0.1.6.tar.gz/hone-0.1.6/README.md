# hone
[![PyPI version](https://badge.fury.io/py/hone.svg)](https://badge.fury.io/py/hone)
[![PyPI license](https://img.shields.io/pypi/l/hone.svg)](https://pypi.python.org/pypi/hone/)

Convert CSV to automatically nested JSON.

## Table of Contents
<!--ts-->
   + [Getting Started](#getting-started)
      + [Installation](#installation)
      + [Usage: Command Line](#usage-command-line)
      + [Usage: Python Module](#usage-python-module)
      + [Standard I/O Support](#standard-i-support)
      + [Delimiters](#delimiters)
   + [Examples](#examples)
   + [Development](#development)
      + [Running tests](#running-tests)
   + [License](#license)
<!--te-->

## Getting Started
Available as both a [Python module](#usage-python-module) and a [command line tool](#usage-command-line).

### Installation
```
pip install hone
```

### Usage: Command Line
To convert a CSV file located at `path/to/input.csv` to JSON (written to new file at `path/to/output.json`):

```
hone "path/to/input.csv" "path/to/output.json"
```

### Usage: Python Module
```
import hone

Hone = hone.Hone()
schema = Hone.get_schema('path/to/input.csv')   # returns nested JSON schema for input.csv
result = Hone.convert('path/to/input.csv')      # returns converted JSON as Python dictionary
```
### Standard I/O Support
What if you want to pass in the CSV data via standard input and/or print the generated JSON data to standard output? Simply replace the appropriate filename with a dash (`-`). This will replace the input/output file with `stdin`/`stdout`.
### Delimiters
The delimiters that are used to generate the nested structure are commas, underscores, and spaces.

## Examples

You can view all examples of conversions in the [examples](/examples) directory.
### CSV
| name  | birth day | birth month | birth year | reference | reference name | 
|-------|-----------|-------------|------------|-----------|----------------| 
| Bob   | 7         | May         | 1985       | TRUE      | Smith          | 
| Julia | 21        | January     | 1997       | FALSE     | N/A            | 
| Rick  | 12        | June        | 1996       | TRUE      | Clara          | 
### Generated JSON
```
[
  {
    "birth": {
      "day": "7",
      "month": "May",
      "year": "1985"
    },
    "name": "Bob",
    "reference": "TRUE",
    "reference name": "Smith"
  },
  {
    "birth": {
      "day": "21",
      "month": "January",
      "year": "1997"
    },
    "name": "Julia",
    "reference": "FALSE",
    "reference name": "N/A"
  },
  {
    "birth": {
      "day": "12",
      "month": "June",
      "year": "1996"
    },
    "name": "Rick",
    "reference": "TRUE",
    "reference name": "Clara"
  }
]
```

## Development
### Running tests
From the root directory of this repository, run `python3 -m unittest` to execute the entire test suite.

# License
Hone is licensed under the [MIT license](LICENSE).
