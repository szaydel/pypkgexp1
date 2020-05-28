# Example Python Package

`pypkgexp1` is an example library and a Command Line application displaying a pretty mainstream approach to packaging and deploying a Python package.

## Directory structure

```
.
├── LICENSE
├── README.md
├── pypkgexp1
│   ├── __init__.py
│   ├── cli.py (main function for CLI usage here)
│   ├── lib
│   │   ├── __init__.py
│   │   └── box.py (business logic here)
│   └── tests
│       └── box_test.py (unit tests here)
└── setup.py (describes the package and installation boilerplate)
```

## Separation between library and CLI
All the business logic belongs in the "library" files, which in this example we call `lib`, but this is by no means a required pattern. The intent though is that the library is fairly self-contained and this logic is imported into other libraries or into CLI programs. The key constraint is not having anything that will execute in the global scope on import.

```
>>> import pypkgexp1.lib

>>> b = pypkgexp1.lib.box.Box()

>>> b.insert_item('a.b', 1)
True

>>> b.get('a.b')
1
```

It is best to leverage setuptools' mechanism known as `entry_points`, which tell Python where the `main` function is. Normally a program meant to be called directly will have something to this end:

```
if __name__ == "__main__":
    [...do stuff...]
```

With setuptools we can do the same thing more or less, except setuptools creates thin wrappers for us, which themselves contain tiny amount of code, just enough to figure out where the `main` function is, and to load it.

For testing purposes, to simulate alternate path we export PYTHONPATH envvar.

For fish:
```
> set -x PYTHONPATH /opt/<something>/lib/python
```
For bash and friends:
```
> export PYTHONPATH=/opt/<something>/lib/python
```

Once we setup our environment, we should be able to install the package into the supplied path.
```
> python setup.py install --home=/opt/<something>
```

## Unit testing
With this organization is it relatively convenient to run unit tests with test files under the actual top-level module, as opposed to tests residing in a module beside the `pypkgexp1` module.
```
> python -m unittest pypkgexp1.tests.box_test -v
test_insert_item_string (pypkgexp1.tests.box_test.TestBoxModule) ... ok
test_insert_items_int (pypkgexp1.tests.box_test.TestBoxModule) ... ok
test_update_item (pypkgexp1.tests.box_test.TestBoxModule) ... ok

----------------------------------------------------------------------
Ran 3 tests in 0.000s

OK
```

The following commands to run unit tests are equivalent.
```
> python3 -m unittest pypkgexp1.tests.box_test -v
```
...and
```
python3 -m unittest pypkgexp1/tests/box_test.py -v
```

### Invoking pytest versus python(3) -m pytest
It is likewise possible to use `pytest` if available to run unit tests. Running `pytest` with `pytest [...]` instead of `python3 -m pytest [...]` is nearly identical, except the latter case adds the current directory to `sys.path`, which is standard python behavior.

While using the `pytest` command directly will fail, it is possible to do this instead:
```
python3 -m pytest -v
====================================================================== test session starts ======================================================================
platform darwin -- Python 3.7.5, pytest-5.0.1, py-1.8.0, pluggy-0.12.0 -- /usr/local/opt/python/bin/python3.7
cachedir: .pytest_cache
rootdir: /Users/szaydel/github.com/szaydel/pypkgexp1
collected 3 items

pypkgexp1/tests/box_test.py::TestBoxModule::test_insert_item_string PASSED                                                                                [ 33%]
pypkgexp1/tests/box_test.py::TestBoxModule::test_insert_items_int PASSED                                                                                  [ 66%]
pypkgexp1/tests/box_test.py::TestBoxModule::test_update_item PASSED                                                                                       [100%]

=================================================================== 3 passed in 0.02 seconds ====================================================================
```
