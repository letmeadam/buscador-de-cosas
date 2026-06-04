# IMPORT THIRD-PARTY LIBRARIES
from Qt import QtCore, QtGui, QtWidgets

from . import _constants
from . import _context_managers


def _get_text_height(font, text, rect_width):
    #: type: (QtGui.QFont, str, int) -> int
    font_metrics = QtGui.QFontMetrics(font)

    return font_metrics.boundingRect(
        QtCore.QRect(0, 0, rect_width, 0),
        QtCore.Qt.TextSingleLine,
        text,
    ).height()


class _TreeItemWidget(QtWidgets.QFrame):

    def __init__(self, primary='', primary_alt='', secondary='', secondary_alt='', parent=None):
        super(_TreeItemWidget, self).__init__(parent=parent)
        self.setObjectName("delegate_widget")

        self.primary_label = QtWidgets.QLabel(primary)
        self.primary_label.setObjectName("primary_label")

        self.primary_alt_label = QtWidgets.QLabel(primary_alt)
        self.primary_alt_label.setObjectName("primary_alt_label")
        if not primary_alt:
            self.primary_alt_label.hide()

        self.secondary_label = QtWidgets.QLabel(secondary)
        self.secondary_label.setObjectName("secondary_label")
        if not secondary:
            self.secondary_label.hide()

        self.secondary_alt_label = QtWidgets.QLabel(secondary_alt)
        self.secondary_alt_label.setObjectName("secondary_alt_label")
        if not secondary_alt:
            self.secondary_alt_label.hide()

        layout = QtWidgets.QHBoxLayout()
        layout.setContentsMargins(_constants.NO_MARGINS)
        layout.setSpacing(0)

        layout.addWidget(self.primary_label, 1)
        layout.addWidget(self.secondary_label)
        layout.addWidget(self.primary_alt_label)
        layout.addWidget(self.secondary_alt_label)

        self.setLayout(layout)


class TreeEditorDelegate(QtWidgets.QStyledItemDelegate):
    """A delegate that uses persistent editors for styling the secondary text."""

    def paint(self, painter, option, index):
        # type: (QtGui.QPainter, QtWidgets.QStyleOptionViewItem, QtCore.QModelIndex) -> None
        # NOTE: Selection styling doesn't really get through this if there are additional stylesheet changes
        style = QtWidgets.QApplication.style()
        if hasattr(option, 'parent') and hasattr(option.parent, 'style'):
            style = option.parent.style()
        if option.widget:
            style = option.widget.style()
        self.initStyleOption(option, index)

        option.text = ''
        style.drawControl(QtWidgets.QStyle.CE_ItemViewItem, option, painter)

        return
        # Draw the background
        style.drawPrimitive(
            QtWidgets.QStyle.PE_PanelItemViewItem,
            option,
            painter
        )

        # DON'T Draw the item text
        # style.drawItemText(
        #     painter,
        #     option.rect,
        #     # option.displayAlignment,
        #     QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop,
        #     option.palette,
        #     True,
        #     option.text
        # )

        # Draw the item's check state if applicable
        if option.checkState:
            check_rect = style.subElementRect(
                QtWidgets.QStyle.SE_ItemViewItemCheckIndicator,
                option
            )
            option.rect = check_rect
            style.drawPrimitive(
                QtWidgets.QStyle.PE_IndicatorItemViewItemCheck,
                option,
                painter
            )

        # Draw focus rectangle if item has focus
        if option.state & QtWidgets.QStyle.State_HasFocus:
            style.drawPrimitive(
                QtWidgets.QStyle.PE_FrameFocusRect,
                option,
                painter
            )

    def createEditor(self, parent, option, index):
        # type: (QtWidgets.QWidget, QtWidgets.QStyleOptionViewItem, QtCore.QModelIndex) -> QtWidgets.QWidget
        object_name = index.data(_constants.OBJECT_NAME_ROLE) or ''
        num_children = int(index.data(_constants.NUM_CHILDREN_ROLE)) or 0
        num_children = str(num_children) if num_children else ''

        editor = _TreeItemWidget(primary=option.text, secondary=object_name, primary_alt=num_children, parent=parent)
        editor.primary_alt_label.setVisible(bool(num_children))

        return editor

    def setEditorData(self, editor, index):
        # type: (QtWidgets.QWidget, QtCore.QModelIndex) -> None
        object_name = index.data(_constants.OBJECT_NAME_ROLE) or ''
        num_children = str(index.data(_constants.NUM_CHILDREN_ROLE) or 0)
        if isinstance(editor, _TreeItemWidget):
            editor.primary_label.setText(index.data(QtCore.Qt.DisplayRole))

            if num_children and int(num_children) > 0:
                editor.primary_alt_label.setText(num_children)
                editor.primary_alt_label.setVisible(bool(num_children))

            editor.secondary_label.setText(object_name)
            editor.secondary_label.setVisible(bool(object_name))
        else:
            super().setEditorData(editor, index)


