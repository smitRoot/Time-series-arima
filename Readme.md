# Time Series Analysis Using ARIMA

## Project Overview
This project involves analyzing time series data using the ARIMA (AutoRegressive Integrated Moving Average) model. The objective is to explore, visualize, and forecast time-dependent data trends with high accuracy.

## Features
- Data preprocessing and handling missing values
- Exploratory Data Analysis (EDA) with visualizations
- Stationarity check using ADF Test
- Building and training the ARIMA model
- Model evaluation using metrics like RMSE and MAPE
- Forecasting future values with confidence intervals

## Technologies Used
- Python 3.8
- Pandas
- NumPy
- Matplotlib & Seaborn
- Statsmodels
- Scikit-learn
- yFinance

## Dataset
The dataset used in this project contains time-stamped stock market data fetched using the `yfinance` library. The dataset is preprocessed to remove missing values and ensure stationarity before modeling.

## Installation
To run this project, install the necessary dependencies:
```bash
pip install -r Requirements.txt
```

## Usage
1. Load the dataset using `yfinance`:
   ```python
   import yfinance as yf
   import pandas as pd
   
   stock = yf.download('AAPL', start='2020-01-01', end='2024-01-01')
   df = stock[['Close']]
   df.rename(columns={'Close': 'value_column'}, inplace=True)
   ```
2. Perform Exploratory Data Analysis (EDA) and check for stationarity.
3. Use the Augmented Dickey-Fuller test to confirm stationarity:
   ```python
   from statsmodels.tsa.stattools import adfuller
   result = adfuller(df['value_column'])
   print('ADF Statistic:', result[0])
   print('p-value:', result[1])
   ```

4. Train the ARIMA model:
   ```python
   from statsmodels.tsa.arima.model import ARIMA
   model = ARIMA(df['value_column'], order=(p, d, q))
   model_fit = model.fit()
   print(model_fit.summary())
   ```
5. Forecast future values and visualize results.

## Results
- The ARIMA model successfully captured the time series trends.


## Future Improvements
- Implement seasonal ARIMA (SARIMA) for seasonal data
- Compare ARIMA with other models like LSTM and Prophet


## Author
Smitkumar Patel

