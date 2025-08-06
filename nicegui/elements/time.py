from typing import Optional

from ..events import Handler, ValueChangeEventArguments
from .mixins.disableable_element import DisableableElement
from .mixins.value_element import ValueElement


class Time(ValueElement, DisableableElement):

    def __init__(self,
                 value: Optional[str] = None, *,
                 mask: str = 'HH:mm',
                 on_change: Optional[Handler[ValueChangeEventArguments]] = None,
                 ) -> None:
        """时间输入框

        此元素基于Quasar的`QTime <https://quasar.dev/vue-components/time>`_组件。
        时间是按`mask`参数定义格式的字符串。

        :param value: 初始时间
        :param mask: 时间字符串的格式（默认：'HH:mm'）
        :param on_change: 更改时间时执行的回调函数
        """
        super().__init__(tag='q-time', value=value, on_value_change=on_change)
        self._props['mask'] = mask