class TreeItemDelegate(QtWidgets.QStyledItemDelegate):
    """A delegate that draws all normal primitives for a QTree item."""

    def paint(self, painter, option, index):
        # type: (QtGui.QPainter, QtWidgets.QStyleOptionViewItem, QtCore.QModelIndex) -> None
        with _context_managers.preserved_painter(painter):
            style = QtWidgets.QApplication.style()
            self.initStyleOption(option, index)

            # Draw the background
            style.drawPrimitive(
                QtWidgets.QStyle.PE_PanelItemViewItem,
                option,
                painter
            )

            # Draw the item text
            style.drawItemText(
                painter,
                option.rect,
                QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop,
                option.palette,
                True,
                option.text
            )

            # Draw the tree branch (disclosure item)
            if option.state & QtWidgets.QStyle.State_Children:
                branch_rect = style.subElementRect(
                    QtWidgets.QStyle.SE_TreeViewDisclosureItem,
                    option
                )
                line_height = option.rect.height()

                num_children = index.data(role=_constants.NUM_CHILDREN_ROLE)
                if num_children:
                    line_height = _get_text_height(option.font, str(num_children), option.rect.width())

                num_children_rect = QtCore.QRect(
                    option.rect.right() - int(line_height * 1.618),
                    option.rect.top(),
                    int(line_height * 1.618),
                    line_height,
                )

                with _context_managers.preserved_painter(painter):
                    painter.setPen(QtGui.QColor(128, 128, 128))
                    style.drawItemText(
                        painter,
                        num_children_rect,
                        QtCore.Qt.AlignCenter,
                        option.palette,
                        True,
                        str(num_children),
                    )

            object_name = index.data(_constants.OBJECT_NAME_ROLE)
            if object_name:
                line_height = _get_text_height(option.font, str(object_name), option.rect.width())
                secondary_option = QtWidgets.QStyleOptionViewItem(option)
                secondary_option.rect = QtCore.QRect(
                    option.rect.left(),
                    option.rect.top() + line_height,
                    option.rect.width(),
                    line_height,
                )
                secondary_option.is_secondary_text = True

                with _context_managers.preserved_painter(painter):
                    painter.setPen(QtGui.QColor(128, 128, 128))
                    style.drawItemText(
                        painter,
                        secondary_option.rect,
                        QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter,
                        option.palette,
                        True,
                        object_name,
                    )

            # Draw the item's check state if applicable
            if option.checkState:
                check_rect = style.subElementRect(
                    QtWidgets.QStyle.SE_ItemViewItemCheckIndicator,
                    option
                )
                option.rect = check_rect
                style.drawPrimitive(
                    QtWidgets.QStyle.PE_IndicatorItemViewItemCheck,
                    option,
                    painter
                )

            # Draw focus rectangle if item has focus
            if option.state & QtWidgets.QStyle.State_HasFocus:
                style.drawPrimitive(
                    QtWidgets.QStyle.PE_FrameFocusRect,
                    option,
                    painter
                )

    def sizeHint(self, option, index):
        # type: (QtWidgets.QStyleOptionViewItem, QtCore.QModelIndex) -> QtCore.QSize
        size_hint = super().sizeHint(option, index)
        size_hint.setWidth(size_hint.width() + (size_hint.height() * 1.618))

        # Only adjust height if secondary text exists
        object_name = index.data(role=_constants.OBJECT_NAME_ROLE)
        if object_name:
            secondary_height = _get_text_height(option.font, str(object_name), size_hint.width())
            size_hint.setHeight(size_hint.height() + secondary_height)
        return size_hint


TreeDelegate = TreeEditorDelegate
