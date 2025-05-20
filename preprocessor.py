import re
import pandas as pd

def preprocess(data):
    # Regex pattern for date with AM/PM format
    pattern = r'(\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s[apAP][mM])\s-\s'

    # Split the text using the pattern
    split_data = re.split(pattern, data)

    # Dates are in every odd index; messages in every even after the first element
    if len(split_data) < 3:
        raise ValueError("Chat data does not match expected format.")

    dates = split_data[1::2]
    messages = split_data[2::2]

    # Safety check
    if len(dates) != len(messages):
        print(f"[DEBUG] Mismatched Lengths - Dates: {len(dates)}, Messages: {len(messages)}")
        raise ValueError("All arrays must be of the same length")

    # Create DataFrame
    df = pd.DataFrame({'message_date': dates, 'user_message': messages})
    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%y, %I:%M %p', errors='coerce')
    df.rename(columns={'message_date': 'date'}, inplace=True)

    users = []
    final_messages = []

    for message in df['user_message']:
        entry = re.split(r'([\w\W]+?):\s', message, maxsplit=1)
        if len(entry) > 2:
            users.append(entry[1])
            final_messages.append(entry[2])
        else:
            users.append('group_notification')
            final_messages.append(entry[0])

    df['user'] = users
    df['message'] = final_messages
    df.drop(columns=['user_message'], inplace=True)

    return df
