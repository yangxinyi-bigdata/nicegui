from nicegui import ui

from . import doc


@doc.demo(ui.circular_progress)
def main_demo() -> None:
    slider = ui.slider(min=0, max=1, step=0.01, value=0.5)
    ui.circular_progress().bind_value_from(slider, 'value')


@doc.demo('嵌套元素', '''
    您可以使用 `with` 语句在圆形进度条中放置任何元素，如图标、按钮等。
    只需确保它适合边界并禁用显示值的默认行为。
''')
def icon() -> None:
    with ui.row().classes('items-center m-auto'):
        with ui.circular_progress(value=0.1, show_value=False) as progress:
            ui.button(
                icon='star',
                on_click=lambda: progress.set_value(progress.value + 0.1)
            ).props('flat round')
        ui.label('点击增加进度')


doc.reference(ui.circular_progress)
