import streamlit as st 

st.set_page_config(
    page_title ="Trading App",
    page_icon ="chart_with_downward_trend",
    layout="wide" 

)

st.title("'Trading Guide app :bar_chart:")

st.header("We provide the Greatest platform for you to collect all informtaion prior to investing in stocks")


st.image("image.png")

st.markdown("## We provide the following services:")


st.markdown("#### :one: stock information")
st.write("Through this page, you can see all information about stock. ")

st.markdown("#### :two: stock Analysis")
st.write("You can obtain various info such as company description, employee, website. price can be obtained through option such candlestick,line.MACD or RSI enabling greater visibility.")


st.markdown("#### :two: stock prediction")
st.write("You can explore predicted closing prices for the next 30 days based on historical  stock data and advanced forecsting models.use this tool to gain valuable insights into market trends and make informed investment decisions. ")

