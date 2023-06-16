import pandas as pd


data1 = pd.read_csv('data1.csv')
data2 = pd.read_csv('data2.csv')
combined_data = data1.merge(data2, on='user_id')
combined_data['day'] = pd.to_datetime(combined_data['event_date']).dt.day
combined_data['month'] = pd.to_datetime(combined_data['event_date']).dt.month
unique_data = combined_data.drop_duplicates(subset='user_id')
unique_data.to_csv('cleaned_data.csv', index=False)

def filter_on_column(df: pd.DataFrame, col_name: str, filter_value) -> pd.DataFrame:
    return df[df[col_name] == filter_value]

def df_to_dict(df: pd.DataFrame) -> dict:
    return df.to_dict()