name = "buscador_de_cosas_base"

version = "1.0.0"

description = "A Qt UI Debugger"

authors = ["letmeadam"]

requires = [
    "python-2.7+<3.12",
    "Qt.py-1.4+<1.5",
    "six-1.17+<2",
    # "PySide2-5.15+<6",
    "PySide6-6.8+<6.10",
]

build_command = "cp -r {root}/python {install_path}/."

_common_run_on = ["default", "pre_release"]

tests = {
    "black_diff": {
        "command": "black --diff --check --line-length=120 python",
        "requires": ["black-25+<26"],
        "run_on": _common_run_on,
    },
    "black": {
        "command": "black --line-length=120 python",
        "requires": ["black-25+<26"],
        "run_on": "explicit",
    },
    "isort": {
        "command": "python -m isort --profile black --diff python",
        "requires": ["isort-6+<7"],
        "run_on": "explicit",
    },
    "isort_check": {
        "command": "python -m isort --profile black --check-only --diff python",
        "requires": ["isort-6+<7"],
        "run_on": _common_run_on,
    },
    "pydocstyle": {
        "command": "python -m pydocstyle python",
        "requires": ["pydocstyle-6+<7"],
        "run_on": _common_run_on,
    },
    "pylint": {
        "command": "python -m pylint --max-line-length 120 python",
        "requires": ["pylint-2.17+<4"],
        "run_on": _common_run_on,
    },
    "mypy": {
        "command": "python -m mypy python",
        "requires": ["mypy-1.4+<2"],
        "run_on": _common_run_on,
    },
}


def commands():
    import os

    env.PYTHONPATH.append(os.path.join(root, "python"))
