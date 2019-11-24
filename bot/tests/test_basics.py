from app import get_admin_ids

def test_get_admin_ids():
    test_data = {
        "": [],
        1: [],
        1.2: [],
        "1": ["1"],
        "1,2": ["1","2"],
        "1,2,,,": ["1", "2"],
        "1,2,,,a,b": ["1","2","a","b"]
    }

    for test, expected in test_data.items():
        assert get_admin_ids(test) == expected