import pandas as pd
import streamlit as st
import psycopg2
import os

os.environ["HADOOP_USER_NAME"] = "aaryapaudel"
st.title("ETL Dashboard")

try:
    conn = psycopg2.connect(
        host="localhost", port=5432, dbname="real_estate_db",
        user="etl_user", password="etl_password"
    )
    df = pd.read_sql("SELECT * FROM public.sales", conn)
    conn.close()

    st.metric("Rows in sales table", len(df))
    st.dataframe(df.head())
    st.bar_chart(df[['quantity', 'unit_price']])
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.info("Make sure to run the ETL pipeline first.")

