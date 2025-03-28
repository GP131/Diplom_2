import allure
import requests

from data.handle import Urls, Handle
from data.ingredient import Ingredient


@allure.suite("Получение заказов пользователя")
class TestGetOrderUser:

    @allure.description("Получение списка заказов авторизованного пользователя")
    @allure.title("Успешное получение заказов с авторизацией")
    def test_get_order_user_with_auth(self, create_user):
        """Тест на получение списка заказов авторизованным пользователем"""

        token = create_user[3]  # now guaranteed "Bearer <token>"
        headers = {"Authorization": token, **Handle.headers}

        auth_check_response = requests.get(f"{Urls.MAIN_URL}{Handle.CHANGE_USER_DATA}", headers=headers)
        assert auth_check_response.status_code == 200, (
            f"Auth token test failed: Expected 200, got {auth_check_response.status_code}, response: {auth_check_response.text}"
        )

        create_order_response = requests.post(
            f"{Urls.MAIN_URL}{Handle.MAKE_ORDER}",
            headers=headers,
            json=Ingredient.correct_ingredients()
        )
        assert create_order_response.status_code == 200, (
            f"Expected 200, got {create_order_response.status_code}, response: {create_order_response.text}"
        )

        response = requests.get(f"{Urls.MAIN_URL}{Handle.GET_ORDERS}", headers=headers)
        assert response.status_code == 200, (
            f"Expected 200, got {response.status_code}, response: {response.text}"
        )
        assert "orders" in response.json(), "Response does not contain orders."

    @allure.description("Попытка получить заказы без авторизации")
    @allure.title("Ошибка при получении заказов без авторизации")
    def test_get_order_user_not_auth(self):
        """Тест на получение списка заказов без авторизации"""

        response = requests.get(f"{Urls.MAIN_URL}{Handle.GET_ORDERS}")

        assert response.status_code == 401, (
            f"Expected 401, got {response.status_code}, response: {response.text}"
        )
        assert response.json().get("message") == "You should be authorised", "Incorrect error message."
