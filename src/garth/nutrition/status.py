from __future__ import annotations

from pydantic.dataclasses import dataclass

from garth import http
from garth.utils import camel_to_snake_dict


@dataclass
class NutritionStatus:
    current_status: str
    has_used_nutrition: bool
    has_used_mfp: bool

    @staticmethod
    def get(*, client: http.Client | None = None) -> NutritionStatus:
        import garth

        client = client or garth.client
        data = client.connectapi(
            "/nutrition-service/user/nutritionCurrentStatus"
        )
        assert isinstance(data, dict)
        return NutritionStatus(**camel_to_snake_dict(data))
