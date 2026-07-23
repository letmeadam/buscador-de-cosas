# IMPORT STANDARD LIBRARIES
import os
import textwrap

# IMPORT THIRD-PARTY LIBRARIES
from Qt import QtCore, QtGui, QtWidgets
from six.moves import range

# IMPORT LOCAL LIBRARIES
from . import (
    _constants,
    _context_managers,
    _decorators,
    _delegates,
    _widgets,
)

ROOT_WIDGET = None  # type: QtWidgets.QWidget


def _recursively_open_persistent_editors(tree_view, parent=None):
    # type: (QtWidgets.QTreeView, QtCore.QModelIndex) -> None
    """
    Iteratively open persistent editors for all valid indices in the tree view.
    Avoids recursion to prevent stack overflow and segmentation faults.
    """
    if not tree_view or not tree_view.model():
        return

    model = tree_view.model()
    stack = [parent]

    while stack:
        current_parent = stack.pop()
        if current_parent is None:
            current_parent = QtCore.QModelIndex()
        elif not current_parent.isValid():
            continue

        num_rows = model.rowCount(current_parent)
        for row in range(num_rows):
            index = model.index(row, 0, current_parent)
            if not index.isValid():
                continue

            if hasattr(tree_view, "openPersistentEditor"):
                tree_view.openPersistentEditor(index)

            # Add children to the stack for further processing
            if model.hasChildren(index):
                stack.append(index)


