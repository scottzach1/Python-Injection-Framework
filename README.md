# Python Injection Framework (PIF)

A simple Python dependency injection framework.

## Usage

**This project is under active development. The following example does not represent the final state for the project.**

The injection framework is configured to inject any default values for method arguments that are instances
of `providers.Provider`.

This implementation works by wrapping decorators around methods any patching any unfilled `providers.Provider` default
arguments at runtime.

All dependency injection is lazily evaluated so providers are only evaluated when a method is called. This approach is
optimal as it reduces necessary computation for expensive services and reduces

### Decorator Injection

With this approach you can automatically inject functions at load time using the `@wiring.injected` decorator.

```python
from pif import wiring, providers


@wiring.injected  # <- automatically injects providers.Provider default arguments!
def my_function(a: str = providers.Singleton[str](lambda: "hello world")):
    return a


if __name__ == "__main__":
    assert "hello world" == my_function()
```

### Module Injection

With this approach you can wire all methods in the specified modules.

```python
from pif import wiring, providers


def my_function(a: str = providers.Singleton[str](lambda: "hello world")):
    return a


if __name__ == "__main__":
    wiring.wire([__name__])  # <- dynamically inject methods with providers.Provider default arguments!

    assert "hello world" == my_function()
```

## Authors

| [![Zac Scott](https://avatars.githubusercontent.com/u/38968222?s=128&v=4)](https://github.com/scottzach1) |
|:----------------------------------------------------------------------------------------------------------|
| [Zac Scott (scottzach1)](https://github.com/scottzach1)                                                   |
