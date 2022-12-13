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

# Perform query.
# Uses st.experimental_memo to only rerun when the query changes or after 10 min.
@st.experimental_memo(ttl=600)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()

rows = run_query("SELECT * from AUTHOR_INGEST_PARQUET;")
q1_df = pd.DataFrame(rows)
#q1_df = pd.DataFrame(rows.items(), columns =['SHOW_ID', 'TYPE', 'TITLE', 'DIRECTOR', 'CAST', 'COUNTRY', 'DATE_ADDED', 'RELEASE_YEAR', 'RATING', 'DURATION', 'LISTED_IN', 'DESCRIPTION'])
#st.table(q1_df)
st.dataframe(q1_df)
# Print results.
#for row in rows:
# st.write(f"{row[0]} has a :{row[1]}:")
