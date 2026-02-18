from __future__ import annotations

from dataclasses import field

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
