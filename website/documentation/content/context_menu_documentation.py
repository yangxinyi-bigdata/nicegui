from nicegui import ui

from . import doc


@doc.demo(ui.context_menu)
def main_demo() -> None:
    with ui.image('https://picsum.photos/id/377/640/360'):
        with ui.context_menu():
            ui.menu_item('水平翻转')
            ui.menu_item('垂直翻转')
            ui.separator()
            ui.menu_item('重置', auto_close=False)


@doc.demo('具有动态内容的上下文菜单', '''
    要显示内容动态变化的上下文菜单，例如基于鼠标位置，
    建议重用相同的上下文菜单实例。
    此演示展示了如何清除上下文菜单并向其添加新项目。
''')
def update_context_menu() -> None:
    from nicegui import events

    def update_menu(e: events.MouseEventArguments) -> None:
        context_menu.clear()
        with context_menu:
            ui.menu_item(f'在 ({e.image_x:.0f}, {e.image_y:.0f}) 添加圆形')

    source = 'https://picsum.photos/id/377/640/360'
    with ui.interactive_image(source, on_mouse=update_menu, events=['contextmenu']):
        context_menu = ui.context_menu()


doc.reference(ui.context_menu)
