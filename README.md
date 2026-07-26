# Buscador de Cosas ("Thing Finder")
A stable-ish Qt debugger for exploring UIs (originally created for Maya UI work)

## Setup

*IMPORTANT* For this runtime debugger to work, there must already be a QMainWindow that exists (see `examples/simple.py` for a standalone example)

## Usage

```python
import buscador_de_cosas

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

# The Style Modification box now has a checkable "Include ancestor
# stylesheet" group box (checked by default) that holds a "Reset" button
# and an editable ancestor-stylesheet box, stacked directly above the
# override box. Unchecking it applies only the override text.
ui_debugger.reset_ancestor_stylesheet()
print(ui_debugger.get_ancestor_stylesheet())
ui_debugger.set_include_ancestor_stylesheet(False)  # apply override text only
```
