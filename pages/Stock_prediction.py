import streamlit as st
from pages.utils.model_train import *
import pandas as pd
from pages.utils.plotly_figure import *

# st.set_page_config(page_title= "Stock Prediction",
#                    page_icon="page_with_curl",
#                    layout='wide') 

# st.title("Stock Prediction")

# col1,col2,col3=st.columns(3)

# with col1:
#     ticker=st.text_input('Stock Ticker','AAPL')
# rmse=0

# st.subheader('Predicting Next 30 days Close price for:'+ticker)

# close_price=get_data(ticker)
# rolling_price=get_rolling_mean(close_price)

# differencing_order=get_differencing_order(rolling_price)
# scaled_data,scaler=scaling(rolling_price)
# rmse=evaluate_model(scaled_data,differencing_order)
 

# st.write("**Model RMSE Score: **",rmse)

# forecast=get_forecast(scaled_data,differencing_order)

# forecast['Close']=inverse_scaling(scaler,forecast['Close'])
# st.write('##### Forecast Data (Next 30 days)')
# fig_tail= plotly_table(forecast.sort_index(ascending=True).round(3))
# fig_tail.update_layout(height=220)
# st.plotly_chart(fig_tail,use_container_width=True)

# forecast= pd.concat([rolling_price,forecast]).sort_index()

# print(forecast.index[-50:])  # Print the last 50 timestamps
# print(forecast.index[:50])   # Print the first 50 timestamps

# st.plotly_chart(Moving_average_forecast(forecast.iloc[150:]),use_container_width=True)



import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller
from sklearn.metrics import mean_squared_error
from datetime import timedelta,datetime
from sklearn.preprocessing import MinMaxScaler


# Set Streamlit page configuration
st.set_page_config(page_title="Stock Prediction", page_icon="📈", layout='wide')

# Title of the app
st.title("Stock Prediction")

# Create columns for user inputs
col1, col2, col3 = st.columns(3)
#today=datetime.date.today()
#two_months_ago = datetime.today() - timedelta(days=60)  # Approx. 2 months
two_months_ago = datetime.now() - timedelta(days=60)  # Approx. 2 months

# User input: Stock ticker
with col1:
    ticker = st.text_input('Stock Ticker', 'AAPL')
with col2:
    start_date = st.date_input('Start Date', two_months_ago)
    #start_date=st.date_input("Choose start date", datetime.date(today.year-1,today.month,today.day))


end_date = datetime.today().strftime('%Y-%m-%d')
st.write(f"Data will be fetched from {start_date} to {end_date}")

# Display the predicted stock prices
if ticker:
    st.subheader(f'Predicting Next 30 Days Close Price for: {ticker}')
    
    # Fetch the stock data
    stock_data = fetch_stock_data(ticker, start_date, end_date)
    if len(stock_data) < 30:
        st.error("Not enough data to make predictions. Please choose a start date with more data.")
    else:
        # Get the differencing order (d)
        rolling_price = get_rolling_mean(stock_data['Close'])

        differencing_order = get_differencing_order(rolling_price)
        scaled_data, scaler = scaling(rolling_price)

        # Get predictions
        forecast = fit_model(scaled_data, differencing_order)
        forecast = inverse_scaling(scaler, forecast)

        # Convert forecast to DataFrame
        future_dates = pd.date_range(stock_data.index[-1], periods=31, freq='B')[1:]
        forecast_df = pd.DataFrame({'Date': future_dates, 'Predicted Close Price': forecast.flatten()})
        forecast_df.set_index('Date', inplace=True)

        # Display the forecast data in a table
        fig_tail = plotly_table(forecast_df)
        fig_tail.update_layout(height=220)
        st.plotly_chart(fig_tail, use_container_width=True)

        # Plotting the historical data and predictions
        plt.figure(figsize=(10, 6))
        plt.plot(stock_data.index, stock_data['Close'], label='Historical Data', color='blue')
        plt.plot(future_dates, forecast.flatten(), label='Predicted Close Price', color='red', linestyle='dashed')
        plt.title(f'{ticker} Stock Price Prediction (Next 30 Days)')
        plt.xlabel('Date')
        plt.ylabel('Close Price')
        plt.legend()
        st.pyplot(plt)









        # # RMSE Calculation
        # actual = stock_data['Close'][-30:].values  # The last 30 actual values for RMSE
        # rmse = np.sqrt(mean_squared_error(actual, forecast))
        
        # # Display RMSE
        # st.write(f'Root Mean Squared Error (RMSE): {rmse:.2f}')
        
        # # Plotting the historical data and predictions
        # plt.figure(figsize=(10, 6))
        # plt.plot(stock_data.index, stock_data['Close'], label='Historical Data', color='blue')
        # future_dates = pd.date_range(stock_data.index[-1], periods=31, freq='B')[1:]
        # plt.plot(future_dates, forecast, label='Predicted Close Price', color='red', linestyle='dashed')
        # plt.title(f'{ticker} Stock Price Prediction (Next 30 Days)')
        # plt.xlabel('Date')
        # plt.ylabel('Close Price')
        # plt.legend()
        # st.pyplot(plt)

        # forecast_df = pd.DataFrame({'Date': future_dates, 'Predicted Close Price': forecast})

        # forecast_df.set_index('Date', inplace=True)


        # fig = plotly_table(forecast_df)
        # st.plotly_chart(fig)
