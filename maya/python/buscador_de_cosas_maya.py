# IMPORT THIRD-PARTY LIBRARIES
# import dialogs
# import maya_ui

# IMPORT LOCAL LIBRARIES
import buscador_de_cosas_base


class BuscadorDeCosas(buscador_de_cosas_base.BuscadorDeCosas):

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
