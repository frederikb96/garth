from __future__ import annotations

from datetime import date

from garth import http
from garth.nutrition._types import Meal
from garth.utils import camel_to_snake_dict, format_end_date


class MealDefinitions:
    @staticmethod
    def get(
        day: date | str | None = None,
        *,
        client: http.Client | None = None,
    ) -> list[Meal]:
        import garth

        client = client or garth.client
        end = format_end_date(day)
        data = client.connectapi(f"/nutrition-service/meals/{end}")
        assert isinstance(data, dict)
        return [Meal(**camel_to_snake_dict(m)) for m in data["meals"]]
