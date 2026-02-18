from garth.nutrition import Meal, MealDefinitions
from garth.utils import camel_to_snake_dict


def test_import_from_top_level():
    from garth import MealDefinitions as MD

    assert MD is MealDefinitions


def test_meal_construction():
    raw = {
        "mealId": 0,
        "mealName": "Breakfast",
        "displayOrder": 0,
        "startTime": "06:00:00",
        "endTime": "10:00:00",
        "goals": {
            "calories": 500.0,
            "carbs": 60.0,
            "fat": 15.0,
            "protein": 40.0,
        },
    }
    meal = Meal(**camel_to_snake_dict(raw))
    assert meal.meal_id == 0
    assert meal.meal_name == "Breakfast"
    assert meal.goals is not None
    assert meal.goals.calories == 500.0


def test_has_get_method():
    assert hasattr(MealDefinitions, "get")
    assert callable(MealDefinitions.get)
