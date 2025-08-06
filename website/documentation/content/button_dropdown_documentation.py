from nicegui import ui

from . import doc


@doc.demo(ui.dropdown_button)
def main_demo() -> None:
    with ui.dropdown_button('Open me!', auto_close=True):
        ui.item('项目 1', on_click=lambda: ui.notify('您点击了项目 1'))
        ui.item('项目 2', on_click=lambda: ui.notify('您点击了项目 2'))


@doc.demo('下拉按钮中的自定义元素', '''
    您可以在下拉按钮中放置任何元素。
    这是一个包含几个开关的演示。
''')
def custom_dropdown_button() -> None:
    with ui.dropdown_button('设置', icon='settings', split=True):
        with ui.row().classes('p-4 items-center'):
            ui.icon('volume_up', size='sm')
            ui.switch().props('color=negative')
            ui.separator().props('vertical')
            ui.icon('mic', size='sm')
            ui.switch().props('color=negative')


doc.reference(ui.dropdown_button)
