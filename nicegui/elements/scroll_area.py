from typing import Literal, Optional

from typing_extensions import Self

from ..element import Element
from ..events import GenericEventArguments, Handler, ScrollEventArguments, handle_event


class ScrollArea(Element, default_classes='nicegui-scroll-area'):

    def __init__(self, *, on_scroll: Optional[Handler[ScrollEventArguments]] = None) -> None:
        """滚动区域

        通过封装内容来自定义滚动条的一种方式。
        此元素暴露了Quasar的`ScrollArea <https://quasar.dev/vue-components/scroll-area/>`_组件。

        :param on_scroll: 滚动位置变化时调用的函数
        """
        super().__init__('q-scroll-area')

        if on_scroll:
            self.on_scroll(on_scroll)

    def on_scroll(self, callback: Handler[ScrollEventArguments]) -> Self:
        """添加滚动位置变化时要调用的回调函数。"""
        self.on('scroll', lambda e: self._handle_scroll(callback, e), args=[
            'verticalPosition',
            'verticalPercentage',
            'verticalSize',
            'verticalContainerSize',
            'horizontalPosition',
            'horizontalPercentage',
            'horizontalSize',
            'horizontalContainerSize',
        ])
        return self

    def _handle_scroll(self, handler: Optional[Handler[ScrollEventArguments]], e: GenericEventArguments) -> None:
        handle_event(handler, ScrollEventArguments(
            sender=self,
            client=self.client,
            vertical_position=e.args['verticalPosition'],
            vertical_percentage=e.args['verticalPercentage'],
            vertical_size=e.args['verticalSize'],
            vertical_container_size=e.args['verticalContainerSize'],
            horizontal_position=e.args['horizontalPosition'],
            horizontal_percentage=e.args['horizontalPercentage'],
            horizontal_size=e.args['horizontalSize'],
            horizontal_container_size=e.args['horizontalContainerSize'],
        ))

    def scroll_to(self, *,
                  pixels: Optional[float] = None,
                  percent: Optional[float] = None,
                  axis: Literal['vertical', 'horizontal'] = 'vertical',
                  duration: float = 0.0,
                  ) -> None:
        """以百分比（浮点数）或像素数（整数）设置滚动区域位置。

        您可以使用`duration_ms`参数为实际滚动操作添加延迟。

        :param pixels: 从顶部开始的滚动位置偏移量（像素）
        :param percent: 从顶部开始的滚动位置偏移量（总滚动大小的百分比）
        :param axis: 滚动轴
        :param duration: 动画持续时间（秒，默认：0.0表示无动画）
        """
        if pixels is not None and percent is not None:
            raise ValueError('You can only specify one of pixels or percent')
        if pixels is not None:
            self.run_method('setScrollPosition', axis, pixels, 1000 * duration)
        elif percent is not None:
            self.run_method('setScrollPercentage', axis, percent, 1000 * duration)
        else:
            raise ValueError('You must specify one of pixels or percent')
