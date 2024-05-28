import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from streamlit_option_menu import option_menu
from numerize.numerize import numerize
import time
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_extras.dataframe_explorer import dataframe_explorer

# Streamlit page settings
st.set_page_config(page_title="Dashboard", page_icon="🌍", layout="wide")
st.header("Etsy Turkish Lamp Category Daily Sales Dashboard")

# load file 
df = pd.read_excel("data_store.xlsx")

# CSS style load
with open('style.css') as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Sidebar'a logo add
st.sidebar.image("logo2.png")

# Date range selection
with st.sidebar:
    st.title("Select Date Range")
    start_date = st.date_input(label="Start Date")
    end_date = st.date_input(label="End Date")
    
st.error("Store Sales between [" + str(start_date) + "] and [" + str(end_date) + "]")

# Date range selection
df_filtered = df[(df['date'] >= pd.to_datetime(start_date)) & (df['date'] <= pd.to_datetime(end_date))]

# Multiselect widget to select stores in sidebar
with st.sidebar:
    st.header("Store Filter")
    selected_stores = st.multiselect(
        "Select Stores",
        options=df_filtered.columns.drop('date').tolist(),
        default=df_filtered.columns.drop('date').tolist()
    )

# Filter DataFrame based on selected stores
df_selection = df_filtered[['date'] + selected_stores]

# Calculate total sales of each store
total_sales = df_selection[selected_stores].sum().reset_index()
total_sales.columns = ['store', 'total_sales']

# Creating bar chart
fig_bar = px.bar(total_sales, x='store', y='total_sales', title='Total Sales by Store')
fig_bar.update_traces(text=total_sales['total_sales'], textposition='outside')

fig_bar.update_layout(
    yaxis=dict(
        range=[0, total_sales['total_sales'].max() * 1.1]  # 10% padding
    )
)

st.plotly_chart(fig_bar)

# Collecting daily sales of selected stores
daily_sales = df_selection.groupby('date')[selected_stores].sum().reset_index()

# Creating a line chart
fig_line = go.Figure()

for store in selected_stores:
    fig_line.add_trace(go.Scatter(x=daily_sales['date'], y=daily_sales[store], mode='lines', name=store))

fig_line.update_layout(title='Daily Sales by Store', xaxis_title='Date', yaxis_title='Sales')

st.plotly_chart(fig_line)

#Creating a pie chart
fig_pie = px.pie(total_sales, values='total_sales', names='store', title='Total Sales Distribution by Store')


st.plotly_chart(fig_pie)


# Filtrelenmiş DataFrame'i gösterme
st.write("Filtered DataFrame:", df_selection)
