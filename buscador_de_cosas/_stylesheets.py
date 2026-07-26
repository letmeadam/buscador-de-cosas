import typing


def get_style_sheet(widget):
    # type: (typing.Any) -> str
    """Safely read styleSheet() from a widget-like object, returning ""
    if unsupported."""
    return widget.styleSheet() if hasattr(widget, "styleSheet") else ""


def set_style_sheet(widget, style_sheet):
    # type: (typing.Any, str) -> bool
    """Safely apply setStyleSheet() to a widget-like object. Returns False
    (no-op) if unsupported, True if applied."""
    if not hasattr(widget, "setStyleSheet"):
        return False
    widget.setStyleSheet(style_sheet)
    return True


def collect_ancestor_stylesheets(widget):
    # type: (typing.Optional[QtWidgets.QWidget]) -> typing.List[typing.Tuple[QtWidgets.QWidget, str]]
    """Climb widget.parent() (mirrors BuscadorDeCosas.select_widget) and
    collect each ancestor's own styleSheet(), root-first. Excludes `widget`
    itself — this is the *ancestor* chain, not including the widget the
    override box already targets."""
    if widget is None:
        return []
    entries = []
    current = widget.parent()
    while current is not None:
        entries.insert(0, (current, get_style_sheet(current)))
        current = current.parent()
    return entries


def _describe_widget(widget):
    # type: (QtWidgets.QWidget) -> str
    class_name = widget.__class__.__name__
    object_name = widget.objectName() if hasattr(widget, "objectName") else ""
    return "{}#{}".format(class_name, object_name) if object_name else class_name


def _format_ancestor_block(widget, style_sheet):
    # type: (QtWidgets.QWidget, str) -> str
    label = _describe_widget(widget)
    divider = "/* {} */".format("-" * len(label))
    return "\n".join([
        divider,
        "/* {} */".format(label),
        divider,
        style_sheet if style_sheet else "/* (no stylesheet) */",
    ])


def format_ancestor_stylesheet(entries):
    # type: (typing.List[typing.Tuple[QtWidgets.QWidget, str]]) -> str
    """Render collect_ancestor_stylesheets()'s output as one block of QSS
    text, root-first, each ancestor labeled with a comment header."""
    if not entries:
        return ""
    blocks = [_format_ancestor_block(widget, style_sheet) for widget, style_sheet in entries]
    return "\n\n".join(blocks)
