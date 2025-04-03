# IMPORT STANDARD LIBRARIES
import contextlib
import typing

# IMPORT THIRD-PARTY LIBRARIES
from Qt import QtCore, QtWidgets


if typing.TYPE_CHECKING:
    import collections


def _get_signals_blocked_status(widget):
    # type: (QtCore.QObject) -> typing.Tuple[QtCore.QObject, typing.Union[bool, None]]
    if not hasattr(widget, "signalsBlocked"):
        return (widget, None)

    return (widget, widget.signalsBlocked())


@contextlib.contextmanager
def disconnect_temporarily(callbacks_tuples):
    # type: (collections.abc.Iterable[typing.Tuple[QtCore.Signal, typing.Callable]]) -> typing.Generator[None, None, None]
    # disconnect all
    for signal, receiver in callbacks_tuples:
        try:
            signal.disconnect(receiver)
        except:
            # TODO add logging for errors... this is a bad stopgap
            pass

    yield

    # Reconnect all signals
    for signal, receiver in callbacks_tuples:
        try:
            signal.connect(receiver)
        except:
            # TODO add logging for errors... this is a bad stopgap
            pass


# TODO use or remove this context manager function
@contextlib.contextmanager
def block_signals(widgets):
    # type: (collections.abc.Iterable[QtWidgets.QWidget]) -> typing.Generator[None, None, None]
    blocked_statuses = map(_get_signals_blocked_status, widgets)

    try:
        for widget, signals_blocked in blocked_statuses:
            if signals_blocked is None:
                continue

            widget.blockSignals(True)
        yield
    finally:
        for widget, signals_blocked in blocked_statuses:
            if signals_blocked is None:
                continue

            widget.blockSignals(signals_blocked)
