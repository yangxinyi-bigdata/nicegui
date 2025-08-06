from typing import Optional

from .mixins.color_elements import BackgroundColorElement, TextColorElement
from .mixins.icon_element import IconElement


class Avatar(IconElement, BackgroundColorElement, TextColorElement):
    TEXT_COLOR_PROP = 'text-color'

    def __init__(self,
                 icon: Optional[str] = None, *,
                 color: Optional[str] = 'primary',
                 text_color: Optional[str] = None,
                 size: Optional[str] = None,
                 font_size: Optional[str] = None,
                 square: bool = False,
                 rounded: bool = False,
                 ) -> None:
        """头像

        封装Quasar的`QAvatar <https://quasar.dev/vue-components/avatar>`_组件的头像元素。

        :param icon: 图标名称或带有"img:"前缀的图像路径（例如"map", "img:path/to/image.png"）
        :param color: 背景颜色（Quasar、Tailwind或CSS颜色，或`None`，默认："primary"）
        :param text_color: Quasar调色板中的颜色名称（例如"primary", "teal-10"）
        :param size: CSS单位的大小，包括单位名称或标准尺寸名称（xs|sm|md|lg|xl）（例如"16px", "2rem"）
        :param font_size: 内容（图标、文本）的CSS单位大小，包括单位名称（例如"18px", "2rem"）
        :param square: 移除border-radius使边框为方形（默认：False）
        :param rounded: 为组件的方形形状应用小的标准border-radius（默认：False）
        """
        super().__init__(tag='q-avatar', background_color=color, text_color=text_color, icon=icon)

        self._props['square'] = square
        self._props['rounded'] = rounded

        if size is not None:
            self._props['size'] = size

        if font_size is not None:
            self._props['font-size'] = font_size
