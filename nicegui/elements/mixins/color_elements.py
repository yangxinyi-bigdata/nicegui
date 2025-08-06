from typing import Any, Optional, get_args

from ...element import Element
from ...tailwind_types.background_color import BackgroundColor

QUASAR_COLORS = {'primary', 'secondary', 'accent', 'dark', 'positive', 'negative', 'info', 'warning'}
for color in ['red', 'pink', 'purple', 'deep-purple', 'indigo', 'blue', 'light-blue', 'cyan', 'teal', 'green',
              'light-green', 'lime', 'yellow', 'amber', 'orange', 'deep-orange', 'brown', 'grey', 'blue-grey']:
    QUASAR_COLORS.add(color)
    for i in range(1, 15):
        QUASAR_COLORS.add(f'{color}-{i}')

TAILWIND_COLORS = get_args(BackgroundColor)


class BackgroundColorElement(Element):
    """背景颜色元素混入

    为元素提供背景颜色设置功能的混入类。
    支持Quasar颜色、Tailwind颜色和自定义CSS颜色。
    """
    BACKGROUND_COLOR_PROP = 'color'

    def __init__(self, *, background_color: Optional[str], **kwargs: Any) -> None:
        """初始化背景颜色元素

        :param background_color: 背景颜色（Quasar颜色、Tailwind颜色或CSS颜色）
        """
        super().__init__(**kwargs)
        if background_color in QUASAR_COLORS:
            self._props[self.BACKGROUND_COLOR_PROP] = background_color
        elif background_color in TAILWIND_COLORS:
            self._classes.append(f'bg-{background_color}')
        elif background_color is not None:
            self._style['background-color'] = background_color


class TextColorElement(Element):
    """文本颜色元素混入

    为元素提供文本颜色设置功能的混入类。
    支持Quasar颜色、Tailwind颜色和自定义CSS颜色。
    """
    TEXT_COLOR_PROP = 'color'

    def __init__(self, *, text_color: Optional[str], **kwargs: Any) -> None:
        """初始化文本颜色元素

        :param text_color: 文本颜色（Quasar颜色、Tailwind颜色或CSS颜色）
        """
        super().__init__(**kwargs)
        if text_color in QUASAR_COLORS:
            self._props[self.TEXT_COLOR_PROP] = text_color
        elif text_color in TAILWIND_COLORS:
            self._classes.append(f'text-{text_color}')
        elif text_color is not None:
            self._style['color'] = text_color
