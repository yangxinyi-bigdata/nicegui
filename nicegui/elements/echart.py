from typing import Callable, Dict, Literal, Optional, Union

from typing_extensions import Self

from .. import optional_features
from ..awaitable_response import AwaitableResponse
from ..element import Element
from ..events import EChartPointClickEventArguments, GenericEventArguments, Handler, handle_event

try:
    from pyecharts.charts.base import default, json
    from pyecharts.charts.chart import Base as Chart
    from pyecharts.commons.utils import JsCode
    JS_CODE_MARKER = JsCode('\n').js_code.split('\n')[0]
    optional_features.register('pyecharts')
except ImportError:
    pass


class EChart(Element,
             component='echart.js',
             dependencies=['lib/echarts/echarts.min.js', 'lib/echarts-gl/echarts-gl.min.js'],
             default_classes='nicegui-echart'):

    def __init__(self,
                 options: Dict,
                 on_point_click: Optional[Handler[EChartPointClickEventArguments]] = None, *,
                 enable_3d: bool = False,
                 renderer: Literal['canvas', 'svg'] = 'canvas',
                 theme: Optional[Union[str, Dict]] = None,
                 ) -> None:
        """Apache EChart图表

        使用`ECharts <https://echarts.apache.org/>`_创建图表的元素。
        可以通过更改`options`属性将更新推送到图表。
        数据更改后，调用`update`方法刷新图表。

        :param options: EChart选项字典
        :param on_click_point: 当点击点时调用的回调函数
        :param enable_3d: 强制导入echarts-gl库
        :param renderer: 使用的渲染器（"canvas"或"svg"，*在版本2.7.0中添加*）
        :param theme: EChart主题配置（字典或返回JSON对象的URL，*在版本2.15.0中添加*）
        """
        super().__init__()
        self._props['options'] = options
        self._props['enable_3d'] = enable_3d or any('3D' in key for key in options)
        self._props['renderer'] = renderer
        self._props['theme'] = theme
        self._update_method = 'update_chart'

        if on_point_click:
            self.on_point_click(on_point_click)

    def on_point_click(self, callback: Handler[EChartPointClickEventArguments]) -> Self:
        """添加点击点时要调用的回调函数。"""
        def handle_point_click(e: GenericEventArguments) -> None:
            handle_event(callback, EChartPointClickEventArguments(
                sender=self,
                client=self.client,
                component_type=e.args['componentType'],
                series_type=e.args['seriesType'],
                series_index=e.args['seriesIndex'],
                series_name=e.args['seriesName'],
                name=e.args['name'],
                data_index=e.args['dataIndex'],
                data=e.args['data'],
                data_type=e.args.get('dataType'),
                value=e.args['value'],
            ))
        self.on('pointClick', handle_point_click, [
            'componentType',
            'seriesType',
            'seriesIndex',
            'seriesName',
            'name',
            'dataIndex',
            'data',
            'dataType',
            'value',
        ])
        return self

    @classmethod
    def from_pyecharts(cls, chart: 'Chart', on_point_click: Optional[Callable] = None) -> Self:
        """从pyecharts对象创建echart元素。

        :param chart: pyecharts图表对象
        :param on_click_point: 点击点时调用的回调函数

        :return: echart元素
        """
        options = json.loads(json.dumps(chart.get_options(), default=default, ignore_nan=True))
        stack = [options]
        while stack:
            current = stack.pop()
            if isinstance(current, list):
                stack.extend(current)
            elif isinstance(current, dict):
                for key, value in tuple(current.items()):
                    if isinstance(value, str) and value.startswith(JS_CODE_MARKER) and value.endswith(JS_CODE_MARKER):
                        current[f':{key}'] = current.pop(key)[len(JS_CODE_MARKER):-len(JS_CODE_MARKER)]
                    else:
                        stack.append(value)
        return cls(options, on_point_click)

    @property
    def options(self) -> Dict:
        """选项字典。"""
        return self._props['options']

    def run_chart_method(self, name: str, *args, timeout: float = 1) -> AwaitableResponse:
        """运行EChart实例的方法。

        有关方法列表，请参见`ECharts文档 <https://echarts.apache.org/en/api.html#echartsInstance>`_。

        如果函数被等待，则返回方法调用的结果。
        否则，方法会在不等待响应的情况下执行。

        :param name: 方法名称（前缀":"表示参数是JavaScript表达式）
        :param args: 传递给方法的参数（Python对象或JavaScript表达式）
        :param timeout: 超时时间（秒）（默认：1秒）

        :return: 可以等待以获取方法调用结果的AwaitableResponse
        """
        return self.run_method('run_chart_method', name, *args, timeout=timeout)
