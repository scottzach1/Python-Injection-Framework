import importlib
import inspect
from pathlib import Path

PROJECT_DIR = Path(__file__).parent.parent
EXAMPLE_DIR = PROJECT_DIR / "examples"


def pytest_generate_tests(metafunc):
    if "example_name" in metafunc.fixturenames:
        metafunc.parametrize("example_name", [item.name for item in EXAMPLE_DIR.glob("*") if item.is_dir()])


def test_example(example_name: str):
    test_module = importlib.import_module(f"examples.{example_name}.test")
    test_functions = inspect.getmembers(test_module, lambda x: inspect.isfunction(x) and x.__name__.startswith("test_"))

    for _name, func in test_functions:
        func()
