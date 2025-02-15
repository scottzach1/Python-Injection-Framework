#                  _   _                 _     _
#    ___  ___ ___ | |_| |_ ______ _  ___| |__ / |
#   / __|/ __/ _ \| __| __|_  / _` |/ __| '_ \| |
#   \__ \ (_| (_) | |_| |_ / / (_| | (__| | | | |
#   |___/\___\___/ \__|\__/___\__,_|\___|_| |_|_|
#
#        Zac Scott (github.com/scottzach1)
#
#  https://github.com/scottzach1/python-injector-framework

from scottzach1.pif import exceptions
from scottzach1.pif.providers.provider import Provider


class Blank(Provider):
    """
    A placeholder for a provider.
    """

    __slots__ = tuple()

    def _evaluate(self) -> None:
        raise exceptions.BlankProviderException()
