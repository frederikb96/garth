from __future__ import annotations

from datetime import date, datetime, timezone
from typing import Any

from garth import http
from garth.nutrition.daily_log import DailyNutritionLog
from garth.utils import camel_to_snake_dict, format_end_date


def _now_iso() -> str:
    now = datetime.now(timezone.utc)
    return (
        now.strftime("%Y-%m-%dT%H:%M:%S.") + f"{now.microsecond // 1000:03d}Z"
    )


def _resolve_meal_time(
    meal_time: str | None,
    meal_id: int,
    day: date,
    client: http.Client,
) -> str:
    if meal_time is not None:
        return meal_time
    from garth.nutrition.meals import MealDefinitions

    meals = MealDefinitions.get(day, client=client)
    for meal in meals:
        if meal.meal_id == meal_id and meal.start_time:
            return meal.start_time
    return "12:00:00"


def _resolve_locale(
    region_code: str | None,
    language_code: str | None,
    day: date | str | None,
    client: http.Client,
) -> tuple[str | None, str | None]:
    if region_code is not None and language_code is not None:
        return region_code, language_code
    from garth.nutrition.settings import NutritionSettings

    settings = NutritionSettings.get(day, client=client)
    return (
        region_code or settings.region_code,
        language_code or settings.language_code,
    )


def _food_log_item(
    *,
    log_id: str | None,
    action: str,
    meal_id: int,
    food_id: str,
    serving_id: str,
    source: str,
    serving_qty: float,
    meal_time: str,
    region_code: str | None,
    language_code: str | None,
) -> dict[str, Any]:
    item: dict[str, Any] = {
        "logId": log_id,
        "logTimestamp": _now_iso(),
        "logSource": "GCW",
        "logCategory": "REGULAR_LOG",
        "mealTime": meal_time,
        "action": action,
        "mealId": meal_id,
        "foodId": food_id,
        "servingId": serving_id,
        "source": source,
        "servingQty": serving_qty,
        "customMealId": None,
    }
    if region_code is not None:
        item["regionCode"] = region_code
    if language_code is not None:
        item["languageCode"] = language_code
    return item


class FoodLog:
    @staticmethod
    def add(
        day: date | str,
        meal_id: int,
        food_id: str,
        serving_id: str,
        source: str,
        serving_qty: float = 1,
        region_code: str | None = None,
        language_code: str | None = None,
        meal_time: str | None = None,
        *,
        client: http.Client | None = None,
    ) -> DailyNutritionLog:
        import garth

        client = client or garth.client
        end = format_end_date(day)
        resolved_time = _resolve_meal_time(meal_time, meal_id, end, client)
        r_region, r_lang = _resolve_locale(
            region_code, language_code, end, client
        )
        body = {
            "mealDate": str(end),
            "foodLogItems": [
                _food_log_item(
                    log_id=None,
                    action="ADD",
                    meal_id=meal_id,
                    food_id=food_id,
                    serving_id=serving_id,
                    source=source,
                    serving_qty=serving_qty,
                    meal_time=resolved_time,
                    region_code=r_region,
                    language_code=r_lang,
                ),
            ],
        }
        data = client.connectapi(
            "/nutrition-service/food/logs", method="PUT", json=body
        )
        assert isinstance(data, dict)
        return DailyNutritionLog(**camel_to_snake_dict(data))

    @staticmethod
    def update(
        day: date | str,
        log_id: str,
        meal_id: int,
        food_id: str,
        serving_id: str,
        source: str,
        serving_qty: float = 1,
        region_code: str | None = None,
        language_code: str | None = None,
        meal_time: str | None = None,
        *,
        client: http.Client | None = None,
    ) -> DailyNutritionLog:
        import garth

        client = client or garth.client
        end = format_end_date(day)
        resolved_time = _resolve_meal_time(meal_time, meal_id, end, client)
        r_region, r_lang = _resolve_locale(
            region_code, language_code, end, client
        )
        body = {
            "mealDate": str(end),
            "foodLogItems": [
                _food_log_item(
                    log_id=log_id,
                    action="UPDATE",
                    meal_id=meal_id,
                    food_id=food_id,
                    serving_id=serving_id,
                    source=source,
                    serving_qty=serving_qty,
                    meal_time=resolved_time,
                    region_code=r_region,
                    language_code=r_lang,
                ),
            ],
        }
        data = client.connectapi(
            "/nutrition-service/food/logs", method="PUT", json=body
        )
        assert isinstance(data, dict)
        return DailyNutritionLog(**camel_to_snake_dict(data))

    @staticmethod
    def move(
        from_date: date | str,
        to_date: date | str,
        log_id: str,
        meal_time: str,
        *,
        client: http.Client | None = None,
    ) -> None:
        import garth

        client = client or garth.client
        from_d = format_end_date(from_date)
        to_d = format_end_date(to_date)
        body: dict[str, Any] = {
            "action": "MOVE",
            "foodLogItems": [
                {
                    "logId": log_id,
                    "logTimestamp": _now_iso(),
                    "logSource": "GCW",
                    "logCategory": "REGULAR_LOG",
                    "mealTime": meal_time,
                },
            ],
            "from": str(from_d),
            "to": [str(to_d)],
        }
        client.connectapi(
            "/nutrition-service/food/logs/bulk", method="PUT", json=body
        )

    @staticmethod
    def copy(
        from_date: date | str,
        to_dates: date | str | list[date | str],
        log_id: str,
        meal_time: str,
        *,
        client: http.Client | None = None,
    ) -> None:
        import garth

        client = client or garth.client
        from_d = format_end_date(from_date)
        if not isinstance(to_dates, list):
            to_dates = [to_dates]
        to_strs = [str(format_end_date(d)) for d in to_dates]
        body: dict[str, Any] = {
            "action": "COPY",
            "foodLogItems": [
                {
                    "logId": log_id,
                    "logTimestamp": _now_iso(),
                    "logSource": "GCW",
                    "logCategory": "REGULAR_LOG",
                    "mealTime": meal_time,
                },
            ],
            "from": str(from_d),
            "to": to_strs,
        }
        client.connectapi(
            "/nutrition-service/food/logs/bulk", method="PUT", json=body
        )

    @staticmethod
    def remove(
        day: date | str,
        log_ids: list[str],
        *,
        client: http.Client | None = None,
    ) -> None:
        import garth

        client = client or garth.client
        end = format_end_date(day)
        body = {"logIds": log_ids}
        client.delete(
            "connectapi",
            f"/nutrition-service/food/logs/{end}",
            api=True,
            json=body,
        )
