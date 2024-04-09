import json
import re

import pandas as pd
from datetime import datetime
import plotly.express as px

# Load JSON data from file
with open('chat_data.json', 'r', encoding='utf-8') as file:
    json_data = json.load(file)


# Define a function to extract hashtags from a message
def extract_hashtags(message):
    hashtags = re.findall(r'#(\w+)', message)
    return hashtags


# Define a function to extract mentions from a message
def extract_mentions(message):
    mentions = re.findall(r'@(\w+)', message)
    return mentions


# Define a function to extract URLs from a message
def extract_urls(message):
    urls = re.findall(r'(https?://\S+)', message)
    return urls


# Define a function to categorize media type from attachment URLs
def categorize_media_type(message):
    if 'share' in message and 'link' in message['share']:
        attachment_url = message['share']['link']
        if attachment_url.endswith('.jpg') or attachment_url.endswith('.png'):
            return 'image'
        elif attachment_url.endswith('.mp4') or attachment_url.endswith('.mov'):
            return 'video'
    return 'other'

# Initialize lists to store data
data_rows = []

# Iterate through messages
for message in json_data['messages']:
    # Convert timestamp to datetime object
    timestamp_ms = message['timestamp_ms'] / 1000
    date = datetime.utcfromtimestamp(timestamp_ms).strftime('%Y-%m-%d %H:%M:%S')
    date_only = datetime.utcfromtimestamp(timestamp_ms).strftime('%Y-%m-%d')
    year = datetime.utcfromtimestamp(timestamp_ms).strftime('%Y')
    month = datetime.utcfromtimestamp(timestamp_ms).strftime('%B')
    month_num = datetime.utcfromtimestamp(timestamp_ms).strftime('%m')
    day = datetime.utcfromtimestamp(timestamp_ms).strftime('%d')
    day_name = datetime.utcfromtimestamp(timestamp_ms).strftime('%A')
    hour = datetime.utcfromtimestamp(timestamp_ms).strftime('%H')
    minute = datetime.utcfromtimestamp(timestamp_ms).strftime('%M')

    # Get message content or set it to an empty string if not present
    message_content = message.get('content', '')

    # Determine message type
    if 'share' in message:
        message_type = 'attachment'
        # Check if the attachment contains a link
        if 'link' in message['share']:
            attachment_link = message['share']['link']
            # Check the type of link and append it to the appropriate list
            if attachment_link.startswith('https://www.instagram.com/reel/'):
                reel_link = attachment_link
                stories_link = ''
                post_link = ''
            elif attachment_link.startswith('https://instagram.com/stories/'):
                reel_link = ''
                stories_link = attachment_link
                post_link = ''
            elif attachment_link.startswith('https://www.instagram.com/p/'):
                reel_link = ''
                stories_link = ''
                post_link = attachment_link
            else:
                reel_link = ''
                stories_link = ''
                post_link = ''
        else:
            # If the 'link' key is not present, set all link columns to empty strings
            reel_link = ''
            stories_link = ''
            post_link = ''
    elif 'reactions' in message:
        message_type = 'reaction'
        reel_link = ''
        stories_link = ''
        post_link = ''
    else:
        message_type = 'text'
        reel_link = ''
        stories_link = ''
        post_link = ''

    # Count reactions
    reactions_count = len(message.get('reactions', []))

    # Calculate word count and average word length
    words = message_content.split()
    word_count = len(words)
    if word_count > 0:
        avg_word_length = sum(len(word) for word in words) / word_count
    else:
        avg_word_length = 0

    # Extract hashtags, mentions, and URLs
    hashtags = extract_hashtags(message_content)
    mentions = extract_mentions(message_content)
    urls = extract_urls(message_content)

    # Categorize media type
    media_type = categorize_media_type(message)

    # Append data row to list
    data_rows.append(
        [date, date_only, year, month, month_num, day, day_name, hour, minute, message['sender_name'].encode("Latin1").decode("UTF-8"), message_content.encode("Latin1").decode("UTF-8"),
         len(message_content), message_type, reactions_count, word_count, avg_word_length, hashtags, mentions,
         media_type, reel_link, stories_link, post_link])

# Create DataFrame
columns = ['date', 'date_only', 'year', 'month', 'month_num', 'day', 'day_name', 'hour', 'minute', 'user', 'message',
           'message_length', 'message_type', 'reactions_count', 'word_count', 'avg_word_length', 'hashtags', 'mentions',
           'media_type', 'reel_link', 'stories_link', 'post_link']
df = pd.DataFrame(data_rows, columns=columns)

# Display the DataFrame
print(df.head())

import streamlit as st
from backend import helper
st.write(df)


num_messages, words, num_media_messages, num_links = helper.fetch_stats("Overall", df)
st.title("Top Statistics")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.header("Total Messages")
    st.metric(" ", num_messages)
with col2:
    st.header("Total Words")
    st.metric(" ", words)
with col3:
    st.header("Media Shared")
    st.metric(" ", num_media_messages)
with col4:
    st.header("Links Shared")
    st.metric(" ", num_links)

# helper.create_wordcloud("Overall",df)
helper.most_busy_users(df)

st.title('Most Busy Users')
x, new_df = helper.most_busy_users(df)
# fig, ax = plt.subplots()

# Create a bar plot using Plotly Express
fig = px.bar(x=x.index, y=x.values, labels={'x': 'User', 'y': 'Count'})
fig.update_layout(title="Most Busy Users")
fig.update_xaxes(title_text='User', tickangle=-45)
fig.update_yaxes(title_text='Count')
st.plotly_chart(fig)

st.dataframe(new_df)

st.title("Wordcloud")

# df_wc = helper.create_wordcloud(selected_user, df)
# fig, ax = plt.subplots()
# ax.imshow(df_wc)
# plt.axis("off")
# st.pyplot(fig)
#
# wordcloud_fig = helper.create_plotly_wordcloud("Overall", df)
# st.plotly_chart(wordcloud_fig)

