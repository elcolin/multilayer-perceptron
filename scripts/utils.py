import pandas as pd

def normalize(df):
    df = df.reset_index(drop=True)     # lignes → 0..n-1
    df.columns = range(df.shape[1])    # colonnes → 0..m-1
    return df