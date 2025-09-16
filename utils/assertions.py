# Custom Assertions
def assert_status_code(resp, expected=200):
    assert resp.status_code == expected, f"Expected {expected}, got {resp.status_code}"


def assert_field_in_response(resp, field, value=None):
    my_json = resp.json()[-1] if isinstance(resp.json(), list) else resp.json()
    assert field in my_json, f"Field '{field}' not found in response"
    if value:
        assert my_json[field] == value


