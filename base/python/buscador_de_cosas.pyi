import typing
from Qt import QtWidgets

ROOT_WIDGET: QtWidgets.QWidget


class BuscadorDeCosas(QtWidgets.QDialog):

    column_headers: typing.Iterable[str]
    title_label: QtWidgets.QLabel
    current_widget: typing.Optional[QtWidgets.QWidget]

    def __init__(self, parent: QtWidgets.QWidget | None = None) -> None: ...

    def clear_style(self) -> None:
        """Clear any currently set style modifications."""

    def get_saved_style(self) -> str: ...

    def get_style(self) -> str: ...

    def refresh(self) -> None:
        """Refresh the debugger."""

    def select_widget(self, widget: typing.Optional[QtWidgets.QWidget] = None) -> None:
        """Attempt to select the given widget in the tree."""

    def set_style(self, style_sheet: typing.Optional[str] = None) -> None: ...

    def toggle_style(self) -> None: ...


def main() -> int:
    """Create the Maya Qt Debugger GUI and show it."""
