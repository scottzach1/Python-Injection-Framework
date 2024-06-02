# Python Injection Framework (PIF)

A simple Python dependency injection framework.

## Usage

**This project is under active development. The following example does not represent the final state for the project.**

```python
from pif import wiring, providers


@wiring.injected
def my_function(a: str = providers.Singleton[str](lambda: "hello world")):
    return a


if __name__ == '__main__':
    assert "hello world" == my_function()
```

## Authors

| [![Zac Scott](https://avatars.githubusercontent.com/u/38968222)](https://github.com/scottzach1) |
|:------------------------------------------------------------------------------------------------|
| [Zac Scott (scottzach1)](https://github.com/scottzach1)                                         |
