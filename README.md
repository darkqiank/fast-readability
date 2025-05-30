# Fast Readability

A Python library that uses QuickJS to call Mozilla's readability.js, implementing all its functionality for extracting readable content from HTML documents.

[![PyPI version](https://badge.fury.io/py/fast-readability.svg)](https://badge.fury.io/py/fast-readability)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

## Features

- 🚀 **Fast**: Uses QuickJS for JavaScript execution with minimal overhead
- 🔧 **Complete**: Implements all features of Mozilla's readability.js
- 🐍 **Pythonic**: Clean Python API with type hints and comprehensive documentation
- 🛠️ **Flexible**: Supports custom parsing options and configurations
- 📦 **Zero Dependencies**: Only requires QuickJS Python binding
- 🌐 **URL Support**: Can fetch and parse content directly from URLs
- 🖥️ **CLI Tool**: Includes command-line interface for easy integration

## Installation

```bash
pip install fast-readability
```

## Quick Start

### Basic Usage

```python
from fast_readability import Readability

# Parse HTML content
html = """
<html>
<head><title>Example Article</title></head>
<body>
    <article>
        <h1>How to Use Fast-Readability</h1>
        <p>This is an example article with readable content.</p>
        <p>The library extracts clean, readable text from HTML.</p>
    </article>
</body>
</html>
"""

with Readability() as reader:
    result = reader.parse(html, "https://example.com")
    
    print(f"Title: {result.title}")
    print(f"Content: {result.text_content}")
    print(f"Length: {result.length} characters")
```

### Using Utility Functions

```python
from fast_readability.utils import parse_html, is_probably_readerable

# Quick parsing
result = parse_html(html, "https://example.com")

# Check if content is readerable
if is_probably_readerable(html):
    print("Content is probably readerable")
```

### Parsing from URL

```python
from fast_readability.utils import parse_from_url

# Parse directly from URL
result = parse_from_url("https://example.com/article")
print(f"Title: {result.title}")
print(f"Author: {result.byline}")
```

## API Reference

### Readability Class

The main `Readability` class provides the core functionality:

```python
class Readability:
    def __init__(self, memory_limit: int = 50*1024*1024, time_limit: int = 10):
        """
        Initialize Readability with resource limits.
        
        Args:
            memory_limit: Memory limit in bytes (default: 50MB)
            time_limit: Time limit in seconds (default: 10s)
        """
    
    def parse(self, html_content: str, url: str = "", options: dict = None) -> ReadabilityResult:
        """Parse HTML content and extract readable content."""
    
    def is_probably_readerable(self, html_content: str, url: str = "", options: dict = None) -> bool:
        """Check if content is probably readerable."""
    
    def parse_from_url(self, url: str, options: dict = None, **kwargs) -> ReadabilityResult:
        """Fetch and parse content from URL."""
```

### ReadabilityResult

The result object contains all extracted information:

```python
@dataclass
class ReadabilityResult:
    title: Optional[str]           # Article title
    content: Optional[str]         # HTML content
    text_content: Optional[str]    # Text content (no HTML)
    length: Optional[int]          # Content length in characters
    excerpt: Optional[str]         # Article excerpt
    byline: Optional[str]          # Author information
    dir: Optional[str]             # Text direction
    site_name: Optional[str]       # Site name
    lang: Optional[str]            # Content language
    published_time: Optional[str]  # Publication time
```

### Custom Options

You can customize the parsing behavior:

```python
from fast_readability.utils import create_custom_options

options = create_custom_options(
    char_threshold=300,           # Minimum characters for article
    keep_classes=True,            # Preserve CSS classes
    classes_to_preserve=["highlight", "code"],  # Specific classes to keep
    max_elems_to_parse=1000,      # Limit elements to process
    debug=True                    # Enable debug output
)

result = parse_html(html, options=options)
```

## Command Line Interface

Fast-readability includes a CLI tool:

```bash
# Parse HTML file
fast-readability article.html

# Parse from URL
fast-readability --url https://example.com/article

# Parse from stdin
curl https://example.com/article | fast-readability --stdin

# Check if content is readerable
fast-readability --check article.html

# Output only text content
fast-readability --text-only article.html

# Output as JSON
fast-readability --json article.html

# Custom options
fast-readability --char-threshold 100 --keep-classes article.html
```

### CLI Options

```
usage: fast-readability [-h] [--url URL | --stdin] [--check] [--json] 
                        [--text-only] [--title-only] [--output OUTPUT]
                        [--char-threshold CHAR_THRESHOLD] [--keep-classes]
                        [--max-elems MAX_ELEMS] [--debug]
                        [--memory-limit MEMORY_LIMIT] [--time-limit TIME_LIMIT]
                        [file]

Extract readable content from HTML using Mozilla's readability.js

positional arguments:
  file                  HTML file to parse

optional arguments:
  -h, --help            show this help message and exit
  --url URL             URL to fetch and parse
  --stdin               Read HTML from stdin
  --check               Only check if content is readerable
  --json                Output results as JSON
  --text-only           Output only the text content
  --title-only          Output only the title
  --output OUTPUT, -o OUTPUT
                        Output file (default: stdout)
  --char-threshold CHAR_THRESHOLD
                        Minimum characters for article (default: 500)
  --keep-classes        Preserve CSS classes in output
  --max-elems MAX_ELEMS
                        Maximum elements to parse (0 = no limit)
  --debug               Enable debug output
  --memory-limit MEMORY_LIMIT
                        Memory limit in MB (default: 50)
  --time-limit TIME_LIMIT
                        Time limit in seconds (default: 10)
```

## Advanced Usage

### Context Manager

Use Readability as a context manager for automatic resource cleanup:

```python
with Readability(memory_limit=25*1024*1024, time_limit=5) as reader:
    if reader.is_probably_readerable(html):
        result = reader.parse(html)
        print(result.title)
```

### Error Handling

```python
from fast_readability import ReadabilityError

try:
    result = parse_html(html)
except ReadabilityError as e:
    print(f"Failed to parse content: {e}")
```

### Batch Processing

```python
from fast_readability import Readability

urls = ["https://example.com/1", "https://example.com/2"]

with Readability() as reader:
    for url in urls:
        try:
            result = reader.parse_from_url(url)
            print(f"Processed: {result.title}")
        except ReadabilityError as e:
            print(f"Failed to process {url}: {e}")
```

## Performance Considerations

- **Memory Usage**: Default memory limit is 50MB. Adjust based on your needs.
- **Time Limits**: Default timeout is 10 seconds. Increase for complex documents.
- **Reuse Instances**: Reuse Readability instances when processing multiple documents.
- **Context Managers**: Use context managers for automatic cleanup.

## Comparison with Other Libraries

| Feature | fast-readability | python-readability | newspaper3k |
|---------|------------------|-------------------|-------------|
| JavaScript Engine | QuickJS | None | None |
| Mozilla Algorithm | ✅ Full | ❌ Python port | ❌ Different |
| Performance | ⚡ Fast | 🐌 Slow | ⚡ Fast |
| Accuracy | 🎯 High | 📊 Medium | 📊 Medium |
| Maintenance | 🔄 Active | ⏸️ Stale | 🔄 Active |

## Requirements

- Python 3.7+
- QuickJS Python binding
- Requests (for URL fetching)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Development

```bash
# Clone repository
git clone https://github.com/darkqiank/fast-readability.git
cd fast-readability

# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run linting
black .
isort .
flake8
```

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Mozilla's [readability.js](https://github.com/mozilla/readability) for the core algorithm
- [QuickJS](https://bellard.org/quickjs/) JavaScript engine
- Firefox Reader View team for the original implementation

## Changelog

### v0.1.0
- Initial release
- Full implementation of Mozilla's readability.js
- Command-line interface
- Python 3.7+ support
- Comprehensive test suite
