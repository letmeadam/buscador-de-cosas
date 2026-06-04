import collections
import contextlib
import typing

from Qt import QtCore, QtGui, QtWidgets

@contextlib.contextmanager
def disconnect_temporarily(callbacks_tuples: collections.abc.Iterable[tuple[QtCore.Signal, typing.Callable]]) -> typing.Generator[None, None, None]: ...
@contextlib.contextmanager
def block_signals(widgets: collections.abc.Iterable[QtWidgets.QWidget]) -> typing.Generator[None, None, None]: ...
@contextlib.contextmanager
def preserved_painter(painter: QtGui.QPainter) -> typing.Generator[None, None, None]: ...
