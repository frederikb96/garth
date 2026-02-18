from garth.nutrition import CustomFood, CustomFoodItem, CustomFoodList
from garth.utils import camel_to_snake_dict


def test_import_from_top_level():
    from garth import CustomFood as CF

    assert CF is CustomFood


def test_custom_food_item_construction():
    raw = {
        "foodMetaData": {
            "foodName": "My Protein Bar",
            "foodId": "cf1",
            "foodType": "GENERIC",
            "source": "GARMIN",
        },
        "nutritionContents": [
            {
                "servingUnit": "BAR",
                "numberOfUnits": 1.0,
                "calories": 200.0,
                "protein": 20.0,
                "fat": 8.0,
                "carbs": 22.0,
            },
        ],
        "foodImages": [],
        "isFavorite": False,
    }
    item = CustomFoodItem(**camel_to_snake_dict(raw))
    assert item.food_meta_data is not None
    assert item.food_meta_data.food_name == "My Protein Bar"
    assert len(item.nutrition_contents) == 1
    assert item.nutrition_contents[0].protein == 20.0


def test_custom_food_list_construction():
    item = CustomFoodItem(
        food_meta_data=None,
        nutrition_contents=[],
        food_images=[],
        is_favorite=False,
    )
    result = CustomFoodList(items=[item], more_data_available=True)
    assert len(result.items) == 1
    assert result.more_data_available is True


def test_custom_food_list_defaults():
    result = CustomFoodList()
    assert result.items == []
    assert result.more_data_available is False


def test_has_methods():
    assert hasattr(CustomFood, "list")
    assert hasattr(CustomFood, "create")
    assert hasattr(CustomFood, "update")
    assert hasattr(CustomFood, "delete")
    assert callable(CustomFood.list)
    assert callable(CustomFood.create)
    assert callable(CustomFood.update)
    assert callable(CustomFood.delete)
