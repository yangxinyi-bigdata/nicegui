from nicegui import ui

from . import doc


@doc.demo(ui.slider)
def main_demo() -> None:
    slider = ui.slider(min=0, max=100, value=50)
    ui.label().bind_text_from(slider, 'value')


@doc.demo('使用前导和后续选项限制事件', '''
    默认情况下，滑块的值变化事件被限制为 0.05 秒。
    这意味着如果您快速移动滑块，值只会每 0.05 秒更新一次。

    默认情况下，"前导"和"后续"事件都被激活。
    这意味着第一个事件会立即触发，最后一个事件会在限制时间后触发。

    这个演示展示了禁用这些选项中的任何一个如何改变行为。
    为了更清楚地看到效果，限制时间设置为 1 秒。
    第一个滑块显示默认行为，第二个只发送前导事件，第三个只发送后续事件。
''')
def throttle_events_with_leading_and_trailing_options():
    ui.label('default')
    ui.slider(min=0, max=10, step=0.1, value=5).props('label-always') \
        .on('update:model-value', lambda e: ui.notify(e.args),
            throttle=1.0)

    ui.label('leading events only')
    ui.slider(min=0, max=10, step=0.1, value=5).props('label-always') \
        .on('update:model-value', lambda e: ui.notify(e.args),
            throttle=1.0, trailing_events=False)

    ui.label('trailing events only')
    ui.slider(min=0, max=10, step=0.1, value=5).props('label-always') \
        .on('update:model-value', lambda e: ui.notify(e.args),
            throttle=1.0, leading_events=False)


@doc.demo('禁用滑块', '''
    您可以使用 `disable()` 方法禁用滑块。
    这将阻止用户移动滑块。
    滑块也会变为灰色。
''')
def disable_slider():
    slider = ui.slider(min=0, max=100, value=50)
    ui.button('Disable slider', on_click=slider.disable)
    ui.button('Enable slider', on_click=slider.enable)


doc.reference(ui.slider)
