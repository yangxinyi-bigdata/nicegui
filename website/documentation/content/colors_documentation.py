from nicegui import ui

from . import doc


@doc.demo(ui.colors)
def main_demo() -> None:
    # ui.button('Default', on_click=lambda: ui.colors())
    # ui.button('Gray', on_click=lambda: ui.colors(primary='#555'))
    # END OF DEMO
    b1 = ui.button('Default', on_click=lambda: [b.classes(replace='!bg-primary') for b in [b1, b2]])
    b2 = ui.button('Gray', on_click=lambda: [b.classes(replace='!bg-[#555]') for b in [b1, b2]])


@doc.demo('自定义颜色', '''
    您可以添加自定义颜色定义用于品牌。
    在这种情况下，必须在自定义颜色被使用之前调用 `ui.colors`。

    *在版本 2.2.0 中添加*
''')
def custom_color_demo() -> None:
    from random import randint

    ui.colors(brand='#424242')
    ui.label('This is your custom brand color').classes('text-brand')
    ui.button('Randomize', color='brand',
              on_click=lambda: ui.colors(brand=f'#{randint(0, 0xffffff):06x}'))


doc.reference(ui.colors)
