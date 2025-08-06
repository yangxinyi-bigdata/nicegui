from typing import Literal

from ..element import Element

PageStickyPositions = Literal[
    'top-right',
    'top-left',
    'bottom-right',
    'bottom-left',
    'top',
    'right',
    'bottom',
    'left',
]


class PageSticky(Element):

    def __init__(self,
                 position: PageStickyPositions = 'bottom-right',
                 x_offset: float = 0,
                 y_offset: float = 0,
                 *,
                 expand: bool = False) -> None:
        """页面固定元素

        此元素基于Quasar的`QPageSticky <https://quasar.dev/layout/page-sticky>`_组件。

        :param position: 屏幕上的位置（默认："bottom-right"）
        :param x_offset: 水平偏移量（默认：0）
        :param y_offset: 垂直偏移量（默认：0）
        :param expand: 是否完全展开而不是收缩以适应内容（默认：``False``，*在版本2.1.0中添加*）
        """
        super().__init__('q-page-sticky')
        self._props['position'] = position
        self._props['offset'] = [x_offset, y_offset]
        if expand:
            self._props['expand'] = True
