from typing import Optional

from typing_extensions import Self

from ..events import ClickEventArguments, Handler, ValueChangeEventArguments, handle_event
from .mixins.color_elements import BackgroundColorElement, TextColorElement
from .mixins.disableable_element import DisableableElement
from .mixins.icon_element import IconElement
from .mixins.selectable_element import SelectableElement
from .mixins.text_element import TextElement
from .mixins.value_element import ValueElement


class Chip(IconElement, ValueElement, TextElement, BackgroundColorElement, TextColorElement, DisableableElement, SelectableElement):
    TEXT_COLOR_PROP = 'text-color'

    def __init__(self,
                 text: str = '',
                 *,
                 icon: Optional[str] = None,
                 color: Optional[str] = 'primary',
                 text_color: Optional[str] = None,
                 on_click: Optional[Handler[ClickEventArguments]] = None,
                 selectable: bool = False,
                 selected: bool = False,
                 on_selection_change: Optional[Handler[ValueChangeEventArguments]] = None,
                 removable: bool = False,
                 on_value_change: Optional[Handler[ValueChangeEventArguments]] = None,
                 ) -> None:
        """芯片

        封装Quasar的`QChip <https://quasar.dev/vue-components/chip>`_组件的芯片元素。
        它可以是可点击、可选择和可移除的。

        :param text: 文本字段的初始值（默认：""）
        :param icon: 显示在芯片上的图标名称（默认：`None`）
        :param color: 组件的颜色名称（Quasar、Tailwind或CSS颜色，或`None`，默认："primary"）
        :param text_color: 文本颜色（Quasar、Tailwind或CSS颜色，或`None`，默认：`None`）
        :param on_click: 芯片被点击时调用的回调函数。设置后使芯片可点击
        :param selectable: 芯片是否可选择（默认：`False`）
        :param selected: 芯片是否被选中（默认：`False`）
        :param on_selection_change: 芯片选择状态更改时调用的回调函数
        :param removable: 芯片是否可移除。如果为True则显示一个小"x"按钮（默认：`False`）
        :param on_value_change: 芯片被移除或未移除时调用的回调函数
        """
        super().__init__(tag='q-chip', value=True, on_value_change=on_value_change,
                         icon=icon, text=text, text_color=text_color, background_color=color,
                         selectable=selectable, selected=selected, on_selection_change=on_selection_change)

        self._props['removable'] = removable

        if on_click:
            self.on_click(on_click)

    def on_click(self, callback: Handler[ClickEventArguments]) -> Self:
        """添加芯片被点击时调用的回调函数。"""
        self._props['clickable'] = True
        self.update()
        self.on('click', lambda _: handle_event(callback, ClickEventArguments(sender=self, client=self.client)), [])
        return self
