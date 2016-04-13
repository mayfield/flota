Flota
========

_Flota (spanish for fleet) - A Docker CLI_ 


About
--------
A arg compatible overlay for the docker CLI.


Requirements
--------
* Unix-oid Platform
* Python 3.5+


Installation
--------

    python3 ./setup.py build
    python3 ./setup.py install

Example
--------

Basic usage follows the standard docker usage with nicer output..
```
$ flota ps
 CONTAINER ID  IMAGE   COMMAND    CREATED    STATUS         PORTS  NAMES            
 a6b8deb508b5  ubuntu  sleep 60   6 seconds  Up 6 seconds          boring_pasteur   
```

Help and usage via `--help`..
```
$ flota ps --help
usage: flota ps [-h] [-a] [--csv | --json | --md | --plain | --terminal]
                [--no-clip] [--table-width COLS] [--table-padding COLS]
                [--table-align JUSTIFY] [--columns COL_INDEX [COL_INDEX ...]]
                [--no-header] [--no-footer]

Process List.

optional arguments:
  -h, --help            show this help message and exit
  -a, --all             Show all containers (default shows just running)

table output format:
  Selection of output formats for table display.  The default behavior is to
  detect the output device's capabilities.

  --csv                 Generate CSV (comma delimited) output of the table.
  --json                Generate JSON output of the table.
  --md                  Render Markdown text format output of the table.
  --plain               Render output without any special formatting.
  --terminal            Render a table designed to fit/fill a terminal. This
                        renderer produces the most human friendly output when on a
                        terminal device.

table render settings:
  Overrides for table render settings.

  --no-clip             Do not clip the table output to fit the screen.
  --table-width COLS    Specify the table width in columns.
  --table-padding COLS  Specify whitespace padding for each table column in
                        characters.
  --table-align JUSTIFY
                        Table column justification.

table filters:
  Options for filtering the table display.

  --columns COL_INDEX [COL_INDEX ...]
                        Only show specific columns.
  --no-header           Hide table header.
  --no-footer           Hide table footer.
```

CSV output..
```
$ flota ps --csv
CONTAINER ID,IMAGE,COMMAND,CREATED,STATUS,PORTS,NAMES
7eb3b70d3894,ubuntu,sleep 60,17 seconds,Up 17 seconds,,sharp_euler
a6b8deb508b5,ubuntu,sleep 60,50 seconds,Up 50 seconds,,boring_pasteur
```

Markdown output..
```
$ flota ps --md
```
| CONTAINER ID | IMAGE  | COMMAND  | CREATED    | STATUS        | PORTS | NAMES          |
|--------------|--------|----------|------------|---------------|-------|----------------|
| 7eb3b70d3894 | ubuntu | sleep 60 | 25 seconds | Up 25 seconds |       | sharp_euler    |
| a6b8deb508b5 | ubuntu | sleep 60 | 58 seconds | Up 58 seconds |       | boring_pasteur |
