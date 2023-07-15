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

## Prompt.py Exmaple
```bash
./prompt.py --config prompts/inferencer_v7.json \
            --target samples/case1/target_1.txt \
            --news-title samples/case1/news_title.txt \
            --news-content samples/case1/news_content.txt \
            --crime-keywords samples/case1/crime_keywords.txt \
            --judge-keywords samples/case1/judge_keywords.txt

```
exmaple output: [inferencer v7](prompts/test/1.inferencer_v7.out)