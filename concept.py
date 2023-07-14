#!/usr/bin/env python
from urllib.parse import urlparse

example = {
    'a': {
        'title': '#title',
        'content': '#content',
        'reporter': '#repoter_name',
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


input_url = "https://fakenews.exmaple-news.com:8080/post/business/168936864"
parse_url = urlparse(input_url)
print(parse_url.netloc)
