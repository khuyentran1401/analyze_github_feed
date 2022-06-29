import json
from datetime import timedelta
from typing import List

import pandas as pd
from helper import load_config
from omegaconf import DictConfig
from prefect import flow, task
from prefect.tasks import task_input_hash
from pydash import py_


@task
def get_data(config: DictConfig):
    with open(config.data.raw, "r") as file:
        data = json.load(file)
    return data


@task(cache_key_fn=task_input_hash, cache_expiration=timedelta(days=1))
def filter_language(data: List[dict], language: str):
    """Only return repositories that are written in the specified language"""
    language = language.title()
    return py_(data).filter({"language": language}).value()


@task(cache_key_fn=task_input_hash, cache_expiration=timedelta(days=1))
def get_relevant_info(data: List[dict], config: DictConfig):
    """Get only the information that we care about in each repo"""
    infos = {}
    for info in config.relevant_info:
        value = py_(data).map(info).value()
        infos[info] = value
    return infos


@task
def create_dataframe_from_dict(data: dict):
    return pd.DataFrame(data)


@task
def remove_duplicates(data: pd.DataFrame, config: DictConfig):
    """Remove the duplicates of a repository"""
    subset = list(config.relevant_info)
    subset.remove("topics")
    return data.drop_duplicates(subset=subset).reset_index(drop=True)


@task
def save_to_pickle(data: pd.DataFrame, config: DictConfig):
    data.to_pickle(config.data.processed)


@flow
def process_data(language: str = "Python"):
    config = load_config()
    data = get_data(config)
    python_repos = filter_language(data, language)
    infos = get_relevant_info(python_repos, config)
    df = create_dataframe_from_dict(infos)
    unique_df = remove_duplicates(df, config)
    save_to_pickle(unique_df, config)


if __name__ == "__main__":
    process_data()
