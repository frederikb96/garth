from __future__ import annotations

from dataclasses import field

from pydantic.dataclasses import dataclass

from garth import http
from garth.nutrition._types import FoodMetaData, NutritionContent
from garth.utils import camel_to_snake_dict


@dataclass
class CustomFoodItem:
    food_meta_data: FoodMetaData | None = None
    nutrition_contents: list[NutritionContent] = field(default_factory=list)
    food_images: list[dict] = field(default_factory=list)
    is_favorite: bool | None = None


class CustomFood:
    @staticmethod
    def list(
        query: str = "",
        start: int = 0,
        limit: int = 20,
        *,
        client: http.Client | None = None,
    ) -> list[CustomFoodItem]:
        import garth

        client = client or garth.client
        params: dict[str, str | int] = {
            "searchExpression": query,
            "start": start,
            "limit": limit,
            "includeContent": "true",
        }
        data = client.connectapi(
            "/nutrition-service/customFood", params=params
        )
        assert isinstance(data, dict)
        return [
            CustomFoodItem(**camel_to_snake_dict(c))
            for c in data.get("customFoods", [])
        ]

    @staticmethod
    def create(
        food_name: str,
        serving_unit: str,
        number_of_units: float,
        calories: float,
        protein: float | None = None,
        fat: float | None = None,
        carbs: float | None = None,
        brand_name: str | None = None,
        food_type: str = "GENERIC",
        region_code: str | None = None,
        language_code: str | None = None,
        *,
        client: http.Client | None = None,
    ) -> CustomFoodItem:
        return CustomFood._put(
            food_id=None,
            serving_id=None,
            food_name=food_name,
            serving_unit=serving_unit,
            number_of_units=number_of_units,
            calories=calories,
            protein=protein,
            fat=fat,
            carbs=carbs,
            brand_name=brand_name,
            food_type=food_type,
            region_code=region_code,
            language_code=language_code,
            client=client,
        )

    @staticmethod
    def update(
        food_id: str,
        serving_id: str,
        food_name: str,
        serving_unit: str,
        number_of_units: float,
        calories: float,
        protein: float | None = None,
        fat: float | None = None,
        carbs: float | None = None,
        brand_name: str | None = None,
        food_type: str = "GENERIC",
        region_code: str | None = None,
        language_code: str | None = None,
        *,
        client: http.Client | None = None,
    ) -> CustomFoodItem:
        return CustomFood._put(
            food_id=food_id,
            serving_id=serving_id,
            food_name=food_name,
            serving_unit=serving_unit,
            number_of_units=number_of_units,
            calories=calories,
            protein=protein,
            fat=fat,
            carbs=carbs,
            brand_name=brand_name,
            food_type=food_type,
            region_code=region_code,
            language_code=language_code,
            client=client,
        )

    @staticmethod
    def delete(
        food_id: str,
        *,
        client: http.Client | None = None,
    ) -> None:
        import garth

        client = client or garth.client
        client.delete(
            "connectapi",
            f"/nutrition-service/customFood/{food_id}",
            api=True,
        )

    @staticmethod
    def _put(
        *,
        food_id: str | None,
        serving_id: str | None,
        food_name: str,
        serving_unit: str,
        number_of_units: float,
        calories: float,
        protein: float | None,
        fat: float | None,
        carbs: float | None,
        brand_name: str | None,
        food_type: str,
        region_code: str | None,
        language_code: str | None,
        client: http.Client | None,
    ) -> CustomFoodItem:
        import garth
        from garth.nutrition.food_log import _resolve_locale

        client = client or garth.client
        r_region, r_lang = _resolve_locale(
            region_code, language_code, None, client
        )
        nutrition: dict = {
            "servingId": serving_id,
            "servingUnit": serving_unit.upper(),
            "numberOfUnits": str(number_of_units),
            "calories": str(calories),
        }
        if protein is not None:
            nutrition["protein"] = str(protein)
        if fat is not None:
            nutrition["fat"] = str(fat)
        if carbs is not None:
            nutrition["carbs"] = str(carbs)
        meta: dict = {
            "foodId": food_id,
            "foodName": food_name,
            "foodType": food_type,
            "brandName": brand_name,
            "source": "GARMIN",
            "imageUuid": None,
        }
        if r_region is not None:
            meta["regionCode"] = r_region
        if r_lang is not None:
            meta["languageCode"] = r_lang
        body = {
            "foodMetaData": meta,
            "nutritionContents": [nutrition],
        }
        data = client.connectapi(
            "/nutrition-service/customFood", method="PUT", json=body
        )
        assert isinstance(data, dict)
        return CustomFoodItem(**camel_to_snake_dict(data))
