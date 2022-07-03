import pandas as pd
import streamlit as st
from Visualize import format_table, get_all_topics, load_config, load_data


def get_unique_topic_selection(topics: list):
    return list(set(topics))


def filter_based_on_topics(topics: list, data: pd.DataFrame):
    """Only show the specified topics"""
    exploded = data.explode("topics")
    filtered = exploded[exploded.topics.isin(topics)]
    return (
        filtered.groupby(["full_name", "html_url", "description"])["topics"]
        .apply(list)
        .reset_index(drop=False)
    )


def create_ui(data: pd.DataFrame, topics: list):
    st.title("Topics")

    st.header("Get repositories based on topics")
    chosen_topics = st.multiselect("Topic", options=topics)
    filtered_df = filter_based_on_topics(chosen_topics, data)
    clickable_df = format_table(filtered_df)
    st.write(clickable_df.to_html(escape=False), unsafe_allow_html=True)


def create_app():
    st.set_page_config(
        page_title="Topics", page_icon=":vertical_traffic_light:"
    )
    config = load_config()
    data = load_data(config)
    topics = get_all_topics(data)
    unique_topics = get_unique_topic_selection(topics)
    create_ui(data, unique_topics)


if __name__ == "__main__":
    create_app()
