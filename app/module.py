#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
author:     Ewen Wang
email:      wolfgangwong2012@gmail.com
license:    Apache License 2.0
"""

import streamlit as st

def add_back_to_top_button():
    html = """
        <style>
            #back-to-top-button {
                position: fixed;
                bottom: 20px;
                right: 20px;
                z-index: 9999;
                font-size: 15px;
                border: none;
                outline: none;
                background-color: #4CAF50;
                color: white;
                cursor: pointer;
                padding: 8px 15px;
                border-radius: 4px;
            }

            #back-to-top-button:hover {
                background-color: #45a049;
            }
        </style>
        <button onclick="backToTop()" id="back-to-top-button" title="Go to top">Back to Top</button>
        <script>
            function backToTop() {
                document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE and Opera
                document.body.scrollTop = 0; // For Safari
            }
        </script>
    """
    # Add the HTML code to the Streamlit app
    st.markdown(html, unsafe_allow_html=True)


def collapse_side_bar():
    # if st.session_state.sidebar_state == 'expanded':
    #     st.session_state.sidebar_state = 'collapsed'
    #     st.experimental_rerun()
    html = """
        <a href="javascript:document.getElementsByClassName('css-1ydp377 edgvbvh6')[1].click();">
        <img src="https://i.ibb.co/yP2wjhW/jaka-02.png" alt="Logo JAKA" style="width:50px;height:50px;"/>
        </a>
    """
    st.markdown(html, unsafe_allow_html=True)

# Example usage
def main():
    st.title("My Streamlit App")
    # ... your app content ...
    add_back_to_top_button()

if __name__ == "__main__":
    main()
