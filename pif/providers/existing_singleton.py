#                  _   _                 _     _
#    ___  ___ ___ | |_| |_ ______ _  ___| |__ / |
#   / __|/ __/ _ \| __| __|_  / _` |/ __| '_ \| |
#   \__ \ (_| (_) | |_| |_ / / (_| | (__| | | | |
#   |___/\___\___/ \__|\__/___\__,_|\___|_| |_|_|
#
#        Zac Scott (github.com/scottzach1)
#
#  https://github.com/scottzach1/python-injector-framework

from pif.providers.provider import Provider


class ExistingSingleton[T](Provider):
    """
    Provide an existing object instance.
    """

    __slots__ = ("t",)

    def __init__(self, t: T):
        self.t = t

    def _evaluate(self) -> T:
        return self.t
