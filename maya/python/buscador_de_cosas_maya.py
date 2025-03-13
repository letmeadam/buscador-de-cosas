# IMPORT THIRD-PARTY LIBRARIES
from mpc.tvcUtils.maya import dialogs
from mpc.tvcUtils.maya import maya_ui

# IMPORT LOCAL LIBRARIES
from buscador_de_cosas import buscador_de_cosas


class BuscadorDeCosas(buscador_de_cosas.BuscadorDeCosasMenos):

    def show(self):
        # type: () -> None
        """Display docked window with the following default settings."""
        dialogs.DockableDialog.dock(
            self, "Buscador de Cosas", load_docked=True, dock_tab="AttributeEditor", width=512
        )

        self.refresh()


def main():
    # type: () -> None
    """Create the Maya Qt Debugger GUI and show it."""
    window = BuscadorDeCosas(parent=maya_ui.get_maya_main_window())
    window.show()
