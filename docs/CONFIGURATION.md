# Configuration Guide

This guide covers all configuration options for the News Inferencer.

## Table of Contents

- [Environment Variables](#environment-variables)
- [Prompt Configurations](#prompt-configurations)
- [Keyword Files](#keyword-files)
- [Crawler Configurations](#crawler-configurations)

## Environment Variables

Configuration via `.env` file in the project root.

### Required Configuration

```bash
# OpenAI API Key (Required)
OPENAI_API_KEY="sk-your-api-key-here"
```

Get your API key from: https://platform.openai.com/api-keys

### Optional Configuration

#### Custom API Endpoints

Use OpenAI-compatible services:

```bash
# Azure OpenAI
OPENAI_BASE_URL="https://your-resource.openai.azure.com/openai/deployments/your-deployment"
OPENAI_API_KEY="your-azure-api-key"
OPENAI_MODEL="gpt-35-turbo"  # Azure naming convention

# LocalAI (self-hosted)
OPENAI_BASE_URL="http://localhost:8080/v1"
OPENAI_MODEL="gpt-3.5-turbo"

# Other OpenAI-compatible service
OPENAI_BASE_URL="https://api.yourservice.com/v1"
```

#### Model Selection

```bash
# Default: gpt-3.5-turbo
OPENAI_MODEL="gpt-4"              # GPT-4
OPENAI_MODEL="gpt-4-turbo-preview" # GPT-4 Turbo
OPENAI_MODEL="gpt-3.5-turbo-16k"  # Extended context
```

#### API Parameters

```bash
# Temperature (0.0 - 2.0)
# Lower = more deterministic, Higher = more creative
OPENAI_TEMPERATURE="0.0"  # Default for legal analysis

# Max tokens (response length limit)
OPENAI_MAX_TOKENS="2000"
```

#### Gradio Demo Configuration

```bash
# Server port
GRADIO_SERVER_PORT="7860"

# Enable public sharing (creates public URL)
GRADIO_SHARE="false"  # Set to "true" to enable
```

#### Logging

```bash
# Log level: DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_LEVEL="INFO"
```

## Prompt Configurations

Prompt configurations define how the AI analyzes news articles.

### Configuration File Structure

Location: `prompts/*.json`

```json
{
  "name": "Human-readable name",
  "files": {
    "system": "system_prompt_file.txt",
    "user": "user_prompt_file.txt"
  },
  "inputs": [
    "crime_keywords",
    "judge_keywords",
    "news_content",
    "target"
  ]
}
```

### Configuration Fields

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Display name for this configuration |
| `files` | object | Prompt file mappings |
| `files.system` | string | System prompt filename (relative to config) |
| `files.user` | string | User prompt filename (relative to config) |
| `inputs` | array | Required input variables |

### Available Extractors

| Config File | Version | Description |
|------------|---------|-------------|
| `extractor_v1.json` | 1.0 | Basic subject extraction |
| `extractor_v1-1.json` | 1.1 | Improved entity recognition |
| `extractor_v1-2.json` | 1.2 | Enhanced accuracy |

### Available Inferencers

| Config File | Version | Description |
|------------|---------|-------------|
| `inferencer_v7.json` | 7.0 | Comprehensive legal analysis |
| `inferencer_v8.json` | 8.0 | Advanced inference with context |
| `inferencer_v8-1.json` | 8.1 | Latest with refined prompts |

### Variable Substitution

Prompt templates use `$variable_name` placeholders:

```text
分析以下新聞內容：

$news_content

請基於以下刑責關鍵字：
$crime_keywords

判斷關鍵字：
$judge_keywords

目標主體：$target
```

At runtime, variables are replaced with actual content.

### Creating Custom Prompts

1. **Create prompt text files**:
   ```bash
   touch prompts/my_prompt_system.txt
   touch prompts/my_prompt_user.txt
   ```

2. **Write your prompts** using `$variable_name` for placeholders

3. **Create configuration JSON**:
   ```json
   {
     "name": "My Custom Prompt",
     "files": {
       "system": "my_prompt_system.txt",
       "user": "my_prompt_user.txt"
     },
     "inputs": [
       "crime_keywords",
       "news_content"
     ]
   }
   ```

4. **Test your configuration**:
   ```bash
   ./prompt.py --config prompts/my_prompt.json \
               --crime-keywords samples/crime_keywords.txt \
               --news-content samples/case1/news_content.txt
   ```

See [PROMPT_ENGINEERING.md](PROMPT_ENGINEERING.md) for best practices.

## Keyword Files

Keyword files define terms for legal analysis.

### Format

Plain text, one term per line:

```text
詐欺
洗錢
侵占
背信
```

### Location

`samples/*.txt`

### Available Keyword Files

| File | Purpose | Example Terms |
|------|---------|---------------|
| `crime_keywords.txt` | Criminal offenses | 詐欺, 洗錢, 侵占 |
| `judge_keywords.txt` | Legal proceedings | 起訴, 羈押, 判決 |

### Creating Custom Keyword Files

```bash
# Create new keyword file
cat > samples/my_keywords.txt << EOF
關鍵字1
關鍵字2
關鍵字3
EOF
```

The file will automatically appear in the Gradio demo dropdowns.

## Crawler Configurations

> **Note**: The crawler is currently in concept phase. Full implementation coming soon.

### Concept Structure

Located in `concept.py` and `concept.js`

```python
crawler_config = {
    'news.example.com': {
        'title': '//h1[@class="article-title"]',
        'content': '//div[@class="article-body"]',
        'reporter': '//span[@class="author-name"]',
        'extra_publish_date': '//time[@datetime]'
    }
}
```

### XPath Selectors

| Field | Required | Description |
|-------|----------|-------------|
| `title` | ✅ | Article headline |
| `content` | ✅ | Main article text |
| `reporter` | ❌ | Author name |
| `extra_*` | ❌ | Additional custom fields |

### Adding New News Sources

1. Inspect the target website's HTML structure
2. Identify XPath selectors for required fields
3. Add configuration entry with domain as key
4. Test extraction

Example:
```python
config = {
    'www.newssite.com': {
        'title': '//article/header/h1',
        'content': '//article/div[@id="content"]//p',
        'reporter': '//div[@class="meta"]/span[@class="author"]',
        'extra_date': '//div[@class="meta"]/time'
    }
}
```

## Configuration Best Practices

### Security

1. **Never commit `.env`** - Add to `.gitignore`
2. **Use `.env.example`** - Template without secrets
3. **Rotate API keys** - Regularly update credentials
4. **Limit permissions** - Use read-only keys when possible

### Performance

1. **Use appropriate models**:
   - `gpt-3.5-turbo` - Fast, cost-effective
   - `gpt-4` - Higher accuracy, slower, more expensive

2. **Set reasonable token limits**:
   - Prevents excessive API costs
   - Ensures timely responses

3. **Adjust temperature**:
   - Use `0.0` for consistent legal analysis
   - Higher values for exploratory analysis

### Organization

1. **Name configurations descriptively**:
   - `extractor_v1-2_enhanced.json` ✅
   - `config.json` ❌

2. **Version your prompts**:
   - Keep old versions for comparison
   - Document changes in commit messages

3. **Organize keyword files by domain**:
   ```
   samples/
   ├── crime_keywords.txt
   ├── criminal_procedure_keywords.txt
   ├── civil_keywords.txt
   └── corporate_keywords.txt
   ```

## Troubleshooting

### Common Issues

**API Key Not Found**:
```
Solution: Ensure .env file exists and contains OPENAI_API_KEY
```

**Configuration File Not Loading**:
```
Solution: Check JSON syntax with jsonlint or similar tool
```

**Variable Not Replaced**:
```
Solution: Ensure variable name in 'inputs' array matches $variable_name in prompt
```

**Custom API Endpoint Not Working**:
```
Solution: Verify OPENAI_BASE_URL includes /v1 suffix for most services
```

## Examples

### Example 1: Azure OpenAI Configuration

`.env`:
```bash
OPENAI_API_KEY="your-azure-key"
OPENAI_BASE_URL="https://your-resource.openai.azure.com/openai/deployments/gpt-35-turbo"
OPENAI_MODEL="gpt-35-turbo"
```

### Example 2: LocalAI Self-Hosted

`.env`:
```bash
OPENAI_API_KEY="not-needed-but-required"
OPENAI_BASE_URL="http://localhost:8080/v1"
OPENAI_MODEL="ggml-gpt4all-j"
```

### Example 3: Production Setup

`.env`:
```bash
OPENAI_API_KEY="sk-prod-key-here"
OPENAI_MODEL="gpt-4"
OPENAI_TEMPERATURE="0.0"
OPENAI_MAX_TOKENS="3000"
LOG_LEVEL="WARNING"
GRADIO_SHARE="false"
```

---

**Related Documentation**:
- [Prompt Engineering Guide](PROMPT_ENGINEERING.md)
- [Architecture Guide](ARCHITECTURE.md)
- [Crawler Guide](CRAWLER_GUIDE.md)
