from behave import when, then


@when('I import the package thecoin')
def import_package(context):
    """Try to import the package. If an exception happened push to context."""
    context.exceptions = []
    try:
        import thecoin  # noqa
    except ImportError as excpt:
        context.exceptions = [excpt]


@then('I see no errors')
def no_exceptions_in_context(context):
    """Check that no previous exceptions have been captured."""
    assert not context.exceptions
