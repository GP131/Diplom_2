import pytest
import requests

from data.handle import Urls, Handle
from data.users_data import User


@pytest.fixture(scope="function")
def create_user():
    """Creates a unique user and ensures proper cleanup after the test."""
    payload = User.create_user_data()
    login_data = payload.copy()
    del login_data["name"]

    response = requests.post(f"{Urls.MAIN_URL}{Handle.CREATE_USER}", json=payload)

    if response.status_code == 403 and "User already exists" in response.text:
        delete_response = requests.post(f"{Urls.MAIN_URL}{Handle.LOGIN}", json=login_data)
        if delete_response.status_code == 200:
            token = delete_response.json().get("accessToken")
            requests.delete(
                f"{Urls.MAIN_URL}{Handle.DELETE_USER}",
                headers={"Authorization": f"Bearer {token}"}
            )
            response = requests.post(f"{Urls.MAIN_URL}{Handle.CREATE_USER}", json=payload)

    token = response.json().get("accessToken")
    yield response, payload, login_data, token

    requests.delete(
        f"{Urls.MAIN_URL}{Handle.DELETE_USER}",
        headers={"Authorization": f"Bearer {token}"}
    )
