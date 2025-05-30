// Readability Wrapper for Python integration
// This file provides a unified interface to Mozilla's readability.js library

// Helper function to check if a node is visible
function isNodeVisible(node) {
    return (!node.style || node.style.display != "none")
        && !node.hasAttribute("hidden")
        && (!node.hasAttribute("aria-hidden") || node.getAttribute("aria-hidden") != "true"
            || (node.className && node.className.indexOf && node.className.indexOf("fallback-image") !== -1));
}

// Regular expressions used by readability (simplified)
var REGEXPS = {
    unlikelyCandidates: /banner|breadcrumbs|combx|comment|community|cover-wrap|disqus|extra|foot|header|legends|menu|related|remark|replies|rss|shoutbox|sidebar|skyscraper|social|sponsor|supplemental|ad-break|agegate|pagination|pager|popup|yom-remote/i,
    okMaybeItsACandidate: /and|article|body|column|main|shadow/i,
};

// Helper function to get elements by tag name across the document
function getElementsByTagNames(document, tagNames) {
    var result = [];
    for (var i = 0; i < tagNames.length; i++) {
        var elements = document.getElementsByTagName(tagNames[i]);
        for (var j = 0; j < elements.length; j++) {
            result.push(elements[j]);
        }
    }
    return result;
}

// Helper function to check if content is probably readerable
function isProbablyReaderable(document, options) {
    options = options || {};
    
    var minContentLength = options.minContentLength || 140;
    var minScore = options.minScore || 20;
    var visibilityChecker = options.visibilityChecker || isNodeVisible;
    
    // Use getElementsByTagName instead of querySelectorAll since JSDOMParser may not support CSS selectors
    var pElements = document.getElementsByTagName("p");
    var preElements = document.getElementsByTagName("pre");
    var nodes = [];
    
    // Combine p and pre elements
    for (var i = 0; i < pElements.length; i++) {
        nodes.push(pElements[i]);
    }
    for (var i = 0; i < preElements.length; i++) {
        nodes.push(preElements[i]);
    }
    
    // For br elements inside divs, get all div elements and check for br children
    var divElements = document.getElementsByTagName("div");
    var brParents = [];
    for (var i = 0; i < divElements.length; i++) {
        var div = divElements[i];
        var brElements = div.getElementsByTagName("br");
        if (brElements.length > 0) {
            brParents.push(div);
        }
    }
    
    // Add br parent divs to nodes
    for (var i = 0; i < brParents.length; i++) {
        if (nodes.indexOf(brParents[i]) === -1) {
            nodes.push(brParents[i]);
        }
    }
    
    var score = 0;
    for (var i = 0; i < nodes.length; i++) {
        var node = nodes[i];
        
        if (!visibilityChecker(node)) {
            continue;
        }
        
        var className = node.className || "";
        var id = node.id || "";
        var matchString = className + " " + id;
        
        if (REGEXPS.unlikelyCandidates.test(matchString) &&
            !REGEXPS.okMaybeItsACandidate.test(matchString)) {
            continue;
        }
        
        // Skip p elements that are inside li elements (simplified check)
        if (node.tagName && node.tagName.toLowerCase() === "p" && node.parentNode) {
            var parent = node.parentNode;
            if (parent.tagName && parent.tagName.toLowerCase() === "li") {
                continue;
            }
        }
        
        var textContent = node.textContent || "";
        var textContentLength = textContent.trim().length;
        if (textContentLength < minContentLength) {
            continue;
        }
        
        score += Math.sqrt(textContentLength - minContentLength);
        
        if (score > minScore) {
            return true;
        }
    }
    
    return false;
}

// Main interface functions
var ReadabilityWrapper = {
    // Parse HTML content and return article
    parseHTML: function(htmlContent, url, options) {
        try {
            // Create a mock document if we don't have a real DOM
            var parser = new JSDOMParser();
            var doc = parser.parse(htmlContent, url);
            
            // Create Readability instance
            var reader = new Readability(doc, options || {});
            
            // Parse and return result
            var result = reader.parse();
            
            return {
                success: true,
                result: result
            };
        } catch (error) {
            return {
                success: false,
                error: error.message || String(error)
            };
        }
    },
    
    // Check if content is probably readerable
    isProbablyReaderable: function(htmlContent, url, options) {
        try {
            var parser = new JSDOMParser();
            var doc = parser.parse(htmlContent, url);
            
            // Use our custom isProbablyReaderable function
            var result = isProbablyReaderable(doc, options || {});
            
            return {
                success: true,
                result: result
            };
        } catch (error) {
            return {
                success: false,
                error: error.message || String(error)
            };
        }
    }
};

// Export for use in different environments
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ReadabilityWrapper;
} else if (typeof window !== 'undefined') {
    window.ReadabilityWrapper = ReadabilityWrapper;
} else {
    // For QuickJS environment
    this.ReadabilityWrapper = ReadabilityWrapper;
} 