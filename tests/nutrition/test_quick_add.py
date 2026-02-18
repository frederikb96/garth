from garth.nutrition import QuickAdd


def test_import_from_top_level():
    from garth import QuickAdd as QA

    assert QA is QuickAdd


def test_has_methods():
    assert hasattr(QuickAdd, "add")
    assert hasattr(QuickAdd, "update")
    assert callable(QuickAdd.add)
    assert callable(QuickAdd.update)
