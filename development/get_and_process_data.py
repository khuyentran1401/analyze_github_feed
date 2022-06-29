import argparse

from get_data import get_data
from prefect import flow
from process_data import process_data


@flow
def get_and_process_data(language: str = "Python"):
    get_data()
    process_data(language=language)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Flow arguments")
    parser.add_argument(
        "--language",
        type=str,
        default="Python",
        help="Language of the repositories that will be saved in your machine.",
    )
    args = parser.parse_args()
    get_and_process_data(args.language)
