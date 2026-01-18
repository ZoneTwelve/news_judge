#!/usr/bin/env python
"""
Demo Web Interface for News Inferencer.

Provides a Gradio-based web interface for interactive legal analysis of news articles.
Users can select extractor/inferencer configurations, provide keywords, and paste
news content to receive structured analysis results.
"""

import os
import gradio as gr
import prompt
import json
import re
from typing import Dict, List, Any


def analysis(
    extractor_conf: str,
    inferencer_conf: str,
    crime_keywords_file: str,
    judge_keywords_file: str,
    news_content: str
) -> str:
    """
    Main analysis pipeline that extracts subjects and infers legal liability.
    
    This function orchestrates the two-stage analysis:
    1. Extract all subjects mentioned in the news article
    2. For each subject, analyze their legal liability
    
    Args:
        extractor_conf: Extractor configuration filename (from prompts/)
        inferencer_conf: Inferencer configuration filename (from prompts/)
        crime_keywords_file: Crime keywords filename (from samples/)
        judge_keywords_file: Legal proceeding keywords filename (from samples/)
        news_content: Raw news article text
        
    Returns:
        Markdown-formatted analysis results with detected subjects and
        their legal liability assessments
    """
    dirname = os.path.dirname(__file__)
    crime_keywords = open(os.path.join(dirname, 'samples', crime_keywords_file)).read()
    judge_keywords = open(os.path.join(dirname, 'samples', judge_keywords_file)).read()
    extractor = complete(extractor_conf, crime_keywords, judge_keywords, news_content)
    inferencer = complete(inferencer_conf, crime_keywords, judge_keywords, news_content)
    print(extractor, inferencer)
    
    # Execute the pipeline
    extractor_result = prompt.submit(
        system_content=extractor['files']['system'],
        user_content=extractor['files']['user']
    )
    
    # users = get_users(response['choices'][0]['message']['content'])
    # convert users array to string
    # Only support extractor_v1-1.json, extractor_v1-2.json
    users = extractor_result['choices'][0]['message']['content'].split(': ')[1].split(',')
    # replace each user whitespaces
    users = [user.strip() for user in users]
    print(users)

    user_list = ""
    analysis_result = ""
    for user in users:
        user_list += f'\n- {user}\n'
        print(inferencer['files']['user'].replace('$target', user))
        inferencer_result = prompt.submit(
            system_content=inferencer['files']['system'],
            user_content=inferencer['files']['user'].replace('$target', user)
        )
        print()
        user_result = inferencer_result['choices'][0]['message']['content'].split("### 輸出格式\n").pop()
        keys = ['主體', '是否有嫌疑', '刑責', '刑責進度', '事件摘要']
        progress = 0
        output = ""
        print(user_result.split('\n'))
        for res in user_result.split("\n"):
            content = res.split(": ")
            output += f"- {keys[progress]}: {content[1]}\n<br>\n"
            progress += 1

        # hardcoded
        ## Regex
        ## 討論的主體(target): (.*)
        ## 是否涉及任何刑責關鍵字(是或否): (是|否)
        ## 涉及刑責關鍵字(逗號分割): (.*)
        ## 涉及刑責進度關鍵字(逗號分割): (.*)
        # ## 事件摘要(50字): (.*)

        # match = re.search(pattern, user_result, re.DOTALL)
        # if match:
        #     target = match.group(1)
        #     involves_crime = match.group(2)
        #     crime_keywords = match.group(3)
        #     crime_progress = match.group(4)
        #     summary = match.group(5)

        #     print("Target:", target)
        #     print("Involves Crime:", involves_crime)
        #     print("Crime Keywords:", crime_keywords)
        #     print("Crime Progress:", crime_progress)
        #     print("Summary:", summary)
        # else:
        #     target = 'Unknow'
        #     involves_crime = 'Unknow'
        #     crime_keywords = 'Unknow'
        #     crime_progress = 'Unknow'
        #     summary = 'Unknow'
        # # hardcode end
        # print(user_result)
        print(output)
        print("=" * 10)
        analysis_result += f'\n### {user}\n<details>\n{output}</details>\n'
    return f"""
    # 檢測結果
    ## 檢測主體:
    {user_list}

    ## 檢測結果:
    {analysis_result}
    """


def read_config(config_file: str) -> Dict[str, Any]:
    """
    Load JSON configuration file.
    
    Args:
        config_file: Path to JSON configuration file
        
    Returns:
        Parsed configuration dictionary
    """
    with open(config_file) as file:
        config = json.load(file)
    return config


def complete(
    conf_file: str,
    crime_keywords: str,
    judge_keywords: str,
    news_content: str
) -> Dict[str, Any]:
    """
    Load configuration and prepare prompts with variable substitution.
    
    Args:
        conf_file: Configuration filename (relative to prompts/)
        crime_keywords: Crime keywords content
        judge_keywords: Legal proceeding keywords content
        news_content: News article content
        
    Returns:
        Configuration dictionary with prompts ready for submission
    """
    inputs = {
        'crime_keywords': crime_keywords,
        'judge_keywords': judge_keywords,
        'news_content': news_content
    }
    dirname = os.path.dirname(__file__)
    conf = read_config(os.path.join(dirname, 'prompts', conf_file))
    for file in conf['files']:
        prompt_text = open(os.path.join(dirname, 'prompts', conf['files'][file])).read()
        for key in conf['inputs']:
            if key in inputs:
                prompt_text = prompt_text.replace(f'${key}', inputs[key])
            else:
                print("Can not find the key: ", key)
        conf['files'][file] = prompt_text
    return conf

    
_ExtractorList = [file for file in os.listdir('./prompts') if file.startswith('extractor') and file.endswith('.json')]
_InferencerList = [file for file in os.listdir('./prompts') if file.startswith('inferencer') and file.endswith('.json')]
_CrimeKeywords = [file for file in os.listdir('./samples') if file.startswith('crime') and file.endswith('.txt')]
_JudgeKeywords = [file for file in os.listdir('./samples') if file.startswith('judge') and file.endswith('.txt')]

demo = gr.Interface(
    fn=analysis,
    inputs=[
        gr.Dropdown(
            _ExtractorList,
            value=_ExtractorList[0],
            label='Extractor',
            info='主體解析器'
        ),
        gr.Dropdown(
            _InferencerList,
            value=_InferencerList[0],
            label='Inferencer',
            info='內文解析器'
        ),
        gr.Dropdown(
            _CrimeKeywords,
            value=_CrimeKeywords[0],
            label='Crime Keywords',
            info='刑責關鍵字'
        ),
        gr.Dropdown(
            _JudgeKeywords,
            value=_JudgeKeywords[0],
            label='Judge Keywords',
            info='刑責進度關鍵字'
        ),
        # news content
        # Multi-line text box
        gr.Textbox(
            label='新聞內容',
            placeholder='請輸入新聞內容',
            lines=10,
        ),
        
        # gr.Textbox(
        #     label='新聞內容',
        #     placeholder='請輸入新聞內容',
        # )
    ],
    outputs=gr.Markdown('# 檢測結果\n範例主體: <details>更多細節</details>'),
    examples=[
        [
           'extractor_v1-1.json', 
           'inferencer_v8-1.json',
            'crime_keywords.txt',
            'judge_keywords.txt',
        ]
    ],
    title='KryptoGO AI',
    description='這是一個自動化分析文章結構、尋找主體、歸納法律責任等的 AI 範例',
    css="footer {visibility: hidden}"
)

demo.launch()
