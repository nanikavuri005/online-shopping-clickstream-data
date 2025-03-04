import pandas as pd
import numpy as np
from datetime import datetime

def process_clickstream_data(df):
    """
    Process raw clickstream data for analysis
    """
    try:
        # Create a copy to avoid modifying original data
        df = df.copy()

        # Map columns to standardized format
        df['timestamp'] = pd.to_datetime(df['Timestamp'])
        df['user_id'] = df['User_ID']
        df['session_id'] = df['Session_ID']
        df['event_type'] = df['Action']

        # Calculate purchase events
        df['purchased'] = (df['Action'].str.lower() == 'purchase').astype(int)

        # Sort by user and timestamp
        df = df.sort_values(['user_id', 'timestamp'])

        # Calculate session duration
        df['session_duration'] = df.groupby('session_id').apply(
            lambda x: (x['timestamp'].max() - x['timestamp'].min()).total_seconds() / 60
            if len(x) > 1 else 0
        ).reset_index(level=0, drop=True)

        # Calculate time between events
        df['time_between_events'] = df.groupby('user_id')['timestamp'].diff().dt.total_seconds().fillna(0)

        # Calculate user metrics
        user_metrics = calculate_user_metrics(df)
        df = df.merge(user_metrics, on='user_id', how='left')

        # Assign initial segments
        df['segment'] = assign_initial_segments(df)

        return df

    except Exception as e:
        raise Exception(f"Error processing data: {str(e)}\nPlease check your data format.")

def calculate_user_metrics(df):
    """
    Calculate various user-level metrics
    """
    try:
        user_metrics = df.groupby('user_id').agg({
            'session_id': 'nunique',
            'event_type': 'count',
            'purchased': 'sum',
            'session_duration': 'mean'
        }).reset_index()

        user_metrics.columns = [
            'user_id',
            'total_sessions',
            'total_events',
            'total_purchases',
            'avg_session_duration'
        ]

        return user_metrics.fillna({
            'total_sessions': 1,
            'total_events': 0,
            'total_purchases': 0,
            'avg_session_duration': 0
        })

    except Exception as e:
        print(f"Warning: Error calculating user metrics: {str(e)}")
        return pd.DataFrame(columns=['user_id', 'total_sessions', 'total_events', 
                                   'total_purchases', 'avg_session_duration'])

def assign_initial_segments(df):
    """
    Assign initial customer segments based on behavior
    """
    try:
        conditions = [
            (df['total_purchases'] > 3) & (df['avg_session_duration'] > 10),
            (df['total_purchases'] > 0),
            (df['total_events'] > 5)
        ]
        choices = ['Power Shoppers', 'Customers', 'Browsers']
        return np.select(conditions, choices, default='Visitors')
    except Exception as e:
        print(f"Warning: Error assigning segments: {str(e)}")
        return pd.Series('Visitors', index=df.index)