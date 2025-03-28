import pytest
import allure
import requests

from data.handle import Urls, Handle
from data.users_data import User


@allure.suite("Создание пользователя")
class TestCreateUser:

    @allure.description("Создание нового пользователя")
    @allure.title("Создание нового пользователя")
    def test_create_new_user_positive(self):
        response = requests.post(f'{Urls.MAIN_URL}{Handle.CREATE_USER}', json=User.create_user_data())
        assert response.status_code == 200 and response.json()["success"] is True

    @allure.description("При создании существующего пользователя показывает предупреждение")
    @allure.title("Создание существующего пользователя")
    def test_create_full_user_error(self):
        user_data = User.create_user_data()
        requests.post(f'{Urls.MAIN_URL}{Handle.CREATE_USER}', json=user_data)
        response = requests.post(f'{Urls.MAIN_URL}{Handle.CREATE_USER}', json=user_data)
        assert response.status_code == 403 and 'User already exists' in response.text

    @allure.description("При создании пользователя с некорректными данными показывает предупреждение")
    @allure.title("Создание пользователя с некорректными данными или без обязательных полей")
    @pytest.mark.parametrize("user_data, expected_message", [
        ({"email": "", "password": User.fake.password(), "name": User.fake.name()},
         "Email, password and name are required fields"),
        ({"email": User.fake.email(), "password": "", "name": User.fake.name()},
         "Email, password and name are required fields"),
        ({"email": User.fake.email(), "password": User.fake.password(), "name": ""},
         "Email, password and name are required fields"),
    ])
    def test_create_user_with_incorrect_data(self, user_data, expected_message):
        response = requests.post(f'{Urls.MAIN_URL}{Handle.CREATE_USER}', json=user_data)
        assert response.status_code == 403 and expected_message in response.text
