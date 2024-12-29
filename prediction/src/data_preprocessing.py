import pandas as pd
from sklearn.model_selection import train_test_split
# src/data_preprocessing.py

import yfinance as yf
import pandas as pd
from typing import Optional

def load_data_from_yfinance(
        ticker: str,
        start_date: str,
        end_date: str,
        interval: str = '1d'
    ) -> pd.DataFrame:
    df = yf.download(ticker, start=start_date, end=end_date, interval=interval)
    df.dropna(inplace=True)
    return df

def load_data(filepath: str) -> pd.DataFrame:
    return pd.read_csv(filepath)

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.dropna()
    df = df.drop_duplicates()
    return df

def split_data(df: pd.DataFrame, target_column: str, test_size=0.2):
    X = df.drop(columns=[target_column])
    y = df[target_column]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, shuffle=False
    )
    return X_train, X_test, y_train, y_test
