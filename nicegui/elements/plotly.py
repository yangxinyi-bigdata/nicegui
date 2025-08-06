from __future__ import annotations

from typing import Dict, Union

from .. import optional_features
from ..element import Element

try:
    import plotly.graph_objects as go
    optional_features.register('plotly')
except ImportError:
    pass


class Plotly(Element, component='plotly.vue', dependencies=['lib/plotly/plotly.min.js']):

    def __init__(self, figure: Union[Dict, go.Figure]) -> None:
        """Plotly元素

        渲染Plotly图表。
        有两种方式传递Plotly图形进行渲染，参见参数`figure`：

        * 传递`go.Figure`对象，参见 https://plotly.com/python/

        * 传递包含键`data`、`layout`、`config`（可选）的Python`dict`对象，参见 https://plotly.com/javascript/

        为获得最佳性能，建议使用声明式的`dict`方法创建Plotly图表。

        :param figure: 要渲染的Plotly图形。可以是`go.Figure`实例，
                       或包含键`data`、`layout`、`config`（可选）的`dict`对象。
        """
        if not optional_features.has('plotly'):
            raise ImportError('Plotly is not installed. Please run "pip install nicegui[plotly]".')

        super().__init__()

        self.figure = figure
        self.update()
        self._classes.append('js-plotly-plot')
        self._update_method = 'update'

    def update_figure(self, figure: Union[Dict, go.Figure]):
        """覆盖此Plotly图表的图形实例并在客户端更新图表。"""
        self.figure = figure
        self.update()

    def update(self) -> None:
        self._props['options'] = self._get_figure_json()
        super().update()

    def _get_figure_json(self) -> Dict:
        if isinstance(self.figure, go.Figure):
            # convert go.Figure to dict object which is directly JSON serializable
            # orjson supports NumPy array serialization
            return self.figure.to_plotly_json()

        if isinstance(self.figure, dict):
            # already a dict object with keys: data, layout, config (optional)
            return self.figure

        raise ValueError(f'Plotly figure is of unknown type "{self.figure.__class__.__name__}".')
