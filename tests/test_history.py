from web.history import search, filter_history, sort_history

def test_search_history():
    history = [
        {"source": "Cat Facts API", "content": "Cats sleep 16 hours", "timestamp": 1},
        {"source": "Dog API", "content": "Dog image", "timestamp": 2},
    ]
    result = search(history, "sleep")
    assert len(result) == 1
    assert "Cats" in result[0]["content"]

def test_filter_history():
    history = [
        {"source": "Cat Facts API", "content": "Cats sleep", "timestamp": 1},
        {"source": "Dog API", "content": "Dog image", "timestamp": 2},
    ]
    result = filter_history(history, source="Dog API")
    assert len(result) == 1
    assert result[0]["source"] == "Dog API"

def test_sort_history():
    history = [
        {"source": "Cat Facts API", "content": "Cats sleep", "timestamp": 2},
        {"source": "Dog API", "content": "Dog image", "timestamp": 1},
    ]
    result = sort_history(history, ascending=True)
    assert result[0]["timestamp"] == 1
