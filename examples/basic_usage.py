#!/usr/bin/env python3
"""
Basic usage examples for fast-readability library
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from fast_readability import Readability, ReadabilityResult
from fast_readability.utils import (
    is_probably_readerable, 
    parse_html, 
    parse_from_url,
    create_custom_options
)


def example_basic_parsing():
    """Example of basic HTML parsing"""
    print("=== Basic HTML Parsing ===")
    
    html_content = """
    <html>
    <head>
        <title>Example Article</title>
        <meta name="author" content="John Doe">
    </head>
    <body>
        <header>
            <nav>Navigation menu</nav>
        </header>
        <main>
            <article>
                <h1>How to Use Fast-Readability</h1>
                <p class="byline">By John Doe</p>
                <p>Fast-readability is a Python library that uses QuickJS to execute Mozilla's readability.js library. This allows you to extract clean, readable content from HTML documents, just like Firefox's Reader View.</p>
                <p>The library provides several key features including content extraction, readability checking, and customizable parsing options. It's designed to be fast, lightweight, and easy to use.</p>
                <h2>Key Features</h2>
                <ul>
                    <li>Extract article title, content, and metadata</li>
                    <li>Check if content is probably readerable</li>
                    <li>Support for custom parsing options</li>
                    <li>Built on Mozilla's battle-tested readability algorithm</li>
                </ul>
                <p>Whether you're building a content aggregator, creating a reader app, or just need to extract clean text from web pages, fast-readability provides the tools you need.</p>
            </article>
        </main>
        <footer>
            <p>Copyright 2023</p>
        </footer>
    </body>
    </html>
    """
    
    # Method 1: Using the Readability class directly
    with Readability() as reader:
        result = reader.parse(html_content, "https://example.com")
        
        print(f"Title: {result.title}")
        print(f"Author: {result.byline}")
        print(f"Content length: {result.length} characters")
        print(f"Excerpt: {result.excerpt}")
        print(f"Text content preview: {result.text_content[:200]}...")
    
    # Method 2: Using utility function
    result = parse_html(html_content, "https://example.com")
    print(f"\nUsing utility function - Title: {result.title}")


def example_readability_check():
    """Example of checking if content is readerable"""
    print("\n=== Readability Check ===")
    
    # Good content
    good_html = """
    <html>
    <body>
        <article>
            <h1>Comprehensive Guide to Python</h1>
            <p>Python is a high-level, interpreted programming language with dynamic semantics. Its high-level built-in data structures, combined with dynamic typing and dynamic binding, make it very attractive for Rapid Application Development.</p>
            <p>Python's simple, easy to learn syntax emphasizes readability and therefore reduces the cost of program maintenance. Python supports modules and packages, which encourages program modularity and code reuse.</p>
        </article>
    </body>
    </html>
    """
    
    # Poor content
    poor_html = """
    <html>
    <body>
        <div>
            <span>Short</span>
            <div>Menu</div>
            <div>Footer</div>
        </div>
    </body>
    </html>
    """
    
    print(f"Good content is readerable: {is_probably_readerable(good_html)}")
    print(f"Poor content is readerable: {is_probably_readerable(poor_html)}")


def example_custom_options():
    """Example of using custom parsing options"""
    print("\n=== Custom Options ===")
    
    html = """
    <html>
    <head><title>Technical Article</title></head>
    <body>
        <article class="main-content">
            <h1 class="article-title">Advanced JavaScript Concepts</h1>
            <div class="article-meta">
                <span class="author">Jane Smith</span>
                <time class="published">2023-12-01</time>
            </div>
            <div class="article-body">
                <p class="intro">JavaScript is a versatile programming language that powers the modern web. Understanding advanced concepts is crucial for building robust applications.</p>
                <p class="content">This article covers closures, prototypes, async programming, and more advanced topics that every JavaScript developer should master.</p>
            </div>
        </article>
    </body>
    </html>
    """
    
    # Custom options to preserve CSS classes and lower character threshold
    options = create_custom_options(
        char_threshold=100,  # Lower threshold for shorter articles
        keep_classes=True,   # Preserve CSS classes
        classes_to_preserve=["article-title", "author", "content"],
        debug=False
    )
    
    result = parse_html(html, "https://example.com", options)
    
    print(f"Title: {result.title}")
    print(f"Content with classes preserved: {result.content[:300]}...")


def example_url_parsing():
    """Example of parsing content from a URL"""
    print("\n=== URL Parsing (Mock Example) ===")
    
    # Note: This is a mock example. In real usage, you would use:
    # result = parse_from_url("https://example.com/article")
    
    print("To parse from a URL in real usage:")
    print("from fast_readability.utils import parse_from_url")
    print("result = parse_from_url('https://example.com/article')")
    print("print(result.title)")


def example_context_manager():
    """Example of using Readability as a context manager"""
    print("\n=== Context Manager Usage ===")
    
    html = "<html><body><article><h1>Title</h1><p>Content goes here with enough text to be readable.</p></article></body></html>"
    
    # Using context manager for automatic resource cleanup
    with Readability(memory_limit=25*1024*1024, time_limit=5) as reader:
        # Check readability first
        if reader.is_probably_readerable(html):
            result = reader.parse(html)
            print(f"Successfully parsed: {result.title}")
        else:
            print("Content is not readerable")


def main():
    """Run all examples"""
    print("Fast-Readability Library Examples")
    print("=" * 40)
    
    try:
        example_basic_parsing()
        example_readability_check()
        example_custom_options()
        example_url_parsing()
        example_context_manager()
        
        print("\n" + "=" * 40)
        print("All examples completed successfully!")
        
    except Exception as e:
        print(f"Error running examples: {e}")
        print("Make sure you have installed the library with: pip install fast-readability")


if __name__ == "__main__":
    main() 