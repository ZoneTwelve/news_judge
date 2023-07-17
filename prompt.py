#!/usr/bin/env python
import os, argparse
from dotenv import load_dotenv
import json
import openai

# Load from .env
load_dotenv()

# Set up your OpenAI API credentials
openai.api_key = os.getenv('OPENAI_API_KEY')

def prompt_conversion(prompt, keys, inputs):
  final_prompt = prompt
  for key in keys:
    with open(inputs[key]) as file:
      c = file.read() # content
    final_prompt = final_prompt.replace(f'${key}', c)
  return final_prompt

# Define the temperature for controlling the randomness of the output
# Need turn this into a modules
def submit( system_content, user_content ):

  response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
          {"role": "system", "content": system_content},
          {"role": "user", "content": user_content},
      ],
      temperature=0.0
  )

  # result = response['choices'][0]['message']['content']
  #print(result)
  return response



if __name__ == "__main__":
    print("Program start")
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
      print("=== Can not get the prompt file(s) ===")
      exit()


    if mode == 1:
      prompt_conversion( prompt=prompt, keys=prompt_config['inputs'], inputs=vars(args) )
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
        system_content= prompt_files['system'],
        user_content  = prompt_files['user']
      )

      print("=== Result ===")
      print(result['choices'][0]['message']['content'])
      print("="*20)
    else:
      print("Not Ready")
# exit()

