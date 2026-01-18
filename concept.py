#!/usr/bin/env python
"""
Concept demonstration for configuration-based web crawler.

This module demonstrates the pattern for creating XPath-based crawler
configurations that can extract content from various news websites.
"""

from urllib.parse import urlparse

# Example crawler configuration pattern
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


input_url = "https://news.example.com:8080/post/business/168936864"
parse_url = urlparse(input_url)
print(parse_url.netloc)
