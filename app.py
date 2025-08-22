# Sample structure of the updated app.py with all 4 features integrated
import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt
import seaborn as sns


st.set_page_config(layout="wide")

st.sidebar.title("Whatsapp Chat Analyzer")
uploaded_file = st.sidebar.file_uploader("Choose a file", type="txt")

if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    # Fetch unique users
    user_list = df['user'].unique().tolist()
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)

    if st.sidebar.button("Show Analysis"):
        # Stats
        num_messages, num_words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)

        tab1, tab2, tab3, tab4 = st.tabs(["📊 Statistics", "📅 Timeline", "😄 Emojis", "☁️ Word Cloud"])

        with tab1:
            st.header("Top Statistics")
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total Messages", num_messages)
            col2.metric("Total Words", num_words)
            col3.metric("Media Shared", num_media_messages)
            col4.metric("Links Shared", num_links)

            st.header("Most Active Users")
            fig, ax = helper.most_active_users(selected_user, df)
            st.pyplot(fig)

        with tab2:
            st.header("Monthly Timeline")
            timeline = helper.monthly_timeline(selected_user, df)
            st.line_chart(timeline.set_index('time')['message'])

            st.header("Daily Timeline")
            daily_timeline = helper.daily_timeline(selected_user, df)
            st.line_chart(daily_timeline.set_index('only_date')['message'])

            st.header("Weekly Activity Heatmap")
            heatmap_data = helper.activity_heatmap(selected_user, df)
            fig, ax = plt.subplots(figsize=(10, 5))
            sns.heatmap(heatmap_data, cmap='YlGnBu', linewidths=0.5, ax=ax)
            st.pyplot(fig)

        with tab3:
            st.header("Top Emojis")
            emoji_df = helper.emoji_helper(selected_user, df)
            st.dataframe(emoji_df)
            st.bar_chart(emoji_df.set_index('emoji')['count'])

        with tab4:
            st.header("Word Cloud")
            wc = helper.generate_wordcloud(selected_user, df)
            fig, ax = plt.subplots()
            ax.imshow(wc, interpolation="bilinear")
            ax.axis("off")
            st.pyplot(fig)

            st.divider()
            st.header("Most Common Words")
            common_words_df = helper.most_common_words(selected_user, df)
            st.dataframe(common_words_df)
