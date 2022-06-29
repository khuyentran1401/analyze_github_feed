import json
import os
from datetime import timedelta

import requests
from dotenv import load_dotenv
from helper import load_config
from omegaconf import DictConfig
from prefect import flow, task
from prefect.tasks import task_input_hash
from pydash import py_


@task
def get_authentication():
    load_dotenv()
    username = os.getenv("username")
    token = os.getenv("token")
    return {"username": username, "token": token}


@task(
    cache_key_fn=task_input_hash,
    cache_expiration=timedelta(days=1),
    retries=3,
    retry_delay_seconds=60,
)
def get_general_info_of_repos(auth: dict):

    response = requests.get(
        f"https://api.github.com/users/{auth['username']}/received_events/public?per_page=100",
        auth=(auth["username"], auth["token"]),
    )
    data = response.json()
    return data


@task(cache_key_fn=task_input_hash, cache_expiration=timedelta(days=1))
def get_starred_repo_urls(data: list):
    return py_(data).filter({"type": "WatchEvent"}).map("repo.url").value()


@task(
    cache_key_fn=task_input_hash,
    cache_expiration=timedelta(days=1),
    retries=3,
    retry_delay_seconds=60,
)
def get_specific_info_of_repos(auth: dict, repo_urls: list):
    data = []
    for url in repo_urls:
        response = requests.get(
            url,
            auth=(auth["username"], auth["token"]),
        )
        data.append(response.json())
    return data


@task
def save_data(data: dict, config: DictConfig):
    with open(config.data.raw, "w") as file:
        json.dump(data, file)


@flow
def get_data():
    config = load_config()
    auth = get_authentication()
    data = get_general_info_of_repos(auth)
    urls = get_starred_repo_urls(data)
    info = get_specific_info_of_repos(auth, urls)
    save_data(info, config)


if __name__ == "__main__":
    get_data()
