# funcmeasure
![python_version](https://img.shields.io/static/v1?label=Python&message=3.5%20|%203.6%20|%203.7&color=blue) [![PyPI downloads/month](https://img.shields.io/pypi/dm/funcmeasure?logo=pypi&logoColor=white)](https://pypi.python.org/pypi/funcmeasure)

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
from funcmeasure import measure

def f1():
    5**2

def f2():
    5**2**10

measure([f1, f2], times=1000)
~~~~
This will print:
~~~~
Ran 1000 times

-------------------------------------
| rank | name |  duration  |  perc  |
-------------------------------------
|    1 |   f1 | 0.00000019 |     1x |
|    2 |   f2 | 0.00000227 | 11.79x |
-------------------------------------
~~~~