#!/usr/bin/env python
from dotenv import load_dotenv
import os
from langchain.chat_models import ChatOpenAI
from langchain import LLMChain
from langchain.prompts.chat import (
        ChatPromptTemplate,
        SystemMessagePromptTemplate,
        HumanMessagePromptTemplate,
    )

# Configrations
load_dotenv()
#openai.api_key = os.getenv("OPENAI_API_KEY")


