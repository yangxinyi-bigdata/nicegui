from typing import Any, List, Literal, Tuple, Union

from .pyplot import Pyplot


class LinePlot(Pyplot):

    def __init__(self, *,
                 n: int = 1,
                 limit: int = 100,
                 update_every: int = 1,
                 close: bool = True,
                 **kwargs: Any,
                 ) -> None:
        """线图

        使用pyplot创建线图。
        `push`方法在与`ui.timer`结合使用时提供实时更新。

        :param n: 线条数量
        :param limit: 每条线最大数据点数（新点将替换最旧的点）
        :param update_every: 仅在多次推送新数据后更新图表以节省CPU和带宽
        :param close: 退出上下文后是否关闭图形；如果要稍后更新则设置为`False`（默认：`True`）
        :param kwargs: 应传递给`pyplot.figure <https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.figure.html>`_的参数，如`figsize`
        """
        super().__init__(close=close, **kwargs)

        self.x: List[float] = []
        self.Y: List[List[float]] = [[] for _ in range(n)]
        self.lines = [self.fig.gca().plot([], [])[0] for _ in range(n)]
        self.slice = slice(0 if limit is None else -limit, None)
        self.update_every = update_every
        self.push_counter = 0

    def with_legend(self, titles: List[str], **kwargs: Any):
        """向图表添加图例。

        :param titles: 线条的标题列表
        :param kwargs: 应传递给`pyplot.legend <https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.legend.html>`_的附加参数
        """
        self.fig.gca().legend(titles, **kwargs)
        self._convert_to_html()
        return self

    def push(self,
             x: List[float],
             Y: List[List[float]],
             *,
             x_limits: Union[None, Literal['auto'], Tuple[float, float]] = 'auto',
             y_limits: Union[None, Literal['auto'], Tuple[float, float]] = 'auto',
             ) -> None:
        """向图表推送新数据。

        :param x: x值列表
        :param Y: y值列表的列表（每条线一个列表）
        :param x_limits: 新的x限制（浮点数元组，或"auto"以适应数据点，或``None``保持不变，*在版本2.10.0中添加*）
        :param y_limits: 新的y限制（浮点数元组，或"auto"以适应数据点，或``None``保持不变，*在版本2.10.0中添加*）
        """
        self.push_counter += 1

        self.x = [*self.x, *x][self.slice]
        for i in range(len(self.lines)):
            self.Y[i] = [*self.Y[i], *Y[i]][self.slice]

        if self.push_counter % self.update_every != 0:
            return

        for i, line in enumerate(self.lines):
            line.set_xdata(self.x)
            line.set_ydata(self.Y[i])

        if isinstance(x_limits, tuple):
            self.fig.gca().set_xlim(*x_limits)
        elif x_limits == 'auto':
            min_x = min(self.x)
            max_x = max(self.x)
            if min_x != max_x:
                pad_x = 0.01 * (max_x - min_x)
                self.fig.gca().set_xlim(min_x - pad_x, max_x + pad_x)

        if isinstance(y_limits, tuple):
            self.fig.gca().set_ylim(*y_limits)
        elif y_limits == 'auto':
            flat_y = [y_i for y in self.Y for y_i in y]
            min_y = min(flat_y)
            max_y = max(flat_y)
            if min_y != max_y:
                pad_y = 0.01 * (max_y - min_y)
                self.fig.gca().set_ylim(min_y - pad_y, max_y + pad_y)

        self._convert_to_html()
        self.update()

    def clear(self) -> None:
        """清除线图。"""
        super().clear()
        self.x.clear()
        for y in self.Y:
            y.clear()
        for line in self.lines:
            line.set_data([], [])
        self._convert_to_html()
        self.update()
