from typing import Optional

from .label import Label as label
from .mixins.color_elements import TextColorElement
from .mixins.value_element import ValueElement


class LinearProgress(ValueElement, TextColorElement):
    VALUE_PROP = 'value'

    def __init__(self,
                 value: float = 0.0, *,
                 size: Optional[str] = None,
                 show_value: bool = True,
                 color: Optional[str] = 'primary',
                 ) -> None:
        """线性进度条

        一个封装Quasar的
        `QLinearProgress <https://quasar.dev/vue-components/linear-progress>`_组件的线性进度条。

        :param value: 字段的初始值（从0.0到1.0）
        :param size: 进度条的高度（带值标签时默认为"20px"，不带时为"4px"）
        :param show_value: 是否在中心显示值标签（默认：`True`）
        :param color: 颜色（Quasar、Tailwind或CSS颜色，或`None`，默认："primary"）
        """
        super().__init__(tag='q-linear-progress', value=value, on_value_change=None, text_color=color)
        self._props['size'] = size if size is not None else '20px' if show_value else '4px'

        if show_value:
            with self:
                label().classes('absolute-center text-sm text-white').bind_text_from(self, 'value')


class CircularProgress(ValueElement, TextColorElement):
    VALUE_PROP = 'value'

    def __init__(self,
                 value: float = 0.0, *,
                 min: float = 0.0,  # pylint: disable=redefined-builtin
                 max: float = 1.0,  # pylint: disable=redefined-builtin
                 size: str = 'xl',
                 show_value: bool = True,
                 color: Optional[str] = 'primary',
                 ) -> None:
        """圆形进度条

        一个封装Quasar的
        `QCircularProgress <https://quasar.dev/vue-components/circular-progress>`_的圆形进度条。

        :param value: 字段的初始值
        :param min: 最小值（默认：0.0）
        :param max: 最大值（默认：1.0）
        :param size: 进度圆的大小（默认："xl"）
        :param show_value: 是否在中心显示值标签（默认：`True`）
        :param color: 颜色（Quasar、Tailwind或CSS颜色，或`None`，默认："primary"）
        """
        super().__init__(tag='q-circular-progress', value=value, on_value_change=None, text_color=color)
        self._props['min'] = min
        self._props['max'] = max
        self._props['size'] = size
        self._props['show-value'] = True  # NOTE always activate the default slot because this is expected by ui.element
        self._props['track-color'] = 'grey-4'

        if show_value:
            with self:
                label().classes('absolute-center text-xs').bind_text_from(self, 'value')
