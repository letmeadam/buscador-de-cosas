# Buscador de Cosas ("Thing Finder")
A stable-ish Qt debugger for exploring UIs (originally created for Maya UI work)

## Setup


## Usage
```python

from buscador_de_cosas import buscador_de_cosas

# ...

widget = MyWidgetToDebug()

ui_debugger = buscador_de_cosas.BuscadorDeCosas(parent=widget)
ui_debugger.show()

####### Optional Setup #######
# Resize to taste
ui_debugger.resize(500, 800)

# Start with a given stylesheet
ui_debugger.set_style("QWidget { color: green; }")

# Turn off automatic stylesheet application
ui_debugger.clear_style()

# Start with the parent selected
ui_debugger.select_widget(widget)

# Refresh immediately (some applications take time to fully load)
ui_debugger.refresh()

```
