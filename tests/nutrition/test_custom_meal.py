from garth.nutrition import CustomMeal, CustomMealItem
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


def test_has_methods():
    assert hasattr(CustomMeal, "list")
    assert hasattr(CustomMeal, "create")
    assert hasattr(CustomMeal, "update")
    assert hasattr(CustomMeal, "delete")
    assert callable(CustomMeal.list)
    assert callable(CustomMeal.create)
    assert callable(CustomMeal.update)
    assert callable(CustomMeal.delete)
