import sys

from . import data

if sys.version_info < (3, 6, 0):
    raise RuntimeError("cnlp requires Python 3.6.0+")

__version__ = "0.1.0"

__all__ = [
    "data"
]
