import pandas as pd

def process_expenses(file):
    df = pd.read_csv(file, parse_dates=['Date'])
    df['Month'] = df['Date'].dt.to_period('M').astype(str)
    df['Year'] = df['Date'].dt.year
    return df

def process_growth(file):
    df = pd.read_csv(file, parse_dates=['Date'])
    df['Month'] = df['Date'].dt.to_period('M').astype(str)
    df['Year'] = df['Date'].dt.year
    return df
