from unittest.mock import MagicMock, patch

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


@patch("garth.nutrition.food_log._resolve_locale", return_value=("US", "en"))
def test_create_payload_sends_numeric_values(_mock_locale):
    mock_client = MagicMock()
    mock_client.connectapi.return_value = {
        "foodMetaData": {"foodName": "Test", "foodId": "123"},
        "nutritionContents": [{"calories": 200.0}],
        "foodImages": [],
        "isFavorite": False,
    }
    CustomFood.create(
        food_name="Test",
        serving_unit="g",
        number_of_units=100.0,
        calories=200.0,
        protein=10.5,
        fat=5.0,
        carbs=30.0,
        client=mock_client,
    )
    body = mock_client.connectapi.call_args.kwargs["json"]
    nutrition = body["nutritionContents"][0]
    assert isinstance(nutrition["numberOfUnits"], float)
    assert isinstance(nutrition["calories"], float)
    assert isinstance(nutrition["protein"], float)
    assert isinstance(nutrition["fat"], float)
    assert isinstance(nutrition["carbs"], float)
    assert nutrition["fiber"] is None
