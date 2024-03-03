import json
import re

import pandas as pd
from datetime import datetime

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

#
# # Initialize lists to store data
# data_rows = []
#
# # Iterate through messages
# for message in json_data['messages']:
#     # Convert timestamp to datetime object
#     timestamp_ms = message['timestamp_ms'] / 1000
#     date = datetime.utcfromtimestamp(timestamp_ms).strftime('%Y-%m-%d %H:%M:%S')
#     date_only = datetime.utcfromtimestamp(timestamp_ms).strftime('%Y-%m-%d')
#     year = datetime.utcfromtimestamp(timestamp_ms).strftime('%Y')
#     month = datetime.utcfromtimestamp(timestamp_ms).strftime('%B')
#     month_num = datetime.utcfromtimestamp(timestamp_ms).strftime('%m')
#     day = datetime.utcfromtimestamp(timestamp_ms).strftime('%d')
#     day_name = datetime.utcfromtimestamp(timestamp_ms).strftime('%A')
#     hour = datetime.utcfromtimestamp(timestamp_ms).strftime('%H')
#     minute = datetime.utcfromtimestamp(timestamp_ms).strftime('%M')
#
#     # Get message content or set it to an empty string if not present
#     message_content = message.get('content', '').encode("Latin1").decode("UTF-8")
#
#     # Determine message type
#     if 'share' in message:
#         message_type = 'attachment'
#     elif 'reactions' in message:
#         message_type = 'reaction'
#     else:
#         message_type = 'text'
#
#     # Initialize lists to store links
#     reel_links = []
#     stories_links = []
#     post_links = []
#
#     # Iterate over each message in the JSON data
#     for message in json_data['messages']:
#         if 'share' in message:
#             link = message['share']['link']
#             # Check the type of link and append it to the appropriate list
#             if link.startswith('https://www.instagram.com/reel/'):
#                 reel_links.append(link)
#                 stories_links.append(None)  # Append None for other columns to maintain alignment
#                 post_links.append(None)
#             elif link.startswith('https://www.instagram.com/stories/'):
#                 reel_links.append(None)
#                 stories_links.append(link)
#                 post_links.append(None)
#             elif link.startswith('https://www.instagram.com/p/'):
#                 reel_links.append(None)
#                 stories_links.append(None)
#                 post_links.append(link)
#             else:
#                 reel_links.append(None)
#                 stories_links.append(None)
#                 post_links.append(None)
#         else:
#             reel_links.append(None)
#             stories_links.append(None)
#             post_links.append(None)
#
#
#
#     # Count reactions
#     reactions_count = len(message.get('reactions', []))
#
#     # Calculate word count and average word length
#     words = message_content.split()
#     word_count = len(words)
#     if word_count > 0:
#         avg_word_length = sum(len(word) for word in words) / word_count
#     else:
#         avg_word_length = 0
#
#     # Extract hashtags, mentions, and URLs
#     hashtags = extract_hashtags(message_content)
#     mentions = extract_mentions(message_content)
#     urls = extract_urls(message_content)
#
#     # Categorize media type
#     media_type = categorize_media_type(message)
#
#     # Append data row to list
#     data_rows.append(
#         [date, date_only, year, month, month_num, day, day_name, hour, minute, message['sender_name'].encode("Latin1").decode("UTF-8"), message_content,
#          len(message_content), message_type, reactions_count, word_count, avg_word_length, hashtags, mentions,
#          media_type, urls , reel_links,stories_links,post_links ])
#
# # Create DataFrame
# columns = ['date', 'date_only', 'year', 'month', 'month_num', 'day', 'day_name', 'hour', 'minute', 'user', 'message',
#            'message_length', 'message_type', 'reactions_count', 'word_count', 'avg_word_length', 'hashtags', 'mentions',
#            'media_type', 'urls','reel_link', 'stories_link', 'post_link']
# df = pd.DataFrame(data_rows, columns=columns)


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
st.write(df)


