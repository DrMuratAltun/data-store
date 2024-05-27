import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
from numerize.numerize import numerize
import time
from streamlit_extras.metric_cards import style_metric_cards
st.set_option('deprecation.showPyplotGlobalUse', False)
import plotly.graph_objs as go

st.set_page_config(page_title="Dashboard",page_icon="🌍",layout="wide")
st.header("Etsy Turkish Daily Sales Dashboard")
df=pd.read_excel("data_store.xlsx")
st.dataframe(df,use_container_width=True)
#streamlit theme=none
theme_plotly = None 

# load CSS Style
with open('style.css')as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)

UI()
#load dataset
df=pd.read_csv('data.csv')

st.sidebar.image("images/logo2.png")
#filter date to view data
with st.sidebar:
 st.title("Select Date Range")
 start_date=st.date_input(label="Start Date")

with st.sidebar:
 end_date=st.date_input(label="End Date")
st.error("Business Metrics between[ "+str(start_date)+"] and ["+str(end_date)+"]")

#compare date
df2 = df[(df['Date'] >= str(start_date)) & (df['Date'] <= str(end_date))]
