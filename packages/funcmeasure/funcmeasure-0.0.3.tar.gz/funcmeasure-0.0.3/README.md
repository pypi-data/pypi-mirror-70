# funcmeasure
![python_version](https://img.shields.io/static/v1?label=Python&message=3.5%20|%203.6%20|%203.7&color=blue) [![PyPI downloads/month](https://img.shields.io/pypi/dm/funcmeasure?logo=pypi&logoColor=white)](https://pypi.python.org/pypi/funcmeasure)

## Todo
- Clean up code because it's messy af
- Add support for easier creation of partials

## Description
Measure and compare function execution times

## Install
~~~~bash
pip install funcmeasure
# or
pip3 install funcmeasure
~~~~

## Usage
~~~~python
from funcmeasure import measure, partial, Measurement

def f1():
    5**2

def f2():
    5**2**10

measurements = measure([f1, f2], times=1000, print_benchmark=True)
~~~~
This will print:
~~~~
Ran 1000 times

-----------------------------------------
| rank | name |   duration  | benchmark |
-----------------------------------------
|    1 |   f1 | 0.00000023s |           |
|    2 |   f2 | 0.00000259s |    11.31x |
-----------------------------------------
~~~~

## Notes
The lib also provides a helper function for partials, so you don't have to import functools