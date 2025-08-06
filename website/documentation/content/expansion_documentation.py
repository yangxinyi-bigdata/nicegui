from nicegui import ui

from . import doc


@doc.demo(ui.expansion)
def main_demo() -> None:
    with ui.expansion('展开!', icon='work').classes('w-full'):
        ui.label('在展开区域内部')


@doc.demo('自定义标题的展开区域', '''
    您可以通过向"header"插槽添加UI元素来填充展开区域的标题，而不是设置纯文本标题。
''')
def expansion_with_custom_header():
    with ui.expansion() as expansion:
        with expansion.add_slot('header'):
            ui.image('https://nicegui.io/logo.png').classes('w-16')
        ui.label('多么好的GUI!')


@doc.demo('带有副标题的展开区域', '''
    可以在标题下方添加副标题或子标签。
''')
def expansion_with_caption():
    with ui.expansion('展开!', caption='展开区域副标题').classes('w-full'):
        ui.label('在展开区域内部')


@doc.demo('带有分组的展开区域', '''
    可以定义展开区域组以实现协调的打开/关闭状态，也称为"手风琴模式"。
''')
def expansion_with_grouping():
    with ui.expansion(text='展开一个!', group='group'):
        ui.label('在展开区域一内部')
    with ui.expansion(text='展开两个!', group='group'):
        ui.label('在展开区域二内部')
    with ui.expansion(text='展开三个!', group='group'):
        ui.label('在展开区域三内部')


doc.reference(ui.expansion)
