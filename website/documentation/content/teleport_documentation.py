from nicegui import ui

from . import doc


@doc.demo(ui.teleport)
def main_demo() -> None:
    markdown = ui.markdown('输入您的**姓名**!')

    def inject_input():
        with ui.teleport(f'#{markdown.html_id} strong'):
            ui.input('姓名').classes('inline-flex').props('dense outlined')

    ui.button('注入输入框', on_click=inject_input)


@doc.demo('带有任意内容的单选按钮元素', '''
    使用正确的CSS选择器，您可以将任何内容放置在标准单选按钮元素内部。
''')
def arbitrary_content():
    options = ['Star', 'Thump Up', 'Heart']
    radio = ui.radio({x: '' for x in options}, value='Star').props('inline')
    with ui.teleport(f'#{radio.html_id} > div:nth-child(1) .q-radio__label'):
        ui.icon('star', size='md')
    with ui.teleport(f'#{radio.html_id} > div:nth-child(2) .q-radio__label'):
        ui.icon('thumb_up', size='md')
    with ui.teleport(f'#{radio.html_id} > div:nth-child(3) .q-radio__label'):
        ui.icon('favorite', size='md')
    ui.label().bind_text_from(radio, 'value')


@doc.demo('向表格单元格注入图表', '''
    此演示展示了如何将ECharts图表注入到表格单元格中。
''')
def graph_in_table():
    columns = [
        {'name': 'name', 'label': 'Product', 'field': 'name', 'align': 'center'},
        {'name': 'sales', 'label': 'Sales', 'field': 'sales', 'align': 'center'},
    ]
    rows = [
        {'name': 'A', 'data': [10, 8, 2, 4]},
        {'name': 'B', 'data': [3, 5, 7, 8]},
        {'name': 'C', 'data': [2, 1, 3, 7]},
    ]
    table = ui.table(columns=columns, rows=rows, row_key='name').classes('w-72')
    for r, row in enumerate(rows):
        with ui.teleport(f'#{table.html_id} tr:nth-child({r+1}) td:nth-child(2)'):
            ui.echart({
                'xAxis': {'type': 'category', 'show': False},
                'yAxis': {'type': 'value', 'show': False},
                'series': [{'type': 'line', 'data': row['data']}],
            }).classes('w-44 h-20')


doc.reference(ui.teleport)
