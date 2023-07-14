# FFHC Inferencer

## Intro

I don't have time to write the intro.

## Crawler

A configration based crawler, that can fetch almost all the website.

### Design pattern

```json
{
  "WEBSITE_HOST": {
    "title": XPATH,
    "content": XPATH,
    "reporter": XPATH,
    "extra_{NAME}": XPATH
    ...
  }
}
```