from src.get_data import get_starred_repo_urls


def test_get_starred_repo_urls():
    data = [
        {"type": "WatchEvent", "repo": {"url": "abc"}},
        {"type": "WatchEvent", "repo": {"url": "bcd"}},
    ]
    out = get_starred_repo_urls.fn(data)
    assert out == ["abc", "bcd"]
