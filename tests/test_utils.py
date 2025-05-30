"""
Tests for fast_readability.utils module
"""

import pytest
from fast_readability.utils import (
    is_probably_readerable,
    parse_html,
    parse_from_url,
    get_default_options,
    create_custom_options
)
from fast_readability import ReadabilityResult, ReadabilityError


class TestUtilityFunctions:
    """Test cases for utility functions"""
    
    def test_get_default_options(self):
        """Test get_default_options function"""
        options = get_default_options()
        
        assert isinstance(options, dict)
        assert options["debug"] is False
        assert options["maxElemsToParse"] == 0
        assert options["nbTopCandidates"] == 5
        assert options["charThreshold"] == 500
        assert options["classesToPreserve"] == []
        assert options["keepClasses"] is False
        assert options["disableJSONLD"] is False
        assert options["allowedVideoRegex"] is None
        assert options["linkDensityModifier"] == 0
    
    def test_create_custom_options_defaults(self):
        """Test create_custom_options with default values"""
        options = create_custom_options()
        
        assert isinstance(options, dict)
        assert options["debug"] is False
        assert options["maxElemsToParse"] == 0
        assert options["nbTopCandidates"] == 5
        assert options["charThreshold"] == 500
        assert options["classesToPreserve"] == []
        assert options["keepClasses"] is False
        assert options["disableJSONLD"] is False
        assert options["linkDensityModifier"] == 0.0
    
    def test_create_custom_options_custom_values(self):
        """Test create_custom_options with custom values"""
        options = create_custom_options(
            char_threshold=200,
            keep_classes=True,
            classes_to_preserve=["article", "content"],
            max_elems_to_parse=1000,
            nb_top_candidates=3,
            debug=True,
            disable_json_ld=True,
            link_density_modifier=0.5
        )
        
        assert options["debug"] is True
        assert options["maxElemsToParse"] == 1000
        assert options["nbTopCandidates"] == 3
        assert options["charThreshold"] == 200
        assert options["classesToPreserve"] == ["article", "content"]
        assert options["keepClasses"] is True
        assert options["disableJSONLD"] is True
        assert options["linkDensityModifier"] == 0.5
    
    def test_is_probably_readerable_utility(self):
        """Test is_probably_readerable utility function"""
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
        
        assert is_probably_readerable(readable_html) is True
        assert is_probably_readerable(non_readable_html) is False
    
    def test_parse_html_utility(self):
        """Test parse_html utility function"""
        html = """
        <html>
        <head><title>Test Article</title></head>
        <body>
            <article>
                <h1>Test Title</h1>
                <p>This is a test paragraph with enough content to be considered readable by the algorithm.</p>
            </article>
        </body>
        </html>
        """
        
        result = parse_html(html, "https://example.com")
        
        assert isinstance(result, ReadabilityResult)
        assert result.title is not None
        assert result.content is not None
        assert result.text_content is not None
    
    def test_parse_html_with_options(self):
        """Test parse_html with custom options"""
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
        
        options = create_custom_options(char_threshold=50, keep_classes=True)
        result = parse_html(html, "", options)
        
        assert isinstance(result, ReadabilityResult)
    
    def test_parse_from_url_utility_mock(self, monkeypatch):
        """Test parse_from_url utility function with mocked requests"""
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
                    <p>This is mock content for testing URL parsing functionality with enough text to be readable.</p>
                </article>
            </body>
            </html>
            """
            return MockResponse(html)
        
        # Mock requests.get
        import requests
        monkeypatch.setattr(requests, "get", mock_get)
        
        result = parse_from_url("https://example.com")
        assert isinstance(result, ReadabilityResult)
        assert result.title is not None
    
    def test_utility_functions_with_errors(self):
        """Test utility functions handle errors properly"""
        # Test with invalid HTML that might cause errors
        with pytest.raises(ReadabilityError):
            # This should trigger some error in the JavaScript execution
            parse_html("<<invalid>>html<<", "") 