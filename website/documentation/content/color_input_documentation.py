from nicegui import ui

from . import doc


@doc.demo(ui.color_input)
def main_demo() -> None:
    label = ui.label('改变我的颜色！')
    ui.color_input(label='颜色', value='#000000',
                   on_change=lambda e: label.style(f'color:{e.value}'))


doc.reference(ui.color_input)
