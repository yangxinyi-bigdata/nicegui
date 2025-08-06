from nicegui import ui

from . import doc


@doc.demo(ui.timer)
def main_demo() -> None:
    from datetime import datetime

    label = ui.label()
    ui.timer(1.0, lambda: label.set_text(f'{datetime.now():%X}'))


@doc.demo('激活、停用和取消计时器', '''
    您可以使用 `active` 属性激活和停用计时器。
    您可以使用 `cancel` 方法取消计时器。
    取消计时器后，它无法再被激活。
''')
def activate_deactivate_demo():
    slider = ui.slider(min=0, max=1, value=0.5)
    timer = ui.timer(0.1, lambda: slider.set_value((slider.value + 0.01) % 1.0))
    ui.switch('激活').bind_value_to(timer, 'active')
    ui.button('取消', on_click=timer.cancel)


@doc.demo('延迟后调用函数', '''
    您可以使用带有 `once` 参数的计时器延迟后调用函数。
''')
def call_after_delay_demo():
    def handle_click():
        ui.timer(1.0, lambda: ui.notify('嗨！'), once=True)
    ui.button('1秒后通知', on_click=handle_click)


@doc.demo("不立即开始", '''
    默认情况下，计时器会立即开始。
    您可以通过将 `immediate` 参数设置为 `False` 来改变这种行为。
    这将延迟回调函数的第一次执行指定的间隔时间。

    *在版本 2.9.0 中新增*
''')
def start_immediately_demo():
    from datetime import datetime

    label = ui.label()
    ui.timer(1.0, lambda: label.set_text(f'{datetime.now():%X}'), immediate=False)


@doc.demo('全局应用计时器', '''
    虽然 `ui.timer` 是一种在当前页面上下文中运行的 UI 元素，
    您也可以使用全局的 `app.timer` 创建独立于 UI 的计时器。

    *在版本 2.9.0 中新增*
''')
def app_timer_demo():
    from nicegui import app

    counter = {'value': 0}
    app.timer(1.0, lambda: counter.update(value=counter['value'] + 1))

    # @ui.page('/')
    def page():
        ui.label().bind_text_from(counter, 'value', lambda value: f'计数: {value}')
    page()  # HIDE


doc.reference(ui.timer)
