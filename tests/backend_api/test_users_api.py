from utils.data_generation import get_user
from utils.assertions import assert_status_code, assert_field_in_response
import logging
import pytest
LOGGER = logging.getLogger(__name__)


def test_user_crud(api_client):
    """
    Test CRUD operations on user
    :param api_client:
    :return:
    """
    endpoint = "/users/"
    # Create user
    LOGGER.info("Create new user")
    user = get_user()
    user_created = api_client.post(endpoint="/users", data=user)
    assert_status_code(user_created, 201)
    assert_field_in_response(user_created, "email", value=user["email"])
    LOGGER.info(f"Successfully create new user {user_created.json()}")

    # Read user
    LOGGER.info("Read an existing user")
    read_user = api_client.get(f"{endpoint}{user_created.json()['id']}")
    assert_status_code(read_user, 200)
    assert_field_in_response(read_user, "id", value=user_created.json()["id"])
    LOGGER.info(f"Successfully read an user: {read_user.json()}")

    # Update user
    new_name = "Peter Parkar"
    LOGGER.info("Update name of an existing user")
    update_user = api_client.put(f"{endpoint}{user_created.json()['id']}", {"name": new_name})
    assert_status_code(update_user, 200)
    assert_field_in_response(update_user, "name", value=new_name)
    LOGGER.info(f"Successfully updated name of an existing user: {update_user.json()}")

    # Delete user
    LOGGER.info("Delete the newly created user")
    delete_user = api_client.delete(f"{endpoint}{user_created.json()['id']}")
    assert_status_code(delete_user, 200)

    # Check is user was deleted
    check_user = api_client.get(f"{endpoint}{user_created.json()['id']}")
    assert_status_code(check_user, 404)
    assert_field_in_response(check_user, "error", value="User not found")
    LOGGER.info("Deleted the newly created user")


def test_create_user_missing_email(api_client):
    """
    Validate that missing email will reject the creation of new user
    :param api_client:
    :return:
    """
    user = {"name": "Test", "accountType": "basic"}
    resp = api_client.post("/users", user)
    assert_status_code(resp, 400)
    assert_field_in_response(resp, "error")


def test_create_user_invalid_email(api_client):
    """
    Invalid email will not create
    :param api_client:
    :return:
    """
    user = {"name": "Test", "email": "invalid-email", "accountType": "basic"}
    resp = api_client.post("/users", user)
    assert_status_code(resp, 400)


def test_create_user_invalid_account_type(api_client):
    """
    Invalid email will not create
    :param api_client:
    :return:
    """
    user = {"name": "Test", "email": "test@example.com", "accountType": "ultra"}
    resp = api_client.post("/users", user, {"Authorization": "Bearer testtoken"})
    assert_status_code(resp, 400)


def test_request_without_auth(api_client):
    """
    Test Auth with Missing token
    :param api_client:
    :return:
    """
    LOGGER.info("Create new user")
    user = get_user()
    user_created = api_client.post(endpoint="/users", data=user)
    assert_status_code(user_created, 201)

    # Read user
    LOGGER.info("Read an existing user with clear token")
    try:
        original_headers = api_client.headers
        api_client.headers = {} # clear token
        read_user = api_client.get(f"/users/{user_created.json()['id']}", headers=api_client.headers)
        assert_status_code(read_user, 401)
    finally:
        # reset the header before exiting
        api_client.headers = original_headers


def test_request_with_invalid_token(api_client):
    """
    Test Auth with Invalid token
    :param api_client:
    :return:
    """
    LOGGER.info("Create new user")
    # api_client.headers = {"Authorization": "Bearer testtoken"}
    user = get_user()
    user_created = api_client.post(endpoint="/users", data=user)
    assert_status_code(user_created, 201)

    # Read user
    LOGGER.info("Read an existing user with clear token")
    try:
        original_headers = api_client.headers
        api_client.headers = {"Authorization": "Bearer wrongtoken"}  # clear token
        read_user = api_client.get(f"/users/{user_created.json()['id']}", headers=api_client.headers)
        assert_status_code(read_user, 401)
    finally:
        # reset the header before exiting
        api_client.headers = original_headers