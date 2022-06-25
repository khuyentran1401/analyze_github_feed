import json
import os

import requests
from dotenv import load_dotenv
from omegaconf import DictConfig
from prefect import flow, task

from helper import load_config


@task
def get_data_from_api():
    load_dotenv()
    username = os.getenv("username")
    token = os.getenv("token")
    print(username)

    response = requests.get(
        f"https://api.github.com/users/{username}/received_events/public",
        auth=(username, token),
    )
    data = response.json()
    return data


@task
def save_data(data: dict, config: DictConfig):
    with open(config.data.raw, "w") as file:
        json.dump(data, file)


@flow
def get_data():
    config = load_config()
    data = get_data_from_api()
    save_data(data, config)


if __name__ == "__main__":
    get_data()
