
# WhatsApp Chat Analyzer

This is a Streamlit-based application that helps you analyze and visualize your WhatsApp chat history.

You can view:

* Total number of messages, words, media, and links
* Most active users in the chat
* Word cloud showing the most used words
* Timeline of message activity
* Emoji usage statistics
* Activity heatmap by day and hour


## How to Use

1. Open WhatsApp, export your chat as a `.txt` file (without media)
2. Save the file on your computer
3. Run the app using the following command:

```bash
streamlit run app.py
```

4. Upload the `.txt` file in the app
5. Choose a user or select "Overall" to see complete chat analysis


## Features

* Total chat statistics (messages, words, media, links)
* Analysis for individual users and overall chat
* Monthly message timeline
* Most active users
* Word frequency and word cloud
* Emoji usage count
* Weekly and hourly activity heatmap


## Requirements

Install the necessary Python libraries with:

```bash
pip install -r requirements.txt
```


## Notes

* Only works with exported WhatsApp `.txt` files (from Android)
* Make sure the chat is exported without media
* File size should be under 200 MB




