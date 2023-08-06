# datamodel-python
This repository contains the classes that model data that can be ingested by Sophize. Also contains utility functions to read and write these classes as json.

## Publish to PyPI
This library is published to PyPI at https://pypi.org/project/sophize-datamodel/

### Publishing steps
To publish a new version of the library to maven, do the following:

* Update the version number in file `setup.py`
* Run the following commands
    ```
    python resource_utils_test.py 
    python setup.py sdist bdist_wheel
    twine check dist/*
    twine upload dist/*
    ```
* Publish a new release [here](https://github.com/Sophize/datamodel-python/release). Use the version number to set the `Tag version` and `Release Title` fields.

The publishing to maven was setup using instructions at [Real Python](https://realpython.com/pypi-publish-python-package/#publishing-to-pypi).
