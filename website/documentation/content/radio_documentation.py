from nicegui import ui

from . import doc


@doc.demo(ui.radio)
def main_demo() -> None:
    radio1 = ui.radio([1, 2, 3], value=1).props('inline')
    radio2 = ui.radio({1: 'A', 2: 'B', 3: 'C'}).props('inline').bind_value(radio1, 'value')


@doc.demo('注入任意内容', '''
    借助 [`ui.teleport` 元素](teleport)，您可以为单选按钮选项使用任意内容。
''')
def arbitrary_content():
    options = ['Star', 'Thump Up', 'Heart']
    radio = ui.radio({x: '' for x in options}, value='Star').props('inline')
    with ui.teleport(f'#{radio.html_id} > div:nth-child(1) .q-radio__label'):
        ui.icon('star', size='md')
    with ui.teleport(f'#{radio.html_id} > div:nth-child(2) .q-radio__label'):
        ui.icon('thumb_up', size='md')
    with ui.teleport(f'#{radio.html_id} > div:nth-child(3) .q-radio__label'):
        ui.icon('favorite', size='md')
    ui.label().bind_text_from(radio, 'value')


doc.reference(ui.radio)
