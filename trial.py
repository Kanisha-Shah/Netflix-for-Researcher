import streamlit as st
import seaborn as sns
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from collections import Counter
from num2words import num2words
import streamlit.components.v1 as stc
import search_general
import nltk
import os
import string
import numpy as np
import copy
import pandas as pd
import pickle
import re
import math
nltk.download('stopwords')
nltk.download('punkt')
st.set_option('deprecation.showPyplotGlobalUse', False)
sns.set_style("darkgrid")

st.title("Netflix for Researcher")
st.sidebar.title("OPTIONS")


m = st.markdown("""
<style>
div.stButton > button:first-child {
    background-color: #053258;
    # color:#ffffff;
    width:50%;
    padding: 4%;
    margin-left:20%;
    corn
}
div.stButton > button:hover {
    background-color: #ff0000;
    color:#000000;
}
#the-title {
  text-align: center;
}
# div.stTitle > title:first-child{
#     # font-size:10cm
#     text-align: centre;
# }
# div.stTextInput>div>div>input {
#     baackground-color: #000000;
# }
</style>""", unsafe_allow_html=True)


JOB_HTML_TEMPLATE = """
<div style="width:100%;height:100%;margin:1px;padding:5px;position:relative;border-radius:5px;border-bottom-right-radius: 10px;
box-shadow:0 0 1px 1px #eee; background-color: #31333F;
  border-left: 5px solid #6c6c6c;color:white;">
<h4>{}</h4>
<h5>{}</h5>
<h6>{}</h6>
</div>
"""

JOB_DES_HTML_TEMPLATE = """
<div style='color:#ffffff'>
{}
</div>
"""



# Side panel
button1 = st.sidebar.button("IEEE")
button2 = st.sidebar.button("Elsevier")
button4 = st.sidebar.button("Springer")
button3 = st.sidebar.button("IJSER")
button4 = st.sidebar.button("IJISRT")
button5 = st.sidebar.button("IJIRE")
button6 = st.sidebar.button("IJSRET")


# data import
search_general.import_data()
search_general.similarity()    





# body of gui

# with st.form(key='searchform'):
#     nav1,nav2,nav3,nav4 = st.columns(4)

#     with nav1:
#         search_title = st.text_input("Search Title")
#     with nav2:
#         search_author = st.text_input("Author")
#     with nav3:
#         search_date = st.date_input("Published After")#,datetime.date(2019, 7, 6))
#     with nav4:
#         st.text("Search ")
#         submit_search = st.form_submit_button(label='Search')

# st.success("You searched for {} by {} published on {}".format(search_title,search_author,search_date))


# if submit_search:
#     st.write("Pressed Submit")




# or

def output(l):
    # global l
    data=search_general.data
    # Number of Results
    num_of_results = len(l)
    st.subheader("Showing {} Research Paper".format(num_of_results))
    # st.write(data)
		

#     Unnamed: 0
# Title
# Authors
# Keyword
# Abstract
    for i in l:
        title = data.iloc[i]['Title']
        authors = data.iloc[i]['Authors']
        keyword = data.iloc[i]['Keyword']
        date = data.iloc[i]['Unnamed: 0'] #when date
        abstract = data.iloc[i]['Abstract']
        st.markdown(JOB_HTML_TEMPLATE.format(title,authors,date),
            unsafe_allow_html=True)

        # Description
        with st.expander("Abstract"):
            stc.html(JOB_DES_HTML_TEMPLATE.format(abstract),scrolling=True)

        # How to Apply
        # with st.beta_expander("How To Apply"):
            # stc.html(job_howtoapply) # For White Theme
            # stc.html(JOB_DES_HTML_TEMPLATE.format(job_howtoapply),scrolling=True) 


with st.form(key='searchform2'):
    option=["Select one","Artificial Intelligence","Big Data","Computer Vision","Neural Networks"]
    search_field = st.selectbox("Select one",option)

    search_input = st.text_input("Search")
    date = st.date_input("Published After")#,datetime.date(2019, 7, 6))

    search_abstract = st.form_submit_button(label='Search in Abstract')    
    search_title = st.form_submit_button(label='Search by Title')
    search_author = st.form_submit_button(label='Search by Author')
    search_date = st.form_submit_button(label='Search by Date')

# st.success("You searched for {} by {} published after {}".format(search_title,search_author,search_date))

if search_abstract:
    # global l
    st.success("You searched for {} in Abstract".format(search_input))

    l = search_general.matching_score(3, search_input)
    # st.write(l)
    # st.write(search_input)
    if len(l)==0:
        st.write("Oops!! No match found ....") # pop up
    else:
        output(l)
        # st.write(search_general.data.iloc[l])

elif search_author:
    st.success("You searched for Author: {} ".format(search_input))

    l=search_general.data[search_general.data["Authors"].str.contains(search_input.strip(),flags=re.IGNORECASE)==True].index.values

    if len(l)==0:
        st.write("Oops!! No match found ....") # pop up
    else:
        output(l)
        # st.write(search_general.data.iloc[l])

elif search_title:
    st.success("You searched for {} in Title ".format(search_input))

    l=search_general.data[search_general.data["Title"].str.contains(search_input.strip(),flags=re.IGNORECASE)==True].index.values
    if len(l)==0:
        st.write("Oops!! No match found ....") # pop up
    else:
        output(l)
elif search_date:
    pass
