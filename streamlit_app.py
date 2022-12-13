import streamlit as st
st.title('My First Visuals App!')
#Adding the csv data from the S3 bucket to be displayed as a dataframe in streamlit library.
import pandas as pd
#import matplotlib as plt
import numpy as np
import snowflake.connector

# Initialize connection.
# Uses st.experimental_singleton to only run once.
@st.experimental_singleton
def init_connection():
    return snowflake.connector.connect(
        **st.secrets["snowflake"], client_session_keep_alive=True
    )

conn = init_connection()

# Perform query.
# Uses st.experimental_memo to only rerun when the query changes or after 10 min.
@st.experimental_memo(ttl=600)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()

rows = run_query("SELECT * from AUTHOR_INGEST_PARQUET;")

# Print results.
df = pd.DataFrame(rows, columns = ['SHOW_ID', 'TYPE', 'TITLE', 'DIRECTOR', 'CAST', 'COUNTRY', 'DATE_ADDED', 'RELEASE_YEAR', 'RATING', 'DURATION', 'LISTED_IN', 'DESCRIPTION'])
table1_df = df.dropna() 
table1_df['DATE_ADDED'] = pd.to_datetime(table1_df['DATE_ADDED'])

st.dataframe(table1_df)

# This function returns the earliest date present in the dataset
def get_min_date():
    return min(table1_df.DATE_ADDED())

# This function returns the latest date present in the dataset
def get_max_date():
    return max(table1_df.DATE_ADDED())
                      
##################################
st.bar_chart(table1_df, x = 'DATE_ADDED', y='TYPE')
