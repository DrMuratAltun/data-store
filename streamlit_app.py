import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from streamlit_option_menu import option_menu
from numerize.numerize import numerize
import time
from streamlit_extras.metric_cards import style_metric_cards
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
df_selection = df_filtered[['date'] + selected_stores]

# Her mağazanın toplam satışlarını hesaplama
total_sales = df_selection[selected_stores].sum().reset_index()
total_sales.columns = ['store', 'total_sales']

# Bar grafiği oluşturma
fig_bar = px.bar(total_sales, x='store', y='total_sales', title='Total Sales by Store')
fig_bar.update_traces(text=total_sales['total_sales'], textposition='outside')

# Y eksenini ayarlama (görünürlüğü artırmak için)
fig_bar.update_layout(
    yaxis=dict(
        range=[0, total_sales['total_sales'].max() * 1.1]  # 10% padding
    )
)

# Grafiği Streamlit ile gösterme
st.plotly_chart(fig_bar)

# Seçilen mağazaların günlük satışlarını toplama
daily_sales = df_selection.groupby('date')[selected_stores].sum().reset_index()

# Çizgi grafiği oluşturma
fig_line = go.Figure()

for store in selected_stores:
    fig_line.add_trace(go.Scatter(x=daily_sales['date'], y=daily_sales[store], mode='lines', name=store))

fig_line.update_layout(title='Daily Sales by Store', xaxis_title='Date', yaxis_title='Sales')

# Grafiği Streamlit ile gösterme
st.plotly_chart(fig_line)

# Her mağazanın toplam satışlarını içeren pastayı oluşturma
fig_pie = px.pie(total_sales, values='total_sales', names='store', title='Total Sales Distribution by Store')

# Grafiği Streamlit ile gösterme
st.plotly_chart(fig_pie)


# Filtrelenmiş DataFrame'i gösterme
st.write("Filtered DataFrame:", df_selection)
