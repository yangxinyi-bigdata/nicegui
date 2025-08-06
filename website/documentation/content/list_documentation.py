from nicegui import ui

from . import doc


@doc.demo(ui.list)
def main_demo() -> None:
    with ui.list().props('dense separator'):
        ui.item('3 个苹果')
        ui.item('5 根香蕉')
        ui.item('8 颗草莓')
        ui.item('13 个核桃')


@doc.demo('项目、部分和标签', '''
    列表项目使用项目部分来构建其内容结构。
    项目标签根据其属性占据不同的位置。
''')
def contact_list():
    with ui.list().props('bordered separator'):
        ui.item_label('联系人').props('header').classes('text-bold')
        ui.separator()
        with ui.item(on_click=lambda: ui.notify('已选择联系人 1')):
            with ui.item_section().props('avatar'):
                ui.icon('person')
            with ui.item_section():
                ui.item_label('好人')
                ui.item_label('名字').props('caption')
            with ui.item_section().props('side'):
                ui.icon('chat')
        with ui.item(on_click=lambda: ui.notify('已选择联系人 2')):
            with ui.item_section().props('avatar'):
                ui.icon('person')
            with ui.item_section():
                ui.item_label('友善的人')
                ui.item_label('名字').props('caption')
            with ui.item_section().props('side'):
                ui.icon('chat')


doc.reference(ui.list, title='Reference for ui.list')
doc.reference(ui.item, title='Reference for ui.item')
doc.reference(ui.item_section, title='Reference for ui.item_section')
doc.reference(ui.item_label, title='Reference for ui.item_label')
