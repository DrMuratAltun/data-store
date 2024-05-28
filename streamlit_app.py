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

# Streamlit sayfa ayarları
st.set_page_config(page_title="Dashboard", page_icon="🌍", layout="wide")
st.header("Etsy Turkish Daily Sales Dashboard")

# Excel dosyasını yükleme

df = pd.read_excel("data_store.xlsx")

# CSS stili yükleme
with open('style.css') as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Sidebar'a logo ekleme
st.sidebar.image("logo2.png")

# Tarih aralığı seçimi
with st.sidebar:
    st.title("Select Date Range")
    start_date = st.date_input(label="Start Date")
    end_date = st.date_input(label="End Date")
    
st.error("Store Sales between [" + str(start_date) + "] and [" + str(end_date) + "]")

# Seçilen tarih aralığında verileri filtreleme
df_filtered = df[(df['date'] >= pd.to_datetime(start_date)) & (df['date'] <= pd.to_datetime(end_date))]

# Sidebar'da mağazaları seçmek için multiselect widget'ı
with st.sidebar:
    st.header("Store Filter")
    selected_stores = st.multiselect(
        "Select Stores",
        options=df_filtered.columns.drop('date').tolist(),
        default=df_filtered.columns.drop('date').tolist()
    )

# Seçilen mağazalara göre DataFrame'i filtreleme
df_selection = df_filtered[selected_stores]

# Her mağazanın toplam satışlarını hesaplama
total_sales = df_selection.sum().reset_index()
total_sales.columns = ['store', 'total_sales']

# Bar grafiği oluşturma
fig = px.bar(total_sales, x='store', y='total_sales', title='Total Sales by Store')

# Grafiği Streamlit ile gösterme
st.plotly_chart(fig)

# Filtrelenmiş DataFrame'i gösterme
st.write("Filtered DataFrame:", df_selection)
