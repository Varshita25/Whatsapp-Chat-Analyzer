import pandas as pd
import emoji
from urlextract import URLExtract
from collections import Counter
from wordcloud import WordCloud

extractor = URLExtract()

def fetch_stats(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]
    num_messages = df.shape[0]
    words = df['message'].apply(lambda x: len(x.split())).sum()
    media = df[df['message'] == '<Media omitted>'].shape[0]
    links = df['message'].apply(lambda msg: len(extractor.find_urls(msg))).sum()
    return num_messages, words, media, links

def most_busy_users(df):
    return df['user'].value_counts().head()

def create_wordcloud(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]
    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    return wc.generate(' '.join(df['message']))

def most_common_words(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]
    words = []
    for message in df['message']:
        words.extend(message.lower().split())
    return pd.DataFrame(Counter(words).most_common(20))

def monthly_timeline(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]
    timeline = df.groupby([df['date'].dt.year, df['date'].dt.month_name()]).count()['message'].reset_index()
    timeline['time'] = timeline['date'].astype(str) + " - " + timeline['month']
    return timeline

def daily_timeline(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]
    return df.groupby(df['date'].dt.date).count()['message'].reset_index()

def activity_map(df):
    busy_day = df['date'].dt.day_name().value_counts()
    busy_month = df['date'].dt.month_name().value_counts()
    return busy_day, busy_month

def emoji_analysis(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]
    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if emoji.is_emoji(c)])
    return pd.DataFrame(Counter(emojis).most_common(10))
