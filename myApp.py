# import symbol
# import yfinance as yf
import streamlit as st
import pandas as pd
# import opstrat as op
# import matplotlib.pyplot as plt
# from PIL import Image
import numpy as np
import altair as alt

option = st.sidebar.selectbox(
    'Which Dashboard would you like to see?',
    ('PayOff Calculator', 'Notes'))

# st.write('You selected:', option)
st.header(option)
st.write(""" ***By   :    Anu Varshini R***
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
    underlying_price = st.sidebar.number_input('Stock Price',key = 'Underlying asset price', step =1)
    option_ls = st.sidebar.selectbox(
    'Long/Short?',
    ('','Long', 'Short'))
    st.sidebar.write("**Select the number of options**")
    layout=st.sidebar.columns(2)

    with layout[0]:
        long_call = st.sidebar.slider("Long Call",0,3)
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
        st.write(""" ### Input the details of the Options""")

    
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
  
    portfolio_cost =  np.sum(lcp) + np.sum(lpp) - np.sum(scp) - np.sum(spp)
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
    def call_payoff(sT, strike_price, premium):
        return np.where(sT > strike_price, sT - strike_price, 0) - premium

    def put_payoff(sT, strike_price, premium):
        return np.where(sT < strike_price, strike_price - sT, 0) - premium

    def plot_final(underlying_price):
        payoff_long_call=0
        payoff_short_call=0
        payoff_long_put=0
        payoff_short_put=0
        if long_call>0:
            
            for i in range(len(lcs)):
                sT = np.arange(0,2*underlying_price,1)
                payoff_long_call+=call_payoff(sT, lcs[i], lcp[i])
        if short_call>0:
            
            for i in range(len(scs)):
                sT = np.arange(0,2*underlying_price,1)
                payoff_short_call+=call_payoff(sT, scs[i], scp[i])*-1
        if long_put>0:
            
            for i in range(len(lps)):
                sT=np.arange(0,2*underlying_price,1)
                payoff_long_put+=put_payoff(sT, lps[i], lpp[i])
        if short_put>0:
            
            for i in range(len(sps)):
                sT=np.arange(0,2*underlying_price,1)
                payoff_short_put+=put_payoff(sT, sps[i], spp[i])*-1
        sT = np.arange(0,2*underlying_price,1)
        # long_stock=np.arange(-underlying_price,netpay,1)
        net_pay=payoff_long_call+payoff_short_call+payoff_long_put+payoff_short_put
        if option_ls=='Long':
            net_pay=net_pay+sT-underlying_price
        if option_ls=='Short':
            net_pay=net_pay+underlying_price-sT
        # long_stock=np.arange(-underlying_price,netpay,1)
        # net_payy=netpay+long_stock
        plot_data = pd.DataFrame({'Stock Price': sT, 'Net Payoff': net_pay})
        # plot_data=plot_data['Net Payoff']-underlying_price
        return plot_data

    dataset = plot_final(underlying_price)               
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
    
