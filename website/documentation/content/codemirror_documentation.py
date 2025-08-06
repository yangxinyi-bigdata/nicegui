from nicegui import ui

from . import doc


@doc.demo(ui.codemirror)
def main_demo() -> None:
    editor = ui.codemirror('print("编辑我!")', language='Python').classes('h-32')
    ui.select(editor.supported_languages, label='语言', clearable=True) \
        .classes('w-32').bind_value(editor, 'language')
    ui.select(editor.supported_themes, label='主题') \
        .classes('w-32').bind_value(editor, 'theme')


doc.reference(ui.codemirror)
