from collections import Counter

import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import streamlit as st
from hydra import compose, initialize
from omegaconf import DictConfig
from pydash import py_
from wordcloud import WordCloud


def load_config():
    with initialize(version_base=None, config_path="../config"):
        config = compose(config_name="main")
    return config


def load_data(config: DictConfig):
    data = pd.read_pickle(config.data.processed)
    return data.sort_values(by="stargazers_count", ascending=False)


def make_link_clickable(link: str):
    text = link.split("=")[0]
    return f'<a target="_blank" href="{link}">{text}</a>'


def format_topics(topics: list):
    topics.sort()
    return ", ".join(topics)


def format_table(df: pd.DataFrame):
    data = df.copy()
    data["html_url"] = data["html_url"].apply(make_link_clickable)
    data["topics"] = data["topics"].apply(format_topics)
    return data


def get_all_topics(data: pd.DataFrame):
    """Get unique tags from all repositories"""
    nested_topics = list(data["topics"].values)
    return py_.flatten(nested_topics)


def get_top_10_topics(topics: list):
    """Get the topics with the highest count"""
    count = Counter(topics)
    data = (
        pd.DataFrame(list(count.items()), columns=["name", "count"])
        .sort_values(by="count", ascending=False)
        .reset_index(drop=True)
    )
    return data[:10]


def make_wordcloud(topics: list):

    text = " ".join(topics)

    wordcloud = WordCloud(
        width=800,
        height=800,
        min_font_size=10,
        background_color="black",
        colormap="Set2",
        collocations=False,
    ).generate(text)

    fig = plt.figure(figsize=(8, 8), facecolor=None)
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.tight_layout(pad=0)
    return fig


def create_app():
    st.set_page_config(
        page_title="Python Repositories", page_icon=":shinto_shrine:"
    )
    config = load_config()
    data = load_data(config)

    st.title("Python Repositories")
    st.header("All Repositories")
    formatted_df = format_table(data)
    st.write(formatted_df.to_html(escape=False), unsafe_allow_html=True)

    st.header("Top 10 most popular repositories")
    star_plot = px.bar(data[:10], x="full_name", y="stargazers_count")
    st.plotly_chart(star_plot)

    st.header("Top 10 most popular topics")
    topics = get_all_topics(data)
    count_df = get_top_10_topics(topics)
    populary_plot = px.bar(count_df, x="name", y="count")
    st.plotly_chart(populary_plot)

    st.header("Wordcloud of topics")
    wordcloud = make_wordcloud(topics)
    st.pyplot(wordcloud)


if __name__ == "__main__":
    create_app()
