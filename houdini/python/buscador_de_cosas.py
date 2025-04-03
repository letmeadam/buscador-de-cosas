# IMPORT THIRD-PARTY LIBRARIES
import hou

# IMPORT LOCAL LIBRARIES
import buscador_de_cosas_base


class BuscadorDeCosasHoudini(buscador_de_cosas_base.BuscadorDeCosas):
    pass


pythonPanelRegistry().registerPanel(panel_name='BuscadorDeCosas', panel_class=BuscadorDeCosas)
window = BuscadorDeCosasHoudini(parent=hou.qt.mainWindow())
window.show()
