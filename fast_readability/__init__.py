"""
Fast Readability - A Python library that uses QuickJS to call Mozilla's readability.js

This library provides a Python interface to Mozilla's readability.js library,
allowing you to extract readable content from HTML documents using the same
algorithm used in Firefox Reader View.
"""

from .readability import Readability, ReadabilityResult
from .utils import is_probably_readerable

__version__ = "0.1.0"
__author__ = "Your Name"

__all__ = [
    "Readability", 
    "ReadabilityResult", 
    "is_probably_readerable"
] 