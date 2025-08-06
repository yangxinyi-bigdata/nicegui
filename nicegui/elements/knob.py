from typing import Optional

from ..events import Handler, ValueChangeEventArguments
from .label import Label
from .mixins.color_elements import TextColorElement
from .mixins.disableable_element import DisableableElement
from .mixins.value_element import ValueElement


class Knob(ValueElement, DisableableElement, TextColorElement):

    def __init__(self,
                 value: float = 0.0,
                 *,
                 min: float = 0.0,  # pylint: disable=redefined-builtin
                 max: float = 1.0,  # pylint: disable=redefined-builtin
                 step: float = 0.01,
                 color: Optional[str] = 'primary',
                 center_color: Optional[str] = None,
                 track_color: Optional[str] = None,
                 size: Optional[str] = None,
                 show_value: bool = False,
                 on_change: Optional[Handler[ValueChangeEventArguments]] = None,
                 ) -> None:
        """旋钮

        此元素基于Quasar的`QKnob <https://quasar.dev/vue-components/knob>`_组件。
        该元素用于通过鼠标/触摸平移从用户获取数字输入。

        :param value: 初始值（默认：0.0）
        :param min: 最小值（默认：0.0）
        :param max: 最大值（默认：1.0）
        :param step: 步长（默认：0.01）
        :param color: 旋钮颜色（Quasar、Tailwind或CSS颜色或`None`，默认："primary"）
        :param center_color: 组件中心部分的颜色名称，例如：primary, teal-10
        :param track_color: 组件轨道的颜色名称，例如：primary, teal-10
        :param size: CSS单位的大小，包括单位名称或标准尺寸名称（xs|sm|md|lg|xl），例如：16px, 2rem
        :param show_value: 是否以文本形式显示值
        :param on_change: 值变化时要执行的回调函数
        """
        super().__init__(tag='q-knob', value=value, on_value_change=on_change, throttle=0.05, text_color=color)

        self._props['min'] = min
        self._props['max'] = max
        self._props['step'] = step
        self._props['show-value'] = True  # NOTE: enable default slot, e.g. for nested icon

        if center_color:
            self._props['center-color'] = center_color

        if track_color:
            self._props['track-color'] = track_color

        if size:
            self._props['size'] = size

        self.label: Optional[Label] = None
        if show_value:
            with self:
                self.label = Label().bind_text_from(self, 'value')
