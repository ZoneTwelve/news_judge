# API Reference

Complete reference for all functions and modules in the News Inferencer.

## Table of Contents

- [prompt.py](#promptpy)
- [demo.py](#demopy)
- [main.py](#mainpy)
- [concept.py](#conceptpy)

## prompt.py

Command-line tool and OpenAI client for news inference.

### Functions

#### `submit(system_content, user_content)`

Send prompts to OpenAI API and get response.

**Parameters**:
- `system_content` (str): System role prompt content
- `user_content` (str): User task prompt content

**Returns**:
- `dict`: OpenAI API response object

**Example**:
```python
import prompt

response = prompt.submit(
    system_content="You are a legal analyst.",
    user_content="Analyze this news article..."
)

result = response['choices'][0]['message']['content']
```

**API Response Structure**:
```python
{
    'id': 'chatcmpl-...',
    'object': 'chat.completion',
    'created': 1234567890,
    'model': 'gpt-3.5-turbo',
    'choices': [
        {
            'index': 0,
            'message': {
                'role': 'assistant',
                'content': '...'
            },
            'finish_reason': 'stop'
        }
    ],
    'usage': {
        'prompt_tokens': 100,
        'completion_tokens': 50,
        'total_tokens': 150
    }
}
```

---

#### `prompt_conversion(prompt, keys, inputs)`

Replace placeholder variables in prompt with actual content from files.

**Parameters**:
- `prompt` (str): Template prompt with `$variable_name` placeholders
- `keys` (list): List of variable names to replace
- `inputs` (dict): Dictionary mapping variable names to file paths

**Returns**:
- `str`: Prompt with all variables replaced with file contents

**Example**:
```python
template = "Analyze: $news_content with keywords: $crime_keywords"
keys = ['news_content', 'crime_keywords']
inputs = {
    'news_content': 'samples/news.txt',
    'crime_keywords': 'samples/keywords.txt'
}

final_prompt = prompt.prompt_conversion(template, keys, inputs)
```

---

### Command-Line Interface

**Usage**:
```bash
./prompt.py [OPTIONS]
```

**Options**:

| Option | Type | Required | Description |
|--------|------|----------|-------------|
| `--config` | str | Yes | Path to prompt configuration JSON file |
| `--target` | str | No | Target subject to analyze |
| `--news-title` | str | No | Path to news title file |
| `--news-content` | str | No | Path to news content file |
| `--crime-keywords` | str | No | Path to crime keywords file |
| `--judge-keywords` | str | No | Path to legal proceeding keywords file |

**Example**:
```bash
./prompt.py \
  --config prompts/inferencer_v8.json \
  --news-content samples/case1/news_content.txt \
  --crime-keywords samples/crime_keywords.txt \
  --judge-keywords samples/judge_keywords.txt \
  --target "張三"
```

---

## demo.py

Gradio-based web interface for interactive analysis.

### Functions

#### `analysis(extractor_conf, inferencer_conf, crime_keywords_file, judge_keywords_file, news_content)`

Main analysis pipeline that extracts subjects and infers legal liability.

**Parameters**:
- `extractor_conf` (str): Extractor configuration filename (from `prompts/`)
- `inferencer_conf` (str): Inferencer configuration filename (from `prompts/`)
- `crime_keywords_file` (str): Crime keywords filename (from `samples/`)
- `judge_keywords_file` (str): Legal proceeding keywords filename (from `samples/`)
- `news_content` (str): Raw news article text

**Returns**:
- `str`: Markdown-formatted analysis results

**Process**:
1. Load keyword files
2. Run extractor to get subject list
3. For each subject, run inferencer
4. Aggregate and format results

**Example Output**:
```markdown
# 檢測結果

## 檢測主體:
- 張三
- 李四

## 檢測結果:

### 張三
<details>
- 主體: 張三
- 是否有嫌疑: 是
- 刑責: 詐欺
- 刑責進度: 起訴
- 事件摘要: 張三涉嫌詐欺罪被起訴
</details>
```

---

#### `complete(conf_file, crime_keywords, judge_keywords, news_content)`

Load configuration and prepare prompts with variable substitution.

**Parameters**:
- `conf_file` (str): Configuration filename (relative to `prompts/`)
- `crime_keywords` (str): Crime keywords content
- `judge_keywords` (str): Legal proceeding keywords content
- `news_content` (str): News article content

**Returns**:
- `dict`: Configuration with prompts ready for submission
  ```python
  {
      'name': 'Config Name',
      'files': {
          'system': '<prepared system prompt>',
          'user': '<prepared user prompt>'
      },
      'inputs': [...]
  }
  ```

**Example**:
```python
config = complete(
    'inferencer_v8.json',
    '詐欺, 洗錢',
    '起訴, 羈押',
    '新聞內容...'
)

result = prompt.submit(
    config['files']['system'],
    config['files']['user']
)
```

---

#### `read_config(config_file)`

Load JSON configuration file.

**Parameters**:
- `config_file` (str): Path to JSON configuration file

**Returns**:
- `dict`: Parsed configuration object

**Example**:
```python
config = read_config('prompts/inferencer_v7.json')
print(config['name'])  # "Inferencer V7"
```

---

### Gradio Interface

The demo interface is launched with:
```python
demo.launch()
```

**Interface Components**:

1. **Extractor Dropdown**: Select subject extraction strategy
2. **Inferencer Dropdown**: Select legal liability analysis strategy
3. **Crime Keywords Dropdown**: Select crime keyword set
4. **Judge Keywords Dropdown**: Select legal proceeding keyword set
5. **News Content Textbox**: Paste article text (multi-line)
6. **Submit Button**: Run analysis
7. **Output**: Markdown-formatted results

**Configuration**:
```python
demo = gr.Interface(
    fn=analysis,
    inputs=[...],
    outputs=gr.Markdown('# 檢測結果'),
    title='KryptoGO AI',
    description='自動化分析文章結構、尋找主體、歸納法律責任'
)
```

---

## main.py

Entry point that loads environment variables.

### Code

```python
#!/usr/bin/env python
from dotenv import load_dotenv
import os

# Configurations
load_dotenv()
```

**Purpose**:
- Loads `.env` file into environment variables
- Can be imported by other modules to ensure env is loaded

**Usage**:
```python
import main  # Loads .env automatically
import prompt

# Now can use environment variables
api_key = os.getenv('OPENAI_API_KEY')
```

---

## concept.py

Demonstration of crawler configuration pattern.

### Example Configuration

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
```

### URL Parsing

```python
from urllib.parse import urlparse

input_url = "https://news.example.com:8080/post/business/168936864"
parse_url = urlparse(input_url)
domain = parse_url.netloc  # "news.example.com:8080"
```

---

## Configuration File Schemas

### Prompt Configuration Schema

File: `prompts/*.json`

```json
{
  "name": "string - Display name",
  "files": {
    "system": "string - System prompt filename",
    "user": "string - User prompt filename"
  },
  "inputs": [
    "string - Variable name 1",
    "string - Variable name 2"
  ]
}
```

**Example**:
```json
{
  "name": "Legal Inferencer V8",
  "files": {
    "system": "inferencer_v8_system.txt",
    "user": "inferencer_v8_user.txt"
  },
  "inputs": [
    "crime_keywords",
    "judge_keywords",
    "news_content",
    "target"
  ]
}
```

---

## Environment Variables

Accessed via `os.getenv()` after loading `.env`:

```python
import os
from dotenv import load_dotenv

load_dotenv()

# Required
api_key = os.getenv('OPENAI_API_KEY')

# Optional with defaults
base_url = os.getenv('OPENAI_BASE_URL', 'https://api.openai.com/v1')
model = os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo')
temperature = float(os.getenv('OPENAI_TEMPERATURE', '0.0'))
```

See [Configuration Guide](CONFIGURATION.md) for all available variables.

---

## Error Handling

> **Note**: Current implementation has minimal error handling. Enhanced error handling is planned for Phase 2.

### Common Exceptions

**OpenAI API Errors**:
```python
try:
    response = prompt.submit(system, user)
except openai.error.AuthenticationError:
    print("Invalid API key")
except openai.error.RateLimitError:
    print("Rate limit exceeded")
except openai.error.APIError as e:
    print(f"API error: {e}")
```

**File Not Found**:
```python
try:
    with open(file_path) as f:
        content = f.read()
except FileNotFoundError:
    print(f"File not found: {file_path}")
```

**JSON Parse Error**:
```python
try:
    config = json.load(file)
except json.JSONDecodeError as e:
    print(f"Invalid JSON: {e}")
```

---

## Type Hints (Recommended)

While not currently implemented, here are recommended type hints:

```python
from typing import Dict, List, Any

def submit(
    system_content: str,
    user_content: str
) -> Dict[str, Any]:
    """Send prompts to OpenAI API."""
    ...

def prompt_conversion(
    prompt: str,
    keys: List[str],
    inputs: Dict[str, str]
) -> str:
    """Replace variables in prompt template."""
    ...

def analysis(
    extractor_conf: str,
    inferencer_conf: str,
    crime_keywords_file: str,
    judge_keywords_file: str,
    news_content: str
) -> str:
    """Run full analysis pipeline."""
    ...
```

---

## Testing

### Unit Test Example

```python
import pytest
from prompt import prompt_conversion

def test_prompt_conversion():
    template = "News: $news Keywords: $keywords"
    keys = ['news', 'keywords']
    
    # Mock file reading
    inputs = {
        'news': 'Test news content',
        'keywords': 'Test keywords'
    }
    
    # Note: Current implementation reads from files
    # This would need refactoring to support testing
    result = prompt_conversion(template, keys, inputs)
    
    assert '$news' not in result
    assert '$keywords' not in result
```

### Integration Test Example

```python
def test_full_pipeline():
    config = read_config('prompts/inferencer_v8.json')
    
    result = analysis(
        'extractor_v1-2.json',
        'inferencer_v8-1.json',
        'crime_keywords.txt',
        'judge_keywords.txt',
        'Test news content...'
    )
    
    assert '檢測結果' in result
    assert '主體' in result
```

---

## Related Documentation

- [Architecture Guide](ARCHITECTURE.md) - System design
- [Configuration Guide](CONFIGURATION.md) - Setup and config
- [Prompt Engineering](PROMPT_ENGINEERING.md) - Creating prompts

---

## Future API Changes (Phase 2)

Planned modernization will update the OpenAI client:

**Current** (v0.27.8):
```python
import openai
openai.api_key = os.getenv('OPENAI_API_KEY')
response = openai.ChatCompletion.create(...)
```

**Future** (v1.x):
```python
from openai import OpenAI
client = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY'),
    base_url=os.getenv('OPENAI_BASE_URL')
)
response = client.chat.completions.create(...)
```

This will be implemented in Phase 2: Code Quality & Modernization.
