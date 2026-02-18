from __future__ import annotations

import builtins
from dataclasses import field
from typing import Any

from pydantic.dataclasses import dataclass

from garth import http
from garth.nutrition._types import FoodMetaData, NutritionContent
from garth.utils import camel_to_snake_dict


@dataclass
class CustomMealItem:
    food_meta_data: FoodMetaData | None = None
    nutrition_contents: list[NutritionContent] = field(default_factory=list)
    food_images: list[dict] = field(default_factory=list)
    is_favorite: bool | None = None


def _enrich_foods_locale(
    foods: builtins.list[dict[str, Any]],
    client: http.Client,
) -> builtins.list[dict[str, Any]]:
    from garth.nutrition.food_log import _resolve_locale

    r_region, r_lang = _resolve_locale(None, None, None, client)
    enriched = []
    for food in foods:
        food = dict(food)
        if r_region and not food.get("regionCode"):
            food["regionCode"] = r_region
        if r_lang and not food.get("languageCode"):
            food["languageCode"] = r_lang
        enriched.append(food)
    return enriched


class CustomMeal:
    @staticmethod
    def list(
        query: str = "",
        start: int = 0,
        limit: int = 20,
        *,
        client: http.Client | None = None,
    ) -> list[CustomMealItem]:
        import garth

        client = client or garth.client
        params: dict[str, str | int] = {
            "searchExpression": query,
            "start": start,
            "limit": limit,
            "includeContent": "true",
        }
        data = client.connectapi(
            "/nutrition-service/customMeal", params=params
        )
        assert isinstance(data, dict)
        return [
            CustomMealItem(**camel_to_snake_dict(c))
            for c in data.get("customMeals", [])
        ]

    @staticmethod
    def create(
        name: str,
        foods: builtins.list[dict[str, Any]],
        *,
        client: http.Client | None = None,
    ) -> dict[str, Any]:
        import garth

        client = client or garth.client
        enriched = _enrich_foods_locale(foods, client)
        body = {
            "customMeals": [
                {
                    "customMealId": None,
                    "name": name,
                    "isFavorite": False,
                    "status": 0,
                    "foods": enriched,
                    "type": "MEAL",
                    "imageUuid": None,
                },
            ],
        }
        data = client.connectapi(
            "/nutrition-service/customMeal", method="PUT", json=body
        )
        assert isinstance(data, dict)
        return data

    @staticmethod
    def update(
        custom_meal_id: int | str,
        name: str,
        foods: builtins.list[dict[str, Any]],
        *,
        client: http.Client | None = None,
    ) -> dict[str, Any]:
        import garth

        client = client or garth.client
        enriched = _enrich_foods_locale(foods, client)
        body = {
            "customMeals": [
                {
                    "customMealId": str(custom_meal_id),
                    "name": name,
                    "isFavorite": False,
                    "status": 0,
                    "foods": enriched,
                    "type": "MEAL",
                    "imageUuid": None,
                },
            ],
        }
        data = client.connectapi(
            "/nutrition-service/customMeal", method="PUT", json=body
        )
        assert isinstance(data, dict)
        return data

    @staticmethod
    def delete(
        custom_meal_id: int | str,
        *,
        client: http.Client | None = None,
    ) -> None:
        import garth

        client = client or garth.client
        client.delete(
            "connectapi",
            f"/nutrition-service/customMeal/{custom_meal_id}",
            api=True,
        )
