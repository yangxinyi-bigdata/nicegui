from nicegui import ui

from . import doc


@doc.demo(ui.checkbox)
def main_demo() -> None:
    checkbox = ui.checkbox('check me')
    ui.label('Check!').bind_visibility_from(checkbox, 'value')


@doc.demo('处理用户交互', '''
    通过参数传递的 `on_change` 函数将在复选框被点击*以及*通过 `set_value` 调用值发生变化时被调用。
    要仅在用户与复选框交互时执行函数，您可以使用通用的 `on` 方法。
''')
def user_interaction():
    with ui.row():
        c1 = ui.checkbox(on_change=lambda e: ui.notify(str(e.value)))
        ui.button('set value', on_click=lambda: c1.set_value(not c1.value))
    with ui.row():
        c2 = ui.checkbox().on('click', lambda e: ui.notify(str(e.sender.value)))
        ui.button('set value', on_click=lambda: c2.set_value(not c2.value))


doc.reference(ui.checkbox)
