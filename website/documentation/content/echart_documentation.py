from nicegui import ui

from . import doc


@doc.demo(ui.echart)
def main_demo() -> None:
    from random import random

    echart = ui.echart({
        'xAxis': {'type': 'value'},
        'yAxis': {'type': 'category', 'data': ['A', 'B'], 'inverse': True},
        'legend': {'textStyle': {'color': 'gray'}},
        'series': [
            {'type': 'bar', 'name': 'Alpha', 'data': [0.1, 0.2]},
            {'type': 'bar', 'name': 'Beta', 'data': [0.3, 0.4]},
        ],
    })

    def update():
        echart.options['series'][0]['data'][0] = random()
        echart.update()

    ui.button('更新', on_click=update)


@doc.demo('带有点击功能的EChart', '''
    您可以为系列点被点击时的事件注册回调函数。
''')
def clickable_points() -> None:
    ui.echart({
        'xAxis': {'type': 'category'},
        'yAxis': {'type': 'value'},
        'series': [{'type': 'line', 'data': [20, 10, 30, 50, 40, 30]}],
    }, on_point_click=ui.notify)


@doc.demo('带有动态属性的EChart', '''
    动态属性可以传递给图表元素以进行自定义，例如应用轴标签格式。
    要使属性成为动态属性，请在属性名称前加冒号":"。
''')
def dynamic_properties() -> None:
    ui.echart({
        'xAxis': {'type': 'category'},
        'yAxis': {'axisLabel': {':formatter': 'value => "$" + value'}},
        'series': [{'type': 'line', 'data': [5, 8, 13, 21, 34, 55]}],
    })


@doc.demo('带有自定义主题的EChart', '''
    您可以应用使用[主题构建器](https://echarts.apache.org/en/theme-builder.html)创建的自定义主题。

    除了将主题作为字典传递，您还可以传递JSON文件的URL。
    这允许浏览器缓存主题，并在多次使用同一主题时更快地加载。

    *在版本2.15.0中新增*
''')
def custom_theme() -> None:
    ui.echart({
        'xAxis': {'type': 'category'},
        'yAxis': {'type': 'value'},
        'series': [{'type': 'bar', 'data': [20, 10, 30, 50, 40, 30]}],
    }, theme={
        'color': ['#b687ac', '#28738a', '#a78f8f'],
        'backgroundColor': 'rgba(254,248,239,1)',
    })


@doc.demo('来自pyecharts的EChart', '''
    您可以使用`from_pyecharts`方法从pyecharts对象创建EChart元素。
    对于定义格式化函数等动态选项，您可以使用`pyecharts.commons.utils`中的`JsCode`类。
    或者，您可以使用冒号":"作为属性名称的前缀，以指示该值是JavaScript表达式。
''')
def echart_from_pyecharts_demo():
    from pyecharts.charts import Bar
    from pyecharts.commons.utils import JsCode
    from pyecharts.options import AxisOpts

    ui.echart.from_pyecharts(
        Bar()
        .add_xaxis(['A', 'B', 'C'])
        .add_yaxis('ratio', [1, 2, 4])
        .set_global_opts(
            xaxis_opts=AxisOpts(axislabel_opts={
                ':formatter': r'(val, idx) => `group ${val}`',
            }),
            yaxis_opts=AxisOpts(axislabel_opts={
                'formatter': JsCode(r'(val, idx) => `${val}%`'),
            }),
        )
    )


@doc.demo('运行方法', '''
    您可以使用`run_chart_method`方法运行EChart实例的方法。
    此演示展示了如何显示和隐藏加载动画，如何获取图表的当前宽度，
    以及如何添加带有自定义格式化器的工具提示。

    方法名称"setOption"前面的冒号":"表示参数是一个JavaScript表达式，
    该表达式在客户端上计算后再传递给方法。

    请注意，从客户端请求数据仅支持页面函数，不支持共享的自动索引页面。
''')
def methods_demo() -> None:
    # @ui.page('/')
    def page():
        echart = ui.echart({
            'xAxis': {'type': 'category', 'data': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']},
            'yAxis': {'type': 'value'},
            'series': [{'type': 'line', 'data': [150, 230, 224, 218, 135]}],
        })

        ui.button('显示加载', on_click=lambda: echart.run_chart_method('showLoading'))
        ui.button('隐藏加载', on_click=lambda: echart.run_chart_method('hideLoading'))

        async def get_width():
            width = await echart.run_chart_method('getWidth')
            ui.notify(f'Width: {width}')
        ui.button('获取宽度', on_click=get_width)

        ui.button('设置工具提示', on_click=lambda: echart.run_chart_method(
            ':setOption', r'{tooltip: {formatter: params => "$" + params.value}}',
        ))
    page()  # HIDE


@doc.demo('任意图表事件', '''
    您可以使用`on`方法和"chart:"前缀为图表注册任意事件监听器。
    此演示展示了如何为"selectchanged"事件注册回调，该事件在用户选择点时触发。
''')
def events_demo() -> None:
    ui.echart({
        'toolbox': {'feature': {'brush': {'type': ['rect']}}},
        'brush': {},
        'xAxis': {'type': 'category'},
        'yAxis': {'type': 'value'},
        'series': [{'type': 'line', 'data': [1, 2, 3]}],
    }).on('chart:selectchanged', lambda e: label.set_text(
        f'Selected point {e.args["fromActionPayload"]["dataIndexInside"]}'
    ))
    label = ui.label()


@doc.demo('3D绘图', '''
    如果初始选项包含字符串"3D"，图表将自动启用3D功能。
    如果没有，请将`enable_3d`参数设置为`True`。
''')
def echarts_gl_demo() -> None:
    ui.echart({
        'xAxis3D': {},
        'yAxis3D': {},
        'zAxis3D': {},
        'grid3D': {},
        'series': [{
            'type': 'line3D',
            'data': [[1, 1, 1], [3, 3, 3]],
        }],
    })


doc.reference(ui.echart)
