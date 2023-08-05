# pecho
[![Tests](https://github.com/nihaals/pecho/workflows/Tests/badge.svg)](https://github.com/nihaals/pecho/actions?query=workflow%3ATests)
[![codecov](https://codecov.io/gh/nihaals/pecho/branch/master/graph/badge.svg)](https://codecov.io/gh/nihaals/pecho)
[![PyPI](https://img.shields.io/pypi/v/pecho)](https://pypi.org/project/pecho/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pecho)](https://pypi.org/project/pecho/)
[![PyPI - Wheel](https://img.shields.io/pypi/wheel/pecho)](https://pypi.org/project/pecho/)

Pecho makes it easy to write things like status bars.

## Usage
```python
from pecho import echo

echo('1%')  # 1%
echo('2%')  # Replaces with 2%
echo('3%', newline=True)  # Replaces with 3% and appends a newline
echo('4%')  # 3%\n4%
```
