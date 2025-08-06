from nicegui import ui

from . import doc


@doc.demo(ui.card)
def main_demo() -> None:
    with ui.card().tight():
        ui.image('https://picsum.photos/id/684/640/360')
        with ui.card_section():
            ui.label('Lorem ipsum dolor sit amet, consectetur adipiscing elit, ...')


@doc.demo('无阴影卡片', '''
    您可以通过添加 `no-shadow` 类来移除卡片的阴影。
    下面的演示显示了 1 像素宽的边框。

    或者，您可以使用 Quasar 的 "flat" 和 "bordered" 属性来实现相同的效果。
''')
def card_without_shadow() -> None:
    with ui.card().classes('no-shadow border-[1px]'):
        ui.label('See, no shadow!')

    with ui.card().props('flat bordered'):
        ui.label('Also no shadow!')


@doc.demo('紧凑卡片布局', '''
    默认情况下，卡片有内边距。
    您可以使用 `tight` 方法移除内边距和嵌套元素之间的间隙。
    这也会隐藏嵌套元素的外边框和阴影，就像原始的 QCard 一样。
''')
def custom_context_menu() -> None:
    rows = [{'age': '16'}, {'age': '18'}, {'age': '21'}]

    with ui.row():
        with ui.card():
            ui.table(rows=rows).props('flat bordered')

        with ui.card().tight():
            ui.table(rows=rows).props('flat bordered')


doc.reference(ui.card)
