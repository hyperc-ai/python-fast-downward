[![PyPI version](https://badge.fury.io/py/downward-ch.svg)](https://badge.fury.io/py/downward-ch) [![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

The Fast-Downward Planning System (www.fast-downward.org) with Critical Hop patches 

# Usage

## Installing:

```
pip install downward-ch
```

## Running:

```
$ fast-downward <options> <domain.pddl> <problem.pddl>
```

# Developing

## Building:

```
python 3.7 setup.py bdist_wheel
```

## Publishing:

1. Build the manylinux distribution

alternatively, rename platform tag to `manylinux1_x86_64`

2. Upload

```
twine upload dist/*
```
