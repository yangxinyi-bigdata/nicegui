from nicegui import ui

from . import doc


@doc.demo(ui.highchart)
def main_demo() -> None:
    from random import random

    chart = ui.highchart({
        'title': False,
        'chart': {'type': 'bar'},
        'xAxis': {'categories': ['A', 'B']},
        'series': [
            {'name': 'Alpha', 'data': [0.1, 0.2]},
            {'name': 'Beta', 'data': [0.3, 0.4]},
        ],
    }).classes('w-full h-64')

    def update():
        chart.options['series'][0]['data'][0] = random()
        chart.update()

    ui.button('更新', on_click=update)


@doc.demo('带有额外依赖的图表', '''
    要使用默认依赖中未包含的图表类型，您可以指定额外的依赖。
    此演示展示了一个实体仪表图表。
''')
def extra_dependencies() -> None:
    ui.highchart({
        'title': False,
        'chart': {'type': 'solidgauge'},
        'yAxis': {
            'min': 0,
            'max': 1,
        },
        'series': [
            {'data': [0.42]},
        ],
    }, extras=['solid-gauge']).classes('w-full h-64')


@doc.demo('带有可拖动点的图表', '''
    此图表允许拖动系列点。
    您可以为以下事件注册回调函数：

    - `on_point_click`: 当点被点击时调用
    - `on_point_drag_start`: 当点开始拖动时调用
    - `on_point_drag`: 当点被拖动时调用
    - `on_point_drop`: 当点被放下时调用
''')
def drag() -> None:
    ui.highchart(
        {
            'title': False,
            'plotOptions': {
                'series': {
                    'stickyTracking': False,
                    'dragDrop': {'draggableY': True, 'dragPrecisionY': 1},
                },
            },
            'series': [
                {'name': 'A', 'data': [[20, 10], [30, 20], [40, 30]]},
                {'name': 'B', 'data': [[50, 40], [60, 50], [70, 60]]},
            ],
        },
        extras=['draggable-points'],
        on_point_click=lambda e: ui.notify(f'Click: {e}'),
        on_point_drag_start=lambda e: ui.notify(f'Drag start: {e}'),
        on_point_drop=lambda e: ui.notify(f'Drop: {e}')
    ).classes('w-full h-64')


doc.reference(ui.highchart)
