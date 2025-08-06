from typing import Optional

from .mixins.color_elements import BackgroundColorElement, TextColorElement
from .mixins.text_element import TextElement


class Badge(TextElement, BackgroundColorElement, TextColorElement):
    TEXT_COLOR_PROP = 'text-color'

    def __init__(self,
                 text: str = '', *,
                 color: Optional[str] = 'primary',
                 text_color: Optional[str] = None,
                 outline: bool = False) -> None:
        """徽章

        封装Quasar的`QBadge <https://quasar.dev/vue-components/badge>`_组件的徽章元素。

        :param text: 文本字段的初始值
        :param color: 组件的颜色名称（Quasar、Tailwind或CSS颜色，或`None`，默认："primary"）
        :param text_color: 文本颜色（Quasar、Tailwind或CSS颜色，或`None`，默认：`None`）
        :param outline: 使用'outline'设计（仅彩色文本和边框）（默认：False）
        """
        super().__init__(tag='q-badge', text=text, text_color=text_color, background_color=color)
        self._props['outline'] = outline
