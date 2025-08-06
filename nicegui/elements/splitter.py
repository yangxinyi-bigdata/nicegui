from typing import Optional, Tuple

from ..events import Handler, ValueChangeEventArguments
from .mixins.disableable_element import DisableableElement
from .mixins.value_element import ValueElement


class Splitter(ValueElement, DisableableElement, default_classes='nicegui-splitter'):

    def __init__(self, *,
                 horizontal: Optional[bool] = False,
                 reverse: Optional[bool] = False,
                 limits: Optional[Tuple[float, float]] = (0, 100),
                 value: Optional[float] = 50,
                 on_change: Optional[Handler[ValueChangeEventArguments]] = None,
                 ) -> None:
        """分割器

        `ui.splitter`元素将屏幕空间划分为可调整大小的部分，
        在应用程序中实现灵活和响应式的布局。

        基于Quasar的分割器组件：
        `Splitter <https://quasar.dev/vue-components/splitter>`_

        它提供三个可自定义的插槽：``before``、``after``和``separator``，
        可用于在分割器中嵌入其他元素。

        :param horizontal: 是否水平分割而不是垂直分割
        :param limits: 表示两个面板最小和最大分割大小的两个数字
        :param value: 第一个面板的大小（如果使用reverse则为第二个面板）
        :param reverse: 是否将模型大小应用于第二个面板而不是第一个面板
        :param on_change: 用户释放分割器时调用的回调函数
        """
        super().__init__(tag='q-splitter', value=value, on_value_change=on_change, throttle=0.05)
        self._props['horizontal'] = horizontal
        self._props['limits'] = limits
        self._props['reverse'] = reverse

        self.before = self.add_slot('before')
        self.after = self.add_slot('after')
        self.separator = self.add_slot('separator')
