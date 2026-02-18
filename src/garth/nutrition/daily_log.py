from __future__ import annotations

from dataclasses import field
from datetime import date

from pydantic.dataclasses import dataclass

from garth import http
from garth.nutrition._types import (
    DailyNutritionSummary,
    MacroGoals,
    MealDetail,
)
from garth.utils import camel_to_snake_dict, format_end_date


@dataclass
class DailyNutritionLog:
    meal_date: str | None = None
    day_start_time: str | None = None
    day_end_time: str | None = None
    daily_nutrition_goals: MacroGoals | None = None
    daily_nutrition_content: DailyNutritionSummary | None = None
    meal_details: list[MealDetail] = field(default_factory=list)
    logged_foods_with_serving_sizes: list[dict] = field(default_factory=list)

    @staticmethod
    def get(
        day: date | str | None = None,
        *,
        client: http.Client | None = None,
    ) -> DailyNutritionLog:
        import garth

        client = client or garth.client
        end = format_end_date(day)
        data = client.connectapi(f"/nutrition-service/food/logs/{end}")
        assert isinstance(data, dict)
        return DailyNutritionLog(**camel_to_snake_dict(data))
