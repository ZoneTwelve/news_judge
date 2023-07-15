# FFHC Inferencer

## Intro

I don't have time to write the intro.

## Initialization

### environment variable (.env)

Example file in [example.env](example.env)

### virtual environment

```bash
# Python 3.11.3

python -m venv venv 
```

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