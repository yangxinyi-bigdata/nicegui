import asyncio
from typing import Optional

from typing_extensions import Self

from ..events import ClickEventArguments, Handler, handle_event
from .mixins.color_elements import BackgroundColorElement
from .mixins.disableable_element import DisableableElement
from .mixins.icon_element import IconElement
from .mixins.text_element import TextElement


class Button(IconElement, TextElement, DisableableElement, BackgroundColorElement):

    def __init__(self,
                 text: str = '', *,
                 on_click: Optional[Handler[ClickEventArguments]] = None,
                 color: Optional[str] = 'primary',
                 icon: Optional[str] = None,
                 ) -> None:
        """按钮

        此元素基于Quasar的`QBtn <https://quasar.dev/vue-components/button>`_组件。

        ``color``参数接受Quasar颜色、Tailwind颜色或CSS颜色。
        如果使用Quasar颜色，按钮将根据Quasar主题进行样式设置，包括文本颜色。
        请注意，像"red"这样的颜色既是Quasar颜色也是CSS颜色。
        在这种情况下将使用Quasar颜色。

        :param text: 按钮的标签文本
        :param on_click: 按钮被按下时调用的回调函数
        :param color: 按钮的颜色（Quasar、Tailwind或CSS颜色，或`None`，默认：'primary'）
        :param icon: 显示在按钮上的图标名称（默认：`None`）
        """
        super().__init__(tag='q-btn', text=text, background_color=color, icon=icon)

        if on_click:
            self.on_click(on_click)

    def on_click(self, callback: Handler[ClickEventArguments]) -> Self:
        """添加一个在按钮被点击时调用的回调函数。"""
        self.on('click', lambda _: handle_event(callback, ClickEventArguments(sender=self, client=self.client)), [])
        return self

    def _text_to_model_text(self, text: str) -> None:
        self._props['label'] = text

    async def clicked(self) -> None:
        """等待直到按钮被点击。"""
        event = asyncio.Event()
        self.on('click', event.set, [])
        await self.client.connected()
        await event.wait()
