import streamlit as st
import ranker as rank

import yfinance as yf

col1, col2, col3 = st.columns(3)
with col1:
    st.write(" ")
with col2:
    st.image("hotstoxlogo.jpeg")
with col3:
    st.write(" ")

# st.markdown("<div style='text-align: center;'> By Kaush</div>", unsafe_allow_html=True)

col1, col_space, col2= st.columns([2,1,2])

with col1:
    left, right = st.columns(2)
    with left:
        sub = st.selectbox(
            "Select a subreddit",
            ("wallstreetbets","stocks", "investing"),
            width="stretch"
        )
    with right:
        filter = st.selectbox(
            "Filter by:",
            ("day", "week", "year", "all"),
            width = "stretch"
        )

# st.markdown("")

with col2:
    st.write("")
    update = st.button("Update", 
                       type="primary",
                       width= "stretch"
                       )

@st.cache_data(ttl = 660)
def insanelycomplexfunction(sub, amount, filter): #cached version of run_rank function
    return rank.run_ranker(sub,amount,filter)

@st.cache_data(ttl=900)
def get_price(tickers):
    df = yf.download(tickers, period='1d', group_by="ticker",auto_adjust=False)
    prices = {}
    for t in tickers:
        try:
            prices[t] = round(df[t]['Close'].iloc[-1],2)
        except Exception:
            prices[t] = None
    return prices

# x = st.slider("number of rows", max_value = 15)

if update:
    with st.spinner("Crunching Reddit stock data...", show_time=True):
        df = rank.run_ranker(sub,1000,filter)
        top_tickers = df['p_mentioned'].head(50).tolist()
        sentiment = df['avg_sent'].head(50).tolist()
        
        prices = get_price(top_tickers)
        
        i = 0
        for rank, ticker in enumerate(top_tickers, start=1):
            col1, col2 = st.columns([1,3])
            current_price = prices.get(ticker, "N/A")
            # yticker = yf.Ticker(ticker)
            # current_price = round(yticker.fast_info['lastPrice'], 2)

            if(sentiment[i] < 0.4):
                color = "red"
            elif (sentiment[i] > 0.7):
                color = "green"
            else:
                color = "orange"
            
            col1.write(f"### {rank}. :{color}[**{ticker}**] \n ${current_price}")
            i += 1
            # yticker = yf.Ticker(ticker)
            # current_price = round(yticker.fast_info['lastPrice'], 2)

            #col1.write(f"### {rank}. **{ticker}** \n ${current_price}")
            #if(sentiment < 0.4):
            #    indicator = 'Negative'
            #elif(sentiment > 0.6):
             #   indicator = 'Positive'
            #else:
            #    indicator = 'Neutral'
            #col1.write(f"Sentiment: {indicator}")
            
            st.divider()

            data = yf.download(ticker, period="1mo")['Close']
            col2.line_chart(data, y_label = "Price")
