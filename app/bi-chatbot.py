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
import tempfile

import pandas_profiling
from streamlit_pandas_profiling import st_profile_report
import seaborn as sns

from pandasai.llm.openai import OpenAI
from pandasai import PandasAI

import agent
import module

cm = sns.light_palette("green", as_cmap=True)

st.set_page_config(
     page_title="BI ChatBot",
     page_icon="🐣",
     layout="wide",
     initial_sidebar_state=st.session_state.get('sidebar_state', 'expanded')
     )
st.session_state.sidebar_state = 'expanded'

st.sidebar.header("🌮 Let's set it up!")

uploaded_file = st.sidebar.file_uploader("#### Upload 🖖🏼", type=["csv"])

user_api_key = st.sidebar.text_input(
    label="#### Your OpenAI API key 👇🏼",
    placeholder="Paste your openAI API key, sk-",
    type="password")


st.header("🥝 Let's make BI easier and smarter!")

with st.expander("About this app"):
    st.write("**AI (Large Language Model)-powered BI**. \
    This innovative technology is designed to revolutionize the way businesses analyze \
    and interpret data by leveraging the power of advanced artificial intelligence algorithms \
    to generate insights and predictions in real-time. With Large Language Model-powered BI, \
    businesses can make faster, more informed decisions that drive growth and profitability.")

col1, col2 = st.columns(spec=[5, 3], gap='large')


with col1:

    st.subheader("🍕 Data preview:")

    if uploaded_file :
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_file_path = tmp_file.name

        df = pd.read_csv(uploaded_file)

        col11, col12, col13 = st.columns(spec=3, gap='medium')
       
        with col11: 
            index_col = st.selectbox("Select the index column", df.columns)
        with col12: 
            heighlight = st.selectbox("Hightlight on", [False, "rows", "column", "both"])
        with col13: 
            precision = st.selectbox("Precision to", [0, 1, 2, 4])

        if index_col:
            df.set_index(index_col, inplace=True)

        if heighlight in ["rows", "column"]:
            styled_df = df.style.format(precision=precision).highlight_max(axis=1 if heighlight == "rows" else 0, 
                        props='color:white; font-weight:bold; background-color:purple;')
            st.dataframe(styled_df)
        elif heighlight == "both":
            styled_df = df.style.format(precision=precision).background_gradient(cmap=cm)
            st.dataframe(styled_df)
        else:
            st.dataframe(df)

        if st.button('🙌🏼 Please show me data profile.'):
            pr = df.profile_report()
            st_profile_report(pr)

            # module.collapse_side_bar()
            # module.add_back_to_top_button()


with col2: 

    st.subheader("🍪 Talk to your data!")

    message("Hi there! 👋 Set up your API KEY before talk!", avatar_style="big-smile")

    if uploaded_file:

        if user_api_key:


            # conversational_chat = agent.create_conversational_chat(filename=tmp_file_path, api_key=user_api_key)
            # conversational_chat = agent.create_homemake_chatbot(df=df, api_key=user_api_key)
            conversational_chat = agent.create_pandasai_chat(df=df, api_key=user_api_key)

            
            if 'history' not in st.session_state:
                st.session_state['history'] = []

            if 'generated' not in st.session_state:
                st.session_state['generated'] = ["Hello! Ask me anything about " + uploaded_file.name + " 🤗"]

            if 'past' not in st.session_state:
                st.session_state['past'] = ["Hey! 👋"]
                
            #container for the chat history
            response_container = st.container()
            #container for the user's text input
            container = st.container()

            with container:
                with st.form(key='my_form', clear_on_submit=True):
                    
                    user_input = st.text_input("Question:", placeholder="Talk about your data here : )", key='input')
                    submit_button = st.form_submit_button(label='Send')
                    
                if submit_button and user_input:
                    output = conversational_chat(user_input)
                    
                    st.session_state['history'].append((user_input, output))
                    st.session_state['past'].append(user_input)
                    st.session_state['generated'].append(output)

            if st.session_state['generated']:
                with response_container:
                    for i in range(len(st.session_state['generated'])):
                        message(st.session_state["past"][i], is_user=True, key=str(i) + '_user', avatar_style="big-smile", seed="openedSmile")
                        message(st.session_state["generated"][i], key=str(i), avatar_style="big-smile")







