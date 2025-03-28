import allure
import requests

from data.handle import Urls, Handle
from data.users_data import User


@allure.suite("Авторизация")
class TestLogin:

    @allure.description("Авторизация существующего пользователя с корректными данными")
    @allure.title("Успешная авторизация пользователя")
    def test_login_the_user(self, create_user):
        """Тест на успешный вход с корректными учетными данными"""

        user_data = {"email": create_user[1]["email"], "password": create_user[1]["password"]}

        response = requests.post(f'{Urls.MAIN_URL}{Handle.LOGIN}', json=user_data)

        assert response.status_code == 200, (
            f"Expected 200, got {response.status_code}, response: {response.text}"
        )
        assert response.json().get("success") is True, "Login was not successful"

    @allure.description("Попытка входа с неверными учетными данными")
    @allure.title("Ошибка авторизации при неверном логине и пароле")
    def test_login_the_user_with_error(self):
        """Тест на авторизацию с неверными учетными данными"""

        user_data = {"email": User().create_user_data()["email"], "password": "incorrectPassword"}

        response = requests.post(f'{Urls.MAIN_URL}{Handle.LOGIN}', json=user_data)

        assert response.status_code == 401, (
            f"Expected 401, got {response.status_code}, response: {response.text}"
        )
        assert response.json().get("success") is False, "Login should have failed but succeeded"
