# -*- coding: utf-8 -*-
"""AI custom data chat  drive

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ufvkBt8YBpArOCT4QpLN_g8YrwQmGMH6
"""

! git clone https://github.com/Suhicodes/insurance_data.git

from google.colab import drive
drive.mount('/content/drive')

!pip install llama-index==0.5.6
!pip install langchain==0.0.148
!pip install PyPDF2

from llama_index import SimpleDirectoryReader, GPTListIndex, readers, GPTSimpleVectorIndex, LLMPredictor, PromptHelper, ServiceContext
from langchain import OpenAI
import sys
import os
from IPython.display import Markdown, display

def construct_index(directory_path):
    # set maximum input size
    max_input_size = 4096
    # set number of output tokens
    num_outputs = 2000
    # set maximum chunk overlap
    max_chunk_overlap = 20
    # set chunk size limit
    chunk_size_limit = 600

    # define prompt helper
    prompt_helper = PromptHelper(max_input_size, num_outputs, max_chunk_overlap, chunk_size_limit=chunk_size_limit)

    # define LLM
    llm_predictor = LLMPredictor(llm=OpenAI(temperature=0.5, model_name="text-davinci-003", max_tokens=num_outputs))

    documents = SimpleDirectoryReader(directory_path).load_data()

    service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor, prompt_helper=prompt_helper)
    index = GPTSimpleVectorIndex.from_documents(documents, service_context=service_context)

    index.save_to_disk('index.json')

    return index

def ask_ai():
    index = GPTSimpleVectorIndex.load_from_disk('index.json')
    while True:
        query = input("What do you want to ask? ")
        response = index.query(query)
        display(Markdown(f"Response: <b>{response.response}</b>"))

"""# Set OpenAI API Key
You need an OPENAI API key to be able to run this code.

If you don't have one yet, get it by [signing up](https://platform.openai.com/overview). Then click your account icon on the top right of the screen and select "View API Keys". Create an API key.

Then run the code below and paste your API key into the text input.
"""

os.environ["OPENAI_API_KEY"] = input("Paste your OpenAI key here and hit enter:")

"""#Construct an index
Now we are ready to construct the index. This will take every file in the folder 'data', split it into chunks, and embed it with OpenAI's embeddings API.

**Notice:** running this code will cost you credits on your OpenAPI account ($0.02 for every 1,000 tokens). If you've just set up your account, the free credits that you have should be more than enough for this experiment.
"""

construct_index("insurance_data/data")

"""#Ask questions
It's time to have fun and test our AI. Run the function that queries GPT and type your question into the input.

If you've used the provided example data for your custom knowledge base, here are a few questions that you can ask:
1. What is the best pension plan in LIC?
2. How LIC help in death benefit?
3. Explain Jeevan Akshay policy and how it benefits?
4. How LIC benefits public?
5. What are the different pension policies?

"""

ask_ai()