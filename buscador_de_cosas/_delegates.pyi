import typing

from Qt import QtCore, QtGui, QtWidgets


class _TreeItemWidget(QtWidgets.QFrame):
    primary_label: str
    primary_alt_label: str
    secondary_label: str
    secondary_alt_label: str
    def __init__(self, primary: str = '', primary_alt: str = '', secondary: str = '', secondary_alt: str = '', parent=None) -> None: ...


class TreeEditorDelegate(QtWidgets.QStyledItemDelegate):
    def paint(self, painter: QtGui.QPainter, option: QtWidgets.QStyleOptionViewItem, index: QtCore.QModelIndex) -> None: ...
    def createEditor(self, parent: QtWidgets.QWidget, option: QtWidgets.QStyleOptionViewItem, index: QtCore.QModelIndex) -> QtWidgets.QWidget: ...
    def setEditorData(self, editor: QtWidgets.QWidget, index: QtCore.QModelIndex) -> None: ...


class TreeItemDelegate(QtWidgets.QStyledItemDelegate):
    def paint(self, painter: QtGui.QPainter, option: QtWidgets.QStyleOptionViewItem, index: QtCore.QModelIndex) -> None: ...
    def sizeHint(self, option: QtWidgets.QStyleOptionViewItem, index: QtCore.QModelIndex) -> QtCore.QSize: ...
TreeDelegate = TreeEditorDelegate
