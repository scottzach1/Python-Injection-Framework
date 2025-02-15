from collections import namedtuple

import pytest
from scottzach1.pif import exceptions, providers


def test_override_standard_shallow():
    """
    Testing basic override logic for providers.
    """
    provide_a = providers.Factory(lambda: "a")
    provide_b = providers.Factory(lambda: "b")
    assert provide_a() == "a"
    assert provide_b() == "b"

    provide_a.override(provide_b)
    assert provide_a() == "b"
    assert provide_b() == "b"

    provide_a.override(None)
    assert provide_a() == "a"
    assert provide_b() == "b"

    provide_b.override(provide_a)
    assert provide_a() == "a"
    assert provide_b() == "a"

    provide_b.override(None)
    assert provide_a() == "a"
    assert provide_b() == "b"


def test_override_contextmanager_shallow():
    """
    Testing basic override logic for providers with contextmanager.
    """
    provide_a = providers.Factory(lambda: "a")
    provide_b = providers.Factory(lambda: "b")

    assert provide_a() == "a"
    assert provide_b() == "b"

    with provide_a.override(provide_b):
        assert provide_a() == "b"
        assert provide_b() == "b"

    assert provide_a() == "a"
    assert provide_b() == "b"

    with provide_b.override(provide_a):
        assert provide_a() == "a"
        assert provide_b() == "a"


def test_override_standard_nested():
    """
    Testing nested override logic for providers.
    """
    provide_a = providers.Factory(lambda: "a")
    provide_b = providers.Factory(lambda: "b")
    provide_c = providers.Factory(lambda: "c")

    assert provide_a() == "a"
    assert provide_b() == "b"
    assert provide_c() == "c"

    provide_a.override(provide_b)
    provide_b.override(provide_c)

    assert provide_a() == "c"
    assert provide_b() == "c"
    assert provide_c() == "c"

    provide_b.override(None)
    assert provide_a() == "b"
    assert provide_b() == "b"
    assert provide_c() == "c"

    provide_a.override(None)
    assert provide_a() == "a"
    assert provide_b() == "b"
    assert provide_c() == "c"


def test_override_contextmanager_nested():
    """
    Testing nested override logic for providers with contextmanager.
    """
    provide_a = providers.Factory(lambda: "a")
    provide_b = providers.Factory(lambda: "b")
    provide_c = providers.Factory(lambda: "c")

    assert provide_a() == "a"
    assert provide_b() == "b"
    assert provide_c() == "c"

    with provide_a.override(provide_b):
        assert provide_a() == "b"
        assert provide_b() == "b"
        assert provide_c() == "c"

        with provide_b.override(provide_c):
            assert provide_a() == "c"
            assert provide_b() == "c"
            assert provide_c() == "c"

        assert provide_a() == "b"
        assert provide_b() == "b"
        assert provide_c() == "c"

    assert provide_a() == "a"
    assert provide_b() == "b"
    assert provide_c() == "c"


def test_blank_provider():
    """
    Checking the blank provider raises a BlankProviderException when it hasn't been overridden.
    """
    provider = providers.Blank()

    with pytest.raises(exceptions.BlankProviderException):
        provider()

    with provider.override_existing("some_value"):
        assert provider() == "some_value"

    with pytest.raises(exceptions.BlankProviderException):
        provider()


def test_existing_singleton():
    """
    Checking the existing singleton provider returns the exact same object.
    """
    obj_1 = object()
    obj_2 = object()

    provider = providers.ExistingSingleton(obj_1)

    assert obj_1 is not obj_2
    assert obj_1 is provider()
    assert obj_1 is provider()

    with provider.override_existing(obj_2):
        assert obj_2 is not obj_1
        assert obj_2 is provider()
        assert obj_2 is provider()

    assert obj_1 is not obj_2
    assert obj_1 is provider()
    assert obj_1 is provider()


