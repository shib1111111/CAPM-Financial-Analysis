# Importing libraries
import streamlit as st
import pandas as pd
import yfinance as yf
import pandas_datareader.data as web
import datetime
from functions import interactive_plot, normalize, daily_return, calculate_beta

# Function to get user input for CAPM
def get_user_input():
    st.markdown("<H1 class='big-title'>Capital Asset Pricing Model (CAPM)</H1>", unsafe_allow_html=True)
    st.markdown("<h3 class='small-subtitle'>Financial Analysis</h3>", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])
    
    # User selects stocks and number of years
    with col1:
        stock_list = st.multiselect(
            "Choose 4 stocks",
            ('TSLA', 'AAPL', 'NFLX', 'MSFT', 'MGM', 'AMZN', 'NVDA', 'GOOGL'),
            ['TSLA', 'AAPL', 'AMZN', 'GOOGL']
        )
    with col2:
        year = st.number_input("Number of years", 1, 10)
        rf = st.number_input("Risk-Free Rate (%)", value=0.0)

    return stock_list, year,rf


# Function to download financial data
def download_data(stock_list, year):
    end = datetime.date.today()
    start = datetime.date(datetime.date.today().year - year, datetime.date.today().month, datetime.date.today().day)
    
    try:
        # Download S&P 500 data
        SP500 = web.DataReader(['sp500'], 'fred', start, end)
        
        # Create DataFrame for stock data
        stocks_df = pd.DataFrame()
        
        # Download data for selected stocks
        for stock in stock_list:
            data = yf.download(stock, period=f'{year}y')
            stock_data = data[['Close']].copy()
            stocks_df[f'{stock}'] = stock_data['Close']
        
        # Reset index and merge with S&P 500 data
        stocks_df.reset_index(inplace=True)
        SP500.reset_index(inplace=True)
        SP500.columns = ['Date', 'sp500']
        stocks_df['Date'] = stocks_df['Date'].astype('datetime64[ns]')
        stocks_df['Date'] = stocks_df['Date'].apply(lambda x: str(x)[:10])
        stocks_df['Date'] = pd.to_datetime(stocks_df['Date'])
        stocks_df = pd.merge(stocks_df, SP500, on='Date', how='inner')
        
        return stocks_df, SP500
    except:
        st.write("Please select valid inputs")



# Displaying dataframes and plots
def display_dataframes_and_plots(stocks_df, SP500):
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("### Dataframe head")
        st.dataframe(stocks_df.head(), use_container_width=True)
    with col2:
        st.markdown("### Dataframe tail")
        st.dataframe(stocks_df.tail(), use_container_width=True)

    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("### Price of all the Stocks")
        st.plotly_chart(interactive_plot(stocks_df))
    with col2:
        st.markdown("### Price of all the Stocks (After Normalizing)")
        st.plotly_chart(interactive_plot(normalize(stocks_df)))

# Function to calculate and display metrics
def calculate_and_display_metrics(stocks_df, SP500, stock_list, rf):
    # Calculate daily returns
    stocks_daily_return = daily_return(stocks_df)

    # Calculate beta and alpha for each stock
    beta = {}
    alpha = {}
    for stock in stocks_daily_return.columns:
        if stock != 'Date' and stock != 'sp500':
            b, a = calculate_beta(stocks_daily_return, stock)
            beta[stock] = b
            alpha[stock] = a

    # Create a DataFrame for beta values
    beta_df = pd.DataFrame(columns=['Stocks', 'Beta Value'])
    beta_df['Stocks'] = beta.keys()
    beta_df['Beta Value'] = [str(round(i, 2)) for i in beta.values()]

    # Display beta values
    st.markdown('### Calculated Beta Value')
    st.dataframe(beta_df, use_container_width=True)

    # Create a DataFrame for alpha values
    alpha_df = pd.DataFrame(columns=['Stocks', 'Alpha Value'])
    alpha_df['Stocks'] = alpha.keys()
    alpha_df['Alpha Value'] = [str(round(i, 2)) for i in alpha.values()]

    # Display alpha values
    st.markdown('### Calculated Alpha Value')
    st.dataframe(alpha_df, use_container_width=True)

    # Calculate returns using CAPM
    return_df = pd.DataFrame()
    return_value = []
    rm = stocks_daily_return['sp500'].mean() * 252
    for stock, b_value in beta.items():
        return_value.append(str(round(rf + (b_value * (rf - rm)), 2)))
    return_df['Stock'] = stock_list
    return_df['Return Value'] = return_value

    # Display returns using CAPM
    st.markdown('### Calculated Return using CAPM')
    st.dataframe(return_df, use_container_width=True)



# Apply CSS
def apply_css():
    st.markdown(
        """
            <style>
                    .big-title {
                        font-size: 3.5em;
                        font-weight: bold;
                        font-family: 'Times New Roman', Times, serif;
                        font-style: italic;
                        text-align: center;
                    }
                    
                    .small-subtitle {
                        font-size: 2.5em;
                        margin-top: -15px; 
                        font-family: 'Arial', sans-serif;
                        font-style: italic;
                        text-align: center;
                        margin-bottom: 40px; 
                    }
                    
            </style>
        """,
        unsafe_allow_html=True
    )