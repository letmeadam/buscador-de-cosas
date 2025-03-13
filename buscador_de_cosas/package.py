name = "mpc.buscador_de_cosas"

version = "1.1.1"

description = "A Qt UI Debugger"

authors = ["@adam-lev"]

requires = [
    "mpc.tvcQtCore-1.3+<3",
    "python-2.7+<3.10",

    "six-1.17+<2",

    "mpc.qt_binding_chooser-1+<2",
    "~PySide2-5.15+<6",
]

private_build_requires = ["rez_build_helper-2+<4"]

build_command = "python -m rez_build_helper --shared-python-packages mpc.buscador_de_cosas:python"

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
        "command": "python -m mypy python --strict",
        "requires": ["mypy-1.4+<2"],
        "run_on": _common_run_on,
    },
}


def commands():
    import os

    env.PYTHONPATH.append(os.path.join(root, "python"))
