from typing import Any, Optional

from ..events import Handler, ValueChangeEventArguments
from .mixins.disableable_element import DisableableElement
from .mixins.value_element import ValueElement


class Editor(ValueElement, DisableableElement, component='editor.js', default_classes='nicegui-editor'):
    VALUE_PROP: str = 'value'
    LOOPBACK = False

    def __init__(self,
                 *,
                 placeholder: Optional[str] = None,
                 value: str = '',
                 on_change: Optional[Handler[ValueChangeEventArguments]] = None,
                 ) -> None:
        """富文本编辑器

        基于`Quasar的QEditor <https://quasar.dev/vue-components/editor>`_的所见即所得编辑器。
        值是包含格式化文本作为HTML代码的字符串。

        :param value: 初始值
        :param on_change: 值更改时要调用的回调函数
        """
        super().__init__(value=value, on_value_change=on_change)
        if placeholder is not None:
            self._props['placeholder'] = placeholder

    def _handle_value_change(self, value: Any) -> None:
        super()._handle_value_change(value)
        if self._send_update_on_value_change:
            self.run_method('updateValue')
