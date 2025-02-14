import dateutil.relativedelta
import plotly.graph_objects as go
import dateutil
import pandas_ta as pta
import datetime

# Function to plot forecast in table format
# def plotly_table(df):
#     fig = go.Figure(data=[go.Table(
#         header=dict(values=["Date", "Predicted Close Price"]),
#         cells=dict(values=[df.index, df['Predicted Close Price']]))
#     ])
#     return fig


def plotly_table(dataframe):
    headerColor='grey'
    rowEvenColor='#f8fafd'
    rowOddColor='#e1efff'

    fig=go.Figure(data=[go.Table(
        header=dict(
            values=["<b><b>"]+["<b>"+str(i)[:10]+"<b>" for i in dataframe.columns],
            line_color='#0078ff',
            fill_color='#0078ff',
            align='center',
            font=dict(color='white',size=15),
            height=35,
        ),
        cells=dict(
            values=[["<b>"+str(i)+"<b>" for i in dataframe.index]]+[dataframe[i] for i in dataframe.columns],
            fill_color=[[rowOddColor,rowEvenColor]* (len(dataframe) // 2 + 1)],
            align='left', 
            line_color=['white'],
            font=dict(color=["black"],size=15)
))
])
    fig.update_layout(height=400,margin=dict(l=0,r=0,t=0,b=0))
    return fig

def filter_data(dataframe, num_period):
    if num_period=='1mo':
        date=dataframe.index[-1]+dateutil.relativedelta.relativedelta(months=-1)
    elif num_period=='5d':
        date=dataframe.index[-1]+dateutil.relativedelta.relativedelta(days=-5)
    elif num_period=='6mo':
        date=dataframe.index[-1]+dateutil.relativedelta.relativedelta(months=-6)
    elif num_period=='1y':
        date=dataframe.index[-1]+dateutil.relativedelta.relativedelta(years=-1)
    elif num_period=='5y':
        date=dataframe.index[-1]+dateutil.relativedelta.relativedelta(years=-5)
    elif num_period=='ytd':
        date=datetime.datetime(dataframe.index[-1].year,1,1).strftime('%Y-%m-%d')
    else:
        date=dataframe.index[0]
    return dataframe.reset_index()[dataframe.reset_index()['Date']>date]


def close_chart(dataframe, num_period=False):
    if num_period:
        dataframe=filter_data(dataframe,num_period)
    fig=go.Figure()
    fig.add_trace(go.Scatter(x=dataframe['Date'],y=dataframe['Open'],
                             mode='lines',
                             name='Open',line=dict(width=2,color='#5ab7ff')))
    fig.add_trace(go.Scatter(x=dataframe['Date'],y=dataframe['Close'],
                             mode='lines',
                             name='Close',line=dict(width=2,color='black')))
    fig.add_trace(go.Scatter(x=dataframe['Date'],y=dataframe['High'],
                             mode='lines',
                             name='High',line=dict(width=2,color='#0078ff')))
    fig.add_trace(go.Scatter(x=dataframe['Date'],y=dataframe['Low'],
                             mode='lines',
                             name='Low',line=dict(width=2,color='red')))
    
    fig.update_xaxes(rangeslider_visible=True)
    fig.update_layout(height=500,margin=dict(l=0,r=20,t=20,b=0),plot_bgcolor='white', paper_bgcolor='#E1EFFF',legend=dict(yanchor="top",xanchor="right"))
    return fig  

def candlesticks(dataframe,num_period):
    dataframe=filter_data(dataframe,num_period)
    fig=go.Figure()
    fig.add_trace(go.Candlestick(x=dataframe['Date'],
                                 open=dataframe['Open'],high=dataframe['High'],
                                 low=dataframe['Low'],close=dataframe['Close']))
    fig.update_layout(showlegend=False,height=500,margin=dict(l=0,r=20,t=20,b=0),plot_bgcolor='white',paper_bgcolor='#E1EFFF')
    return fig

def RSI(dataframe,num_period):
    dataframe['RSI']=pta.rsi(dataframe['Close'])
    dataframe=filter_data(dataframe,num_period)
    fig=go.Figure()
    fig.add_trace(go.Scatter(
        x=dataframe['Date'],
        y=dataframe.RSI,name='RSI',marker_color='orange',line=dict(width=2,color='orange'),
    ))
    fig.add_trace(go.Scatter(
        x=dataframe['Date'],
        y=[70]*len(dataframe),name='Overbought',line=dict(width=2,color='red',dash='dash')
    ))
    fig.add_trace(go.Scatter(
        x=dataframe['Date'],
        y=[30]*len(dataframe),fill='tonexty',name='Oversold',line=dict(width=2,color='#79da84',dash='dash')
    ))
    fig.update_layout(yaxis_range=[0,100],height=200,plot_bgcolor='white',paper_bgcolor='#E1EFFF',margin=dict(l=0,r=0,t=0,b=0),legend=dict(orientation="h",yanchor="top",y=1.02,xanchor="right",x=1))

    return fig

def Moving_average(dataframe,num_period):
    dataframe['sma_50']=pta.sma(dataframe['Close'],50)
    dataframe= filter_data(dataframe,num_period)
    fig=go.Figure()

    fig.add_trace(go.Scatter(x=dataframe['Date'],y=dataframe['Open'],
                             mode='lines',
                             name='Open',line=dict(width=2,color='#5ab7ff')))
    fig.add_trace(go.Scatter(x=dataframe['Date'],y=dataframe['Close'],
                             mode='lines',
                             name='Close',line=dict(width=2,color='black')))
    fig.add_trace(go.Scatter(x=dataframe['Date'],y=dataframe['High'],
                             mode='lines',
                             name='High',line=dict(width=2,color='#0078ff')))
    fig.add_trace(go.Scatter(x=dataframe['Date'],y=dataframe['Low'],
                             mode='lines',
                             name='Low',line=dict(width=2,color='red')))
    fig.add_trace(go.Scatter(x=dataframe['Date'],y=dataframe['sma_50'],
                             mode='lines',
                             name='sma 50',line=dict(width=2,color='purple')))
    
    fig.update_xaxes(rangeslider_visible=True)
    fig.update_layout(height=500,margin=dict(l=0,r=20,t=20,b=0),plot_bgcolor='white',paper_bgcolor='#E1EFFF',legend=dict(yanchor="top",xanchor="right"))
    return fig  


def MACD(dataframe,num_period):
    macd=pta.macd(dataframe['Close']).iloc[:,0]
    macd_signal=pta.macd(dataframe['Close']).iloc[:,1]
    macd_hist=pta.macd(dataframe['Close']).iloc[:,2]
    dataframe['MACD']=macd
    dataframe['MACD signal']=macd_signal
    dataframe['MACD Hist']=macd_hist
    dataframe=filter_data(dataframe,num_period)
    fig=go.Figure()
    fig.add_trace(go.Scatter(
        x=dataframe['Date'],
        y=dataframe['MACD'],name='RSI',marker_color='orange',line=dict(width=2,color='orange'),
    ))
    fig.add_trace(go.Scatter(
        x=dataframe['Date'],
        y=dataframe['MACD signal'],name='Overbought',marker_color='red',line=dict(width=2,color='red',dash='dash'),
    ))

    c=['red'  if cl<0 else "green" for cl in macd_hist]    
    fig.update_layout(height=200,plot_bgcolor='white',paper_bgcolor='#E1EFFF',
                      margin=dict(l=0,r=0,t=0,b=0),legend=dict(orientation="h",
                    yanchor="top",
                    y=1.02,
                    xanchor="right",
                    x=1) )
    return fig
  

# def Moving_average_forecast(forecast):
#     fig=go.Figure()
#     split_index = len(forecast) - 30

#     fig.add_trace(go.Scatter(x=forecast.index[:split_index],y=forecast['Close'].iloc[:split_index],
#                              mode='lines',
#                              name='Close Price', line=dict(width=2,color='black')))
    
#     fig.add_trace(go.Scatter(x=forecast.index[split_index:],y=forecast['Close'].iloc[split_index:],
#                              mode='lines',
#                              name='Future close Price ', line=dict(width=2,color='red')))
#     fig.update_xaxes(rangeslider_visible=True)
#     fig.update_layout(height=500,margin=dict(l=0,r=20,t=20,b=0),plot_bgcolor='white', paper_bgcolor='#e1efff',legend=dict(yanchor="top",xanchor="right"))

#     return fig

import pandas as pd

def Moving_average_forecast(forecast):
    fig = go.Figure()

    # Ensure index is a datetime object
    forecast = forecast.copy()
    forecast.index = pd.to_datetime(forecast.index)

    # Get the most recent date in the dataset
    last_historical_date = forecast.index[-30]  # Use the 30th last available date

    # Split historical and future data
    past_data = forecast[forecast.index <= last_historical_date]
    future_data = forecast[forecast.index > last_historical_date]

    # Plot historical close prices
    fig.add_trace(go.Scatter(
        x=past_data.index, 
        y=past_data['Close'],
        mode='lines',
        name='Close Price',
        line=dict(width=2, color='black')
    ))

    # Plot future predicted close prices
    fig.add_trace(go.Scatter(
        x=future_data.index,
        y=future_data['Close'],
        mode='lines',
        name='Future Close Price',
        line=dict(width=2, color='red', dash='dash')  # Dashed red for clarity
    ))

    # Add range slider
    fig.update_xaxes(rangeslider_visible=True)

    # Improve layout
    fig.update_layout(
        height=500,
        margin=dict(l=0, r=20, t=20, b=0),
        plot_bgcolor='white',
        paper_bgcolor='#E1EFFF',
        legend=dict(yanchor="top", xanchor="right")
    )

    return fig
