# IMPORT STANDARD LIBRARIES
import typing

# IMPORT THIRD-PARTY LIBRARIES
from Qt import QtCore, QtGui, QtWidgets


PHI = 1.618033988749895  # Golden ratio


class PillButton(QtWidgets.QPushButton):

    _TRACK_HEIGHT = 18
    _TRACK_WIDTH = int(_TRACK_HEIGHT * PHI)
    _KNOB_MARGIN = 2

    def __init__(self, text='', uses_highlight=True, parent=None):
        # type: (str, typing.Optional[QtWidgets.QWidget]) -> None
        super(PillButton, self).__init__(text, parent=parent)
        # self.setCheckable(True)

    # def paintEvent(self, event):
    #     super(PillButton, self).paintEvent(event)

        # # type: (QtGui.QPaintEvent) -> None
        # painter = QtWidgets.QStylePainter(self)
        # painter.setRenderHint(QtGui.QPainter.Antialiasing)
        #
        # option = QtWidgets.QStyleOptionButton()
        # self.initStyleOption(option)
        #
        # rect = self.rect()
        # diameter = rect.height() // 2 - 1
        # circle_rect = QtCore.QRect(0, 0, diameter, diameter)
        # circle_rect.moveCenter(rect.center())
        #
        # # Track behind the circular button: twice as wide, with _KNOB_MARGIN padding around the circle.
        # track_rect = QtCore.QRect(
        #     0, 0, (diameter * 2) + (self._KNOB_MARGIN * 2), diameter + (self._KNOB_MARGIN * 2)
        # )
        # track_rect.moveCenter(rect.center())
        #
        # painter.setPen(QtCore.Qt.NoPen)
        # painter.setBrush(option.palette.color(QtGui.QPalette.Mid))
        # painter.drawRoundedRect(track_rect, track_rect.height() / 2.0, track_rect.height() / 2.0)
        #
        # clip_path = QtGui.QPainterPath()
        # clip_path.addEllipse(QtCore.QRectF(circle_rect))
        # painter.setClipPath(clip_path)
        #
        # # Let the active style paint its real bevel/gradient, just masked to a circle.
        # painter.drawControl(QtWidgets.QStyle.CE_PushButtonBevel, option)
        # # painter.setPen(QtCore.Qt.NoPen)
        # # painter.setBrush(option.palette.text())
        # # painter.drawEllipse(circle_rect)
        #
        # if self.text():
        #     group = (
        #         QtGui.QPalette.Active
        #         if option.state & QtWidgets.QStyle.State_Enabled
        #         else QtGui.QPalette.Disabled
        #     )
        #     painter.setPen(option.palette.color(group, QtGui.QPalette.ButtonText))
        #     painter.drawText(circle_rect, QtCore.Qt.AlignCenter, self.text())
        #
    def minimumSizeHint(self):
        size_hint = super(PillButton, self).minimumSizeHint()
        return QtCore.QSize(int(size_hint.height() * PHI), size_hint.height())

    def sizeHint(self):
        size_hint = super(PillButton, self).sizeHint()
        return QtCore.QSize(int(size_hint.height() * PHI), size_hint.height())


class PillSwitch(QtWidgets.QPushButton):
    """A QPushButton that paints itself as a sliding pill toggle switch."""

    _TRACK_HEIGHT = 18
    _TRACK_WIDTH = int(_TRACK_HEIGHT * PHI)
    _KNOB_MARGIN = 2

    def __init__(self, text='', uses_highlight=True, parent=None):
        # type: (str, typing.Optional[QtWidgets.QWidget]) -> None
        super(PillSwitch, self).__init__(text, parent=parent)
        self.setCheckable(True)
        self._uses_highlight = uses_highlight

        self._knob_position = float(self._knob_offset_for_state(self.isChecked()))

        self._animation = QtCore.QPropertyAnimation(self, b"knob_position", self)
        self._animation.setDuration(180)
        self._animation.setEasingCurve(QtCore.QEasingCurve.OutQuart)

        self.toggled.connect(self._animate_to_state)

    def _knob_diameter(self):
        # type: () -> int
        return self._TRACK_HEIGHT - (self._KNOB_MARGIN * 2)

    def _knob_offset_for_state(self, checked):
        # type: (bool) -> int
        if checked:
            return self._TRACK_WIDTH - self._KNOB_MARGIN - self._knob_diameter()
        return self._KNOB_MARGIN

    def _animate_to_state(self, checked):
        # type: (bool) -> None
        self._animation.stop()
        self._animation.setStartValue(self._knob_position)
        self._animation.setEndValue(float(self._knob_offset_for_state(checked)))
        self._animation.start()

    def _get_knob_position(self):
        # type: () -> float
        return self._knob_position

    def _set_knob_position(self, position):
        # type: (float) -> None
        self._knob_position = position
        self.update()

    knob_position = QtCore.Property(float, _get_knob_position, _set_knob_position)

    def sizeHint(self):
        # type: () -> QtCore.QSize
        size_hint = super(PillSwitch, self).sizeHint()
        size_hint.setWidth(size_hint.width() + self._TRACK_WIDTH)
        size_hint.setHeight(max(size_hint.height(), self._TRACK_HEIGHT))
        return size_hint

    def hitButton(self, position):
        # type: (QtCore.QPoint) -> bool
        return self.contentsRect().contains(position)

    def _track_rect(self):
        # type: () -> QtCore.QRect
        return QtCore.QRect(
            0,
            (self.height() - self._TRACK_HEIGHT) // 2,
            self._TRACK_WIDTH,
            self._TRACK_HEIGHT,
        )

    def _paintEvent(self, event):
        # type: (QtGui.QPaintEvent) -> None
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        palette = self.palette()
        track_rect = self._track_rect()

        if not self.isEnabled():
            track_color = palette.color(QtGui.QPalette.Dark)
        elif self.isChecked() and self._uses_highlight:
            track_color = palette.color(QtGui.QPalette.Highlight)
        else:
            track_color = palette.color(QtGui.QPalette.Mid)

        # Draw slot
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(track_color)
        painter.drawRoundedRect(track_rect, self._TRACK_HEIGHT / 2.0, self._TRACK_HEIGHT / 2.0)

        # Draw knob
        knob_diameter = self._knob_diameter()
        knob_rect = QtCore.QRect(
            track_rect.left() + int(self._knob_position),
            track_rect.top() + self._KNOB_MARGIN,
            knob_diameter,
            knob_diameter,
        )

        painter.setBrush(palette.color(QtGui.QPalette.Button if self.isEnabled() else QtGui.QPalette.Mid))
        painter.drawEllipse(knob_rect)

        # Draw text
        if self.text():
            text_rect = QtCore.QRect(
                track_rect.right() + 6,
                0,
                self.width() - track_rect.right() - 6,
                self.height(),
            )
            painter.setPen(palette.color(QtGui.QPalette.WindowText))
            painter.drawText(text_rect, QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter, self.text())