def test_singleton():
    """
    Checking the singleton provider creates only once.
    """
    provider = providers.Singleton(dict, a=1, b=2)

    dict_1 = provider()
    dict_2 = provider()

    with provider.override(providers.Singleton(dict, a=1, b=2)):
        dict_alt = provider()

    dict_3 = provider()

    assert dict_1 == {"a": 1, "b": 2}
    assert dict_1 is not {"a": 1, "b": 2}
    assert dict_2 is dict_1
    assert dict_3 is dict_1

    assert dict_1 == dict_alt
    assert dict_1 is not dict_alt


def test_factory():
    """
    Checking the factory provider creates every single time.
    """
    provider = providers.Factory(dict, a=1, b=2)

    dict_1 = provider()
    dict_2 = provider()

    with provider.override(providers.Factory(dict, a=1, b=2)):
        dict_alt = provider()

    dict_3 = provider()

    assert dict_1 == {"a": 1, "b": 2}
    assert dict_1 is not {"a": 1, "b": 2}

    assert dict_2 == dict_1
    assert dict_2 is not dict_1

    assert dict_3 == dict_1
    assert dict_3 is not dict_1

    assert dict_alt == dict_1
    assert dict_alt is not dict_1


def test_transitive_factory_wired():
    """
    Checking the factory provider evaluates Provider args and kwargs.
    """
    model = namedtuple("Model", "a b")

    provider_a = providers.Factory(lambda: "a")
    provider_b = providers.Factory(lambda: "b")

    provider = providers.Factory(model, provider_a, b=provider_b)

    assert provider_a() == "a"
    assert provider_b() == "b"

    model_1 = provider()
    model_2 = provider()
    assert model("a", "b") == model_1
    assert model_1 == model_2
    assert model_1 is not model_2


def test_transitive_factory_override():
    """
    Checking the factory provider generates different value when Provider arg and kwarg is overridden.
    """
    model = namedtuple("Model", "a b")

    provider_a = providers.Factory(lambda: "a")
    provider_b = providers.Factory(lambda: "b")
    assert provider_a() == "a"
    assert provider_b() == "b"

    provider = providers.Factory(model, provider_a, b=provider_b)

    model_1 = provider()
    model_2 = provider()
    assert model("a", "b") == model_1
    assert model_1 == model_2
    assert model_1 is not model_2

    with (
        provider_a.override_existing("b"),
        provider_b.override_existing("a"),
    ):
        assert provider_a() == "b"
        assert provider_b() == "a"

        model_3 = provider()
        model_4 = provider()
        assert model("b", "a") == model_3
        assert model_3 == model_4
        assert model_3 is not model_4

    model_5 = provider()
    model_6 = provider()
    assert model("a", "b") == model_5
    assert model_5 == model_6
    assert model_5 is not model_6


def test_transitive_singleton_wired():
    """
    Checking the singleton provider evaluates Provider args and kwargs.
    """
    model = namedtuple("Model", "a b")

    provider_a = providers.Singleton(lambda: "a")
    provider_b = providers.Singleton(lambda: "b")
    assert provider_a() == "a"
    assert provider_b() == "b"

    provider = providers.Singleton(model, provider_a, provider_b)

    model_1 = provider()
    model_2 = provider()
    assert model("a", "b") == model_1
    assert model_1 == model_2
    assert model_1 is model_2


def test_transitive_singleton_override():
    """
    Checking the singleton provide retains cached value even when Provider arg and kwarg is overridden.
    """
    model = namedtuple("Model", "a b")

    provider_a = providers.Singleton(lambda: "a")
    provider_b = providers.Singleton(lambda: "b")
    assert provider_a() == "a"
    assert provider_b() == "b"

    provider = providers.Singleton(model, provider_a, provider_b)

    model_1 = provider()
    model_2 = provider()
    assert model("a", "b") == model_1
    assert model_1 == model_2
    assert model_1 is model_2

    with (
        provider_a.override_existing("b"),
        provider_b.override_existing("a"),
    ):
        assert model_1 == provider()  # Overriding does not change the cached value.
