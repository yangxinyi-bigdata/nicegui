from typing import Optional

from ..events import Handler, ValueChangeEventArguments
from .mixins.disableable_element import DisableableElement
from .mixins.text_element import TextElement
from .mixins.value_element import ValueElement


class Checkbox(TextElement, ValueElement, DisableableElement):

    def __init__(self, text: str = '', *, value: bool = False, on_change: Optional[Handler[ValueChangeEventArguments]] = None) -> None:
        """复选框

        此元素基于Quasar的`QCheckbox <https://quasar.dev/vue-components/checkbox>`_组件。

        :param text: 显示在复选框旁边的标签文本
        :param value: 是否应该初始选中（默认：`False`）
        :param on_change: 值发生变化时执行的回调函数
        """
        super().__init__(tag='q-checkbox', text=text, value=value, on_value_change=on_change)
