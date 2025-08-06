from .. import helpers, optional_features
from ..element import Element
from .markdown import Markdown

try:
    from nicegui_highcharts import highchart
    optional_features.register('highcharts')
    __all__ = ['highchart']
except ImportError:
    class highchart(Element):  # type: ignore
        def __init__(self, *args, **kwargs) -> None:  # pylint: disable=unused-argument
            """Highcharts图表

            使用`Highcharts <https://www.highcharts.com/>`_创建图表的元素。
            可以通过更改`options`属性将更新推送到图表。
            数据更改后，调用`update`方法刷新图表。

            由于Highcharts的限制性许可证，此元素不是标准NiceGUI包的一部分。
            它在`单独的仓库 <https://github.com/zauberzeug/nicegui-highcharts/>`_中维护，
            可以使用`pip install nicegui[highcharts]`安装。
            """
            super().__init__()
            Markdown('Highcharts is not installed. Please run `pip install nicegui[highcharts]`.')
            helpers.warn_once('Highcharts is not installed. Please run "pip install nicegui[highcharts]".')
