# Contributing

Here's how to run all the development stuff.

## Setup Development Environment
* `poetry install`

## Testing
* `pipenv run pytest -v` in the root directory

## Releasing
Refer to [the python docs on packaging for clarification](https://packaging.python.org/tutorials/packaging-projects/).
* Make sure you've updated `setup.py`
* `python setup.py sdist bdist_wheel` - Create a source distribution and a binary wheel distribution into `dist/`
* `twine upload dist/unitypackage_extractor-x.x.x*` - Upload all `dist/` files to PyPI of a given version
* Make sure to tag the commit you released!