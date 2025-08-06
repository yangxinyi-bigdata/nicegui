from typing import Optional

from ..events import Handler, ValueChangeEventArguments
from .mixins.disableable_element import DisableableElement
from .mixins.icon_element import IconElement
from .mixins.text_element import TextElement
from .mixins.value_element import ValueElement


class Expansion(IconElement, TextElement, ValueElement, DisableableElement, default_classes='nicegui-expansion'):

    def __init__(self,
                 text: str = '', *,
                 caption: Optional[str] = None,
                 icon: Optional[str] = None,
                 group: Optional[str] = None,
                 value: bool = False,
                 on_value_change: Optional[Handler[ValueChangeEventArguments]] = None
                 ) -> None:
        """展开元素

        提供基于Quasar的`QExpansionItem <https://quasar.dev/vue-components/expansion-item>`_组件的可展开容器。

        :param text: 标题文本
        :param caption: 可选的标题（或子标签）文本
        :param icon: 可选图标（默认：None）
        :param group: 可选的组名，用于在组内协调打开/关闭状态，即"手风琴模式"
        :param value: 创建时是否应该打开展开（默认：`False`）
        :param on_value_change: 值更改时执行的回调函数
        """
        super().__init__(tag='q-expansion-item', icon=icon, text=text, value=value, on_value_change=on_value_change)
        if caption is not None:
            self._props['caption'] = caption
        if group is not None:
            self._props['group'] = group

    def open(self) -> None:
        """打开展开。"""
        self.value = True

    def close(self) -> None:
        """关闭展开。"""
        self.value = False

    def _text_to_model_text(self, text: str) -> None:
        self._props['label'] = text
