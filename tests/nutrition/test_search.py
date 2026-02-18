from garth.nutrition import (
    FoodSearch,
    RecentFoods,
    SearchResult,
    SearchResults,
)
from garth.utils import camel_to_snake_dict


def test_import_from_top_level():
    from garth import FoodSearch as FS

    assert FS is FoodSearch


def test_search_result_construction():
    raw = {
        "foodMetaData": {
            "foodName": "Banana",
            "foodId": "ban1",
            "source": "GARMIN",
        },
        "nutritionContents": [
            {
                "servingUnit": "MEDIUM",
                "calories": 105.0,
            },
        ],
        "foodImages": [],
        "isRecent": True,
        "isFavorite": False,
        "type": "FOOD",
    }
    result = SearchResult(**camel_to_snake_dict(raw))
    assert result.food_meta_data is not None
    assert result.food_meta_data.food_name == "Banana"
    assert len(result.nutrition_contents) == 1
    assert result.nutrition_contents[0].calories == 105.0
    assert result.is_recent is True


def test_search_results_construction():
    raw = {
        "results": [
            {
                "foodMetaData": {
                    "foodName": "Apple",
                    "foodId": "a1",
                },
                "nutritionContents": [],
                "foodImages": [],
            },
        ],
        "moreDataAvailable": True,
    }
    results = SearchResults(**camel_to_snake_dict(raw))
    assert len(results.results) == 1
    assert results.more_data_available is True


def test_recent_foods_construction():
    raw = {
        "frequentFoods": [],
        "recentFoods": [
            {
                "foodMetaData": {
                    "foodName": "Toast",
                    "foodId": "t1",
                },
                "nutritionContents": [],
                "foodImages": [],
            },
        ],
    }
    recent = RecentFoods(**camel_to_snake_dict(raw))
    assert len(recent.recent_foods) == 1
    assert recent.recent_foods[0].food_meta_data is not None
    assert recent.recent_foods[0].food_meta_data.food_name == "Toast"


def test_has_search_methods():
    assert hasattr(FoodSearch, "search")
    assert hasattr(FoodSearch, "autocomplete")
    assert hasattr(FoodSearch, "recent")
    assert callable(FoodSearch.search)
    assert callable(FoodSearch.autocomplete)
    assert callable(FoodSearch.recent)
