#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
author:     Ewen Wang
email:      wolfgangwong2012@gmail.com
license:    Apache License 2.0
"""
import os
import json
import pandas as pd

from langchain import OpenAI
from langchain.agents import create_pandas_dataframe_agent

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.vectorstores import FAISS

import streamlit as st
import plotly.express as px
import plotly.io as pio


def create_conversational_chat(filename, api_key):

    os.environ['OPENAI_API_KEY'] = api_key

    loader = CSVLoader(file_path=filename, encoding="utf-8")
    data = loader.load()

    embeddings = OpenAIEmbeddings()
    vectors = FAISS.from_documents(data, embeddings)

    chain = ConversationalRetrievalChain.from_llm(llm = ChatOpenAI(temperature=0.0, model_name='gpt-3.5-turbo'),
        retriever=vectors.as_retriever())

    def conversational_chat(query):
        result = chain({"question": query, "chat_history": st.session_state['history']})
        return result

    return conversational_chat


def create_homemake_chatbot(df, api_key, prompteng_file='prompteng.txt'):

    llm = OpenAI(openai_api_key=api_key)
    agent = create_pandas_dataframe_agent(llm, df, verbose=False)

    with open(prompteng_file) as f:
        prompteng = f.read()

    def conversational_chat(query):
        prompt = (prompteng + query)
        result = agent.run(prompt)
        result = result.__str__()
        return result

    return conversational_chat

    


def present_response(response_dict, style='streamlit'):
    """
    Present the response from an agent to the front.

    Args:
        response_dict: The response from the agent.
        style (str): The presentation style, support 'streamlit' and 'notebook'.
 
    Returns:
        None.
    """    
    response = json.loads(response_dict)

    answer = response['answer']
    present = response['present']
    data = response['data']

    def make_df(data):
        df = pd.DataFrame(data)
        df['value'] = df['value'].astype(float)
        df.set_index("columns", inplace=True)
        return df

    if present is not None:
        df = make_df(data)
    
    if style=="streamlit":        
        st.write(response["answer"])

        if present=="bar":
            fig = px.bar(df)
            st.plotly_chart(fig)
    
        if present=="line":
            fig = px.line(df)
            st.plotly_chart(fig)
            
    elif style=="notebook":
        pio.renderers.default = 'iframe'
        
        print(response["answer"])
        if present=="bar":
            fig = px.bar(df)
            fig.show()
    
        if present=="line":
            fig = px.line(df)
            fig.show()
    
    else:
        print("Please choose a supported style from [streamlit] and [notebook]")

    return None