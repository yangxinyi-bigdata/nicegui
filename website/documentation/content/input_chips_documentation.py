from nicegui import ui

from . import doc


@doc.demo(ui.input_chips)
def main_demo() -> None:
    ui.input_chips('我最喜欢的芯片', value=['Pringles', 'Doritos', "Lay's"])


@doc.demo('新建值模式', '''
    新建值模式有三种："add"、"add-unique" 和 "toggle"（默认）。

    - "add" 将所有值添加到列表中（允许重复）。
    - "add-unique" 仅将唯一值添加到列表中。
    - "toggle" 添加或删除值（基于值是否存在于列表中）。
''')
def new_value_modes():
    ui.input_chips('Add', new_value_mode='add')
    ui.input_chips('Add unique', new_value_mode='add-unique')
    ui.input_chips('Toggle', new_value_mode='toggle')


@doc.demo('自动分割值', '''
    此演示展示了当用户输入逗号分隔的值时如何自动分割值。
''')
def delimit_values():
    from nicegui import events

    def split_values(e: events.ValueChangeEventArguments):
        for value in e.value[:]:
            e.value.remove(value)
            e.value.extend(value.split(','))

    ui.input_chips(on_change=split_values)
    ui.label('尝试输入 "x,y,z"!')


doc.reference(ui.input_chips)
