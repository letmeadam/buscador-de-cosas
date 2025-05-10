# IMPORT STANDARD LIBRARIES
import functools
import typing

# IMPORT THIRD-PARTY LIBRARIES
from Qt import QtCore, QtGui, QtWidgets


def cursor_override_decorator(cursor=QtGui.QCursor(QtCore.Qt.WaitCursor)):
    # type: (QtGui.QCursor) -> typing.Callable[..., typing.Callable[..., typing.Any]]
    def decorator(func):
        # type: (typing.Callable[..., typing.Any]) -> typing.Callable[..., typing.Any]
        @functools.wraps(func)
        def wrapper(*args):
            # type: (typing.List[typing.Any]) -> typing.Any
            result = None
            application: QtWidgets.QApplication = QtWidgets.QApplication.instance()

            application.setOverrideCursor(cursor)

            try:
                result = func(*args)
            finally:
                application.restoreOverrideCursor()

            return result
        return wrapper
    return decorator
