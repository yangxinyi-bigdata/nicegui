from nicegui import ui

from . import doc


@doc.demo(ui.color_picker)
def main_demo() -> None:
    with ui.button(icon='colorize') as button:
        ui.color_picker(on_pick=lambda e: button.classes(f'!bg-[{e.color}]'))


@doc.demo('自定义颜色选择器', '''
    您可以通过属性、类和样式属性自定义颜色选择器。
    因为 QColor 组件嵌套在菜单内，您不能直接使用 `props` 方法，
    而是通过 `q_color` 属性。
''')
def color_picker_props() -> None:
    with ui.button(icon='palette'):
        picker = ui.color_picker(on_pick=lambda e: ui.notify(f'You chose {e.color}'))
        picker.q_color.props('default-view=palette no-header no-footer')


doc.reference(ui.color_picker)
