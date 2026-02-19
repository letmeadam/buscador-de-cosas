import textwrap

import hou
import buscador_de_cosas


def run():
    houdini_window = hou.qt.mainWindow()

    ui_debugger = buscador_de_cosas.BuscadorDeCosas(parent=houdini_window)
    ui_debugger.set_style(
        textwrap.dedent(
            """\
                QPushButton:hover {
                    border: 1px solid transparent;
                    border-radius: 0px;  /* border-color corners aren't very smart */
                    border-color:
                        qlineargradient(x1:0, y1:0, x2:1, y2:0, stop: 0 red, stop: 0.01 red, stop:0.99 yellow, stop:1 yellow)
                        qlineargradient(x1:0, y1:0, x2:0, y2:1, stop: 0 yellow, stop:0.01 yellow, stop: 0.99 green, stop:1 green)
                        qlineargradient(x1:1, y1:0, x2:0, y2:0, stop: 0 green, stop: 0.1 green, stop: 0.99 blue, stop:1 blue)
                        qlineargradient(x1:0, y1:1, x2:0, y2:0, stop: 0 blue, stop: 0.1 blue, stop: 0.99 red, stop:1 red);
                    background: qradialgradient(
                        cx: 0.5, cy: 0.5, radius: 1, fx: 0.5, fy: 0.5,
                        stop: 1 palette(base), stop: 0 palette(alternate-base)
                    );
                }\
            """
        )
    )
    ui_debugger.refresh()
    ui_debugger.show()
