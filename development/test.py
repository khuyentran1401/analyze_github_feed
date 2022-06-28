import json
import os
from datetime import timedelta

import requests
from dotenv import load_dotenv
from helper import load_config
from omegaconf import DictConfig
from pydash import py_


def get_authentication():
    load_dotenv()
    username = os.getenv("username")
    token = os.getenv("token")
    return {"username": username, "token": token}

def get_data_from_api(auth: dict):

    response = requests.get(
        f"https://api.github.com/users/{auth['username']}/received_events/public?per_page=100",
        auth=(auth["username"], auth["token"]),
    )
    data = response.json()
    return data


def get_starred_repo_urls(data: list):
    return py_(data).filter({"type": "WatchEvent"}).map("repo.url").value()


def get_info_all_repo(auth: dict, repo_urls: list):
    data = []
    for url in repo_urls:
        response = requests.get(
            url,
            auth=(auth["username"], auth["token"]),
        )
        data.append(response.json())
    return data


def save_data(data: dict, config: DictConfig):
    with open(config.data.raw, "w") as file:
        json.dump(data, file)


def get_data():
    config = load_config()
    auth = get_authentication()
    data = get_data_from_api(auth)
    urls = get_starred_repo_urls(data)
    info = get_info_all_repo(auth, urls)
    save_data(info, config)


if __name__ == "__main__":
    get_data()
