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

query = """
    SELECT 
        *
    FROM AUTHOR_INGEST_PARQUET;
    """

# Perform query.
# Creating a function to load the data into a pandas data frame
def load_data():
    cur = conn.cursor().execute(query)
    table1_df = pd.DataFrame.from_records(iter(cur), 
                  columns=[x[0] for x in cur.description])
    return payments_df


#q1_df = pd.DataFrame(rows.items(), columns =['SHOW_ID', 'TYPE', 'TITLE', 'DIRECTOR', 'CAST', 'COUNTRY', 'DATE_ADDED', 'RELEASE_YEAR', 'RATING', 'DURATION', 'LISTED_IN', 'DESCRIPTION'])
#st.table(q1_df)
#st.dataframe(q1_df)
# Print results.
#for row in rows:
# st.write(f"{row[0]} has a :{row[1]}:")
