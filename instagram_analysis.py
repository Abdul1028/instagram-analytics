import streamlit as st
from backend import helper

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


helper.most_busy_users(df)
helper.create_wordcloud()