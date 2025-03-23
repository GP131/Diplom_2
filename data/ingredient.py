import requests
from data.handle import Urls, Handle


class Ingredient:
    @staticmethod
    def get_ingredients():

        response = requests.get(f"{Urls.MAIN_URL}/api/ingredients")
        if response.status_code == 200:
            data = response.json()
            return [ingredient["_id"] for ingredient in data["data"]]
        else:
            raise Exception(f"Failed to fetch ingredients: {response.status_code}, {response.text}")

    @staticmethod
    def correct_ingredients():

        ingredient_ids = Ingredient.get_ingredients()
        return {"ingredients": ingredient_ids[:2]}

    @staticmethod
    def incorrect_ingredients():

        return {"ingredients": ["fake_id_123", "wrong_id_456"]}
