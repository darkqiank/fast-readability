"""
Fast Readability - HTML content extractor
"""

import os
import json
import quickjs
from bs4 import BeautifulSoup
from typing import Optional, Dict, Any, Union



class Readability:
    """
    A fast HTML content extractor based on Mozilla's Readability.js
    
    This class provides methods to extract clean article content from HTML,
    either from a URL or from HTML strings directly.
    """
    
    def __init__(self, debug: bool = False):
        """
        Initialize the Readability extractor.
        
        Args:
            debug (bool): Enable debug mode for detailed loggings
        """
        self.debug = debug
        self._js_context = None
        self._initialize_js_context()
    
    def _initialize_js_context(self):
        """Initialize the JavaScript context with required libraries."""
        try:
            # 获取JS文件路径
            package_dir = os.path.dirname(__file__)
            js_dir = os.path.join(package_dir, "js")
            
            jsdom_parser_path = os.path.join(js_dir, "JSDOMParser.js")
            readability_path = os.path.join(js_dir, "Readability.js")
            
            # 读取JS脚本
            with open(jsdom_parser_path, "r", encoding="utf-8") as f:
                js_dom_parser = f.read()
            with open(readability_path, "r", encoding="utf-8") as f:
                js_readability = f.read()
            
            # 初始化JS执行器
            self._js_context = quickjs.Context()
            self._js_context.eval(js_dom_parser)
            self._js_context.eval(js_readability)
            
            if self.debug:
                print("JavaScript context initialized successfully")
                
        except Exception as e:
            raise RuntimeError(f"Failed to initialize JavaScript context: {e}")
    
    def _clean_html(self, html: str) -> str:
        """
        Clean HTML by removing script tags and style attributes.
        
        Args:
            html (str): Raw HTML string
            
        Returns:
            str: Cleaned HTML string
        """
        try:
            soup = BeautifulSoup(html, "html.parser")
            
            # 删除所有 script 标签
            for script in soup.find_all('script'):
                script.decompose()
            
            # 删除所有 style 属性
            for tag in soup.find_all(style=True):
                del tag['style']
            
            # 返回清理后的HTML
            return str(soup.html) if soup.html else str(soup)
            
        except Exception as e:
            if self.debug:
                print(f"HTML cleaning failed: {e}")
            return html
    
    def _extract_content(self, html: str) -> Dict[str, Any]:
        """
        Extract article content from HTML using Readability.js.
        
        Args:
            html (str): HTML string to process
            
        Returns:
            Dict[str, Any]: Extracted article data
        """
        try:
            # 清理HTML
            clean_html = self._clean_html(html)
            
            # 转义HTML字符串用于JavaScript
            escaped_html = json.dumps(clean_html)
            
            # 构建JavaScript执行代码
            js_code = f"""
            (() => {{
                let parser = new JSDOMParser();
                let doc = parser.parse({escaped_html});
                
                // 如果没有documentElement，但有childNodes，手动设置documentElement
                if (!doc.documentElement && doc.childNodes && doc.childNodes.length > 0) {{
                    for (let i = 0; i < doc.childNodes.length; i++) {{
                        if (doc.childNodes[i].nodeName === 'HTML') {{
                            doc.documentElement = doc.childNodes[i];
                            break;
                        }}
                    }}
                }}
                
                let reader = new Readability(doc);
                let article = reader.parse();
                return JSON.stringify(article);
            }})()
            """
            
            # 执行JavaScript并获取结果
            result_json = self._js_context.eval(js_code)
            result = json.loads(result_json)
            
            return result
            
        except Exception as e:
            if self.debug:
                print(f"Content extraction failed: {e}")
            return {
                "title": "",
                "content": "",
                "textContent": "",
                "length": 0,
                "excerpt": "",
                "byline": "",
                "dir": "",
                "siteName": "",
                "lang": ""
            }
    
    def extract_from_html(self, html: str) -> Dict[str, Any]:
        """
        Extract article content from HTML string.
        
        Args:
            html (str): HTML string to process
            
        Returns:
            Dict[str, Any]: Dictionary containing extracted article data with keys:
                - title: Article title
                - content: Article content in HTML format
                - textContent: Article content in plain text
                - length: Content length
                - excerpt: Article excerpt
                - byline: Author information
                - dir: Text direction
                - siteName: Site name
                - lang: Language
        """
        return self._extract_content(html)
    
    
    def get_text_content(self, html: str) -> str:
        """
        Get plain text content from HTML.
        
        Args:
            html (str): HTML string to process
            
        Returns:
            str: Extracted plain text content
        """
        result = self.extract_from_html(html)
        return result.get("textContent", "")
    
    def get_title(self, html: str) -> str:
        """
        Get article title from HTML.
        
        Args:
            html (str): HTML string to process
            
        Returns:
            str: Extracted article title
        """
        result = self.extract_from_html(html)
        return result.get("title", "")
    
    def is_probably_readable(self, html: str, min_content_length: int = 140) -> bool:
        """
        Check if the HTML contains readable content.
        
        Args:
            html (str): HTML string to check
            min_content_length (int): Minimum content length to consider readable
            
        Returns:
            bool: True if the content is probably readable
        """
        result = self.extract_from_html(html)
        content_length = result.get("length", 0)
        return content_length >= min_content_length


def extract_content(html: str, debug: bool = False) -> Dict[str, Any]:
    """
    Convenience function to extract content from HTML.
    
    Args:
        html (str): HTML string to process
        debug (bool): Enable debug mode
        
    Returns:
        Dict[str, Any]: Extracted article data
    """
    readability = Readability(debug=debug)
    return readability.extract_from_html(html)