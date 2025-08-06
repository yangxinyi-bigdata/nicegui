from nicegui import ui

from . import doc


@doc.demo(ui.menu)
def main_demo() -> None:
    with ui.row().classes('w-full items-center'):
        result = ui.label().classes('mr-auto')
        with ui.button(icon='menu'):
            with ui.menu() as menu:
                ui.menu_item('菜单项 1', lambda: result.set_text('选择了项目 1'))
                ui.menu_item('菜单项 2', lambda: result.set_text('选择了项目 2'))
                ui.menu_item('菜单项 3 (保持打开)',
                             lambda: result.set_text('选择了项目 3'), auto_close=False)
                ui.separator()
                ui.menu_item('关闭', menu.close)


@doc.demo('客户端自动关闭', '''
    使用 `auto-close` 属性在任何点击事件时直接自动关闭菜单，无需服务器往返。
''')
def auto_close():
    with ui.button(icon='menu'):
        with ui.menu().props('auto-close'):
            toggle = ui.toggle(['快餐', '蛋糕', '冰淇淋'], value='fastfood')
    ui.icon('', size='md').bind_name_from(toggle, 'value')


@doc.demo('带子菜单的菜单', '''
    您可以在 `ui.menu_item` 内嵌套 `ui.menu` 来创建嵌套子菜单。
    "anchor" 和 "self" 属性可用于定位子菜单。
    确保在相应的菜单项上禁用 `auto-close`，以在导航子菜单时保持菜单打开。
''')
def submenus():
    with ui.button(icon='menu'):
        with ui.menu():
            ui.menu_item('选项 1')
            ui.menu_item('选项 2')
            with ui.menu_item('选项 3', auto_close=False):
                with ui.item_section().props('side'):
                    ui.icon('keyboard_arrow_right')
                with ui.menu().props('anchor="top end" self="top start" auto-close'):
                    ui.menu_item('子选项 1')
                    ui.menu_item('子选项 2')
                    ui.menu_item('子选项 3')


doc.reference(ui.menu, title='Reference for ui.menu')
doc.reference(ui.menu_item, title='Reference for ui.menu_item')
