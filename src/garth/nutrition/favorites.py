from __future__ import annotations

from dataclasses import field

from pydantic.dataclasses import dataclass

from garth import http
from garth.nutrition._types import FoodMetaData, NutritionContent
from garth.utils import camel_to_snake_dict


@dataclass
class FavoriteFood:
    food_meta_data: FoodMetaData | None = None
    nutrition_contents: list[NutritionContent] = field(default_factory=list)
    food_images: list[dict] = field(default_factory=list)
    is_favorite: bool | None = None


class FavoriteFoods:
    @staticmethod
    def list(
        query: str = "",
        start: int = 0,
        limit: int = 50,
        *,
        client: http.Client | None = None,
    ) -> list[FavoriteFood]:
        import garth

        client = client or garth.client
        params: dict[str, str | int] = {
            "searchExpression": query,
            "start": start,
            "limit": limit,
            "includeContent": "true",
        }
        data = client.connectapi("/nutrition-service/favorite", params=params)
        assert isinstance(data, dict)
        return [
            FavoriteFood(**camel_to_snake_dict(c))
            for c in data.get("consumables", [])
        ]

    @staticmethod
    def add(
        food_id: str,
        serving_id: str,
        source: str,
        serving_qty: float = 1,
        region_code: str | None = None,
        language_code: str | None = None,
        *,
        client: http.Client | None = None,
    ) -> None:
        import garth
        from garth.nutrition.food_log import _resolve_locale

        client = client or garth.client
        r_region, r_lang = _resolve_locale(
            region_code, language_code, None, client
        )
        body: dict = {
            "foodId": food_id,
            "servingId": serving_id,
            "source": source,
            "servingQty": serving_qty,
        }
        if r_region is not None:
            body["regionCode"] = r_region
        if r_lang is not None:
            body["languageCode"] = r_lang
        client.put(
            "connectapi",
            "/nutrition-service/favorite/food",
            api=True,
            json=body,
        )

    @staticmethod
    def remove(
        food_id: str,
        *,
        client: http.Client | None = None,
    ) -> None:
        import garth

        client = client or garth.client
        client.delete(
            "connectapi",
            f"/nutrition-service/favorite/food/{food_id}",
            api=True,
        )
