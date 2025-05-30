"""
Utility functions for fast-readability
"""

from typing import Dict, Any, Optional
from .readability import Readability, ReadabilityResult, ReadabilityError


def is_probably_readerable(
    html_content: str,
    url: str = "",
    options: Optional[Dict[str, Any]] = None
) -> bool:
    """
    Convenience function to check if HTML content is probably readerable
    
    Args:
        html_content: HTML content to check
        url: URL of the content (optional)
        options: Options for readability check (optional)
        
    Returns:
        True if content is probably readerable, False otherwise
        
    Raises:
        ReadabilityError: If check fails
    """
    with Readability() as reader:
        return reader.is_probably_readerable(html_content, url, options)


def parse_html(
    html_content: str,
    url: str = "",
    options: Optional[Dict[str, Any]] = None
) -> ReadabilityResult:
    """
    Convenience function to parse HTML content
    
    Args:
        html_content: HTML content to parse
        url: URL of the content (optional)
        options: Options to pass to readability.js (optional)
        
    Returns:
        ReadabilityResult containing extracted content
        
    Raises:
        ReadabilityError: If parsing fails
    """
    with Readability() as reader:
        return reader.parse(html_content, url, options)


def parse_from_url(
    url: str,
    options: Optional[Dict[str, Any]] = None,
    **kwargs
) -> ReadabilityResult:
    """
    Convenience function to fetch and parse content from URL
    
    Args:
        url: URL to fetch and parse
        options: Options to pass to readability.js (optional)
        **kwargs: Additional arguments to pass to requests.get()
        
    Returns:
        ReadabilityResult containing extracted content
        
    Raises:
        ReadabilityError: If fetching or parsing fails
    """
    with Readability() as reader:
        return reader.parse_from_url(url, options, **kwargs)


def get_default_options() -> Dict[str, Any]:
    """
    Get default options for readability parsing
    
    Returns:
        Dictionary with default options based on Mozilla's readability.js
    """
    return {
        "debug": False,
        "maxElemsToParse": 0,  # 0 means no limit
        "nbTopCandidates": 5,
        "charThreshold": 500,
        "classesToPreserve": [],
        "keepClasses": False,
        "disableJSONLD": False,
        "allowedVideoRegex": None,
        "linkDensityModifier": 0,
    }


def create_custom_options(
    char_threshold: int = 500,
    keep_classes: bool = False,
    classes_to_preserve: Optional[list] = None,
    max_elems_to_parse: int = 0,
    nb_top_candidates: int = 5,
    debug: bool = False,
    disable_json_ld: bool = False,
    link_density_modifier: float = 0.0
) -> Dict[str, Any]:
    """
    Create custom options for readability parsing
    
    Args:
        char_threshold: Minimum characters an article must have to return a result
        keep_classes: Whether to preserve all CSS classes
        classes_to_preserve: List of CSS classes to preserve (when keep_classes=False)
        max_elems_to_parse: Maximum number of elements to parse (0 = no limit)
        nb_top_candidates: Number of top candidates to consider
        debug: Whether to enable debug logging
        disable_json_ld: Whether to disable JSON-LD parsing
        link_density_modifier: Modifier for link density threshold
        
    Returns:
        Dictionary with custom options
    """
    if classes_to_preserve is None:
        classes_to_preserve = []
    
    return {
        "debug": debug,
        "maxElemsToParse": max_elems_to_parse,
        "nbTopCandidates": nb_top_candidates,
        "charThreshold": char_threshold,
        "classesToPreserve": classes_to_preserve,
        "keepClasses": keep_classes,
        "disableJSONLD": disable_json_ld,
        "linkDensityModifier": link_density_modifier,
    } 