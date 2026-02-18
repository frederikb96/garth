from garth.nutrition import (
    CustomMeal,
    CustomMealDetail,
    CustomMealItem,
    CustomMealList,
)
from garth.utils import camel_to_snake_dict


def test_import_from_top_level():
    from garth import CustomMeal as CM

    assert CM is CustomMeal


def test_custom_meal_item_construction():
    raw = {
        "foodMetaData": {
            "foodName": "My Breakfast Combo",
            "foodId": "cm1",
        },
        "nutritionContents": [
            {
                "calories": 450.0,
                "protein": 30.0,
            },
        ],
        "foodImages": [],
        "isFavorite": False,
    }
    item = CustomMealItem(**camel_to_snake_dict(raw))
    assert item.food_meta_data is not None
    assert item.food_meta_data.food_name == "My Breakfast Combo"


def test_custom_meal_list_construction():
    item = CustomMealItem(
        food_meta_data=None,
        nutrition_contents=[],
        food_images=[],
        is_favorite=False,
    )
    result = CustomMealList(items=[item], has_more=True)
    assert len(result.items) == 1
    assert result.has_more is True


def test_custom_meal_list_defaults():
    result = CustomMealList()
    assert result.items == []
    assert result.has_more is False


def test_custom_meal_detail_construction():
    raw = {
        "customMealId": 123,
        "name": "My Meal",
        "isFavorite": False,
        "status": 1,
        "type": "MEAL",
        "foods": [
            {
                "id": "456",
                "foodMetaData": {
                    "foodId": "f1",
                    "foodName": "Apple",
                    "source": "GARMIN",
                },
                "nutritionContents": [
                    {"calories": 95.0},
                ],
                "foodImages": [],
                "servingQty": 1.0,
                "isFavorite": False,
                "type": "FOOD",
            },
        ],
        "contentSummary": {
            "calories": 95.0,
        },
    }
    detail = CustomMealDetail(**camel_to_snake_dict(raw))
    assert detail.name == "My Meal"
    assert detail.custom_meal_id == 123
    assert len(detail.foods) == 1
    assert detail.foods[0].food_meta_data is not None
    assert detail.foods[0].food_meta_data.food_name == "Apple"
    assert detail.content_summary is not None
    assert detail.content_summary.calories == 95.0


def test_has_methods():
    assert hasattr(CustomMeal, "list")
    assert hasattr(CustomMeal, "create")
    assert hasattr(CustomMeal, "update")
    assert hasattr(CustomMeal, "delete")
    assert callable(CustomMeal.list)
    assert callable(CustomMeal.create)
    assert callable(CustomMeal.update)
    assert callable(CustomMeal.delete)
