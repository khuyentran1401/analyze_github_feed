from collections import Counter

import pandas as pd
from pydash import py_


def get_all_topics(data: pd.DataFrame):
    """Get unique tags from all repositories"""
    nested_topics = list(data["topics"].values)
    return py_.flatten(nested_topics)


def filter_based_on_topics(topics: list, data: pd.DataFrame):
    """Only show the specified topics"""
    exploded = data.explode("topics")
    filtered = exploded[exploded.topics.isin(topics)]
    return (
        filtered.groupby(["full_name", "html_url", "description"])["topics"]
        .apply(list)
        .reset_index(drop=False)
    )


def get_top_10_topics(topics: list):
    """Get the topics with the highest count"""
    count = Counter(topics)
    data = (
        pd.DataFrame(list(count.items()), columns=["name", "count"])
        .sort_values(by="count", ascending=False)
        .reset_index(drop=True)
    )
    return data[:10]
