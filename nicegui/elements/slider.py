from typing import Optional

from ..events import Handler, ValueChangeEventArguments
from .mixins.disableable_element import DisableableElement
from .mixins.value_element import ValueElement


class Slider(ValueElement, DisableableElement):

    def __init__(self, *,
                 min: float,  # pylint: disable=redefined-builtin
                 max: float,  # pylint: disable=redefined-builtin
                 step: float = 1.0,
                 value: Optional[float] = None,
                 on_change: Optional[Handler[ValueChangeEventArguments]] = None,
                 ) -> None:
        """滑块

        此元素基于Quasar的`QSlider <https://quasar.dev/vue-components/slider>`_组件。

        :param min: 滑块的下限
        :param max: 滑块的上限
        :param step: 步长
        :param value: 设置滑块位置的初始值
        :param on_change: 当用户释放滑块时调用的回调函数
        """
        super().__init__(tag='q-slider', value=value, on_value_change=on_change, throttle=0.05)
        self._props['min'] = min
        self._props['max'] = max
        self._props['step'] = step
