import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
from numerize.numerize import numerize
import time
from streamlit_extras.metric_cards import style_metric_cards
st.set_option('deprecation.showPyplotGlobalUse', False)
import plotly.graph_objs as go
from streamlit_extras.dataframe_explorer import dataframe_explorer

st.set_page_config(page_title="Dashboard",page_icon="🌍",layout="wide")
st.header("Etsy Turkish Daily Sales Dashboard")
df=pd.read_excel("data_store.xlsx")
# 'date' sütununu düşürmek için
df3 = df.drop(columns=['date'])


#streamlit theme=none
theme_plotly = None 

# load CSS Style
with open('style.css')as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)


st.sidebar.image("logo2.png")
#filter date to view data
with st.sidebar:
 st.title("Select Date Range")
 start_date=st.date_input(label="Start Date")

with st.sidebar:
 end_date=st.date_input(label="End Date")
st.error("Business Metrics between[ "+str(start_date)+"] and ["+str(end_date)+"]")

#compare date
df2 = df[(df['date'] >= str(start_date)) & (df['date'] <= str(end_date))]
st.dataframe(df2)

# Sidebar'da kolonları seçmek için multiselect widget'ı
with st.sidebar:
    st.header("Store Filter")
    selected_columns = st.multiselect(
        "Filter Department",
        options=df3.columns.tolist(),
        default=df3.columns.tolist()
    )

# Seçilen kolonlara göre DataFrame'i filtreleme
df_selection = df3[selected_columns]

# Filtrelenmiş DataFrame'i gösterme
st.write("Filtered DataFrame:", df_selection)
