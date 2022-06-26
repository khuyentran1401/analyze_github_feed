import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import streamlit as st
from hydra import compose, initialize
from omegaconf import DictConfig
from process_data import get_top_10_topics
from pydash import py_
from wordcloud import WordCloud


def load_config():
    with initialize(version_base=None, config_path="../config"):
        config = compose(config_name="main")
    return config


def load_data(config: DictConfig):
    data = pd.read_pickle(config.data.processed)
    return data.sort_values(by="stargazers_count", ascending=False)


def get_all_topics(data: pd.DataFrame):
    nested_topics = list(data["topics"].values)
    return py_.flatten(nested_topics)


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
    st.dataframe(data)

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
