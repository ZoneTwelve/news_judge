# Crawler Guide

## Overview

The News Inferencer includes a configuration-based web crawler that can extract content from various news websites using XPath selectors.

> **Status**: Currently in concept/prototype phase. Full implementation coming in future releases.

## Concept

The crawler uses a simple but powerful configuration pattern:

```python
{
  "website_domain": {
    "title": "xpath_selector",
    "content": "xpath_selector",
    "reporter": "xpath_selector",
    "extra_field_name": "xpath_selector"
  }
}
```

## Configuration Format

### Basic Structure

```json
{
  "news.example.com": {
    "title": "//h1[@class='headline']",
    "content": "//div[@class='article-body']",
    "reporter": "//span[@class='author']"
  }
}
```

### Required Fields

| Field | Description | Example XPath |
|-------|-------------|---------------|
| `title` | Article headline | `//h1[@class="title"]` |
| `content` | Main article text | `//div[@id="content"]` |

### Optional Fields

| Field | Description | Example XPath |
|-------|-------------|---------------|
| `reporter` | Author/reporter name | `//span[@class="author"]` |
| `extra_*` | Custom fields (any name starting with `extra_`) | `//time[@class="date"]` |

### Extra Fields

Add custom fields by prefixing with `extra_`:

```json
{
  "news.example.com": {
    "title": "//h1",
    "content": "//article/p",
    "reporter": "//span[@class='author']",
    "extra_publish_date": "//time[@datetime]",
    "extra_category": "//div[@class='category']/span",
    "extra_tags": "//div[@class='tags']/a"
  }
}
```

## XPath Basics

### Common Patterns

**Select by class**:
```xpath
//div[@class="article-content"]
```

**Select by ID**:
```xpath
//div[@id="main-content"]
```

**Select by attribute**:
```xpath
//article[@data-type="news"]
```

**Select nested elements**:
```xpath
//article/div[@class="body"]/p
```

**Select all paragraphs in article**:
```xpath
//article//p
```

**Select by multiple conditions**:
```xpath
//div[@class="content" and @data-visible="true"]
```

###  Advanced Selectors

**Get attribute value**:
```xpath
//img[@class="cover"]/@src
//time/@datetime
```

**Get text content**:
```xpath
//h1/text()
```

**Select by partial match**:
```xpath
//div[contains(@class, "article")]
```

**Select by position**:
```xpath
//div[@class="section"][1]  # First section
//div[@class="section"][last()]  # Last section
```

## Testing XPath Selectors

### Browser Developer Tools

1. **Open DevTools** (F12 or Right-click → Inspect)
2. **Go to Console tab**
3. **Test XPath**:
   ```javascript
   $x("//h1[@class='title']")
   ```

### Python Testing

```python
from lxml import html
import requests

# Fetch page
response = requests.get('https://news.example.com/article/123')
tree = html.fromstring(response.content)

# Test XPath
title = tree.xpath('//h1[@class="title"]/text()')
print(title)
```

## Example Configurations

### Example 1: Simple News Site

```python
config = {
    'simplenews.com': {
        'title': '//h1[@class="article-title"]',
        'content': '//div[@class="article-content"]//p',
        'reporter': '//span[@class="author-name"]'
    }
}
```

### Example 2: Complex Structure

```python
config = {
    'complexnews.com': {
        'title': '//article/header/h1[@class="headline"]',
        'content': '//article/div[@id="article-body"]//p[not(@class="ad")]',
        'reporter': '//div[@class="metadata"]/span[@itemprop="author"]',
        'extra_publish_date': '//time[@class="publish-date"]/@datetime',
        'extra_category': '//nav[@class="breadcrumb"]/a[last()]/text()',
        'extra_image_url': '//meta[@property="og:image"]/@content'
    }
}
```

### Example 3: Multiple News Sources

```python
config = {
    'siteA.com': {
        'title': '//h1[@class="title"]',
        'content': '//div[@class="content"]',
        'reporter': '//span[@class="author"]',
        'extra_date': '//time'
    },
    'siteB.com': {
        'title': '//article/h1',
        'content': '//article/div[@class="body"]',
        'reporter': None,  # No reporter on this site
        'extra_date': '//div[@class="meta"]/time'
    },
    'siteC.com': {
        'title': '//div[@id="headline"]/text()',
        'content': '//div[@id="story"]//p',
        'reporter': '//div[@class="byline"]/a',
        'extra_image': '//img[@class="featured"]/@src'
    }
}
```

