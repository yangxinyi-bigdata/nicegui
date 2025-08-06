from nicegui import ui

from . import doc


@doc.demo(ui.switch)
def main_demo() -> None:
    switch = ui.switch('switch me')
    ui.label('Switch!').bind_visibility_from(switch, 'value')


@doc.demo('处理用户交互', '''
    通过参数传递的 `on_change` 函数将在开关被点击*以及*通过 `set_value` 调用值发生变化时被调用。
    要仅在用户与开关交互时执行函数，您可以使用通用的 `on` 方法。
''')
def user_interaction():
    with ui.row():
        s1 = ui.switch(on_change=lambda e: ui.notify(str(e.value)))
        ui.button('set value', on_click=lambda: s1.set_value(not s1.value))
    with ui.row():
        s2 = ui.switch().on('click', lambda e: ui.notify(str(e.sender.value)))
        ui.button('set value', on_click=lambda: s2.set_value(not s2.value))


doc.reference(ui.switch)
