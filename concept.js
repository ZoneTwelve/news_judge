#!/usr/bin/env node
const url = require('node:url');
let example = {
  'a': {
    'title': '#title',
    'content': '#content',
    'reporter': '#repoter_name',
    'extra_img_alt': '#cover[alt]',
  },
  'b': {
    'title': '#news_title',
    'content': '#news_content',
    'reporter': null,
    'extra_image_cover_alt': '#img_cover[alt]',
    'extra_image_sub_alt': '#img_sub[alt]',
  },
}

for(let site in example){
  let config = example[site];
  console.log(site, config);
}

let input_url = "https://fakenews.example-news.com:8080/post/business/168936864";

let parse_url = url.parse(input_url, false);

console.log(parse_url.host);