## Implementation Reference

### Current Concept Code

See [concept.py](file:///private/tmp/news_inferencer/concept.py):

```python
example = {
    'a': {
        'title': '#title',
        'content': '#content',
        'reporter': '#reporter_name',
        'extra_img_alt': '#cover[alt]',
    },
    'b': {
        'title': '#news_title',
        'content': '#news_content',
        'reporter': None,
        'extra_image_cover_alt': '#img_cover[alt]',
        'extra_image_sub_alt': '#img_sub[alt]',
    },
}

for site, config in example.items():
    print(site, config)
```

### Domain Extraction

From URL to configuration key:

```python
from urllib.parse import urlparse

url = "https://news.example.com:8080/post/business/168936864"
parsed = urlparse(url)
domain = parsed.netloc  # Returns: "news.example.com:8080"
```

## Creating Your Own Crawler Configuration

### Step-by-Step Guide

1. **Identify Target Website**
   - Choose the news website you want to scrape
   - Ensure you have permission to scrape

2. **Inspect HTML Structure**
   - Navigate to a sample article
   - Right-click on the title → Inspect
   - Note the element structure and classes/IDs

3. **Create XPath Selectors**
   - Write XPath for title, content, reporter
   - Test in browser console using `$x()`
   - Verify selectors return correct elements

4. **Add Configuration Entry**
   ```python
   config = {
       'your-news-site.com': {
           'title': '//your/xpath/here',
           'content': '//your/xpath/here',
           'reporter': '//your/xpath/here',
       }
   }
   ```

5. **Test Extraction**
   - Run the crawler on sample URLs
   - Verify extracted content is correct
   - Adjust XPath selectors as needed

## Best Practices

### XPath Guidelines

1. **Be Specific**: Use class and ID attributes when available
2. **Avoid Position-Based**: Don't rely on `[1]`, `[2]` unless necessary
3. **Handle Variations**: Use `contains()` for flexible matching
4. **Test Multiple Articles**: Ensure selectors work across different articles

### Configuration Tips

1. **Use Descriptive Extra Fields**:
   - Good: `extra_publish_date`, `extra_category`
   - Bad: `extra_field1`, `extra_x`

2. **Handle Missing Elements Gracefully**:
   - Set to `None` if field doesn't exist on site
   - Crawler should handle missing optional fields

3. **Document Special Cases**:
   ```python
   config = {
       'special-site.com': {
           # This site uses JS rendering, needs special handling
           'title': '//h1[@data-title]/@data-title',
           'content': '//div[@id="dynamic-content"]'
       }
   }
   ```

## Limitations & Future Work

### Current Limitations

- ❌ No JavaScript rendering support
- ❌ No pagination handling
- ❌ No rate limiting
- ❌ Basic error handling only
- ❌ No proxy support

### Planned Features

- ✅ Playwright/Selenium integration for JS-heavy sites
- ✅ Automatic retry with exponential backoff
- ✅ Rate limiting per domain
- ✅ Proxy rotation
- ✅ User-agent rotation
- ✅ Cookie/session management
- ✅ Result caching

## Troubleshooting

### Common Issues

**XPath Returns Empty**:
- Check if element exists in page source
- Verify XPath syntax in browser console
- Check for JavaScript-rendered content

**Wrong Content Extracted**:
- Inspect actual HTML structure
- Look for more specific selectors
- Check if site structure changed

**Character Encoding Issues**:
- Ensure proper UTF-8 handling
- Check response headers for charset
- Use lxml's built-in encoding detection

## Resources

- [XPath Tutorial (W3Schools)](https://www.w3schools.com/xml/xpath_intro.asp)
- [XPath Cheatsheet](https://devhints.io/xpath)
- [lxml Documentation](https://lxml.de/)

---

**Related Documentation**:
- [Architecture Guide](ARCHITECTURE.md)
- [Configuration Guide](CONFIGURATION.md)
