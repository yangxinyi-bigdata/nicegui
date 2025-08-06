from typing import Optional

from typing_extensions import Self

from ..events import ClickEventArguments, Handler, handle_event
from .mixins.disableable_element import DisableableElement
from .mixins.text_element import TextElement


class Item(DisableableElement):

    def __init__(self, text: str = '', *, on_click: Optional[Handler[ClickEventArguments]] = None) -> None:
        """列表项

        基于Quasar的`QItem <https://quasar.dev/vue-components/list-and-list-items#qitem-api>`_组件创建可点击的列表项。
        该项应放置在``ui.list``或``ui.menu``元素内。
        如果提供了text参数，将使用给定文本创建项目部分。
        如果要自定义文本的显示方式，需要创建自己的项目部分和标签元素。

        :param text: 要显示的文本（默认：""）
        :param on_click: 点击项目时要执行的回调函数（将"clickable"属性设置为True）
        """
        super().__init__(tag='q-item')

        if on_click:
            self.on_click(on_click)

        if text:
            with self:
                ItemSection(text=text)

    def on_click(self, callback: Handler[ClickEventArguments]) -> Self:
        """添加点击列表项时要调用的回调函数。"""
        self._props['clickable'] = True  # idempotent
        self.on('click', lambda _: handle_event(callback, ClickEventArguments(sender=self, client=self.client)))
        return self


class ItemSection(TextElement):

    def __init__(self, text: str = '') -> None:
        """列表项部分

        基于Quasar的`QItemSection <https://quasar.dev/vue-components/list-and-list-items#qitemsection-api>`_组件创建项目部分。
        该部分应放置在``ui.item``元素内。

        :param text: 要显示的文本（默认：""）
        """
        super().__init__(tag='q-item-section', text=text)


class ItemLabel(TextElement):

    def __init__(self, text: str = '') -> None:
        """列表项标签

        基于Quasar的`QItemLabel <https://quasar.dev/vue-components/list-and-list-items#qitemlabel-api>`_组件创建项目标签。

        :param text: 要显示的文本（默认：""）
        """
        super().__init__(tag='q-item-label', text=text)
