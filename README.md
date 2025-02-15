# Python Injection Framework (PIF)

[![python](https://github.com/scottzach1/Python-Injector-Framework/blob/gh-pages/python.svg?raw=true)](https://github.com/scottzach1/Python-Injector-Framework/)
[![version](https://github.com/scottzach1/Python-Injector-Framework/blob/gh-pages/version.svg?raw=true)](https://github.com/scottzach1/Python-Injector-Framework/)
[![coverage](https://github.com/scottzach1/Python-Injector-Framework/blob/gh-pages/coverage.svg?raw=true)](https://github.com/scottzach1/Python-Injector-Framework/)
[![pytest](https://github.com/scottzach1/Python-Injector-Framework/blob/gh-pages/pytest.svg?raw=true)](https://github.com/scottzach1/Python-Injector-Framework/)
[![ruff](https://github.com/scottzach1/Python-Injector-Framework/blob/gh-pages/ruff.svg?raw=true)](https://github.com/scottzach1/Python-Injector-Framework/)

A simple Python dependency injection framework.

## Usage

**This project is under active development. The following example does not represent the final state for the project.**

You can install this project from pypi.

```shell
pip install python-injection-framework
```

### Dependency Injection

The injection framework is configured to inject any default values for method arguments that are instances
of `providers.Provider`.

This implementation works by wrapping decorators around methods any patching any unfilled `providers.Provider` default
arguments at runtime.

All dependency injection is lazily evaluated so providers are only evaluated when a method is called. This approach is
optimal as it reduces necessary computation for expensive services and reduces

#### Decorator Injection

With this approach you can automatically inject functions at load time using the `@wiring.inject` decorator.

```python
from pif import providers
from pif import wiring


@wiring.inject  # <- automatically injects providers.Provider default arguments!
def my_function(a: str = providers.ExistingSingleton("hello world")):
   return a


if __name__ == "__main__":
   assert "hello world" == my_function()
```

### Module Injection

With this approach you can wire all methods in the specified modules.

```python
from pif import providers
from pif import wiring


def my_function(a: str = providers.ExistingSingleton("hello world")):
   return a


if __name__ == "__main__":
   wiring.wire([__name__])  # <- dynamically inject methods with providers.Provider default arguments!

   assert "hello world" == my_function()
```

### Overriding

This package provides a simple mechanism to override providers. This can be very useful when it comes to mocking
services for testing or dynamically patching application behavior based on application configuration.

#### Standard Overriding

If you want to patch a value all you need to do is call `.override()` on the provider in question. If you are wanting to
override an existing singleton you may call the convenience method `.override_existing()`.

```python
from pif import providers
from pif import wiring

StringProvider = providers.ExistingSingleton("hello world")


@wiring.inject
def my_function(a: str = StringProvider):
   return a


if __name__ == "__main__":
   assert "hello world" == my_function()

   override = StringProvider.override_existing("overridden_1")

   assert "overridden_1"
```

### Context Managers

If you want more control around the override lifecycles then you may use the `Override` context manager.

```python
from pif import providers
from pif import wiring

StringProvider = providers.ExistingSingleton("hello world")


@wiring.inject
def my_function(a: str = StringProvider):
   return a


if __name__ == "__main__":
   assert "hello world" == my_function()

   OverrideProvider = providers.ExistingSingleton("overridden_1")

   with StringProvider.override(OverrideProvider):
      assert "overridden_1" == my_function()

      with OverrideProvider.override_existing("overridden_2"):
         assert "overridden_2" == my_function()  # You can even stack overrides!!

      assert "overridden_1" == my_function()

   assert "hello world" == my_function()
```

## Examples

If you would like to see more examples, feel free to check out [examples/](examples).

## Contributing

1. Clone the repository and setup with uv 🪄

    ```shell
    git clone git@github.com:scottzach1/Python-Injection-Framework.git
    cd Python-Injection-Framework
    uv sync --dev
    ```

2. Configure pre-commit hooks 🪝

    ```shell
    pre-commit install
    ```

3. Write your changes! 💻️

4. Run test cases 🧪

    ```shell
    pytest
    ```

5. Submit a Pull Request ↖️

## Authors

| [![Zac Scott](https://avatars.githubusercontent.com/u/38968222?s=128&v=4)](https://github.com/scottzach1) |
|:----------------------------------------------------------------------------------------------------------|
| [Zac Scott (scottzach1)](https://github.com/scottzach1)                                                   |
