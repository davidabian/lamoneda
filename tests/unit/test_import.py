"""Base library tests."""


def test_import():
    """Test basic import."""
    import importlib
    try:
        importlib.import_module('thecoin')
    except ImportError:
        assert False
