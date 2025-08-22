from collections import Counter
import pandas as pd
import re
import emoji
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import seaborn as sns
import urlextract


def emoji_helper(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([char for char in message if emoji.is_emoji(char)])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(), columns=['emoji', 'count'])
    return emoji_df


def most_common_words(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[~df['message'].str.contains('media omitted', case=False)]
    temp = temp[~temp['message'].str.contains('This message was deleted', case=False)]

    words = []
    for message in temp['message']:
        message = re.sub(r"http\S+", "", message)
        for word in message.lower().split():
            if len(word) > 2 and word.isalpha():
                words.append(word)

    common_words_df = pd.DataFrame(Counter(words).most_common(20), columns=['word', 'count'])
    return common_words_df


def generate_wordcloud(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[~df['message'].str.contains('media omitted', case=False)]
    temp = temp[~df['message'].str.contains('This message was deleted', case=False)]

    text = ' '.join(temp['message'].tolist())

    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    return wordcloud


def activity_heatmap(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    heatmap_data = df.pivot_table(index='day_name', columns='hour', values='message', aggfunc='count').fillna(0)

    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    heatmap_data = heatmap_data.reindex(days)

    return heatmap_data


def fetch_stats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    num_messages = df.shape[0]

    words = []
    for message in df['message']:
        words.extend(message.split())
    num_words = len(words)

    num_media_messages = df[df['message'] == '<Media omitted>'].shape[0]

    extractor = urlextract.URLExtract()
    links = []
    for message in df['message']:
        links.extend(extractor.find_urls(message))
    num_links = len(links)

    return num_messages, num_words, num_media_messages, num_links


def most_active_users(selected_user, df):
    if selected_user == 'Overall':
        user_counts = df['user'].value_counts().head(10)
        fig, ax = plt.subplots()
        ax.bar(user_counts.index, user_counts.values, color='skyblue')
        plt.xticks(rotation=45)
        plt.xlabel("User")
        plt.ylabel("Message Count")
        plt.title("Top 10 Most Active Users")
        return fig, ax
    else:
        st.info("This chart is only available for 'Overall' selection.")
        return None, None


def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    timeline['time'] = timeline['month'] + '-' + timeline['year'].astype(str)
    return timeline


def daily_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['message'].reset_index()
    return daily_timeline
