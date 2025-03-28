import pytest
import allure
import requests

from data.handle import Urls, Handle
from data.users_data import User


@allure.suite("Создание пользователя")
class TestCreateUser:

    @allure.description("Создание нового пользователя")
    @allure.title("Создание нового пользователя")
    def test_create_new_user_positive(self, create_user):
        response, user_payload, login_data, token = create_user

        assert response.status_code == 200, (
            f"Expected 200, got {response.status_code}, response: {response.text}"
        )
        assert response.json().get("success") is True, (
            f"User creation failed, response: {response.text}"
        )

    @allure.description("Попытка создать уже существующего пользователя")
    @allure.title("Создание существующего пользователя должно выдавать ошибку")
    def test_create_existing_user_error(self):
        user_data = User.create_user_data()
        headers = {**Handle.headers}

        requests.post(f'{Urls.MAIN_URL}{Handle.CREATE_USER}', headers=headers, json=user_data)

        response = requests.post(f'{Urls.MAIN_URL}{Handle.CREATE_USER}', headers=headers, json=user_data)

        assert response.status_code == 403, f"Expected 403 (but API should return 409), got {response.status_code}, response: {response.text}"
        assert 'User already exists' in response.text, f"Unexpected error message, response: {response.text}"

    @allure.description("Попытка создать пользователя без обязательных полей")
    @allure.title("Ошибка при создании пользователя с неполными данными")
    @pytest.mark.parametrize("user_data, expected_message", [
        ({"email": "", "password": "password", "name": "Username"}, "Email, password and name are required fields"),
        ({"email": "test@example.com", "password": "", "name": "Username"},
         "Email, password and name are required fields"),
        ({"email": "test@example.com", "password": "password", "name": ""},
         "Email, password and name are required fields"),
    ])
    def test_create_user_with_missing_fields(self, user_data, expected_message):
        headers = {**Handle.headers}

        response = requests.post(f'{Urls.MAIN_URL}{Handle.CREATE_USER}', headers=headers, json=user_data)

        assert response.status_code == 403, f"Expected 403 (but API should return 400), got {response.status_code}, response: {response.text}"
        assert expected_message in response.text, f"Unexpected error message, response: {response.text}"
