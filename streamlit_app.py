import streamlit as st
st.title('My First Visuals App!')
#Adding the csv data from the S3 bucket to be displayed as a dataframe in streamlit library.
import pandas as pd
import snowflake.connector

# Initialize connection.
# Uses st.experimental_singleton to only run once.
@st.experimental_singleton
def init_connection():
    return snowflake.connector.connect(
        **st.secrets["snowflake"], client_session_keep_alive=True
    )

conn = init_connection()

# Uses st.experimental_memo to only rerun when the query changes or after 10 min.
@st.experimental_memo(ttl=600)

# SQL query

