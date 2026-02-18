from garth.nutrition import NutritionStatus
from garth.utils import camel_to_snake_dict


def test_import_from_top_level():
    from garth import NutritionStatus as NS

    assert NS is NutritionStatus


def test_construction_from_api_dict():
    raw = {
        "currentStatus": "NUTRITION_ENABLED",
        "hasUsedNutrition": True,
        "hasUsedMfp": False,
    }
    status = NutritionStatus(**camel_to_snake_dict(raw))
    assert status.current_status == "NUTRITION_ENABLED"
    assert status.has_used_nutrition is True
    assert status.has_used_mfp is False


def test_has_get_method():
    assert hasattr(NutritionStatus, "get")
    assert callable(NutritionStatus.get)
