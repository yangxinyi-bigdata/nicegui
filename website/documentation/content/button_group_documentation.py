from nicegui import ui

from . import doc


@doc.demo(ui.button_group)
def main_demo() -> None:
    with ui.button_group():
        ui.button('一', on_click=lambda: ui.notify('您点击了按钮 1！'))
        ui.button('二', on_click=lambda: ui.notify('您点击了按钮 2！'))
        ui.button('三', on_click=lambda: ui.notify('您点击了按钮 3！'))


@doc.demo('带有下拉按钮的按钮组', '''
    您也可以向下拉按钮组添加下拉按钮。
''')
def with_dropdown() -> None:
    with ui.button_group():
        ui.button('One')
        ui.button('Two')
        with ui.dropdown_button('下拉菜单'):
            ui.item('项目 1', on_click=lambda: ui.notify('项目 1'))
            ui.item('项目 2', on_click=lambda: ui.notify('项目 2'))


@doc.demo('按钮组样式', '''
    您可以像按钮一样对按钮组应用相同的样式选项，如 "flat"、"outline"、"push" 等...
    但是，您必须始终为按钮组及其包含的按钮使用相同的设计属性。
''')
def styling() -> None:
    with ui.button_group().props('rounded'):
        ui.button('One')
        ui.button('Two')
        ui.button('Three')
    with ui.button_group().props('push glossy'):
        ui.button('One', color='red').props('push')
        ui.button('Two', color='orange').props('push text-color=black')
        ui.button('Three', color='yellow').props('push text-color=black')
    with ui.button_group().props('outline'):
        ui.button('One').props('outline')
        ui.button('Two').props('outline')
        ui.button('Three').props('outline')


doc.reference(ui.button_group)
