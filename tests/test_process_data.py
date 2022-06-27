import pandas as pd
from omegaconf import OmegaConf
from pandas.testing import assert_frame_equal

from development.process_data import (create_dataframe_from_dict,
                                      get_python_repos, get_relevant_info)


def test_get_python_repos():
    data = [
        {"language": "Python", "url": "abc"},
        {"language": "Go", "url": "abc"},
        {"language": "Javascript", "url": "abc"},
    ]
    res = get_python_repos.fn(data, language="Python")
    assert res == [{"language": "Python", "url": "abc"}]


def test_get_relevant_info():
    config = OmegaConf.create({"relevant_info": ["html_url", "description"]})
    data = [
        {"html_url": "abc", "description": "abc"},
        {"html_url": "bcd", "description": "bcd"},
    ]
    res = get_relevant_info.fn(data, config)
    expected = {"html_url": ["abc", "bcd"], "description": ["abc", "bcd"]}
    assert res == expected


def test_create_dataframe_from_dict():
    data = {"html_url": ["abc", "bcd"], "description": ["abc", "bcd"]}
    res = create_dataframe_from_dict.fn(data)
    expected = pd.DataFrame(
        {"html_url": ["abc", "bcd"], "description": ["abc", "bcd"]}
    )
    assert_frame_equal(res, expected)
