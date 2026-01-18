#!/usr/bin/env python
"""
News Inferencer - AI-powered legal liability analysis for news articles.

This module provides the command-line interface and core API client for
interacting with OpenAI's GPT models to perform legal analysis on news content.

Supports custom OpenAI-compatible API endpoints via environment variables.
"""

import os
import argparse
from dotenv import load_dotenv
import json
from typing import Dict, List, Any, Optional
from openai import OpenAI

# Load from .env
load_dotenv()

# Initialize OpenAI client with support for custom base URL
client = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY'),
    base_url=os.getenv('OPENAI_BASE_URL')  # None defaults to official API
)


def prompt_conversion(prompt: str, keys: List[str], inputs: Dict[str, str]) -> str:
    """
    Replace placeholder variables in prompt template with actual content from files.
    
    Args:
        prompt: Template string containing $variable_name placeholders
        keys: List of variable names to replace
        inputs: Dictionary mapping variable names to file paths
        
    Returns:
        Prompt string with all variables replaced with file contents
        
    Example:
        >>> template = "News: $news_content"
        >>> keys = ['news_content']
        >>> inputs = {'news_content': 'samples/news.txt'}
        >>> result = prompt_conversion(template, keys, inputs)
    """
    final_prompt = prompt
    for key in keys:
        with open(inputs[key]) as file:
            c = file.read()  # content
        final_prompt = final_prompt.replace(f'${key}', c)
    return final_prompt


def submit(system_content: str, user_content: str) -> Dict[str, Any]:
    """
    Send prompts to OpenAI API and get completion response.
    
    Uses the ChatCompletion API with temperature=0.0 for deterministic output,
    which is ideal for legal analysis requiring consistent results.
    
    Supports custom API endpoints via OPENAI_BASE_URL environment variable,
    allowing integration with Azure OpenAI, LocalAI, and other compatible services.
    
    Args:
        system_content: System role prompt defining AI behavior and expertise
        user_content: User prompt containing the specific task and input data
        
    Returns:
        Dictionary containing OpenAI API response with structure:
            - choices: List of completion choices with messages
            - usage: Token usage statistics
            - model: Model used for completion
            
    Example:
        >>> response = submit(
        ...     system_content="You are a legal analyst.",
        ...     user_content="Analyze this article..."
        ... )
        >>> result = response['choices'][0]['message']['content']
    """
    # Get model and temperature from environment or use defaults
    model = os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo')
    temperature = float(os.getenv('OPENAI_TEMPERATURE', '0.0'))
    
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_content},
        ],
        temperature=temperature
    )
    
    # Convert response to dictionary for backward compatibility
    return response.model_dump()


if __name__ == "__main__":
    print("Program start")
    
    # Parse the arguments
    parser = argparse.ArgumentParser(
        description='OpenAI News Inferencer - AI-powered legal analysis for news articles',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        '--config',
        type=str,
        required=True,
        help='Path to prompt configuration JSON file (ex. --config prompts/inferencer_v8.json)'
    )
    
    # Input arguments
    parser.add_argument('--target', type=str, default=None, help="Target subject to analyze")
    parser.add_argument('--news-title', type=str, default=None, help="Path to news title file")
    parser.add_argument('--news-content', type=str, default=None, help="Path to news content file")
    parser.add_argument('--crime-keywords', type=str, default=None, help="Path to crime keywords file")
    parser.add_argument('--judge-keywords', type=str, default=None, help="Path to legal proceeding keywords file")
    args = parser.parse_args()

    dirname = os.path.dirname(args.config)
    
    # args = parser.parse_args(args=[]) # Jupyter
    # Load configurations
    with open(args.config) as file:
        prompt_config = json.load(file)
    print(f"You're using '{prompt_config['name']}'")


    # Define the prompt for generating text
    prompt_mode = 0
    if 'file' in prompt_config:
        mode = 1
        prompt_file = os.path.join(dirname, prompt_config['file'])
        with open(prompt_file, encoding='utf-8') as file:
            prompt = file.read()
        # print(prompt)
    elif 'files' in prompt_config:
        mode = 2
        prompt_files = dict()
        files = prompt_config['files']
        for key in files:
            pfile = os.path.join(dirname, files[key])
            with open(pfile, encoding='utf8') as file:
                prompt_files[key] = file.read()
    else:
        print("=== Cannot get the prompt file(s) ===")
        exit(1)


    if mode == 1:
        prompt_conversion(prompt=prompt, keys=prompt_config['inputs'], inputs=vars(args))
    elif mode == 2:
        for key in prompt_files:
            p = prompt_files[key]
            # print(key, p)
            prompt_files[key] = prompt_conversion(
                prompt=p,
                keys=prompt_config['inputs'],
                inputs=vars(args)
            )
        # print(prompt_files)
        result = submit(
            system_content=prompt_files['system'],
            user_content=prompt_files['user']
        )

        print("=== Result ===")
        print(result['choices'][0]['message']['content'])
        print("=" * 20)
    else:
        print("Not Ready")
    # exit()
