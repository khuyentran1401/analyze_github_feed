import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from hydra import compose, initialize
from matplotlib.figure import Figure
from omegaconf import DictConfig
from pydash import py_
from wordcloud import WordCloud


def load_config():
    with initialize(version_base=None, config_path="../config"):
        config = compose(config_name="main")
    return config


def load_data(config: DictConfig):
    return pd.read_pickle(config.data.processed)


def turn_topics_to_text(data: pd.DataFrame):
    nested_topics = list(data["topics"].values)
    flattened_topics = py_.flatten(nested_topics)
    return " ".join(flattened_topics)


def make_wordcloud(text: str):

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

    plt.show()

    return fig


def create_ui(data: pd.DataFrame, wordcloud: Figure):
    st.dataframe(data)
    st.pyplot(wordcloud)


def create_app():
    config = load_config()
    data = load_data(config)
    text_topics = turn_topics_to_text(data)
    wordcloud_plot = make_wordcloud(text_topics)
    create_ui(data, wordcloud_plot)


if __name__ == "__main__":
    create_app()
