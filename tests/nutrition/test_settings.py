from garth.nutrition import NutritionSettings
from garth.utils import camel_to_snake_dict


def test_import_from_top_level():
    from garth import NutritionSettings as NS

    assert NS is NutritionSettings


def test_construction_from_api_dict():
    raw = {
        "weightChangeType": "MAINTAIN",
        "activeDailyCalories": 2200,
        "userDefinedActiveCalories": False,
        "calorieGoal": 2000,
        "macroGoals": {
            "calories": 2000.0,
            "carbs": 250.0,
            "fat": 65.0,
            "protein": 150.0,
        },
        "autoCalorieAdjustment": True,
        "regionCode": "US",
        "languageCode": "en",
        "dailyTimelineStartTime": "06:00:00",
        "dailyTimelineEndTime": "22:00:00",
        "nutritionStatus": "NUTRITION_ENABLED",
    }
    settings = NutritionSettings(**camel_to_snake_dict(raw))
    assert settings.weight_change_type == "MAINTAIN"
    assert settings.calorie_goal == 2000
    assert settings.macro_goals is not None
    assert settings.macro_goals.calories == 2000.0
    assert settings.region_code == "US"
    assert settings.auto_calorie_adjustment is True


def test_has_get_method():
    assert hasattr(NutritionSettings, "get")
    assert callable(NutritionSettings.get)
