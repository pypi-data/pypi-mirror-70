# raptorstr

A library for working with strings with the purpose of generating code

## What and Why

When generating code based off of format description files it is sometimes necessary to conform strings to the code standard you are generating for. This lib is made for this sole purpose and has some convenient functions for doing so with some thought out decisions regarding where one is to break strings in different scenarios.

## Developing

### General development

Per usual set up your python virtual environment first.

Install pre-commit
```bash
pip install pre-commit
pre-commit install
```
Now every time you commit it will run the pre-commit checks

To test the suite run:
```bash
pip install nox
nox
```
This will run the sessions defined in [noxfile.py](noxfile.py)

### Tests
In [tests/common.py](tests/common.py) test cases are listed with their expected values going from some-case string to another.

## License
See [LICENSE](LICENSE)
