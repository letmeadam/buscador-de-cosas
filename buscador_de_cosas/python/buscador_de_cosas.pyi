import typing
from Qt import QtWidgets

ROOT_WIDGET: QtWidgets.QWidget

class BuscadorDeCosasMenos(QtWidgets.QDialog):
    column_headers: typing.Iterable[str]
    title_label: QtWidgets.QLabel
    current_widget: typing.Optional[QtWidgets.QWidget]
    def __init__(self, parent: typing.Optional[QtWidgets.QWidget] = ...) -> None: ...
    def clear_style(self) -> None: ...
    def get_saved_style(self) -> str: ...
    def get_style(self) -> str: ...
    def refresh(self) -> None: ...
    def select_widget(self, widget: typing.Optional[QtWidgets.QWidget]) -> None: ...
    def set_style(self, style_sheet: typing.Optional[str] = ...) -> None: ...
    def toggle_style(self) -> None: ...

def main() -> int: ...
