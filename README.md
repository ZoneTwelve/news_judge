# News Inferencer

> An AI-powered news analysis system for detecting legal liabilities and extracting entities from Chinese news articles using OpenAI's GPT models.

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Usage](#usage)
  - [Command Line Interface](#command-line-interface)
  - [Demo Interface](#demo-interface)
  - [Configuration-Based Crawler](#configuration-based-crawler)
- [Configuration](#configuration)
- [Project Structure](#project-structure)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

News Inferencer (also known as KryptoGO AI) is an intelligent system that automatically analyzes news articles to:
- Extract subjects/entities mentioned in articles
- Identify potential legal liabilities and criminal implications
- Track legal proceeding statuses
- Provide structured summaries of legal-related events

The system uses a two-stage analysis pipeline:
1. **Extractor**: Identifies all subjects/entities mentioned in the news article
2. **Inferencer**: For each subject, analyzes their legal liability, criminal involvement, and case progress

## ✨ Features

- **Dual-Stage Analysis**: Subject extraction followed by legal liability inference
- **Configurable Prompts**: Multiple prompt templates for different analysis strategies
- **Web Interface**: User-friendly Gradio demo for interactive analysis
- **Configuration-Based Crawler**: Flexible XPath-based web scraping for news sources
- **Custom API Support**: Compatible with OpenAI-compatible APIs (Azure OpenAI, LocalAI, etc.)
- **Batch Processing**: Analyze multiple subjects from a single article
- **Multilingual Support**: Primarily designed for Chinese news articles

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/yourusername/news_inferencer.git
cd news_inferencer

# Set up virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env and add your OpenAI API key

# Run the demo interface
python demo.py
```

The Gradio interface will open in your browser at `http://localhost:7860`

## 📦 Installation

### Prerequisites

- Python 3.11.3 or higher
- OpenAI API key (or compatible API endpoint)

### Step-by-Step Installation

1. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and configure:
   ```bash
   # Required
   OPENAI_API_KEY="your-api-key-here"
   
   # Optional: For custom OpenAI-compatible endpoints
   # OPENAI_BASE_URL="https://api.openai.com/v1"
   # OPENAI_MODEL="gpt-3.5-turbo"
   ```

## 💻 Usage

### Command Line Interface

Analyze news articles using the command-line tool:

```bash
./prompt.py --config prompts/inferencer_v7.json \
            --target samples/case1/target_1.txt \
            --news-title samples/case1/news_title.txt \
            --news-content samples/case1/news_content.txt \
            --crime-keywords samples/case1/crime_keywords.txt \
            --judge-keywords samples/case1/judge_keywords.txt
```

**Parameters**:
- `--config`: Path to the prompt configuration file
- `--target`: Subject/entity to analyze
- `--news-title`: Path to file containing the news title
- `--news-content`: Path to file containing the news content
- `--crime-keywords`: Path to file with crime-related keywords
- `--judge-keywords`: Path to file with legal proceeding keywords

**Example output**: [inferencer v7 result](prompts/test/1.inferencer_v7.out)

### Demo Interface

Launch the interactive Gradio interface:

```bash
python demo.py
```

Features of the demo interface:
- Select extractor and inferencer versions from dropdowns
- Choose keyword sets for analysis
- Paste news content directly into the text box
- View structured results with expandable details
- Test different prompt strategies interactively

### Configuration-Based Crawler

The crawler can fetch content from various news websites using XPath configurations.

**Configuration Format**:
```json
{
  "news.example.com": {
    "title": "//article/h1[@class='title']",
    "content": "//article/div[@class='content']",
    "reporter": "//span[@class='author']",
    "extra_publish_date": "//time[@class='date']"
  }
}
```

See [docs/CRAWLER_GUIDE.md](docs/CRAWLER_GUIDE.md) for detailed usage.

## ⚙️ Configuration

### Prompt Configuration Files

Prompt configurations are stored in the `prompts/` directory in JSON format:

```json
{
  "name": "Inferencer V7",
  "files": {
    "system": "inferencer_v7_system.txt",
    "user": "inferencer_v7_user.txt"
  },
  "inputs": [
    "crime_keywords",
    "judge_keywords",
    "news_content"
  ]
}
```

### Available Configurations

**Extractors** (Subject Extraction):
- `extractor_v1.json` - Basic subject extraction
- `extractor_v1-1.json` - Improved entity recognition
- `extractor_v1-2.json` - Enhanced accuracy

**Inferencers** (Legal Liability Analysis):
- `inferencer_v7.json` - Comprehensive legal analysis
- `inferencer_v8.json` - Advanced inference with context
- `inferencer_v8-1.json` - Latest version with refined prompts

See [docs/PROMPT_ENGINEERING.md](docs/PROMPT_ENGINEERING.md) for creating custom prompts.

## 📁 Project Structure

```
news_inferencer/
├── prompts/              # Prompt configuration files and templates
├── samples/              # Sample data for testing
│   └── case1/           # Example case with test files
├── benchmark/            # Benchmarking tools and scripts
├── kgai/                # Core library module
├── prompt.py            # Command-line inference tool
├── demo.py              # Gradio web interface
├── main.py              # Entry point with env loading
├── concept.py           # Crawler concept demonstration
├── requirements.txt     # Python dependencies
├── .env.example         # Environment variable template
└── docs/                # Documentation
```

## 📚 Documentation

- **[Architecture Guide](docs/ARCHITECTURE.md)** - System design and data flow
- **[API Reference](docs/API_REFERENCE.md)** - Function and class documentation
- **[Configuration Guide](docs/CONFIGURATION.md)** - Detailed configuration options
- **[Crawler Guide](docs/CRAWLER_GUIDE.md)** - Web scraping usage
- **[Prompt Engineering](docs/PROMPT_ENGINEERING.md)** - Creating custom prompts
- **[Contributing](CONTRIBUTING.md)** - How to contribute

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guide](CONTRIBUTING.md) for details on:
- Code style guidelines
- Development setup
- Testing requirements
- Pull request process

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Powered by [OpenAI GPT models](https://openai.com/)
- UI built with [Gradio](https://gradio.app/)

---

**Note**: This system is designed for research and analysis purposes. Legal determinations should always be made by qualified legal professionals.