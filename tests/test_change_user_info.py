import allure
import requests

from data.handle import Urls, Handle
from data.users_data import User


@allure.suite('Изменение данных пользователя')
class TestChangeUserData:

    @allure.description("Изменение email-адреса авторизованного пользователя")
    @allure.title("Успешное изменение email-адреса авторизованного пользователя")
    def test_change_auth_user_email(self, create_user):
        payload = {"email": User.create_user_data()["email"]}
        headers = {"Authorization": create_user[3], **Handle.headers}
        r = requests.patch(f"{Urls.MAIN_URL}{Handle.CHANGE_USER_DATA}", headers=headers, json=payload)

        assert r.status_code == 200, f"Expected 200, got {r.status_code}"
        assert r.json().get("user", {}).get("email") == payload["email"], "Email was not updated"

    @allure.description("Изменение пароля авторизованного пользователя")
    @allure.title("Успешное изменение пароля авторизованного пользователя")
    def test_change_auth_user_password(self, create_user):
        payload = {"password": User.create_user_data()["password"]}
        headers = {"Authorization": create_user[3], **Handle.headers}
        r = requests.patch(f"{Urls.MAIN_URL}{Handle.CHANGE_USER_DATA}", headers=headers, json=payload)

        assert r.status_code == 200, f"Expected 200, got {r.status_code}"
        assert r.json().get("success") is True, "Password change was not successful"

    @allure.description("Изменение имени авторизованного пользователя")
    @allure.title("Успешное изменение имени авторизованного пользователя")
    def test_change_auth_user_name(self, create_user):
        payload = {"name": User.create_user_data()["name"]}
        headers = {"Authorization": create_user[3], **Handle.headers}
        r = requests.patch(f"{Urls.MAIN_URL}{Handle.CHANGE_USER_DATA}", headers=headers, json=payload)

        assert r.status_code == 200, f"Expected 200, got {r.status_code}"
        assert r.json().get("user", {}).get("name") == payload["name"], "Name was not updated"

    @allure.description("Изменение данных пользователя без авторизации")
    @allure.title("Изменение данных пользователя без авторизации")
    def test_change_not_auth_user_data(self):
        r = requests.patch(f"{Urls.MAIN_URL}{Handle.CHANGE_USER_DATA}", json=User.create_user_data())

        assert r.status_code == 401, f"Expected 401, got {r.status_code}"
        assert r.json().get("message") == "You should be authorised", "Incorrect error message for unauthorized user"
