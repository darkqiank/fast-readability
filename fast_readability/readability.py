"""
Core readability functionality using QuickJS to execute Mozilla's readability.js
"""

import os
from typing import Dict, Any, Optional, Union
from dataclasses import dataclass
from quickjs import Function, Context
import json


@dataclass
class ReadabilityResult:
    """
    Result object containing parsed article information
    """
    title: Optional[str] = None
    content: Optional[str] = None
    text_content: Optional[str] = None
    length: Optional[int] = None
    excerpt: Optional[str] = None
    byline: Optional[str] = None
    dir: Optional[str] = None
    site_name: Optional[str] = None
    lang: Optional[str] = None
    published_time: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ReadabilityResult":
        """Create ReadabilityResult from dictionary"""
        if not data:
            return cls()
        
        return cls(
            title=data.get("title"),
            content=data.get("content"),
            text_content=data.get("textContent"),
            length=data.get("length"),
            excerpt=data.get("excerpt"),
            byline=data.get("byline"),
            dir=data.get("dir"),
            site_name=data.get("siteName"),
            lang=data.get("lang"),
            published_time=data.get("publishedTime"),
        )


class ReadabilityError(Exception):
    """Custom exception for readability errors"""
    pass


class Readability:
    """
    Main Readability class that uses QuickJS to execute Mozilla's readability.js
    """
    
    def __init__(self, memory_limit: int = 50 * 1024 * 1024, time_limit: int = 10):
        """
        Initialize Readability with QuickJS context
        
        Args:
            memory_limit: Memory limit for JavaScript execution in bytes (default: 50MB)
            time_limit: Time limit for JavaScript execution in seconds (default: 10s)
        """
        self.memory_limit = memory_limit
        self.time_limit = time_limit
        self._context = None
        self._initialized = False
        
    def _get_js_dir(self) -> str:
        """Get the path to the JavaScript files directory"""
        return os.path.join(os.path.dirname(__file__), "js")
    
    def _load_js_file(self, filename: str) -> str:
        """Load JavaScript file content"""
        js_path = os.path.join(self._get_js_dir(), filename)
        if not os.path.exists(js_path):
            raise ReadabilityError(f"JavaScript file not found: {js_path}")
        
        with open(js_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def _initialize_context(self) -> None:
        """Initialize QuickJS context with readability JavaScript code"""
        if self._initialized:
            return
            
        try:
            # Create QuickJS context
            self._context = Context()
            self._context.set_memory_limit(self.memory_limit)
            self._context.set_time_limit(self.time_limit)
            
            # Load JavaScript files in correct order
            js_files = [
                "JSDOMParser.js",
                "Readability.js", 
                "readability_wrapper.js"
            ]
            
            for js_file in js_files:
                js_content = self._load_js_file(js_file)
                self._context.eval(js_content)
            
            self._initialized = True
            
        except Exception as e:
            raise ReadabilityError(f"Failed to initialize JavaScript context: {str(e)}")
    
    def _convert_js_result(self, js_result) -> Dict[str, Any]:
        """Convert QuickJS result to Python dictionary"""
        try:
            # First try to use a simple JSON conversion
            conversion_code = f"""
            (function() {{
                var obj = {js_result if isinstance(js_result, str) else 'arguments[0]'};
                return JSON.stringify(obj);
            }})()
            """
            
            if isinstance(js_result, str):
                json_str = self._context.eval(conversion_code)
            else:
                # For objects, create a function and call it
                json_fn = self._context.eval("(function(obj) { return JSON.stringify(obj); })")
                json_str = json_fn(js_result)
            
            return json.loads(json_str)
            
        except Exception as e1:
            # Fallback 1: Direct property access
            try:
                result = {}
                if hasattr(js_result, 'success'):
                    result['success'] = bool(js_result.success)
                else:
                    result['success'] = False
                    
                if hasattr(js_result, 'result'):
                    result['result'] = js_result.result
                    
                if hasattr(js_result, 'error'):
                    result['error'] = str(js_result.error)
                    
                return result
                
            except Exception as e2:
                # Fallback 2: Try to convert to string first
                try:
                    str_result = str(js_result)
                    if str_result.startswith('{') and str_result.endswith('}'):
                        return json.loads(str_result)
                except Exception:
                    pass
                
                # Ultimate fallback
                return {
                    'success': False, 
                    'error': f'Failed to convert JavaScript result: {str(e1)}, {str(e2)}'
                }
    
    def parse(
        self,
        html_content: str,
        url: str = "",
        options: Optional[Dict[str, Any]] = None
    ) -> ReadabilityResult:
        """
        Parse HTML content and extract readable content
        
        Args:
            html_content: HTML content to parse
            url: URL of the content (optional)
            options: Options to pass to readability.js (optional)
            
        Returns:
            ReadabilityResult containing extracted content
            
        Raises:
            ReadabilityError: If parsing fails
        """
        self._initialize_context()
        
        if options is None:
            options = {}
        
        try:
            # Prepare JavaScript function call with JSON encoding
            js_code = f"""
            (function() {{
                try {{
                    var result = ReadabilityWrapper.parseHTML({json.dumps(html_content)}, {json.dumps(url)}, {json.dumps(options)});
                    return result;
                }} catch (e) {{
                    return {{
                        success: false,
                        error: e.message || String(e)
                    }};
                }}
            }})()
            """
            
            # Execute JavaScript
            js_result = self._context.eval(js_code)
            
            # Convert result to Python dict
            result = self._convert_js_result(js_result)
            
            if not result.get("success", False):
                error_msg = result.get("error", "Unknown parsing error")
                raise ReadabilityError(f"JavaScript parsing failed: {error_msg}")
            
            # Convert result to ReadabilityResult object
            article_data = result.get("result")
            return ReadabilityResult.from_dict(article_data)
            
        except Exception as e:
            if isinstance(e, ReadabilityError):
                raise
            raise ReadabilityError(f"Failed to parse HTML content: {str(e)}")
    
    def is_probably_readerable(
        self,
        html_content: str,
        url: str = "",
        options: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Check if HTML content is probably readerable
        
        Args:
            html_content: HTML content to check
            url: URL of the content (optional)
            options: Options for readability check (optional)
            
        Returns:
            True if content is probably readerable, False otherwise
            
        Raises:
            ReadabilityError: If check fails
        """
        self._initialize_context()
        
        if options is None:
            options = {}
        
        try:
            # Prepare JavaScript function call with JSON encoding
            js_code = f"""
            (function() {{
                try {{
                    var result = ReadabilityWrapper.isProbablyReaderable({json.dumps(html_content)}, {json.dumps(url)}, {json.dumps(options)});
                    return result;
                }} catch (e) {{
                    return {{
                        success: false,
                        error: e.message || String(e)
                    }};
                }}
            }})()
            """
            
            # Execute JavaScript
            js_result = self._context.eval(js_code)
            
            # Convert result to Python dict
            result = self._convert_js_result(js_result)
            
            if not result.get("success", False):
                error_msg = result.get("error", "Unknown error")
                raise ReadabilityError(f"JavaScript check failed: {error_msg}")
            
            return bool(result.get("result", False))
            
        except Exception as e:
            if isinstance(e, ReadabilityError):
                raise
            raise ReadabilityError(f"Failed to check readability: {str(e)}")
    
    def parse_from_url(
        self,
        url: str,
        options: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> ReadabilityResult:
        """
        Fetch HTML content from URL and parse it
        
        Args:
            url: URL to fetch and parse
            options: Options to pass to readability.js (optional)
            **kwargs: Additional arguments to pass to requests.get()
            
        Returns:
            ReadabilityResult containing extracted content
            
        Raises:
            ReadabilityError: If fetching or parsing fails
        """
        try:
            import requests
            
            # Set default headers
            headers = kwargs.pop('headers', {})
            if 'User-Agent' not in headers:
                headers['User-Agent'] = (
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                    '(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                )
            
            # Fetch content
            response = requests.get(url, headers=headers, **kwargs)
            response.raise_for_status()
            
            # Parse content
            return self.parse(response.text, url, options)
            
        except requests.RequestException as e:
            raise ReadabilityError(f"Failed to fetch URL {url}: {str(e)}")
        except Exception as e:
            if isinstance(e, ReadabilityError):
                raise
            raise ReadabilityError(f"Failed to parse URL {url}: {str(e)}")
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        if self._context:
            # QuickJS context will be garbage collected
            self._context = None
            self._initialized = False 