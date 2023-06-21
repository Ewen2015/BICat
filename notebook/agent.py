#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
author:     Ewen Wang
email:      wolfgangwong2012@gmail.com
license:    Apache License 2.0
"""
import json
from langchain import OpenAI
from langchain.agents import create_pandas_dataframe_agent
import pandas as pd

import streamlit as st
import plotly.express as px
import plotly.io as pio

def create_agent(filename, api_key):
    """
    Create an agent that can access and use a large language model (LLM).

    Args:
        filename (str): The path to the CSV file that contains the data.
        api_key (str): The OpenAI API key.
        
    Returns:
        An agent that can access and use the LLM.
    """
    llm = OpenAI(openai_api_key=api_key)
    df = pd.read_csv(filename)
    return create_pandas_dataframe_agent(llm, df, verbose=False)


def query_agent(agent, query, prompteng_file='prompteng.txt'):
    """
    Query an agent and return the response as a string.

    Args:
        agent: The agent to query.
        query (str): The query to ask the agent.
        prompteng_file (str): The prompt engineering filename, default 'prompteng.txt'.

    Returns:
        The response from the agent as a string.
    """
    with open(prompteng_file) as f:
        prompteng = f.read()
        
    prompt = (prompteng + query)
    response = agent.run(prompt)

    return response.__str__()


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