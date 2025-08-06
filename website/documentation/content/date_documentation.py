from nicegui import ui

from . import doc


@doc.demo(ui.date)
def main_demo() -> None:
    ui.date(value='2023-01-01', on_change=lambda e: result.set_text(e.value))
    result = ui.label()


@doc.demo('带日期选择器的输入元素', '''
    本演示展示如何实现一个带日期选择器的输入元素。
    我们在输入元素的append插槽中放置一个图标。
    当点击图标时，我们打开一个包含日期选择器的菜单。
    使用[QMenu](https://quasar.dev/vue-components/menu)的"no-parent-event"属性
    来防止在点击输入字段时打开菜单。
    由于菜单默认不带有"关闭"按钮，我们为了方便添加了一个。

    日期与输入元素的值绑定。
    因此，每当日期更改时，输入元素和日期选择器都会保持同步。
''')
def date_picker_demo():
    with ui.input('日期') as date:
        with ui.menu().props('no-parent-event') as menu:
            with ui.date().bind_value(date):
                with ui.row().classes('justify-end'):
                    ui.button('关闭', on_click=menu.close).props('flat')
        with date.add_slot('append'):
            ui.icon('edit_calendar').on('click', menu.open).classes('cursor-pointer')


@doc.demo('日期范围输入', '''
    您可以使用"range"属性来选择日期范围。
    `value`将是一个包含"from"和"to"键的字典。
    以下演示展示如何将日期范围选择器绑定到输入元素，
    使用`forward`和`backward`函数在日期选择器的字典和输入字符串之间进行转换。
''')
def date_range_input():
    date_input = ui.input('日期范围').classes('w-40')
    ui.date().props('range').bind_value(
        date_input,
        forward=lambda x: f'{x["from"]} - {x["to"]}' if x else None,
        backward=lambda x: {
            'from': x.split(' - ')[0],
            'to': x.split(' - ')[1],
        } if ' - ' in (x or '') else None,
    )


@doc.demo('日期过滤器', '''
    本演示展示如何在日期选择器中过滤日期。
    为了向日期选择器传递函数，我们使用`:options`属性。
    前导的`:`告诉NiceGUI该值是一个JavaScript表达式。
''')
def date_filter():
    ui.date().props('''default-year-month=2023/01 :options="date => date <= '2023/01/15'"''')


doc.reference(ui.date)
