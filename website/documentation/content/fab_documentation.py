from nicegui import ui

from . import doc


@doc.demo(ui.fab)
def main_demo() -> None:
    with ui.fab('navigation', label='交通'):
        ui.fab_action('train', on_click=lambda: ui.notify('火车'))
        ui.fab_action('sailing', on_click=lambda: ui.notify('船只'))
        ui.fab_action('rocket', on_click=lambda: ui.notify('火箭'))


@doc.demo('样式', '''
    您可以使用 `color` 参数为FAB及其操作设置样式。
    `color` 参数接受Quasar颜色、Tailwind颜色或CSS颜色。
    您还可以使用 `direction` 参数更改FAB的方向。
''')
def styling_demo() -> None:
    with ui.fab('shopping_cart', label='商店', color='teal', direction='up') \
            .classes('mt-40 mx-auto'):
        ui.fab_action('sym_o_nutrition', label='水果', color='green')
        ui.fab_action('local_pizza', label='披萨', color='yellow')
        ui.fab_action('sym_o_icecream', label='冰淇淋', color='orange')


doc.reference(ui.fab, title='Reference for ui.fab')
doc.reference(ui.fab_action, title='Reference for ui.fab_action')
