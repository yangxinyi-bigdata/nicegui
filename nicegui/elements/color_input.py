from typing import Any, Optional

from ..events import Handler, ValueChangeEventArguments
from .button import Button as button
from .color_picker import ColorPicker as color_picker
from .mixins.disableable_element import DisableableElement
from .mixins.label_element import LabelElement
from .mixins.value_element import ValueElement


class ColorInput(LabelElement, ValueElement, DisableableElement):
    LOOPBACK = False

    def __init__(self,
                 label: Optional[str] = None, *,
                 placeholder: Optional[str] = None,
                 value: str = '',
                 on_change: Optional[Handler[ValueChangeEventArguments]] = None,
                 preview: bool = False,
                 ) -> None:
        """颜色输入框

        此元素扩展了Quasar的`QInput <https://quasar.dev/vue-components/input>`_组件，增加了颜色选择器功能。

        :param label: 颜色输入框的显示标签
        :param placeholder: 如果没有选择颜色时显示的文本
        :param value: 当前的颜色值
        :param on_change: 值更改时要执行的回调函数
        :param preview: 将按钮背景更改为选定的颜色（默认：False）
        """
        super().__init__(tag='q-input', label=label, value=value, on_value_change=on_change)
        if placeholder is not None:
            self._props['placeholder'] = placeholder

        with self.add_slot('append'):
            self.picker = color_picker(on_pick=lambda e: self.set_value(e.color))
            self.button = button(on_click=self.open_picker, icon='colorize') \
                .props('flat round', remove='color').classes('cursor-pointer')

        self.preview = preview
        self._update_preview()

    def open_picker(self) -> None:
        """打开颜色选择器"""
        if self.value:
            self.picker.set_color(self.value)
        self.picker.open()

    def _handle_value_change(self, value: Any) -> None:
        super()._handle_value_change(value)
        self._update_preview()

    def _update_preview(self) -> None:
        if not self.preview:
            return
        self.button.style(f'''
            background-color: {(self.value or "#fff").split(";", 1)[0]};
            text-shadow: 2px 0 #fff, -2px 0 #fff, 0 2px #fff, 0 -2px #fff, 1px 1px #fff, -1px -1px #fff, 1px -1px #fff, -1px 1px #fff;
        ''')
