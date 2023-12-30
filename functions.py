# Importing libraries
import plotly.express as px
import numpy as np

# Function to plot interactive plotly chart
def interactive_plot(df, title="Interactive Plot", x_axis_label="Time (Years)", y_axis_label="Value", height=500):
    fig = px.line(df, x='Date', y=df.columns[1:], title=title)
    # Customize layout
    fig.update_layout(
        width=600,
        height=400,  
        margin=dict(l=20, r=20, t=20, b=20),
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1,),
        xaxis_title=x_axis_label,
        yaxis_title=y_axis_label,
    )
    return fig


# Function to normalize the prices based on the initial price
def normalize(df_2):
    df = df_2.copy()
    for i in df.columns[1:]:
        df[i] = df[i]/df[i][0]
    return df

# Function to calculate daily returns
def daily_return(df):
    df_daily_return = df.copy()
    for i in df.columns[1:]:
        for j in range(1,len(df)):
            df_daily_return[i][j] = (df[i][j]-df[i][j-1])/df[i][j-1]*100
        df_daily_return[i][0] = 0
    return df_daily_return

# Function to calculate beta
def calculate_beta(stocks_daily_return, stock):
    rm = stocks_daily_return['sp500'].mean()*252
    b, a = np.polyfit(stocks_daily_return['sp500'], stocks_daily_return[stock],1)
    return b,a