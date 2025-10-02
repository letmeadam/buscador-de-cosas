import collections
import typing

from Qt import QtCore, QtWidgets

def disconnect_temporarily(callbacks_tuples: collections.abc.Iterable[tuple[QtCore.Signal, typing.Callable]]) -> typing.Generator[None, None, None]: ...
def block_signals(widgets: collections.abc.Iterable[QtWidgets.QWidget]) -> typing.Generator[None, None, None]: ...
