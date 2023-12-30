# Importing libraries
import streamlit as st
from content_renderer import download_data, calculate_and_display_metrics, display_dataframes_and_plots, get_user_input,apply_css
from signature import display_signature

def main():
    # Set Streamlit page configuration
    st.set_page_config(
        page_title="CAPM Financial Analysis",
        page_icon="chart_with_upwards_trend",
        layout='wide'
    )
    apply_css()

    # Get user input for CAPM
    stock_list, year,rf = get_user_input()
    
    # Download financial data
    stocks_df, SP500 = download_data(stock_list, year)
    
    # Display dataframes and plots
    display_dataframes_and_plots(stocks_df, SP500)
    
    # Calculate and display metrics (Beta values and Returns)
    calculate_and_display_metrics(stocks_df, SP500, stock_list, rf)
    

    # Adding the signature
    display_signature()

if __name__ == "__main__":
    main()
