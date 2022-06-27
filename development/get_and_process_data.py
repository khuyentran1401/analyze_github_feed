from get_data import get_data
from prefect import flow
from process_data import process_data


@flow
def get_and_process_data(language: str = "Python"):
    get_data()
    process_data(language=language)


if __name__ == "__main__":
    get_and_process_data()
