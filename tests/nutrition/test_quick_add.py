from unittest.mock import MagicMock, patch

from garth.nutrition import QuickAdd


def test_import_from_top_level():
    from garth import QuickAdd as QA

    assert QA is QuickAdd


def test_has_methods():
    assert hasattr(QuickAdd, "add")
    assert hasattr(QuickAdd, "update")
    assert callable(QuickAdd.add)
    assert callable(QuickAdd.update)


@patch("garth.nutrition.quick_add._resolve_meal_time", return_value="12:00:00")
def test_add_payload_sends_numeric_values(_mock_time):
    mock_client = MagicMock()
    mock_client.connectapi.return_value = {
        "date": "2026-02-19",
        "mealDetails": [],
    }
    QuickAdd.add(
        day="2026-02-19",
        meal_id=1,
        name="Test",
        calories=383.7,
        protein=20.5,
        fat=10.3,
        carbs=50.9,
        client=mock_client,
    )
    body = mock_client.connectapi.call_args.kwargs["json"]
    item = body["quickAddItems"][0]
    assert isinstance(item["calories"], int)
    assert isinstance(item["protein"], int)
    assert isinstance(item["fat"], int)
    assert isinstance(item["carbs"], int)
    assert item["calories"] == 383
    assert item["protein"] == 20
