from nicegui import ui

from . import doc


@doc.demo(ui.select)
def main_demo() -> None:
    select1 = ui.select([1, 2, 3], value=1)
    select2 = ui.select({1: 'One', 2: 'Two', 3: 'Three'}).bind_value(select1, 'value')


@doc.demo('边输入边搜索', '''
    您可以激活 `with_input` 来获得一个带有自动完成功能的文本输入框。
    选项将在您输入时被过滤。
''')
def search_as_you_type():
    continents = [
        'Asia',
        'Africa',
        'Antarctica',
        'Europe',
        'Oceania',
        'North America',
        'South America',
    ]
    ui.select(options=continents, with_input=True,
              on_change=lambda e: ui.notify(e.value)).classes('w-40')


@doc.demo('多选', '''
    您可以激活 `multiple` 来允许选择多个项目。
''')
def multi_select():
    names = ['Alice', 'Bob', 'Carol']
    ui.select(names, multiple=True, value=names[:2], label='comma-separated') \
        .classes('w-64')
    ui.select(names, multiple=True, value=names[:2], label='with chips') \
        .classes('w-64').props('use-chips')


@doc.demo('更新选项', '''
    可以使用 `options` 属性更改选项。
    但之后您还需要调用 `update()` 使更改生效。
    `set_options` 是一个快捷方式，它同时执行这两个操作，适用于 lambda 函数。
''')
def update_selection():
    select = ui.select([1, 2, 3], value=1)
    with ui.row():
        ui.button('4, 5, 6', on_click=lambda: select.set_options([4, 5, 6], value=4))
        ui.button('1, 2, 3', on_click=lambda: select.set_options([1, 2, 3], value=1))


doc.reference(ui.select)
