from __future__ import annotations

from dataclasses import field
from datetime import date

from pydantic.dataclasses import dataclass

from garth import http
from garth.nutrition._types import FoodMetaData, NutritionContent
from garth.utils import camel_to_snake_dict, format_end_date


@dataclass
class SearchResult:
    food_meta_data: FoodMetaData | None = None
    nutrition_contents: list[NutritionContent] = field(default_factory=list)
    food_images: list[dict] = field(default_factory=list)
    is_recent: bool | None = None
    is_favorite: bool | None = None
    type: str | None = None


@dataclass
class SearchResults:
    results: list[SearchResult] = field(default_factory=list)
    more_data_available: bool = False


@dataclass
class RecentFoods:
    frequent_foods: list[SearchResult] = field(default_factory=list)
    recent_foods: list[SearchResult] = field(default_factory=list)


class FoodSearch:
    @staticmethod
    def search(
        query: str,
        start: int = 0,
        limit: int = 50,
        region_code: str | None = None,
        language_code: str | None = None,
        *,
        client: http.Client | None = None,
    ) -> SearchResults:
        import garth

        client = client or garth.client
        params: dict[str, str | int] = {
            "searchExpression": query,
            "start": start,
            "limit": limit,
        }
        if region_code is not None:
            params["regionCode"] = region_code
        if language_code is not None:
            params["languageCode"] = language_code
        data = client.connectapi(
            "/nutrition-service/food/search", params=params
        )
        assert isinstance(data, dict)
        return SearchResults(**camel_to_snake_dict(data))

    @staticmethod
    def autocomplete(
        query: str,
        region_code: str | None = None,
        language_code: str | None = None,
        *,
        client: http.Client | None = None,
    ) -> list[str]:
        import garth

        client = client or garth.client
        params: dict[str, str] = {"searchExpression": query}
        if region_code is not None:
            params["regionCode"] = region_code
        if language_code is not None:
            params["languageCode"] = language_code
        data = client.connectapi(
            "/nutrition-service/food/search/autocomplete", params=params
        )
        assert isinstance(data, dict)
        return data.get("suggestions", [])

    @staticmethod
    def recent(
        meal_id: int,
        day: date | str | None = None,
        start: int = 0,
        limit: int = 50,
        *,
        client: http.Client | None = None,
    ) -> RecentFoods:
        import garth

        client = client or garth.client
        end = format_end_date(day)
        params: dict[str, str | int] = {
            "mealId": meal_id,
            "start": start,
            "limit": limit,
            "includeContent": "true",
            "allowOverlap": "false",
        }
        data = client.connectapi(
            f"/nutrition-service/food/recent/{end}", params=params
        )
        assert isinstance(data, dict)
        return RecentFoods(**camel_to_snake_dict(data))
