#!/usr/bin/env python3
"""
Command-line interface for fast-readability
"""

import argparse
import json
import sys
from typing import Optional

from .readability import Readability, ReadabilityError
from .utils import create_custom_options


def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="Extract readable content from HTML using Mozilla's readability.js",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Parse HTML from file
  fast-readability input.html

  # Parse HTML from URL
  fast-readability --url https://example.com/article

  # Parse HTML from stdin
  curl https://example.com/article | fast-readability --stdin

  # Check if content is readerable
  fast-readability --check input.html

  # Output only text content
  fast-readability --text-only input.html

  # Use custom options
  fast-readability --char-threshold 100 --keep-classes input.html

  # Output as JSON
  fast-readability --json input.html
        """
    )
    
    # Input options (mutually exclusive)
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument(
        "file", 
        nargs="?", 
        help="HTML file to parse"
    )
    input_group.add_argument(
        "--url", 
        help="URL to fetch and parse"
    )
    input_group.add_argument(
        "--stdin", 
        action="store_true",
        help="Read HTML from stdin"
    )
    
    # Output options
    parser.add_argument(
        "--check", 
        action="store_true",
        help="Only check if content is readerable (returns exit code 0 if yes, 1 if no)"
    )
    parser.add_argument(
        "--json", 
        action="store_true",
        help="Output results as JSON"
    )
    parser.add_argument(
        "--text-only", 
        action="store_true",
        help="Output only the text content"
    )
    parser.add_argument(
        "--title-only", 
        action="store_true",
        help="Output only the title"
    )
    parser.add_argument(
        "--output", "-o",
        help="Output file (default: stdout)"
    )
    
    # Readability options
    parser.add_argument(
        "--char-threshold", 
        type=int, 
        default=500,
        help="Minimum characters for article (default: 500)"
    )
    parser.add_argument(
        "--keep-classes", 
        action="store_true",
        help="Preserve CSS classes in output"
    )
    parser.add_argument(
        "--max-elems", 
        type=int, 
        default=0,
        help="Maximum elements to parse (0 = no limit)"
    )
    parser.add_argument(
        "--debug", 
        action="store_true",
        help="Enable debug output"
    )
    
    # QuickJS options
    parser.add_argument(
        "--memory-limit", 
        type=int, 
        default=50,
        help="Memory limit in MB (default: 50)"
    )
    parser.add_argument(
        "--time-limit", 
        type=int, 
        default=10,
        help="Time limit in seconds (default: 10)"
    )
    
    return parser.parse_args()


def read_input(args) -> str:
    """Read HTML content based on input arguments"""
    if args.file:
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                return f.read()
        except IOError as e:
            print(f"Error reading file {args.file}: {e}", file=sys.stderr)
            sys.exit(1)
    
    elif args.url:
        try:
            import requests
            headers = {
                'User-Agent': 'Mozilla/5.0 (compatible; fast-readability/1.0)'
            }
            response = requests.get(args.url, headers=headers, timeout=30)
            response.raise_for_status()
            return response.text
        except ImportError:
            print("Error: requests library not installed. Install with: pip install requests", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"Error fetching URL {args.url}: {e}", file=sys.stderr)
            sys.exit(1)
    
    elif args.stdin:
        try:
            return sys.stdin.read()
        except KeyboardInterrupt:
            print("Interrupted", file=sys.stderr)
            sys.exit(1)
    
    else:
        print("Error: No input specified", file=sys.stderr)
        sys.exit(1)


def write_output(content: str, output_file: Optional[str] = None):
    """Write content to output file or stdout"""
    if output_file:
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(content)
        except IOError as e:
            print(f"Error writing to file {output_file}: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print(content)


def main():
    """Main CLI function"""
    args = parse_args()
    
    # Read input
    html_content = read_input(args)
    
    # Create readability options
    options = create_custom_options(
        char_threshold=args.char_threshold,
        keep_classes=args.keep_classes,
        max_elems_to_parse=args.max_elems,
        debug=args.debug
    )
    
    # Create Readability instance
    memory_limit_bytes = args.memory_limit * 1024 * 1024
    
    try:
        with Readability(memory_limit=memory_limit_bytes, time_limit=args.time_limit) as reader:
            
            # Handle --check option
            if args.check:
                url = args.url if args.url else ""
                is_readerable = reader.is_probably_readerable(html_content, url, options)
                
                if args.json:
                    result = {"readerable": is_readerable}
                    write_output(json.dumps(result, indent=2), args.output)
                else:
                    write_output("yes" if is_readerable else "no", args.output)
                
                # Exit with appropriate code
                sys.exit(0 if is_readerable else 1)
            
            # Parse content
            url = args.url if args.url else ""
            result = reader.parse(html_content, url, options)
            
            # Handle different output formats
            if args.title_only:
                write_output(result.title or "", args.output)
            
            elif args.text_only:
                write_output(result.text_content or "", args.output)
            
            elif args.json:
                output_data = {
                    "title": result.title,
                    "content": result.content,
                    "textContent": result.text_content,
                    "length": result.length,
                    "excerpt": result.excerpt,
                    "byline": result.byline,
                    "dir": result.dir,
                    "siteName": result.site_name,
                    "lang": result.lang,
                    "publishedTime": result.published_time
                }
                write_output(json.dumps(output_data, indent=2, ensure_ascii=False), args.output)
            
            else:
                # Default output format
                output_lines = []
                if result.title:
                    output_lines.append(f"Title: {result.title}")
                if result.byline:
                    output_lines.append(f"Author: {result.byline}")
                if result.published_time:
                    output_lines.append(f"Published: {result.published_time}")
                if result.site_name:
                    output_lines.append(f"Site: {result.site_name}")
                if result.length:
                    output_lines.append(f"Length: {result.length} characters")
                
                output_lines.append("")  # Empty line
                
                if result.excerpt:
                    output_lines.append(f"Excerpt: {result.excerpt}")
                    output_lines.append("")
                
                if result.text_content:
                    output_lines.append("Content:")
                    output_lines.append("-" * 40)
                    output_lines.append(result.text_content)
                
                write_output("\n".join(output_lines), args.output)
    
    except ReadabilityError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("Interrupted", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        if args.debug:
            import traceback
            traceback.print_exc()
        else:
            print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main() 