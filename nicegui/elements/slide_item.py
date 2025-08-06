from __future__ import annotations

from typing import Literal, Optional

from typing_extensions import Self

from ..events import Handler, SlideEventArguments, handle_event
from ..slot import Slot
from .item import Item
from .label import Label
from .mixins.disableable_element import DisableableElement

SlideSide = Literal['left', 'right', 'top', 'bottom']


class SlideItem(DisableableElement):

    def __init__(self, text: str = '', *, on_slide: Optional[Handler[SlideEventArguments]] = None) -> None:
        """滑动项

        此元素基于Quasar的`QSlideItem <https://quasar.dev/vue-components/slide-item/>`_组件。

        如果提供了``text``参数，将使用给定文本创建嵌套的``ui.item``元素。
        如果要自定义文本的显示方式，可以在滑动项内放置自定义元素。

        要填充各个滑动操作的插槽，使用``left``、``right``、``top``或``bottom``方法，
        或使用带有侧边参数（"left"、"right"、"top"或"bottom"）的``action``方法。

        一旦发生滑动操作，可以使用``reset``方法将滑动项重置回其初始状态。

        *在版本2.12.0中添加*

        :param text: 要显示的文本（默认：""）
        :param on_slide: 激活任何滑动操作时调用的回调函数
        """
        super().__init__(tag='q-slide-item')

        if text:
            with self:
                Item(text)

        if on_slide:
            self.on_slide(None, on_slide)

    def action(self,
               side: SlideSide,
               text: str = '', *,
               on_slide: Optional[Handler[SlideEventArguments]] = None,
               color: Optional[str] = 'primary',
               ) -> Slot:
        """向指定侧边添加滑动操作。

        :param side: 应添加滑动的滑动项侧边（"left"、"right"、"top"、"bottom"）
        :param text: 要显示的文本（默认：""）
        :param on_slide: 激活滑动操作时调用的回调函数
        :param color: 滑动背景的颜色（Quasar、Tailwind或CSS颜色或``None``，默认："primary"）
        """
        if color:
            self._props[f'{side}-color'] = color

        if on_slide:
            self.on_slide(side, on_slide)

        slot = self.add_slot(side)
        if text:
            with slot:
                Label(text)

        return slot

    def left(self,
             text: str = '', *,
             on_slide: Optional[Handler[SlideEventArguments]] = None,
             color: Optional[str] = 'primary',
             ) -> Slot:
        """向左侧添加滑动操作。

        :param text: 要显示的文本（默认：""）
        :param on_slide: 激活滑动操作时调用的回调函数
        :param color: 滑动背景的颜色（Quasar、Tailwind或CSS颜色或``None``，默认："primary"）
        """
        return self.action('left', text=text, on_slide=on_slide, color=color)

    def right(self,
              text: str = '', *,
              on_slide: Optional[Handler[SlideEventArguments]] = None,
              color: Optional[str] = 'primary',
              ) -> Slot:
        """向右侧添加滑动操作。

        :param text: 要显示的文本（默认：""）
        :param on_slide: 激活滑动操作时调用的回调函数
        :param color: 滑动背景的颜色（Quasar、Tailwind或CSS颜色或``None``，默认："primary"）
        """
        return self.action('right', text=text, on_slide=on_slide, color=color)

    def top(self,
            text: str = '', *,
            on_slide: Optional[Handler[SlideEventArguments]] = None,
            color: Optional[str] = 'primary',
            ) -> Slot:
        """向顶部添加滑动操作。

        :param text: 要显示的文本（默认：""）
        :param on_slide: 激活滑动操作时调用的回调函数
        :param color: 滑动背景的颜色（Quasar、Tailwind或CSS颜色或``None``，默认："primary"）
        """
        return self.action('top', text=text, on_slide=on_slide, color=color)

    def bottom(self,
               text: str = '', *,
               on_slide: Optional[Handler[SlideEventArguments]] = None,
               color: Optional[str] = 'primary',
               ) -> Slot:
        """向底部添加滑动操作。

        :param text: 要显示的文本（默认：""）
        :param on_slide: 激活滑动操作时调用的回调函数
        :param color: 滑动背景的颜色（Quasar、Tailwind或CSS颜色或``None``，默认："primary"）
        """
        return self.action('bottom', text=text, on_slide=on_slide, color=color)

    def on_slide(self, side: SlideSide | None, handler: Handler[SlideEventArguments]) -> Self:
        """添加激活滑动操作时要调用的回调函数。"""
        self.on(side or 'action', lambda e: handle_event(handler, SlideEventArguments(sender=self,
                                                                                      client=self.client,
                                                                                      side=e.args.get('side', side))))
        return self

    def reset(self) -> None:
        """将滑动项重置为初始状态。"""
        self.run_method('reset')
