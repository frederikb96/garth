from garth.nutrition import FoodLog


def test_import_from_top_level():
    from garth import FoodLog as FL

    assert FL is FoodLog


def test_has_methods():
    assert hasattr(FoodLog, "add")
    assert hasattr(FoodLog, "update")
    assert hasattr(FoodLog, "move")
    assert hasattr(FoodLog, "copy")
    assert hasattr(FoodLog, "remove")
    assert callable(FoodLog.add)
    assert callable(FoodLog.update)
    assert callable(FoodLog.move)
    assert callable(FoodLog.copy)
    assert callable(FoodLog.remove)
