# IMPORT STANDARD LIBRARIES
import functools
import typing

# IMPORT THIRD-PARTY LIBRARIES
from Qt import QtCore, QtGui

def cursor_override_decorator(cursor=QtGui.QCursor(QtCore.Qt.WaitCursor)):
    # type: (QtGui.QCursor) -> typing.Callable[..., typing.Callable[..., typing.Any]]
    def decorator(func):
        # type: (typing.Callable[..., typing.Any]) -> typing.Callable[..., typing.Any]
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # type: (typing.List[typing.Any], typing.Dict[str, typing.Any]) -> typing.Any
            result = None
            application: QtGui.QGuiApplication = QtGui.QGuiApplication.instance()

            application.setOverrideCursor(cursor)

            try:
                result = func(args, kwargs)
            finally:
                application.restoreOverrideCursor()

            return result
        return wrapper
    return decorator
