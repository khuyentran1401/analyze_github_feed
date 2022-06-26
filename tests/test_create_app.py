import pandas as pd
from pandas.testing import assert_frame_equal

from app.process_data import filter_based_on_topics, get_repo_count


def test_filter_based_on_topics():
    data = pd.DataFrame(
        {
            "full_name": ["a", "b"],
            "html_url": ["a", "b"],
            "topics": [["1", "2", "3"], ["1", "2"]],
        }
    )
    topics = ["1", "2"]
    res = filter_based_on_topics(topics, data)
    expected = pd.DataFrame(
        {
            "full_name": ["a", "b"],
            "html_url": ["a", "b"],
            "topics": [["1", "2"], ["1", "2"]],
        }
    )
    assert_frame_equal(res, expected)


def test_get_repo_count():
    topics = ["a", "a", "b"]
    res = get_repo_count(topics)
    assert_frame_equal(
        res, pd.DataFrame({"name": ["a", "b"], "count": [2, 1]})
    )
