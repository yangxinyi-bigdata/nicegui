from nicegui import ui

from . import doc


@doc.demo(ui.chip)
def main_demo() -> None:
    with ui.row().classes('gap-1'):
        ui.chip('点击我', icon='ads_click', on_click=lambda: ui.notify('已点击'))
        ui.chip('可选择', selectable=True, icon='bookmark', color='orange')
        ui.chip('可移除', removable=True, icon='label', color='indigo-3')
        ui.chip('样式化', icon='star', color='green').props('outline square')
        ui.chip('已禁用', icon='block', color='red').set_enabled(False)


@doc.demo('动态芯片元素作为标签/标记', '''
    本演示展示如何实现一个动态的芯片列表作为标签或标记。
    您可以通过输入标签并按Enter键或按加号按钮来添加新的芯片。
    被移除的芯片仍然存在，但其值被设置为`False`。
''')
def labels():
    def add_chip():
        with chips:
            ui.chip(label_input.value, icon='label', color='silver', removable=True)
        label_input.value = ''

    label_input = ui.input('添加标签').on('keydown.enter', add_chip)
    with label_input.add_slot('append'):
        ui.button(icon='add', on_click=add_chip).props('round dense flat')

    with ui.row().classes('gap-0') as chips:
        ui.chip('标签 1', icon='label', color='silver', removable=True)

    ui.button('恢复已移除的芯片', icon='unarchive',
              on_click=lambda: [chip.set_value(True) for chip in chips]) \
        .props('flat')


doc.reference(ui.chip)
