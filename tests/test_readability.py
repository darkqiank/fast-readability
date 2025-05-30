"""
Tests for fast_readability.readability module
"""

import pytest
from fast_readability import Readability, ReadabilityResult, ReadabilityError


class TestReadability:
    """Test cases for Readability class"""
    
    def test_initialization(self):
        """Test Readability initialization"""
        reader = Readability()
        assert reader.memory_limit == 50 * 1024 * 1024
        assert reader.time_limit == 10
        assert not reader._initialized
        
        # Test custom limits
        reader = Readability(memory_limit=100000, time_limit=5)
        assert reader.memory_limit == 100000
        assert reader.time_limit == 5
    
    def test_context_manager(self):
        """Test context manager functionality"""
        with Readability() as reader:
            assert isinstance(reader, Readability)
        # Context should be cleaned up after exit
        assert not reader._initialized
    
    def test_simple_html_parsing(self):
        """Test parsing simple HTML content"""
        html = """
        <html>
        <head><title>Test Article</title></head>
        <body>
            <article>
                <h1>Test Title</h1>
                <p>This is a test paragraph with enough content to be considered readable by the algorithm. It contains multiple sentences and should pass the readability test.</p>
                <p>This is another paragraph to ensure we have enough content for the readability algorithm to work properly.</p>
            </article>
        </body>
        </html>
        """
        
        with Readability() as reader:
            result = reader.parse(html, "https://example.com")
            
            assert isinstance(result, ReadabilityResult)
            assert result.title is not None
            assert result.content is not None
            assert result.text_content is not None
            assert isinstance(result.length, int)
    
    def test_is_probably_readerable_simple(self):
        """Test isProbablyReaderable with simple content"""
        readable_html = """
        <html>
        <body>
            <article>
                <h1>Article Title</h1>
                <p>This is a substantial paragraph with enough content to be considered readable. It has multiple sentences and meaningful content that should pass the readability test.</p>
                <p>Another paragraph with more content to ensure the algorithm recognizes this as readable content.</p>
            </article>
        </body>
        </html>
        """
        
        non_readable_html = """
        <html>
        <body>
            <div>Short</div>
        </body>
        </html>
        """
        
        with Readability() as reader:
            assert reader.is_probably_readerable(readable_html) is True
            assert reader.is_probably_readerable(non_readable_html) is False
    
    def test_empty_html(self):
        """Test parsing empty or invalid HTML"""
        with Readability() as reader:
            result = reader.parse("", "")
            assert isinstance(result, ReadabilityResult)
            # Empty content might return empty result
    
    def test_custom_options(self):
        """Test parsing with custom options"""
        html = """
        <html>
        <head><title>Test</title></head>
        <body>
            <div class="content">
                <h1>Title</h1>
                <p>Content paragraph with enough text to be readable.</p>
            </div>
        </body>
        </html>
        """
        
        options = {
            "charThreshold": 50,
            "keepClasses": True,
            "debug": False
        }
        
        with Readability() as reader:
            result = reader.parse(html, "", options)
            assert isinstance(result, ReadabilityResult)
    
    def test_parse_from_url_mock(self, monkeypatch):
        """Test parse_from_url with mocked requests"""
        class MockResponse:
            def __init__(self, text, status_code=200):
                self.text = text
                self.status_code = status_code
            
            def raise_for_status(self):
                if self.status_code >= 400:
                    raise Exception(f"HTTP {self.status_code}")
        
        def mock_get(url, **kwargs):
            html = """
            <html>
            <head><title>Mock Article</title></head>
            <body>
                <article>
                    <h1>Mock Title</h1>
                    <p>This is mock content for testing URL parsing functionality.</p>
                </article>
            </body>
            </html>
            """
            return MockResponse(html)
        
        # Mock requests.get
        import requests
        monkeypatch.setattr(requests, "get", mock_get)
        
        with Readability() as reader:
            result = reader.parse_from_url("https://example.com")
            assert isinstance(result, ReadabilityResult)
            assert result.title is not None


class TestReadabilityResult:
    """Test cases for ReadabilityResult class"""
    
    def test_from_dict_empty(self):
        """Test creating ReadabilityResult from empty dict"""
        result = ReadabilityResult.from_dict({})
        assert result.title is None
        assert result.content is None
        assert result.text_content is None
    
    def test_from_dict_full(self):
        """Test creating ReadabilityResult from full dict"""
        data = {
            "title": "Test Title",
            "content": "<p>Test content</p>",
            "textContent": "Test content",
            "length": 100,
            "excerpt": "Test excerpt",
            "byline": "Test Author",
            "dir": "ltr",
            "siteName": "Test Site",
            "lang": "en",
            "publishedTime": "2023-01-01"
        }
        
        result = ReadabilityResult.from_dict(data)
        assert result.title == "Test Title"
        assert result.content == "<p>Test content</p>"
        assert result.text_content == "Test content"
        assert result.length == 100
        assert result.excerpt == "Test excerpt"
        assert result.byline == "Test Author"
        assert result.dir == "ltr"
        assert result.site_name == "Test Site"
        assert result.lang == "en"
        assert result.published_time == "2023-01-01"
    
    def test_from_dict_none(self):
        """Test creating ReadabilityResult from None"""
        result = ReadabilityResult.from_dict(None)
        assert result.title is None


class TestReadabilityError:
    """Test cases for ReadabilityError"""
    
    def test_readability_error(self):
        """Test ReadabilityError exception"""
        with pytest.raises(ReadabilityError):
            raise ReadabilityError("Test error")
        
        try:
            raise ReadabilityError("Test message")
        except ReadabilityError as e:
            assert str(e) == "Test message" 