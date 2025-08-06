from typing import Literal, Optional

from ..element import Element


class Row(Element, default_classes='nicegui-row'):

    def __init__(self, *,
                 wrap: bool = True,
                 align_items: Optional[Literal['start', 'end', 'center', 'baseline', 'stretch']] = None,
                 ) -> None:
        """行元素

        提供一个将其子元素排列在行中的容器。

        :param wrap: 是否换行内容（默认：`True`）
        :param align_items: 行中项目的对齐方式（"start"、"end"、"center"、"baseline"或"stretch"；默认：`None`）
        """
        super().__init__('div')
        self._classes.append('row')  # NOTE: for compatibility with Quasar's col-* classes
        if align_items:
            self._classes.append(f'items-{align_items}')

        if not wrap:
            self._style['flex-wrap'] = 'nowrap'
