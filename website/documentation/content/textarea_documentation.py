from nicegui import ui

from . import doc


@doc.demo(ui.textarea)
def main_demo() -> None:
    ui.textarea(label='Text', placeholder='start typing',
                on_change=lambda e: result.set_text('you typed: ' + e.value))
    result = ui.label()


@doc.demo('可清除', '''
    来自 [Quasar](https://quasar.dev/) 的 `clearable` 属性为输入框添加一个清除文本的按钮。
''')
def clearable():
    i = ui.textarea(value='some text').props('clearable')
    ui.label().bind_text_from(i, 'value')


doc.reference(ui.textarea)
