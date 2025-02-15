import importlib
import inspect
from pathlib import Path

PROJECT_DIR = Path(__file__).parent.parent
EXAMPLE_DIR = PROJECT_DIR / "examples"


def pytest_generate_tests(metafunc):
    if "func" in metafunc.fixturenames:
        targets = []
        ids = []

        for example_dir in EXAMPLE_DIR.glob("*"):
            if not example_dir.is_dir():
                continue

            for test_file in example_dir.glob("test*.py"):
                test_module = importlib.import_module(
                    test_file.relative_to(PROJECT_DIR).with_suffix("").as_posix().replace("/", ".")
                )
                test_functions = inspect.getmembers(
                    test_module,
                    lambda x: inspect.isfunction(x) and x.__name__.startswith("test_"),
                )

                for name, func in test_functions:
                    targets.append(func)
                    ids.append(f"{test_file.relative_to(EXAMPLE_DIR).with_suffix('').as_posix()}/{name}")

        metafunc.parametrize("func", targets, ids=ids)


def test_example(func):
    func()
