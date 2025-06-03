"""
Fast Readability - A fast HTML content extractor based on Mozilla's Readability.js

This package provides a simple interface to extract clean article content from HTML.
"""

from .readability import Readability, extract_content

__version__ = "0.1.0"
__all__ = ["Readability", "extract_content"] 