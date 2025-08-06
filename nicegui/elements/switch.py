from typing import Optional

from ..events import Handler, ValueChangeEventArguments
from .mixins.disableable_element import DisableableElement
from .mixins.text_element import TextElement
from .mixins.value_element import ValueElement


class Switch(TextElement, ValueElement, DisableableElement):

    def __init__(self, text: str = '', *, value: bool = False, on_change: Optional[Handler[ValueChangeEventArguments]] = None) -> None:
        """开关

        此元素基于Quasar的`QToggle <https://quasar.dev/vue-components/toggle>`_组件。

        :param text: 显示在开关旁边的标签
        :param value: 是否应该初始激活（默认：`False`）
        :param on_change: 当用户更改状态时调用的回调函数
        """
        super().__init__(tag='q-toggle', text=text, value=value, on_value_change=on_change)
