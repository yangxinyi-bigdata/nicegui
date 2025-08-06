from nicegui import ui

from ..windows import WINDOW_BG_COLORS
from . import doc


@doc.demo(ui.dark_mode)
def main_demo() -> None:
    # dark = ui.dark_mode()
    # ui.label('Switch mode:')
    # ui.button('Dark', on_click=dark.enable)
    # ui.button('Light', on_click=dark.disable)
    # END OF DEMO
    label = ui.label('切换模式：')
    container = label.parent_slot.parent
    ui.button('深色', on_click=lambda: (
        label.style('color: white'),
        container.style(f'background-color: {WINDOW_BG_COLORS["browser"][1]}'),
    ))
    ui.button('浅色', on_click=lambda: (
        label.style('color: black'),
        container.style(f'background-color: {WINDOW_BG_COLORS["browser"][0]}'),
    ))


@doc.demo('绑定到开关', '''
    `ui.dark_mode` 元素的值可以绑定到其他元素，如 `ui.switch`。
''')
def bind_to_switch() -> None:
    # dark = ui.dark_mode()
    # ui.switch('Dark mode').bind_value(dark)
    # END OF DEMO
    ui.switch('深色模式', on_change=lambda e: (
        e.sender.style('color: white' if e.value else 'color: black'),
        e.sender.parent_slot.parent.style(f'background-color: {WINDOW_BG_COLORS["browser"][1 if e.value else 0]}'),
    ))


doc.reference(ui.dark_mode)
