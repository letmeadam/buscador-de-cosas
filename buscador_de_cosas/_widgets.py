# IMPORT STANDARD LIBRARIES
import typing

# IMPORT THIRD-PARTY LIBRARIES
from Qt import QtCore, QtGui, QtWidgets


class PillSwitch(QtWidgets.QCheckBox):
    """A QCheckBox that paints itself as a sliding pill toggle switch."""

    _TRACK_WIDTH = 36
    _TRACK_HEIGHT = 18
    _KNOB_MARGIN = 2

    def __init__(self, text='', parent=None):
        # type: (str, typing.Optional[QtWidgets.QWidget]) -> None
        super(PillSwitch, self).__init__(text, parent=parent)
        self.setCursor(QtCore.Qt.PointingHandCursor)

        self._knob_position = float(self._knob_offset_for_state(self.isChecked()))

        self._animation = QtCore.QPropertyAnimation(self, b"knob_position", self)
        self._animation.setDuration(120)
        self._animation.setEasingCurve(QtCore.QEasingCurve.InOutCubic)

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

    def paintEvent(self, event):
        # type: (QtGui.QPaintEvent) -> None
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        palette = self.palette()
        track_rect = self._track_rect()

        if not self.isEnabled():
            track_color = palette.color(QtGui.QPalette.Disabled, QtGui.QPalette.Mid)
        elif self.isChecked():
            track_color = palette.color(QtGui.QPalette.Highlight)
        else:
            track_color = palette.color(QtGui.QPalette.Mid)

        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(track_color)
        painter.drawRoundedRect(track_rect, self._TRACK_HEIGHT / 2.0, self._TRACK_HEIGHT / 2.0)

        knob_diameter = self._knob_diameter()
        knob_rect = QtCore.QRect(
            track_rect.left() + int(self._knob_position),
            track_rect.top() + self._KNOB_MARGIN,
            knob_diameter,
            knob_diameter,
        )
        painter.setBrush(palette.color(QtGui.QPalette.Light))
        painter.drawEllipse(knob_rect)

        if self.text():
            text_rect = QtCore.QRect(
                track_rect.right() + 6,
                0,
                self.width() - track_rect.right() - 6,
                self.height(),
            )
            painter.setPen(palette.color(QtGui.QPalette.WindowText))
            painter.drawText(text_rect, QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter, self.text())
