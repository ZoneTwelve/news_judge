#!/usr/bin/env python
import os, argparse
from dotenv import load_dotenv
import json
import openai

# Load from .env
load_dotenv()

# Set up your OpenAI API credentials
openai.api_key = os.getenv('OPENAI_API_KEY')

# Parse the argements
parser = argparse.ArgumentParser(description='OpenAI News Inferencer', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--config', type=str, default=None, help='The configration you want (ex. --config prompts/config.json)')
# Temperoary config
parser.add_argument('--target', type=str, default=None, help="target")
parser.add_argument('--news-title', type=str, default=None, help="news title")
parser.add_argument('--news-content', type=str, default=None, help="news content")
parser.add_argument('--crime-keywords', type=str, default=None, help="target")
parser.add_argument('--judge-keywords', type=str, default=None, help="target")
args = parser.parse_args()

dirname = os.path.dirname(args.config)
#args = parser.parse_args(args=[]) # Jupyter
# load configrations
with open(args.config) as file:
  prompt_config = json.load(file)
print(f"You're using '{prompt_config['name']}'")


# Define the prompt for generating text
prompt_file = os.path.join(dirname, prompt_config['file'])
with open(prompt_file, encoding='utf-8') as file:
  prompt = file.read()
print(prompt)


def prompt_conversion(prompt, keys, inputs):
  print(inputs)
  final_prompt = prompt
  for key in keys:
    print('READ', inputs[key])
    with open(inputs[key]) as file:
      c = file.read() # content
    final_prompt = final_prompt.replace(f'${key}', c)
  print('--- final prompt ---')
  print(final_prompt)
  print('-'*20)
prompt_conversion( prompt=prompt, keys=prompt_config['inputs'], inputs=vars(args) )
# exit()
# Define the temperature for controlling the randomness of the output
temperature = 0.0

# Generate text using the OpenAI API
response = openai.Completion.create(
    engine="gpt-3.5-turbo",
    prompt=prompt,
    max_tokens=100,
    temperature=temperature,
    n=1,
    stop=None,
)

# Extract the generated text from the API response
generated_text = response.choices[0].text.strip()

# Print the generated text
print(generated_text)
