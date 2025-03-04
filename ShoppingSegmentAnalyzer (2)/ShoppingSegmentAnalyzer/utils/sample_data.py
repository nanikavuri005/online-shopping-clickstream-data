import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_sample_data(num_users=100, days_back=30):
    """
    Generate sample clickstream data for testing
    """
    np.random.seed(42)
    
    # Generate user IDs
    user_ids = [f"user_{i}" for i in range(num_users)]
    
    # Generate events
    event_types = [
        'page_view',
        'product_view',
        'add_to_cart',
        'remove_from_cart',
        'purchase',
        'search'
    ]
    
    # Generate timestamps
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days_back)
    
    # Create sample data
    data = []
    for user_id in user_ids:
        # Random number of events for each user
        num_events = np.random.randint(5, 50)
        
        # Generate session IDs for user
        num_sessions = np.random.randint(1, 5)
        sessions = [f"session_{user_id}_{i}" for i in range(num_sessions)]
        
        for _ in range(num_events):
            timestamp = start_date + timedelta(
                seconds=np.random.randint(0, days_back * 24 * 60 * 60)
            )
            data.append({
                'user_id': user_id,
                'event_type': np.random.choice(event_types),
                'timestamp': timestamp,
                'session_id': np.random.choice(sessions)
            })
    
    # Convert to DataFrame
    df = pd.DataFrame(data)
    
    # Sort by user and timestamp
    df = df.sort_values(['user_id', 'timestamp'])
    
    return df

def get_sample_data():
    """
    Return sample data and display info about its structure
    """
    df = generate_sample_data()
    
    info = """
    Sample Data Structure:
    - user_id: Unique identifier for each user
    - event_type: Type of user interaction (page_view, product_view, etc.)
    - timestamp: When the event occurred
    - session_id: Unique identifier for user sessions
    """
    
    return df, info
