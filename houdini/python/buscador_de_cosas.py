# IMPORT THIRD-PARTY LIBRARIES
import hou

# IMPORT LOCAL LIBRARIES
from buscador_de_cosas import buscador_de_cosas


class BuscadorDeCosas(buscador_de_cosas.BuscadorDeCosasMenos):
    pass


pythonPanelRegistry().registerPanel(panel_name='BuscadorDeCosas', panel_class=BuscadorDeCosas)
window = BuscadorDeCosas(parent=hou.qt.mainWindow())
window.show()
