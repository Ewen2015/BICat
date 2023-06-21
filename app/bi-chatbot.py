#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
author:     Ewen Wang
email:      wolfgangwong2012@gmail.com
license:    Apache License 2.0
"""
import os
import pandas as pd
import streamlit as st
from streamlit_chat import message
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.vectorstores import FAISS
import tempfile

from agent import *

user_api_key = st.sidebar.text_input(
    label="#### Your OpenAI API key 👇",
    placeholder="Paste your openAI API key, sk-",
    type="password")

os.environ['OPENAI_API_KEY'] = user_api_key

uploaded_file = st.sidebar.file_uploader("#### Upload", type="csv")

query = st.text_area("Talk to your data: ")

if uploaded_file :


    if st.button("Send", type="primary"):

        agent = create_agent(filename=uploaded_file, api_key=user_api_key)
        
        response = query_agent(agent, query)

        present_response(response_dict=response, style="streamlit")

