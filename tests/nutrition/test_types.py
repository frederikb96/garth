from garth.nutrition import (
    DailyNutritionSummary,
    FoodMetaData,
    LoggedFood,
    MacroGoals,
    Meal,
    MealDetail,
    NutritionContent,
)
from garth.utils import camel_to_snake_dict


def test_food_meta_data():
    raw = {
        "foodName": "Apple",
        "foodId": "abc123",
        "foodType": "GENERIC",
        "brandName": None,
        "source": "GARMIN",
        "regionCode": "US",
        "languageCode": "en",
    }
    meta = FoodMetaData(**camel_to_snake_dict(raw))
    assert meta.food_name == "Apple"
    assert meta.food_id == "abc123"
    assert meta.food_type == "GENERIC"
    assert meta.source == "GARMIN"


def test_nutrition_content():
    raw = {
        "servingId": "s1",
        "servingUnit": "CUP",
        "numberOfUnits": 1.0,
        "calories": 95.0,
        "carbs": 25.0,
        "protein": 0.5,
        "fat": 0.3,
        "fiber": 4.4,
    }
    content = NutritionContent(**camel_to_snake_dict(raw))
    assert content.serving_unit == "CUP"
    assert content.calories == 95.0
    assert content.fiber == 4.4


def test_macro_goals():
    raw = {
        "calories": 2000.0,
        "adjustedCalories": 2200.0,
        "carbs": 250.0,
        "fat": 65.0,
        "protein": 150.0,
    }
    goals = MacroGoals(**camel_to_snake_dict(raw))
    assert goals.calories == 2000.0
    assert goals.adjusted_calories == 2200.0


def test_meal():
    raw = {
        "mealId": 1,
        "mealName": "Breakfast",
        "displayOrder": 0,
        "startTime": "06:00:00",
        "endTime": "10:00:00",
    }
    meal = Meal(**camel_to_snake_dict(raw))
    assert meal.meal_id == 1
    assert meal.meal_name == "Breakfast"
    assert meal.display_order == 0


def test_logged_food():
    raw = {
        "id": "log1",
        "logId": "log1",
        "logTimestamp": "2025-01-01T12:00:00.000Z",
        "logSource": "GCW",
        "logCategory": "REGULAR_LOG",
        "servingQty": 1.5,
        "foodMetaData": {
            "foodName": "Banana",
            "foodId": "ban1",
        },
        "selectedNutritionContent": {
            "calories": 105.0,
            "carbs": 27.0,
        },
        "nutritionContents": [],
        "foodImages": [],
        "isFavorite": False,
    }
    food = LoggedFood(**camel_to_snake_dict(raw))
    assert food.log_id == "log1"
    assert food.serving_qty == 1.5
    assert food.food_meta_data is not None
    assert food.food_meta_data.food_name == "Banana"
    assert food.selected_nutrition_content is not None
    assert food.selected_nutrition_content.calories == 105.0


def test_meal_detail():
    raw = {
        "meal": {
            "mealId": 2,
            "mealName": "Lunch",
            "displayOrder": 1,
        },
        "mealNutritionContent": {
            "calories": 500.0,
        },
        "loggedFoods": [],
    }
    detail = MealDetail(**camel_to_snake_dict(raw))
    assert detail.meal.meal_id == 2
    assert detail.meal_nutrition_content is not None
    assert detail.meal_nutrition_content.calories == 500.0


def test_daily_nutrition_summary():
    raw = {
        "calories": 1800.0,
        "carbs": 200.0,
        "fat": 60.0,
        "protein": 120.0,
        "caloriesPercentage": 90.0,
    }
    summary = DailyNutritionSummary(**camel_to_snake_dict(raw))
    assert summary.calories == 1800.0
    assert summary.calories_percentage == 90.0
