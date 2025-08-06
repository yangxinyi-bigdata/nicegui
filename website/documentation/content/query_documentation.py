from nicegui import ui

from . import doc


@doc.demo(ui.query)
def main_demo() -> None:
    def set_background(color: str) -> None:
        ui.query('body').style(f'background-color: {color}')

    # ui.button('Blue', on_click=lambda: set_background('#ddeeff'))
    # ui.button('Orange', on_click=lambda: set_background('#ffeedd'))
    # END OF DEMO
    ui.button('Blue', on_click=lambda e: e.sender.parent_slot.parent.style('background-color: #ddeeff'))
    ui.button('Orange', on_click=lambda e: e.sender.parent_slot.parent.style('background-color: #ffeedd'))


@doc.demo('设置背景渐变', '''
    设置背景渐变、图像或类似内容很容易。
    参见 [w3schools.com](https://www.w3schools.com/cssref/pr_background-image.php) 了解有关使用 CSS 设置背景的更多信息。
''')
def background_image():
    # ui.query('body').classes('bg-gradient-to-t from-blue-400 to-blue-100')
    # END OF DEMO
    ui.context.slot_stack[-1].parent.classes('bg-gradient-to-t from-blue-400 to-blue-100')


@doc.demo('修改默认页面填充', '''
    默认情况下，NiceGUI 在页面内容周围提供内置的填充。
    您可以使用类选择器 `.nicegui-content` 修改它。
''')
def remove_padding():
    # ui.query('.nicegui-content').classes('p-0')
    ui.context.slot_stack[-1].parent.classes(remove='p-4')  # HIDE
    # with ui.column().classes('h-screen w-full bg-gray-400 justify-between'):
    with ui.column().classes('h-full w-full bg-gray-400 justify-between'):  # HIDE
        ui.label('top left')
        ui.label('bottom right').classes('self-end')


doc.reference(ui.query)
