import json
from datetime import timedelta
from re import L
from typing import List

import pandas as pd
from omegaconf import DictConfig
from prefect import flow, task
from prefect.tasks import task_input_hash
from pydash import py_

from helper import load_config


@task
def get_data(config: DictConfig):
    with open(config.data.raw, "r") as file:
        data = json.load(file)
    return data


@task(cache_key_fn=task_input_hash, cache_expiration=timedelta(days=1))
def get_python_repos(data: List[dict]):
    return py_(data).filter({"language": "Python"}).value()


@task(cache_key_fn=task_input_hash, cache_expiration=timedelta(days=1))
def get_relevant_info(data: List[dict], config: DictConfig):
    infos = {}
    for info in config.relevant_info:
        value = py_(data).map(info).value()
        infos[info] = value
    return infos


@task
def create_dataframe_from_dict(data: dict):
    return pd.DataFrame(data)


@task
def save_data(data: pd.DataFrame, config: DictConfig):
    data.to_pickle(config.data.processed)


@flow
def process_data():
    config = load_config()
    data = get_data(config)
    python_repos = get_python_repos(data)
    infos = get_relevant_info(python_repos, config)
    df = create_dataframe_from_dict(infos)
    save_data(df, config)


if __name__ == "__main__":
    process_data()
