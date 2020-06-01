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

Separating the library from the command line processing and interactive presentation layer enables us to test the library code without the difficulties that end-up being imposed on us when we attempt to test command line utilities.

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
> python3 -m unittest pypkgexp1.tests.box_test -v
test_insert_items_int (pypkgexp1.tests.box_test.TestBoxModule) ... ok
test_insert_items_string (pypkgexp1.tests.box_test.TestBoxModule) ... ok
test_insert_items_tuple (pypkgexp1.tests.box_test.TestBoxModule) ... ok
test_remove_item (pypkgexp1.tests.box_test.TestBoxModule) ... ok
test_update_item (pypkgexp1.tests.box_test.TestBoxModule) ... ok

----------------------------------------------------------------------
Ran 5 tests in 0.001s

OK
```

The following commands to run unit tests are equivalent.
```
> python3 -m unittest pypkgexp1.tests.box_test -v
> python3 -m unittest pypkgexp1/tests/box_test.py -v
```

### Executing unit tests without using the `-m` possible with `unittest.main()`
Adding the following to the end of `*_test.py` files:
```
if __name__ == "__main__":
    unittest.main()
```
allows them to be executed directly with interpreter. This is just another way of achieving test execution as above, but without need to explicitly specify `python3 -m unittest`. To casual observer it looks like you are just executing a compiled test harness.

```
python3 pypkgexp1/tests/box_test.py -v
test_insert_items_int (__main__.TestBoxModule) ... ok
test_insert_items_string (__main__.TestBoxModule) ... ok
test_insert_items_tuple (__main__.TestBoxModule) ... ok
test_remove_item (__main__.TestBoxModule) ... ok
test_update_item (__main__.TestBoxModule) ... ok

----------------------------------------------------------------------
Ran 5 tests in 0.000s

OK
```

### Alternative approach with including unit tests near the main function
Depending on what the package is intended to do, it may be convenient to include the tests right next to where the code is actually executed. In other words, if the package is delivering a utility meant to be used from the command line, as opposed to strictly a library, it can make sense to reduce the boilerplate by placing tests right in the file which actually implements the main function. It is really important 

### Invoking pytest versus python(3) -m pytest
It is likewise possible to use `pytest` if available to run unit tests. Running `pytest` with `pytest [...]` instead of `python3 -m pytest [...]` is nearly identical, except the latter case adds the current directory to `sys.path`, which is standard python behavior.

While using the `pytest` command directly will fail, it is possible to do this instead:
```
python3 -m pytest -v
====================================================================== test session starts ======================================================================
platform darwin -- Python 3.7.5, pytest-5.4.2, py-1.8.1, pluggy-0.13.1 -- /Users/szaydel/github.com/szaydel/pypkgexp1/venv/bin/python
cachedir: .pytest_cache
rootdir: /Users/szaydel/github.com/szaydel/pypkgexp1
collected 5 items

pypkgexp1/tests/box_test.py::TestBoxModule::test_insert_items_int PASSED                                                                                  [ 20%]
pypkgexp1/tests/box_test.py::TestBoxModule::test_insert_items_string PASSED                                                                               [ 40%]
pypkgexp1/tests/box_test.py::TestBoxModule::test_insert_items_tuple PASSED                                                                                [ 60%]
pypkgexp1/tests/box_test.py::TestBoxModule::test_remove_item PASSED                                                                                       [ 80%]
pypkgexp1/tests/box_test.py::TestBoxModule::test_update_item PASSED                                                                                       [100%]

======================================================================= 5 passed in 0.04s =======================================================================
```
