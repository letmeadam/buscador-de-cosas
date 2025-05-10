import textwrap

from Qt import QtCore, QtWidgets


def _create_main_window():
    window = QtWidgets.QMainWindow()
    central_widget = QtWidgets.QWidget()
    window.setCentralWidget(central_widget)

    layout = QtWidgets.QVBoxLayout()

    label = QtWidgets.QLabel("This is an example host application for testing!")
    layout.addWidget(label, alignment=QtCore.Qt.AlignCenter)

    sub_layout = QtWidgets.QHBoxLayout()
    layout.addLayout(sub_layout)

    hooray_button = QtWidgets.QPushButton("Hooray!")
    hooray_button.setObjectName("hoorayButton")
    sub_layout.addWidget(hooray_button)

    close_button = QtWidgets.QPushButton("Close")
    close_button.setObjectName("closeButton")
    close_button.clicked.connect(window.close)
    sub_layout.addWidget(close_button)

    central_widget.setLayout(layout)
    return window


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    app.setPalette(app.style().standardPalette())

    window = _create_main_window()

    # Import now that a QApplication has been established.
    from buscador_de_cosas import buscador_de_cosas

    ui_debugger = buscador_de_cosas.BuscadorDeCosas(parent=window)
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
    ui_debugger.select_widget(window.centralWidget())

    window.show()
    ui_debugger.show()
    app.exec()
