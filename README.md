# yesand

```
Yes, I would like an Ivy counterexample, please
Yes, and, I would like one more,
```

## Setup

0) Install Poetry and initialise your virtual environment.

Yesand uses Poetry for dependency management.

```
$ curl -sSL https://install.python-poetry.org | python3 -
```

Then activate the virtual environment.

```
$ poetry shell
...
(yesand-py3.10) $ 
```

1) Install the python3 fork of Ivy.

The `ms-ivy` package is not explicitly a dependency because we may wish to
either install a stock release of Ivy or use a version checked out from source.
Let's do the latter; clone the python3 port of Ivy (such as my [WIP
branch](https://github.com/dijkstracula/ivy/tree/nathan/python3_port)) and
install it into your venv.

```
(venv) $ pushd ~/code/ivy/
(venv) $ python setup.py develop
...
Finished processing dependencies for ms-ivy==1.8.23
(venv) $ which ivyc
/Users/ntaylor/Library/Caches/pypoetry/virtualenvs/yesand-QRffHztw-py3.10/bin/ivyc
(venv) $
```

Ivy depends on a particular fork of z3, pulled in as a submodule.

```
(venv) $ cd submodules/z3
(venv) $ python scripts/mk_make.py --python --prefix=$VIRTUAL_ENV
...
Python pkg dir: /Users/ntaylor/Library/Caches/pypoetry/virtualenvs/yesand-QRffHztw-py3.10/lib/python3.10/site-packages
Python version: 3.10
Writing build/Makefile
Makefile was successfully generated.
  compilation mode: Release
Type 'cd build; make' to build Z3
(venv) $ cd build; make -j8
...
Z3 was successfully built.
...
(venv) $ make install
```

## Running

TODO: these suck.

### Generate:

Does the needful for a particular Ivy file.

```
$ poetry run generate ~/school/phd/projects/ivy_synthesis/sandbox/counter.ivy 
```
