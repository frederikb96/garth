from __future__ import annotations

from datetime import date

from garth import http
from garth.nutrition._utils import _now_iso
from garth.nutrition.daily_log import DailyNutritionLog
from garth.nutrition.food_log import _resolve_meal_time
from garth.utils import camel_to_snake_dict, format_end_date


class QuickAdd:
    @staticmethod
    def add(
        day: date | str,
        meal_id: int,
        name: str,
        calories: float,
        protein: float = 0,
        fat: float = 0,
        carbs: float = 0,
        meal_time: str | None = None,
        *,
        client: http.Client | None = None,
    ) -> DailyNutritionLog:
        import garth

        client = client or garth.client
        end = format_end_date(day)
        resolved_time = _resolve_meal_time(meal_time, meal_id, end, client)
        body = {
            "mealDate": str(end),
            "quickAddItems": [
                {
                    "name": name,
                    "logId": None,
                    "logTimestamp": _now_iso(),
                    "logSource": "GCW",
                    "logCategory": "QUICK_ADD",
                    "mealTime": resolved_time,
                    "mealId": meal_id,
                    "action": "ADD",
                    "calories": str(int(calories)),
                    "carbs": str(int(carbs)),
                    "protein": str(int(protein)),
                    "fat": str(int(fat)),
                },
            ],
        }
        data = client.connectapi(
            "/nutrition-service/food/logs/quickAdd",
            method="PUT",
            json=body,
        )
        assert isinstance(data, dict)
        return DailyNutritionLog(**camel_to_snake_dict(data))

    @staticmethod
    def update(
        day: date | str,
        log_id: str,
        meal_id: int,
        name: str,
        calories: float,
        protein: float = 0,
        fat: float = 0,
        carbs: float = 0,
        meal_time: str | None = None,
        *,
        client: http.Client | None = None,
    ) -> DailyNutritionLog:
        import garth

        client = client or garth.client
        end = format_end_date(day)
        resolved_time = _resolve_meal_time(meal_time, meal_id, end, client)
        body = {
            "mealDate": str(end),
            "quickAddItems": [
                {
                    "name": name,
                    "logId": log_id,
                    "logTimestamp": _now_iso(),
                    "logSource": "GCW",
                    "logCategory": "QUICK_ADD",
                    "mealTime": resolved_time,
                    "mealId": meal_id,
                    "action": "UPDATE",
                    "calories": str(int(calories)),
                    "carbs": str(int(carbs)),
                    "protein": str(int(protein)),
                    "fat": str(int(fat)),
                },
            ],
        }
        data = client.connectapi(
            "/nutrition-service/food/logs/quickAdd",
            method="PUT",
            json=body,
        )
        assert isinstance(data, dict)
        return DailyNutritionLog(**camel_to_snake_dict(data))
