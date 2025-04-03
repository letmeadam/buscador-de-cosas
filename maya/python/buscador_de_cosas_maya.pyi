from _typeshed import Incomplete
import buscador_de_cosas_base
from maya.app.general import mayaMixin


class BuscadorDeCosas(mayaMixin.MayaQWidgetDockableMixin, buscador_de_cosas_base.BuscadorDeCosas):

    def __init__(self, parent: Incomplete | None = ...) -> None: ...

    @classmethod
    def deleteInstances(cls) -> None: ...

    def show(self) -> None: ...

    @staticmethod
    def get_workspace_name(widget: QtWidgets.QWidget) -> str: ...

    def dock_to_panel(self) -> None: ...


def main() -> None: ...
