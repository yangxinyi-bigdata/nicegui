from typing import Literal, Optional

from ..element import Element


class Column(Element, default_classes='nicegui-column'):

    def __init__(self, *,
                 wrap: bool = False,
                 align_items: Optional[Literal['start', 'end', 'center', 'baseline', 'stretch']] = None,
                 ) -> None:
        """列元素

        提供一个将其子元素排列在列中的容器。

        :param wrap: 是否换行内容（默认：`False`）
        :param align_items: 列中项目的对齐方式（"start"、"end"、"center"、"baseline"或"stretch"；默认：`None`）
        """
        super().__init__('div')
        if align_items:
            self._classes.append(f'items-{align_items}')

        if wrap:
            self._style['flex-wrap'] = 'wrap'
