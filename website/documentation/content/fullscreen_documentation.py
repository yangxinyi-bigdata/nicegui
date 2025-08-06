from nicegui import ui

from . import doc


@doc.demo(ui.fullscreen)
def main_demo() -> None:
    fullscreen = ui.fullscreen()

    ui.button('进入全屏', on_click=fullscreen.enter)
    ui.button('退出全屏', on_click=fullscreen.exit)
    ui.button('切换全屏', on_click=fullscreen.toggle)


@doc.demo('需要长按退出', '''
    您可以要求用户长按退出键来退出全屏模式。
    这对于防止意外退出很有用，例如在处理表单或编辑数据时。

    请注意，此功能仅在某些浏览器（如Google Chrome或Microsoft Edge）中有效。
''')
def long_press_demo():
    fullscreen = ui.fullscreen()
    ui.switch('需要长按退出').bind_value_to(fullscreen, 'require_escape_hold')
    ui.button('切换全屏', on_click=fullscreen.toggle)


@doc.demo('跟踪全屏状态', '''
    您可以跟踪全屏状态何时更改。

    请注意，出于安全原因，全屏模式只能从先前的用户交互（如按钮点击）进入。
''')
def state_demo():
    fullscreen = ui.fullscreen(
        on_value_change=lambda e: ui.notify('进入' if e.value else '退出')
    )
    ui.button('切换全屏', on_click=fullscreen.toggle)
    ui.label().bind_text_from(fullscreen, 'state',
                              lambda state: '全屏' if state else '')


doc.reference(ui.fullscreen)