class BuscadorDeCosas(QtWidgets.QDialog):
    def __init__(self, parent=None):
        # type: (typing.Optional[QtWidgets.QWidget]) -> None
        global ROOT_WIDGET
        super(BuscadorDeCosas, self).__init__(parent=parent)
        self.setObjectName("buscadorDeCosa")
        ROOT_WIDGET = self if parent is None else parent

        self._error_display = False

        self.column_headers = (self.tr("Class"), )
        # type: typing.Iterable[str]

        self.setWindowTitle(self.tr("Buscador de Cosas (unattached)"))
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        title = self.tr("Name of this Widget")
        self.title_label = QtWidgets.QLabel("{}: {}".format(title, self.objectName()))
        # type: QtWidgets.QLabel

        self.title_label.setObjectName("title_label")

        self._language_switch_widget = QtWidgets.QWidget()
        language_switch_layout = QtWidgets.QHBoxLayout()
        language_switch_layout.setContentsMargins(_constants.NO_MARGINS)
        self._language_switch_widget.setLayout(language_switch_layout)

        language_switch_layout.addWidget(QtWidgets.QLabel("EN"))
        # self._language_switch_checkbox = QtWidgets.QPushButton("TEST")
        self._language_switch_checkbox = _widgets.PillButton("", uses_highlight=False)
        # self._language_switch_checkbox = _widgets.PillSwitch("", uses_highlight=False)
        self._language_switch_checkbox.setAutoDefault(False)
        language_switch_layout.addWidget(self._language_switch_checkbox)
        language_switch_layout.addWidget(QtWidgets.QLabel("ES"))

        self._translator = QtCore.QTranslator(self)

        self._saved_style = ""

        self.current_widget = None
        # type: typing.Optional[QtWidgets.QWidget]

        self._last_selected_index = None
        self._last_selected_widgets = []

        style_sheet = textwrap.dedent(
            """\
                QLabel#title_label {
                    font: bold;
                }
                QCheckBox#apply_checkbox, QCheckBox#error_checkbox {
                    padding-left: 5px;
                }
                QSplitter::handle:vertical {
                    height: 15px;
                }
                QWidget#delegate_widget {
                    background-color: transparent;
                    border: 0px solid transparent;
                    padding: 2px;
                    padding-left: 0px;
                }
                QWidget#delegate_widget > QLabel {
                    padding-left: 2px;
                }
                QWidget#delegate_widget > QLabel#secondary_label,
                QWidget#delegate_widget > QLabel#primary_alt_label {
                    color: palette(highlighted-text);
                    font-family: "Courier New";
                    font-size: 12px;
                }
                QWidget#delegate_widget > QLabel#secondary_label,
                QWidget#delegate_widget > QLabel#secondary_alt_label {
                    color: palette(placeholder-text);
                }\
            """
        )
        self.setStyleSheet(style_sheet)

        # Widget Tree
        tree_widget = QtWidgets.QWidget()
        tree_layout = QtWidgets.QVBoxLayout()
        tree_layout.setContentsMargins(_constants.NO_MARGINS)
        tree_layout.setSpacing(0)
        tree_widget.setLayout(tree_layout)

        self._tree = QtWidgets.QTreeView()
        self._tree.setAlternatingRowColors(True)
        self._tree.setItemDelegateForColumn(0, _delegates.TreeDelegate(parent=self._tree))
        tree_layout.addWidget(self._tree, stretch=1)

        self._refresh_button = QtWidgets.QPushButton(self.tr("Refresh"))
        tree_layout.addWidget(self._refresh_button)

        # Style Modifications
        style_group_box = QtWidgets.QGroupBox(self.tr("Style Modification"))
        style_group_layout = QtWidgets.QGridLayout()
        style_group_layout.setContentsMargins(_constants.NO_MARGINS)
        style_group_layout.setSpacing(2)
        style_group_box.setLayout(style_group_layout)

        self._style_apply_button = QtWidgets.QPushButton(self.tr("Apply"))
        self._style_apply_button.setToolTip(
            self.tr("Apply style modification to current widget(s), once.")
        )
        style_group_layout.addWidget(self._style_apply_button, 0, 0)

        self._style_apply_checkbox = QtWidgets.QCheckBox("")
        self._style_apply_checkbox.setObjectName("apply_checkbox")
        self._style_apply_checkbox.setToolTip(
            self.tr("Toggle constant style modification to current widget(s).")
        )
        style_group_layout.addWidget(
            self._style_apply_checkbox,
            0,
            0,
            alignment=QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter,
        )

        self._style_clear_button = QtWidgets.QPushButton(self.tr("Clear"))
        self._style_clear_button.setToolTip(
            self.tr("Clear style on currently affected widget(s).")
        )
        style_group_layout.addWidget(self._style_clear_button, 0, 1)

        self._style_edit = QtWidgets.QTextEdit(
            textwrap.dedent(
                """\
                    * {
                        background-color: #00ffcc;
                        color: black;
                        font: bold;
                    }\
                """
            )
        )
        style_group_layout.addWidget(self._style_edit, 1, 0, 1, -1)
        style_group_layout.setRowStretch(1, 1)

        # Widget Interaction
        widget_group_box = QtWidgets.QGroupBox(self.tr("Widget Interaction"))
        widget_group_layout = QtWidgets.QGridLayout()
        widget_group_layout.setContentsMargins(_constants.NO_MARGINS)
        widget_group_layout.setSpacing(2)
        widget_group_box.setLayout(widget_group_layout)

        self._widget_apply_button = QtWidgets.QPushButton(self.tr("Apply"))
        self._widget_apply_button.setToolTip(self.tr("Run code on current widget, once."))
        widget_group_layout.addWidget(self._widget_apply_button, 0, 0)

        self._error_checkbox = QtWidgets.QCheckBox(self.tr("show errors"))
        self._error_checkbox.setObjectName("error_checkbox")
        self._error_checkbox.setToolTip(
            self.tr("Show errors raised from running code on current widget.")
        )
        widget_group_layout.addWidget(
            self._error_checkbox,
            0,
            0,
            alignment=QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter,
        )

        self._widget_edit = QtWidgets.QTextEdit("")
        self._widget_edit.setPlaceholderText(
            self.tr(
                'Use "WIDGET" or "RAW_WIDGET" to reference currently selected widget.\n'
                r'i.e. print"\{\}".format(RAW_WIDGET.objectName())'
            )
        )
        widget_group_layout.addWidget(self._widget_edit, 1, 0)
        widget_group_layout.setRowStretch(1, 1)

        # Splitter Widget/Layout
        splitter = QtWidgets.QSplitter(QtCore.Qt.Vertical)

        splitter.addWidget(tree_widget)
        splitter.setStretchFactor(0, 2)

        splitter.addWidget(style_group_box)
        splitter.setStretchFactor(1, 1)

        splitter.addWidget(widget_group_box)
        splitter.setStretchFactor(2, 1)

        title_row_layout = QtWidgets.QHBoxLayout()
        title_row_layout.addWidget(self.title_label)
        title_row_layout.addStretch()
        title_row_layout.addWidget(self._language_switch_widget)

        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().addLayout(title_row_layout)
        self.layout().addWidget(splitter)

        self._style_apply_button.clicked.connect(self._update_style_from_click)
        self._style_apply_checkbox.toggled.connect(self._update_style_from_toggle)
        self._style_apply_checkbox.setChecked(True)
        self._style_clear_button.clicked.connect(self.clear_style)
        self._style_edit.textChanged.connect(self._update_style)

        self._widget_apply_button.clicked.connect(self._update_widget)
        self._error_checkbox.stateChanged.connect(self._update_error_display)
        self._error_checkbox.setChecked(True)

        self._refresh_button.clicked.connect(self.refresh)
        self._language_switch_checkbox.toggled.connect(self._update_language)
        self.resize(500, 800)

    def keyPressEvent(self, event):
        # type: (Qt.QtGui.QKeyEvent) -> None
        # Disable Escape key from closing the dialog window.
        if event.key() != QtCore.Qt.Key_Escape:
            super(BuscadorDeCosas, self).keyPressEvent(event)

    @_decorators.cursor_override_decorator()
    def _populate_model(self):
        # type: () -> None
        # If refreshing, undo style alterations first.
        if self._tree.model():
            preserve_current_saved_context = _context_managers.disconnect_temporarily(
                [
                    (
                        self._tree.selectionModel().selectionChanged,
                        self._save_current_index,
                    )
                ]
            )
            with preserve_current_saved_context:
                self._tree.clearSelection()

        # Create the headers
        tree_model = QtGui.QStandardItemModel(0, len(self.column_headers))
        for col, col_name in enumerate(self.column_headers):
            tree_model.setHeaderData(col, QtCore.Qt.Horizontal, col_name)

        # Recurse through child widgets
        parent_item = tree_model.invisibleRootItem()

        if not self.parent():
            return

        self._recursively_populate_children(parent_item, ROOT_WIDGET)
        self._tree.setModel(tree_model)
        self._tree.selectionModel().selectionChanged.connect(
            self._update_style
        )  # Does this work ok?
        # self._tree.selectionModel().selectionChanged.connect(self._reapply_style)
        self._tree.selectionModel().selectionChanged.connect(self._save_current_index)
        self._tree.setExpanded(parent_item.child(0, 0).index(), True)
        self._tree.setAnimated(True)
        self._tree.header().setSectionResizeMode(
            0, QtWidgets.QHeaderView.ResizeToContents
        )

        self._attempt_reselect()

    def _recursively_populate_children(self, parent_item, widget):
        # type: (QtGui.QStandardItem, QtWidgets.QWidget) -> None
        # Construct the item data and append the row
        class_name_str = str(widget.__class__).split("'")[1]
        class_name_str = _normalize_class_name(class_name_str)

        name_item = QtGui.QStandardItem(class_name_str)
        name_item.setData(widget, role=_constants.WIDGET_ROLE)
        name_item.setData(widget.objectName(), role=_constants.OBJECT_NAME_ROLE)
        name_item.setData(str(len(widget.children())), role=_constants.NUM_CHILDREN_ROLE)
        name_item.setEditable(False)

        items = [name_item]
        parent_item.appendRow(items)

        # Recurse children and perform the same action
        for child_widget in widget.children():
            self._recursively_populate_children(items[0], child_widget)

    def _save_current_index(self, selected, deselected):
        if not selected.indexes():
            self._last_selected_index = None
            return

        first_selected_index = selected.indexes()[0]
        selected_row = first_selected_index.row()

        tree_model = self._tree.model()

        self._last_selected_index = tree_model.index(
            selected_row, 0, first_selected_index.parent()
        )
        self._last_selected_widgets = []

        temp_index = tree_model.index(
            selected_row, 0, self._last_selected_index.parent()
        )
        self._last_selected_widgets.append(temp_index.data(_constants.WIDGET_ROLE))
        while temp_index.parent().isValid():
            temp_index = temp_index.parent()
            self._last_selected_widgets.insert(0, temp_index.data(_constants.WIDGET_ROLE))

    def _attempt_reselect(self):
        # type: () -> None
        current_index = self._tree.model().invisibleRootItem().index()
        for last_selected_widget in self._last_selected_widgets:
            if current_index.isValid():
                self._tree.setExpanded(current_index, True)

            new_current_index = self._find_row_with_matching_user_data(
                current_index, last_selected_widget
            )
            if not new_current_index:
                print(
                    "Cannot reselect previous selection: {}".format(
                        " > ".join(
                            [
                                _normalize_class_name(str(w.__class__).split("'")[1])
                                for w in self._last_selected_widgets
                            ]
                        )
                    )
                )
                # Reselect last parent
                self._tree.setCurrentIndex(current_index)
                return

            current_index = new_current_index

        self._tree.setCurrentIndex(current_index)

    def _find_row_with_matching_user_data(self, parent_index, user_data):
        # type: (QtCore.QModelIndex, QtWidgets.QWidget) -> None
        tree_model = self._tree.model()

        for row_index in range(tree_model.rowCount(parent=parent_index)):
            child_index = tree_model.index(row_index, 0, parent_index)
            child_user_data = tree_model.data(child_index, _constants.WIDGET_ROLE)
            if user_data == child_user_data:
                return child_index

        return None

    def clear_style(self):
        # type: () -> None
        """Clear any currently set style modifications."""
        self._unset_style()
        self._style_apply_checkbox.setCheckState(QtCore.Qt.Unchecked)

    def get_saved_style(self):
        # type: () -> str
        return self._saved_style

    def get_style(self):
        # type: () -> str
        return self._style_edit.toPlainText()

    def refresh(self):
        # type: () -> None
        """Refresh the debugger."""
        self._populate_model()
        _recursively_open_persistent_editors(self._tree)

    def select_widget(self, widget=None):
        # type: (typing.Optional[QtWidgets.QWidget]) -> None
        """Attempt to select the given widget in the tree."""
        if not widget:
            self._last_selected_widgets = []
        else:
            self._last_selected_widgets = [widget]
            while widget.parent():
                self._last_selected_widgets.insert(0, widget.parent())
                widget = widget.parent()

        self._attempt_reselect()

    def set_style(self, style_sheet=None):
        # type: (typing.Optional[str]) -> None
        if style_sheet is None:
            self._set_style()
        else:
            self._style_edit.setPlainText(style_sheet)

    def toggle_style(self):
        # type: () -> None
        self._style_apply_checkbox.toggle()

    def _update_style_from_click(self):
        self._set_style()

    def _update_style_from_toggle(self, checked):
        # type: (bool) -> None
        if checked:
            self._update_style()
        else:
            self._unset_style()

    def _update_style(self):
        # type: () -> None
        if self._style_apply_checkbox.isChecked() or self._style_apply_button.isFlat():
            self._set_style()

    def _reapply_style(self, selected, deselected):
        # type: (typing.Iterable[QtCore.QModelIndex], typing.Iterable[QtCore.QModelIndex]) -> None
        if self._style_apply_checkbox.checkState():
            self._set_style()

    def _set_style(self):
        # type: () -> None
        indices = [
            index for index in self._tree.selectedIndexes() if index.column() == 0
        ]
        if not indices:
            return

        index = indices[0]
        item = self._tree.model().itemFromIndex(index)

        self._unset_style()

        try:
            self.current_widget = item.data(role=_constants.WIDGET_ROLE)
            if not hasattr(self.current_widget, "styleSheet"):
                raise AttributeError

            self._saved_style = self.current_widget.styleSheet()
            self.current_widget.setStyleSheet(self._style_edit.toPlainText())
        except AttributeError:
            print(
                self.tr('(set) "{}" can not understand the current "styleSheet" :(').format(
                    item.data(role=QtCore.Qt.DisplayRole)
                )
            )
            self._saved_style = ""

    def _unset_style(self):
        # type: () -> None
        if self.current_widget:
            try:
                if not hasattr(self.current_widget, "setStyleSheet"):
                    raise AttributeError

                self.current_widget.setStyleSheet(self._saved_style)
            except AttributeError:
                print(
                    self.tr(
                        '(unset) "{}" can not understand the current "styleSheet" :('
                    ).format(self.current_widget)
                )
            finally:
                self.current_widget = None
                self._saved_style = ""

    def _update_widget(self):
        # type: () -> None
        indices = [
            index for index in self._tree.selectedIndexes() if index.column() == 0
        ]
        if not indices:
            return

        index = indices[0]
        widget_item = self._tree.model().itemFromIndex(index)
        # type_item = self._tree.model().itemFromIndex(index.sibling(index.row(), 2))
        WIDGET = widget_item.data(role=_constants.WIDGET_ROLE)  # noqa: N806 (for user-side macro)

        print("[DEBUG] WIDGET: {}".format(WIDGET))
        if WIDGET:
            try:
                exec(self._widget_edit.toPlainText())
            except Exception as error:
                print(
                    self.tr('(widget) "{}" does not understand the executed code :(').format(
                        WIDGET
                    )
                )
                if self._error_display:
                    print(error)

    def _update_error_display(self, checkstate):
        # type: (bool) -> None
        self._error_display = checkstate == QtCore.Qt.Checked

    def _update_language(self, checked):
        # type: (bool) -> None
        app = QtWidgets.QApplication.instance()
        app.removeTranslator(self._translator)
        if checked:
            qm_path = os.path.join(os.path.dirname(__file__), "translations", "es.qm")
            if self._translator.load(qm_path):
                app.installTranslator(self._translator)

    def show(self):
        # type: () -> None
        self.refresh()
        super(BuscadorDeCosas, self).show()


def _normalize_class_name(class_name):
    class_name = class_name.replace("PySide2.", "")
    class_name = class_name.replace("PySide6.", "")
    class_name = class_name.replace("QtGui.", "")
    class_name = class_name.replace("QtCore.", "")
    class_name = class_name.replace("QtWidgets.", "")
    return class_name


def main():
    # type: () -> int
    """Create the Maya Qt Debugger GUI and show it."""
    import sys  # noqa: PLC0415

    # NOTE: UI strings are wrapped in self.tr(...); install a QTranslator
    # loaded from a compiled .qm file here to localize them.
    app = QtWidgets.QApplication(sys.argv)

    buscador = BuscadorDeCosas()
    buscador.show()

    return app.exec_()


if __name__ == "__main__":
    main()
