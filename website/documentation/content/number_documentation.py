from nicegui import ui

from . import doc


@doc.demo(ui.number)
def main_demo() -> None:
    ui.number(label='数字', value=3.1415927, format='%.2f',
              on_change=lambda e: result.set_text(f'您输入了: {e.value}'))
    result = ui.label()


@doc.demo('可清除', '''
    来自[Quasar](https://quasar.dev/)的`clearable`属性会向输入框添加一个清除文本的按钮。
''')
def clearable():
    i = ui.number(value=42).props('clearable')
    ui.label().bind_text_from(i, 'value')


@doc.demo('小数位数', '''
    您可以使用`precision`参数指定小数位数。
    负值表示小数点前的位数。
    舍入发生在输入失去焦点时，
    当最小值、最大值或精度等清理参数更改时，
    或手动调用`sanitize()`时。
''')
def integer():
    n = ui.number(value=3.14159265359, precision=5)
    n.sanitize()


doc.reference(ui.number)
