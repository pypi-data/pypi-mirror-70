# Python Library: Generic Tree Implementation for Banking Simulation Game 2020

## Requirements

- Python 3.8
- pip
- pipenv

### Installation Instructions

Run `pipenv install --dev` to install all dependencies
Run `pipenv shell` to enter the virtualenv created by pipenv for this project.

PS: if the installation doesn't work use `--pre` since some packages might only be in pre-release state.

### How to build a new release?

Make sure you're inside the previously created pipenv.

#### Create the build (package)

Run `python3 setup.py sdist bdist_wheel` which creates a `dist/` and `build` folder.

#### Upload the package

Run `python3 -m twine upload --repository testpypi dist/*` to upload to the TestPyPi repository.

In order for the upload to work, you need to create an API token on the TestPyPi or PyPi.
Use `__token__` for username and `pypi-...` as password.

PS: the credentails can also be stored inside a `$HOME/.pypirc` file.

```
[pypi]
  username = __token__
  password = pypi-...
```

[pypi]
username = **token**
password = pypi-AgENdGVzdC5weXBpLm9yZwIkYjIzNTg5MTItYWJhNi00YWQxLWE1MzItMTA5YWYwZmRlYThhAAIleyJwZXJtaXNzaW9ucyI6ICJ1c2VyIiwgInZlcnNpb24iOiAxfQAABiDMHsyCTzEnqlUVgB7ySqxoDGMNUNLgHC1t4y8ZCxaD8g

non-test pypi-AgEIcHlwaS5vcmcCJDRmNDQ3NGFmLTk3YzMtNGMxOS1hOTA4LWQ5ZmJjYjA2MTE5ZgACJXsicGVybWlzc2lvbnMiOiAidXNlciIsICJ2ZXJzaW9uIjogMX0AAAYg1-WaxOAe6EijqGpdArttFaNbkXGxuhC-y4mvA-fUER4
