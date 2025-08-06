from ..element import Element
from .mixins.color_elements import QUASAR_COLORS


class Colors(Element, component='colors.js'):

    def __init__(self, *,
                 primary: str = '#5898d4',
                 secondary: str = '#26a69a',
                 accent: str = '#9c27b0',
                 dark: str = '#1d1d1d',
                 dark_page: str = '#121212',
                 positive: str = '#21ba45',
                 negative: str = '#c10015',
                 info: str = '#31ccec',
                 warning: str = '#f2c037',
                 **custom_colors: str) -> None:
        """颜色主题

        设置`Quasar <https://quasar.dev/style/theme-builder>`_使用的主要颜色（主要、次要、强调等）。

        :param primary: 主要颜色（默认："#5898d4"）
        :param secondary: 次要颜色（默认："#26a69a"）
        :param accent: 强调颜色（默认："#9c27b0"）
        :param dark: 深色（默认："#1d1d1d"）
        :param dark_page: 深色页面（默认："#121212"）
        :param positive: 正面颜色（默认："#21ba45"）
        :param negative: 负面颜色（默认："#c10015"）
        :param info: 信息颜色（默认："#31ccec"）
        :param warning: 警告颜色（默认："#f2c037"）
        :param custom_colors: 品牌自定义颜色定义（需要在自定义颜色使用之前调用``ui.colors``，*在版本2.2.0中添加*）
        """
        super().__init__()
        self._props['primary'] = primary
        self._props['secondary'] = secondary
        self._props['accent'] = accent
        self._props['dark'] = dark
        self._props['dark_page'] = dark_page
        self._props['positive'] = positive
        self._props['negative'] = negative
        self._props['info'] = info
        self._props['warning'] = warning
        self._props['customColors'] = custom_colors
        QUASAR_COLORS.update({name.replace('_', '-') for name in custom_colors})
        self.update()
