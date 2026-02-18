from garth.nutrition import FavoriteFood, FavoriteFoodList, FavoriteFoods
from garth.utils import camel_to_snake_dict


def test_import_from_top_level():
    from garth import FavoriteFoods as FF

    assert FF is FavoriteFoods


def test_favorite_food_construction():
    raw = {
        "foodMetaData": {
            "foodName": "Oatmeal",
            "foodId": "oat1",
            "source": "GARMIN",
        },
        "nutritionContents": [
            {
                "servingUnit": "CUP",
                "calories": 150.0,
            },
        ],
        "foodImages": [],
        "isFavorite": True,
    }
    fav = FavoriteFood(**camel_to_snake_dict(raw))
    assert fav.food_meta_data is not None
    assert fav.food_meta_data.food_name == "Oatmeal"
    assert fav.is_favorite is True


def test_favorite_food_list_construction():
    fav = FavoriteFood(
        food_meta_data=None,
        nutrition_contents=[],
        food_images=[],
        is_favorite=True,
    )
    result = FavoriteFoodList(items=[fav], has_more=True)
    assert len(result.items) == 1
    assert result.has_more is True


def test_favorite_food_list_defaults():
    result = FavoriteFoodList()
    assert result.items == []
    assert result.has_more is False


def test_has_methods():
    assert hasattr(FavoriteFoods, "list")
    assert hasattr(FavoriteFoods, "add")
    assert hasattr(FavoriteFoods, "remove")
    assert callable(FavoriteFoods.list)
    assert callable(FavoriteFoods.add)
    assert callable(FavoriteFoods.remove)
