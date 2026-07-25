"""Reference/runnable script for the screenshot-ui skill.

Builds the app the same way `examples/simple.py` does, captures the
`BuscadorDeCosas` debugger widget, and saves it to the given output path.
Works for both the native (Option A) and headless (Option B) modes; the
mode is selected via the `QT_QPA_PLATFORM` environment variable.

Usage:
    .env/bin/python3 simple_example.py <OUTPUT>.png
    QT_QPA_PLATFORM=offscreen .env/bin/python3 simple_example.py <OUTPUT>.png
"""
import sys

from Qt import QtWidgets

EVENT_CYCLES = 10


def main(output_path):
    app = QtWidgets.QApplication([])
    app.setPalette(app.style().standardPalette())

    from examples import simple

    window = simple.create_main_window()
    ui_debugger = simple.create_main_widget(parent=window)
    ui_debugger.select_widget(window.centralWidget())

    window.show()
    ui_debugger.show()

    for _ in range(EVENT_CYCLES):
        app.processEvents()

    ui_debugger.grab().save(output_path, "PNG")
    print("Saved screenshot to {}".format(output_path))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("usage: {} <OUTPUT>.png".format(sys.argv[0]))
    main(sys.argv[1])
