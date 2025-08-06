from nicegui import ui

from . import doc


@doc.demo(ui.time)
def main_demo() -> None:
    ui.time(value='12:00', on_change=lambda e: result.set_text(e.value))
    result = ui.label()


@doc.demo('带时间选择器的输入元素', '''
    本演示展示如何实现一个带时间选择器的输入元素。
    我们在输入元素的append插槽中放置一个图标。
    当点击图标时，我们打开一个包含时间选择器的菜单。
    使用[QMenu](https://quasar.dev/vue-components/menu)的"no-parent-event"属性
    来防止在点击输入字段时打开菜单。
    由于菜单默认不带有"关闭"按钮，我们为了方便添加了一个。

    时间与输入元素的值绑定。
    因此，每当时间更改时，输入元素和时间选择器都会保持同步。
''')
def time_picker_demo():
    with ui.input('时间') as time:
        with ui.menu().props('no-parent-event') as menu:
            with ui.time().bind_value(time):
                with ui.row().classes('justify-end'):
                    ui.button('关闭', on_click=menu.close).props('flat')
        with time.add_slot('append'):
            ui.icon('access_time').on('click', menu.open).classes('cursor-pointer')


doc.reference(ui.time)
