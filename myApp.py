# import symbol
# import yfinance as yf
import streamlit as st
import pandas as pd
# import opstrat as op
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import altair as alt

option = st.sidebar.selectbox(
    'Which Dashboard would you like to see?',
    ('PayOff Calculator', 'Notes'))

# st.write('You selected:', option)
st.header(option)
st.write(""" ***By   :    Anu Varshini R, Abishek Srikanth and Kailash S***

""" )
# if option =='Stock Price':
#     # st.subheader("Stock Price dashboard")
#     company=st.sidebar.text_input("Company Name",value='AAPL')
#     st.write(f"""Shown are the stock **closing price** and volume of {company}!
#     """)

#     tickerSymbol =company

#     tickerData = yf.Ticker(tickerSymbol)

#     tickerDf=tickerData.history(period='1d',start='2012-10-6', end='2022-10-6')

#     st.write("""
#     ## Closing Price
#     """)
#     st.line_chart(tickerDf.Close)

#     st.write("""
#     ## Volume
#     """)
#     st.line_chart(tickerDf.Volume)

if option == 'PayOff Calculator':
    st.sidebar.write("**Input stock price of underlying asset**")
    underlying_price = st.sidebar.number_input('Stock Price',key = 'Underlying asset price', step =1, value = 100)
    st.sidebar.write("**Select the number of options**")
    layout=st.sidebar.columns(2)

    with layout[0]:
        long_call = st.sidebar.slider("Long Call",0,3,value=1)
        short_call = st.sidebar.slider("Short Call",0,3)

    with layout[-1]:
        long_put = st.sidebar.slider("Long Put",0,3)
        short_put = st.sidebar.slider("Short Put",0,3)
    
    

    #array for premiums
    lcp = np.ones(long_call)
    scp = np.ones(short_call)
    lpp = np.ones(long_put)
    spp = np.ones(short_put)
    #array for strike price
    lcs = np.ones(long_call)
    scs = np.ones(short_call)
    lps = np.ones(long_put)
    sps = np.ones(short_put)

    if long_call+short_call+long_put+short_put > 0:
        st.write('Input the individual options')

    
    col1, col2, col3, col4 = st.columns(4)
    if long_call >0:
        col1.write('**Long Calls**')
    else:
        col1.write('**No Long Calls**')
    if long_put >0:
        col3.write('**Long Puts**')
    else:
        col3.write('**No Long Puts**')
    
    lcol1, lcol2, lcol3, lcol4 = st.columns(4)
    for i in range(long_call):
        with lcol1:
            lcp[i]=st.number_input("Option Premium", key=('lcp'+str(i)),step=1e-1)
        with lcol2:
            lcs[i]=st.number_input("Strike Price",key=('lcs'+str(i)),step=1)

    for i in range(long_put):
        with lcol3:
            lpp[i]=st.number_input("Option Premium", key=('lpp'+str(i)),step=1e-1)
        with lcol4:
            lps[i]=st.number_input("Strike Price",key=('lps'+str(i)),step=1)
    
    col1, col2, col3, col4 = st.columns(4)
    if short_call >0:
        col1.write('**Short Calls**')
    else:
        col1.write('**No Short Calls**')
    if short_put >0:
        col3.write('**Short Puts**')
    else:
        col3.write('**No Short Puts**')
    
    scol1, scol2, scol3, scol4 = st.columns(4)
    for i in range(short_call):
        with scol1:
            scp[i]=st.number_input("Option Premium", key=('scp'+str(i)),step=1e-1)
        with scol2:
            scs[i]=st.number_input("Strike Price",key=('scs'+str(i)),step=1)

    for i in range(short_put):
        with scol3:
            spp[i]=st.number_input("Option Premium", key=('spp'+str(i)),step=1e-1)
        with scol4:
            sps[i]=st.number_input("Strike Price",key=('sps'+str(i)),step=1)
    # st.write(lcp)
    # st.write(lcs[1])
    # st.write(lpp)
    # st.write(lps)
  
    portfolio_cost = underlying_price + np.sum(lcp) + np.sum(lpp) - np.sum(scp) - np.sum(spp)
    st.write(""" ### Set up cost""")
    if portfolio_cost == 0:
        st.metric(label="Cost to set up the portfolio", value = ('$'+str(0)))
    if portfolio_cost > 0:
        st.metric(label="Cost to set up the portfolio", value = ('$'+str(abs(portfolio_cost))), delta='Loss',delta_color= "inverse")
    if portfolio_cost < 0:
        st.metric(label="Cost to set up the portfolio", value = ('$'+str(abs(portfolio_cost))), delta='Profit')

    # op.single_plotter(save=True,file='simple_option.jpeg')
    # image=Image.open("simple_option.jpeg")
    # st.image(image)

    def plot_option_payoff(k):
    # x-axis
        S_t = np.arange(start = 0, stop = 2*k, step = 0.1)
            
        # defining y variables
        y_1 = np.empty(len(S_t))
        y_2 = np.empty(len(S_t))
        y_3 = np.empty(len(S_t))
        y_4 = np.empty(len(S_t))
        

        # y-axis is sum of payoffs
        # long call
        for i in range (len(S_t)):
            y_1[i] = np.sum(np.maximum((S_t[i] - lcs), 0))
        # short call
            y_2[i] = np.sum(np.minimum((scs - S_t[i]), 0))
        # long put
            y_3[i] = np.sum(np.maximum((lps - S_t[i]), 0))
        # short put
            y_4[i] = np.sum(np.minimum((S_t[i] - sps), 0))
        # buying a buying/selling stocks
        s = (S_t - k)

        # total
        y = y_1 + y_2 + y_3 + y_4+s-portfolio_cost
            
        # converting to df
        plot_data = pd.DataFrame({'Stock Price': S_t, 'Net Payoff': y})
        return plot_data

    dataset = plot_option_payoff(underlying_price)               
    #Line Chart

    st.write(""" ### Payoff Graph""")

    chart = (
            alt.Chart(
                data=dataset
            )
            .mark_line()
            .encode(
                x=alt.X("Stock Price", title="Stock Price"),
                y=alt.Y("Net Payoff", title="Net Payoff"),
                tooltip = ['Stock Price', 'Net Payoff']
            ).configure_axis(
    grid=False
    )
    )

    st.altair_chart(chart, use_container_width=True)

# st.sidebar.write("Options")

if option == 'Notes':
    st.image('https://analystprep.com/cfa-level-1-exam/wp-content/uploads/2019/10/56c-2.png')
    st.image('https://analystprep.com/cfa-level-1-exam/wp-content/uploads/2019/10/56c-3.png')
    st.image('https://analystprep.com/cfa-level-1-exam/wp-content/uploads/2019/10/56c-4.png')
    st.image('https://analystprep.com/cfa-level-1-exam/wp-content/uploads/2019/10/56c-5.png')
    

