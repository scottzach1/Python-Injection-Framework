from unittest.mock import MagicMock

from examples.simple_service import main


def test_main():
    """
    Showcase how we can patch our main method for testing.
    """
    mock = MagicMock()

    with main.ApiClientProvider.override_existing(mock):
        main.main()

    assert mock.do_stuff.call_count == 1
