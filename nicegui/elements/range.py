from typing import Dict, Optional

from ..events import Handler, ValueChangeEventArguments
from .mixins.disableable_element import DisableableElement
from .mixins.value_element import ValueElement


class Range(ValueElement, DisableableElement):

    def __init__(self, *,
                 min: float,  # pylint: disable=redefined-builtin
                 max: float,  # pylint: disable=redefined-builtin
                 step: float = 1.0,
                 value: Optional[Dict[str, int]] = None,
                 on_change: Optional[Handler[ValueChangeEventArguments]] = None,
                 ) -> None:
        """范围选择器

        此元素基于Quasar的`QRange <https://quasar.dev/vue-components/range>`_组件。

        :param min: 范围的下限
        :param max: 范围的上限
        :param step: 步长
        :param value: 设置范围最小和最大位置的初始值
        :param on_change: 用户释放范围选择器时调用的回调函数
        """
        super().__init__(tag='q-range', value=value, on_value_change=on_change, throttle=0.05)
        self._props['min'] = min
        self._props['max'] = max
        self._props['step'] = step

    @property
    def min(self) -> float:
        """允许的最小值。"""
        return self._props['min']

    @min.setter
    def min(self, value: float) -> None:
        if self._props['min'] == value:
            return
        self._props['min'] = value
        self.update()

    @property
    def max(self) -> float:
        """允许的最大值。"""
        return self._props['max']

    @max.setter
    def max(self, value: float) -> None:
        if self._props['max'] == value:
            return
        self._props['max'] = value
        self.update()

    @property
    def step(self) -> float:
        """有效值之间的步长。"""
        return self._props['step']

    @step.setter
    def step(self, value: float) -> None:
        if self._props['step'] == value:
            return
        self._props['step'] = value
        self.update()
