from __future__ import annotations

import asyncio
import io
import os
import weakref
from typing import Any

from typing_extensions import Self

from .. import background_tasks, optional_features
from ..client import Client
from ..element import Element

try:
    if os.environ.get('MATPLOTLIB', 'true').lower() == 'true':
        import matplotlib.figure
        import matplotlib.pyplot as plt
        optional_features.register('matplotlib')

        class MatplotlibFigure(matplotlib.figure.Figure):

            def __init__(self, element: Matplotlib, *args: Any, **kwargs: Any) -> None:
                super().__init__(*args, **kwargs)
                self._element = weakref.ref(element)

            @property
            def element(self) -> Matplotlib:
                """此matplotlib图形所属的元素。"""
                element = self._element()
                if element is None:
                    raise RuntimeError('The element this matplotlib figure belongs to has been deleted.')
                return element

            def __enter__(self) -> Self:
                return self

            def __exit__(self, *_) -> None:
                self.element.update()

except ImportError:
    pass


class Pyplot(Element, default_classes='nicegui-pyplot'):

    def __init__(self, *, close: bool = True, **kwargs: Any) -> None:
        """Pyplot上下文

        创建用于配置`Matplotlib <https://matplotlib.org/>`_图表的上下文。

        :param close: 退出上下文后是否关闭图形；如果要稍后更新则设置为`False`（默认：`True`）
        :param kwargs: 应传递给`pyplot.figure <https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.figure.html>`_的参数，如`figsize`
        """
        if not optional_features.has('matplotlib'):
            raise ImportError('Matplotlib is not installed. Please run "pip install matplotlib".')

        super().__init__('div')
        self.close = close
        self.fig = plt.figure(**kwargs)  # pylint: disable=possibly-used-before-assignment
        self._convert_to_html()

        if not self.client.shared:
            background_tasks.create(self._auto_close(), name='auto-close plot figure')

    def _convert_to_html(self) -> None:
        with io.StringIO() as output:
            self.fig.savefig(output, format='svg')
            self._props['innerHTML'] = output.getvalue()

    def __enter__(self) -> Self:
        plt.figure(self.fig)
        return self

    def __exit__(self, *_) -> None:
        self._convert_to_html()
        if self.close:
            plt.close(self.fig)
        self.update()

    async def _auto_close(self) -> None:
        while self.client.id in Client.instances:
            await asyncio.sleep(1.0)
        plt.close(self.fig)


class Matplotlib(Element, default_classes='nicegui-matplotlib'):

    def __init__(self, **kwargs: Any) -> None:
        """Matplotlib图形

        创建渲染Matplotlib图形的`Matplotlib <https://matplotlib.org/>`_元素。
        离开图形上下文时图形会自动更新。

        :param kwargs: 应传递给`matplotlib.figure.Figure <https://matplotlib.org/stable/api/figure_api.html#matplotlib.figure.Figure>`_的参数，如`figsize`
        """
        if not optional_features.has('matplotlib'):
            raise ImportError('Matplotlib is not installed. Please run "pip install matplotlib".')

        super().__init__('div')
        self.figure = MatplotlibFigure(self, **kwargs)
        self._convert_to_html()

    def _convert_to_html(self) -> None:
        with io.StringIO() as output:
            self.figure.savefig(output, format='svg')
            self._props['innerHTML'] = output.getvalue()

    def update(self) -> None:
        self._convert_to_html()
        return super().update()
