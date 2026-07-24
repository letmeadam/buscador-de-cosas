# Buscador de Cosas ("Thing Finder")
A stable-ish Qt debugger for exploring UIs (originally created for Maya UI work)

## Setup

*IMPORTANT* This debugger works best with an explicit `parent` (typically your host application's main window), e.g. `BuscadorDeCosas(parent=my_main_window)`. If no `parent` is given, it will try to automatically find a suitable top-level window to inspect on first refresh (falling back to itself if none is found), then keep inspecting that same window on later refreshes — in apps with several independent windows this guess may not be the one you want, so an explicit `parent` is still recommended for precision. See `examples/simple.py` for a standalone example.

If a detached `BuscadorDeCosas()` is later attached to a real UI by some other mechanism, call `buscador_de_cosas.set_root_widget(widget)` and then `ui_debugger.refresh()` to point the tree at it. Call `buscador_de_cosas.set_root_widget(None)` to force re-detection (e.g. if the current root widget has since been destroyed). Note that `ROOT_WIDGET` is shared across all `BuscadorDeCosas` instances, so `set_root_widget()` affects whichever instance refreshes next, not one specific instance. Directly assigning `buscador_de_cosas.ROOT_WIDGET = widget` does **not** work — it's a one-time snapshot copied at package-import time, not a live reference — always use `set_root_widget()` / `get_root_widget()` instead.

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
```
