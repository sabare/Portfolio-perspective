import streamlit as st
from datetime import date
import yfinance as yf
from prophet import Prophet
import plotly.graph_objs as go
from prophet.plot import plot_plotly
import pandas as pd
import numpy as np
import tensorflow as tf
# from tensorflow import keras


df = pd.read_csv('dataset.csv')
stocks=df['Symbol'].values
START = "2010-01-01"
TODAY = date.today().strftime("%Y-%m-%d")

st.title('Stock Forecast App')
selected_stock = st.selectbox('Select dataset for prediction', stocks)

n_years = st.slider('Years of prediction:', 1, 6)
period = n_years * 365


@st.cache_data
def load_data(ticker):
    data = yf.download(ticker, START, TODAY)
    data.reset_index(inplace=True)
    return data


data_load_state = st.text('Loading data...')
data = load_data(selected_stock)
data_load_state.text('Loading data... done!')
data.shape
st.subheader('Raw data')
st.write(data.tail())

# Plot raw data
def plot_raw_data():
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name="stock_open"))
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name="stock_close"))
    fig.layout.update(title_text='Time Series data with Rangeslider', xaxis_rangeslider_visible=True)
    st.plotly_chart(fig)

plot_raw_data()

# Predict forecast with Prophet.
df_train = data[['Date','Close']]
df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})

m = Prophet()
m.fit(df_train)
future = m.make_future_dataframe(periods=period)
forecast = m.predict(future)

# Show and plot forecast
st.subheader('Forecast data')
st.write(forecast.tail())

st.write(f'Forecast plot for {n_years} years')
fig1 = plot_plotly(m, forecast)
st.plotly_chart(fig1)

st.write("Forecast components")
fig2 = m.plot_components(forecast)
st.write(fig2)

st.subheader("Run the app.py 1st to able to run this code through this")
import webbrowser
# Define the URL of your Flask application
flask_app_url = "http://localhost:5000"
# Create a button that will open the Flask application when clicked
if st.button("Open Portfolio and Stock Price analysis"):
    webbrowser.open_new_tab(flask_app_url)
