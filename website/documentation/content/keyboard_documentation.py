from nicegui import ui

from . import doc


@doc.demo(ui.keyboard)
def main_demo() -> None:
    from nicegui.events import KeyEventArguments

    def handle_key(e: KeyEventArguments):
        if e.key == 'f' and not e.action.repeat:
            if e.action.keyup:
                ui.notify('f 刚刚被释放')
            elif e.action.keydown:
                ui.notify('f 刚刚被按下')
        if e.modifiers.shift and e.action.keydown:
            if e.key.arrow_left:
                ui.notify('向左')
            elif e.key.arrow_right:
                ui.notify('向右')
            elif e.key.arrow_up:
                ui.notify('向上')
            elif e.key.arrow_down:
                ui.notify('向下')

    keyboard = ui.keyboard(on_key=handle_key)
    ui.label('键盘事件可以通过使用键盘元素全局捕获。')
    ui.checkbox('跟踪键盘事件').bind_value_to(keyboard, 'active')


doc.reference(ui.keyboard)
