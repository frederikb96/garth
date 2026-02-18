from garth.nutrition import DailyNutritionLog
from garth.utils import camel_to_snake_dict


def test_import_from_top_level():
    from garth import DailyNutritionLog as DNL

    assert DNL is DailyNutritionLog


def test_construction_from_api_dict():
    raw = {
        "mealDate": "2025-01-15",
        "dayStartTime": "06:00:00",
        "dayEndTime": "22:00:00",
        "dailyNutritionGoals": {
            "calories": 2000.0,
            "carbs": 250.0,
            "fat": 65.0,
            "protein": 150.0,
        },
        "dailyNutritionContent": {
            "calories": 1500.0,
            "carbs": 180.0,
            "fat": 50.0,
            "protein": 110.0,
        },
        "mealDetails": [
            {
                "meal": {
                    "mealId": 0,
                    "mealName": "Breakfast",
                    "displayOrder": 0,
                },
                "loggedFoods": [],
            },
        ],
        "loggedFoodsWithServingSizes": [],
    }
    log = DailyNutritionLog(**camel_to_snake_dict(raw))
    assert log.meal_date == "2025-01-15"
    assert log.daily_nutrition_goals is not None
    assert log.daily_nutrition_goals.calories == 2000.0
    assert log.daily_nutrition_content is not None
    assert log.daily_nutrition_content.calories == 1500.0
    assert len(log.meal_details) == 1
    assert log.meal_details[0].meal.meal_name == "Breakfast"


def test_has_get_method():
    assert hasattr(DailyNutritionLog, "get")
    assert callable(DailyNutritionLog.get)
