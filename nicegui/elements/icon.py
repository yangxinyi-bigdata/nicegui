from typing import Optional

from .mixins.color_elements import TextColorElement
from .mixins.name_element import NameElement


class Icon(NameElement, TextColorElement):

    def __init__(self,
                 name: str,
                 *,
                 size: Optional[str] = None,
                 color: Optional[str] = None,
                 ) -> None:
        """图标

        此元素基于Quasar的`QIcon <https://quasar.dev/vue-components/icon>`_组件。

        `此处 <https://fonts.google.com/icons?icon.set=Material+Icons>`_ 是可能的名称参考。

        :param name: 图标名称（蛇形命名法，例如`add_circle`）
        :param size: CSS单位的大小，包括单位名称或标准尺寸名称（xs|sm|md|lg|xl），示例：16px, 2rem
        :param color: 图标颜色（Quasar、Tailwind或CSS颜色，或`None`，默认：`None`）
        """
        super().__init__(tag='q-icon', name=name, text_color=color)

        if size:
            self._props['size'] = size
