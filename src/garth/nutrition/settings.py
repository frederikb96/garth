from __future__ import annotations

from datetime import date

from pydantic.dataclasses import dataclass

from garth import http
from garth.nutrition._types import MacroGoals
from garth.utils import camel_to_snake_dict, format_end_date


@dataclass
class NutritionSettings:
    weight_change_type: str | None = None
    target_date: str | None = None
    weight_change_rate: int | None = None
    active_daily_calories: int | None = None
    user_defined_active_calories: bool | None = None
    calorie_goal: int | None = None
    macro_goals: MacroGoals | None = None
    auto_calorie_adjustment: bool | None = None
    region_code: str | None = None
    language_code: str | None = None
    daily_timeline_start_time: str | None = None
    daily_timeline_end_time: str | None = None
    starting_weight: int | None = None
    target_weight_goal: int | None = None
    effective_date: str | None = None
    nutrition_status: str | None = None

    @staticmethod
    def get(
        day: date | str | None = None,
        *,
        client: http.Client | None = None,
    ) -> NutritionSettings:
        import garth

        client = client or garth.client
        end = format_end_date(day)
        data = client.connectapi(f"/nutrition-service/settings/{end}")
        assert isinstance(data, dict)
        return NutritionSettings(**camel_to_snake_dict(data))
