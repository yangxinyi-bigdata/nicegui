from nicegui import ui, ElementFilter

from . import doc


@doc.demo(ui.aggrid)
def main_demo() -> None:
    grid = ui.aggrid({
        'defaultColDef': {'flex': 1},
        'columnDefs': [
            {'headerName': 'Name', 'field': 'name'},
            {'headerName': 'Age', 'field': 'age'},
            {'headerName': 'Parent', 'field': 'parent', 'hide': True},
        ],
        'rowData': [
            {'name': 'Alice', 'age': 18, 'parent': 'David'},
            {'name': 'Bob', 'age': 21, 'parent': 'Eve'},
            {'name': 'Carol', 'age': 42, 'parent': 'Frank'},
        ],
        'rowSelection': 'multiple',
    }).classes('max-h-40')

    def update():
        grid.options['rowData'][0]['age'] += 1
        grid.update()

    ui.button('Update', on_click=update)
    ui.button('Select all', on_click=lambda: grid.run_grid_method('selectAll'))
    ui.button('Show parent', on_click=lambda: grid.run_grid_method('setColumnsVisible', ['parent'], True))


@doc.demo('选择AG网格行', '''
    您可以添加复选框到网格单元格以允许用户选择单行或多行。

    要检索当前选中的行，请使用 `get_selected_rows` 方法。
    该方法返回一个包含行的字典列表。

    如果 `rowSelection` 设置为 `'single'` 或要获取第一个选中的行，
    您也可以使用 `get_selected_row` 方法。
    该方法返回单个行的字典，如果没有选中行则返回 `None`。

    有关更多信息，请参阅 [AG Grid 文档](https://www.ag-grid.com/javascript-data-grid/row-selection/#example-single-row-selection)。
''')
def aggrid_with_selectable_rows():
    # @ui.page('/')
    def page():
        grid = ui.aggrid({
            'columnDefs': [
                {'headerName': 'Name', 'field': 'name', 'checkboxSelection': True},
                {'headerName': 'Age', 'field': 'age'},
            ],
            'rowData': [
                {'name': 'Alice', 'age': 18},
                {'name': 'Bob', 'age': 21},
                {'name': 'Carol', 'age': 42},
            ],
            'rowSelection': 'multiple',
        }).classes('max-h-40')

        async def output_selected_rows():
            rows = await grid.get_selected_rows()
            if rows:
                for row in rows:
                    ui.notify(f"{row['name']}, {row['age']}")
            else:
                ui.notify('没有选择任何行。')

        async def output_selected_row():
            row = await grid.get_selected_row()
            if row:
                ui.notify(f"{row['name']}, {row['age']}")
            else:
                ui.notify('没有选择行！')

        ui.button('输出选中的行', on_click=output_selected_rows)
        ui.button('输出选中的行', on_click=output_selected_row)
    page()  # HIDE


@doc.demo('使用迷你过滤器过滤行', '''
    您可以添加 [迷你过滤器](https://ag-grid.com/javascript-data-grid/filter-set-mini-filter/)
    到每列的标题来过滤行。

    注意 "agTextColumnFilter" 如何匹配单个字符，比如 "Alice" 和 "Carol" 中的 "a"，
    而 "agNumberColumnFilter" 匹配整个数字，比如 "18" 和 "21"，但不匹配 "1"。
''')
def aggrid_with_minifilters():
    ui.aggrid({
        'columnDefs': [
            {'headerName': 'Name', 'field': 'name', 'filter': 'agTextColumnFilter', 'floatingFilter': True},
            {'headerName': 'Age', 'field': 'age', 'filter': 'agNumberColumnFilter', 'floatingFilter': True},
        ],
        'rowData': [
            {'name': 'Alice', 'age': 18},
            {'name': 'Bob', 'age': 21},
            {'name': 'Carol', 'age': 42},
        ],
    }).classes('max-h-40')


@doc.demo('具有条件单元格格式的AG网格', '''
    此演示展示了如何使用 [cellClassRules](https://www.ag-grid.com/javascript-grid-cell-styles/#cell-class-rules)
    根据单元格的值进行条件格式化。
''')
def aggrid_with_conditional_cell_formatting():
    ui.aggrid({
        'columnDefs': [
            {'headerName': 'Name', 'field': 'name'},
            {'headerName': 'Age', 'field': 'age', 'cellClassRules': {
                'bg-red-300': 'x < 21',
                'bg-green-300': 'x >= 21',
            }},
        ],
        'rowData': [
            {'name': 'Alice', 'age': 18},
            {'name': 'Bob', 'age': 21},
            {'name': 'Carol', 'age': 42},
        ],
    })


@doc.demo('从Pandas DataFrame创建网格', '''
    您可以使用 `from_pandas` 方法从Pandas DataFrame创建AG网格。
    该方法接受Pandas DataFrame作为输入并返回一个AG网格。
''')
def aggrid_from_pandas():
    import pandas as pd

    df = pd.DataFrame(data={'col1': [1, 2], 'col2': [3, 4]})
    ui.aggrid.from_pandas(df).classes('max-h-40')


