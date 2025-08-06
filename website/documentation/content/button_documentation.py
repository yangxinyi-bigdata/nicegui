from nicegui import ui

from . import doc


@doc.demo(ui.button)
def main_demo() -> None:
    ui.button('Click me!', on_click=lambda: ui.notify('你点击了我！'))


@doc.demo('图标', '''
    您也可以为按钮添加图标。
''')
def icons() -> None:
    with ui.row():
        ui.button('demo', icon='history')
        ui.button(icon='thumb_up')
        with ui.button():
            ui.label('子元素')
            ui.image('https://picsum.photos/id/377/640/360') \
                .classes('rounded-full w-16 h-16 ml-4')


@doc.demo('等待按钮点击', '''
    有时等待按钮点击后再继续执行是很方便的。
''')
async def await_button_click() -> None:
    # @ui.page('/')
    # async def index():
    with ui.column():  # HIDE
        b = ui.button('Step')
        await b.clicked()
        ui.label('One')
        await b.clicked()
        ui.label('Two')
        await b.clicked()
        ui.label('Three')


@doc.demo('使用上下文管理器禁用按钮', '''
    这展示了一个上下文管理器，可用于在异步过程期间禁用按钮。
''')
def disable_context_manager() -> None:
    from contextlib import contextmanager

    import httpx

    @contextmanager
    def disable(button: ui.button):
        button.disable()
        try:
            yield
        finally:
            button.enable()

    async def get_slow_response(button: ui.button) -> None:
        with disable(button):
            async with httpx.AsyncClient() as client:
                response = await client.get('https://httpbin.org/delay/1', timeout=5)
                ui.notify(f'Response code: {response.status_code}')

    ui.button('获得缓慢响应', on_click=lambda e: get_slow_response(e.sender))


@doc.demo('自定义切换按钮', '''
    就像所有其他元素一样，您可以实现自己的子类，包含专门的逻辑。
    比如这个带有内部布尔状态的红/绿切换按钮。
''')
def toggle_button() -> None:
    class ToggleButton(ui.button):

        def __init__(self, *args, **kwargs) -> None:
            super().__init__(*args, **kwargs)
            self._state = False
            self.on('click', self.toggle)

        def toggle(self) -> None:
            """切换按钮状态。"""
            self._state = not self._state
            self.update()

        def update(self) -> None:
            self.props(f'color={"green" if self._state else "red"}')
            super().update()

    ToggleButton('Toggle me')


@doc.demo('悬浮操作按钮', '''
    如 [Quasar 文档](https://quasar.dev/vue-components/floating-action-button) 中所述，
    悬浮操作按钮 (FAB) 只是一个内部包含按钮的"页面固定"元素。
    使用 "fab" 属性，按钮将变为圆形并获得阴影。
    颜色可以自由选择，但通常是强调色。
''')
def fab() -> None:
    ui.colors(accent='#6AD4DD')
    # with ui.page_sticky(x_offset=18, y_offset=18):
    with ui.row().classes('w-full h-full justify-end items-end'):  # HIDE
        ui.button(icon='home', on_click=lambda: ui.notify('home')) \
            .props('fab color=accent')


doc.text('可展开的浮动操作按钮', '''
    要创建一个具有多个操作的浮动操作按钮 (FAB)，当点击 FAB 时会显示这些操作，
    您可以使用 [`ui.fab` 和 `ui.fab_action`](fab) 元素，
    它们基于 [Quasar 的 QFab 组件](https://quasar.dev/vue-components/floating-action-button)。
''')

doc.reference(ui.button)
