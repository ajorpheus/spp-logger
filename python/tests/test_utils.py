from cawdrey import frozendict

from spp_logger import context_to_dict, dict_to_context


def test_context_to_dict():
    context = frozendict({
        "correlation_id":"test-correlation-id",
        "log_level":"INFO",
    })
    assert context_to_dict(context) == {
        "correlation_id": "test-correlation-id",
        "log_level": "INFO",
    }


def test_dict_to_context():
    context_dict = {"correlation_id": "test-correlation-id", "log_level": "INFO"}
    assert dict_to_context(context_dict) == frozendict({
        "correlation_id":"test-correlation-id",
        "log_level":"INFO",
   } )


def test_dict_to_context_empty():
    context_dict = {}
    assert dict_to_context(context_dict) is None


def test_dict_to_context_none():
    context_dict = None
    assert dict_to_context(context_dict) is None