@doc.demo('从Polars DataFrame创建网格', '''
    您可以使用 `from_polars` 方法从Polars DataFrame创建AG网格。
    该方法接受Polars DataFrame作为输入并返回一个AG网格。

    *2.7.0版本新增*
''')
def aggrid_from_polars():
    import polars as pl

    df = pl.DataFrame(data={'col1': [1, 2], 'col2': [3, 4]})
    ui.aggrid.from_polars(df).classes('max-h-40')


@doc.demo('将列渲染为HTML', '''
    您可以通过将列索引列表传递给 `html_columns` 参数来将列渲染为HTML。
''')
def aggrid_with_html_columns():
    ui.aggrid({
        'columnDefs': [
            {'headerName': 'Name', 'field': 'name'},
            {'headerName': 'URL', 'field': 'url'},
        ],
        'rowData': [
            {'name': 'Google', 'url': '<a href="https://google.com">https://google.com</a>'},
            {'name': 'Facebook', 'url': '<a href="https://facebook.com">https://facebook.com</a>'},
        ],
    }, html_columns=[1])


@doc.demo('响应AG网格事件', '''
    所有AG网格事件都通过AG网格全局监听器传递给NiceGUI。
    这些事件可以使用 `.on()` 方法订阅。
''')
def aggrid_respond_to_event():
    ui.aggrid({
        'columnDefs': [
            {'headerName': 'Name', 'field': 'name'},
            {'headerName': 'Age', 'field': 'age'},
        ],
        'rowData': [
            {'name': 'Alice', 'age': 18},
            {'name': 'Bob', 'age': 21},
            {'name': 'Carol', 'age': 42},
        ],
    }).on('cellClicked', lambda event: ui.notify(f'单元格值: {event.args["value"]}'))


@doc.demo('具有复杂对象的AG网格', '''
    您可以通过用句点分隔字段名在AG网格中使用嵌套的复杂对象。
    (这就是为什么 `rowData` 中的键不允许包含句号的原因。)
''')
def aggrid_with_complex_objects():
    ui.aggrid({
        'columnDefs': [
            {'headerName': '名字', 'field': 'name.first'},
            {'headerName': '姓氏', 'field': 'name.last'},
            {'headerName': 'Age', 'field': 'age'}
        ],
        'rowData': [
            {'name': {'first': 'Alice', 'last': 'Adams'}, 'age': 18},
            {'name': {'first': 'Bob', 'last': 'Brown'}, 'age': 21},
            {'name': {'first': 'Carol', 'last': 'Clark'}, 'age': 42},
        ],
    }).classes('max-h-40')


@doc.demo('具有动态行高的AG网格', '''
    您可以通过将函数传递给 `getRowHeight` 参数来设置单个行的高度。
''')
def aggrid_with_dynamic_row_height():
    ui.aggrid({
        'columnDefs': [{'field': 'name'}, {'field': 'age'}],
        'rowData': [
            {'name': 'Alice', 'age': '18'},
            {'name': 'Bob', 'age': '21'},
            {'name': 'Carol', 'age': '42'},
        ],
        ':getRowHeight': 'params => params.data.age > 35 ? 50 : 25',
    }).classes('max-h-40')


@doc.demo('运行行方法', '''
    您可以使用 `run_row_method` 方法在单个行上运行方法。
    该方法接受行ID、方法名和方法参数作为参数。
    行ID可以是行索引（作为字符串）或 `getRowId` 函数的值。

    以下演示展示了如何使用它来更新单元格值。
    注意，当值更新时，行选择会被保留。
    如果使用 `update` 方法更新网格，情况就不是这样了。
''')
def aggrid_run_row_method():
    grid = ui.aggrid({
        'columnDefs': [
            {'field': 'name', 'checkboxSelection': True},
            {'field': 'age'},
        ],
        'rowData': [
            {'name': 'Alice', 'age': 18},
            {'name': 'Bob', 'age': 21},
            {'name': 'Carol', 'age': 42},
        ],
        ':getRowId': '(params) => params.data.name',
    })
    ui.button('Update',
              on_click=lambda: grid.run_row_method('Alice', 'setDataValue', 'age', 99))


@doc.demo('过滤返回值', '''
    您可以通过传递定义JavaScript函数的字符串来过滤方法调用的返回值。
    此演示运行网格方法 "getDisplayedRowAtIndex" 并返回结果的 "data" 属性。

    注意，从客户端请求数据仅支持页面函数，不支持共享的自动索引页面。
''')
def aggrid_filter_return_values():
    # @ui.page('/')
    def page():
        grid = ui.aggrid({
            'columnDefs': [{'field': 'name'}],
            'rowData': [{'name': 'Alice'}, {'name': 'Bob'}],
        })

        async def get_first_name() -> None:
            row = await grid.run_grid_method('g => g.getDisplayedRowAtIndex(0).data')
            ui.notify(row['name'])

        ui.button('获取名字', on_click=get_first_name)
    page()  # HIDE


@doc.demo('处理主题更改', '''
    您可以通过添加或删除类来更改AG网格的主题。
    此演示展示了如何使用开关来更改主题。
''')
def aggrid_handle_theme_change():
    from nicegui import events

    grid = ui.aggrid({})

    def handle_theme_change(e: events.ValueChangeEventArguments):
        grid.classes(add='ag-theme-balham-dark' if e.value else 'ag-theme-balham',
                     remove='ag-theme-balham ag-theme-balham-dark')

    ui.switch('深色', on_change=handle_theme_change)


doc.reference(ui.aggrid)
