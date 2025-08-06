from __future__ import annotations

from typing import Any, Optional, Union, cast

from ..context import context
from ..events import Handler, ValueChangeEventArguments
from .mixins.disableable_element import DisableableElement
from .mixins.value_element import ValueElement


class Carousel(ValueElement):

    def __init__(self, *,
                 value: Union[str, CarouselSlide, None] = None,
                 on_value_change: Optional[Handler[ValueChangeEventArguments]] = None,
                 animated: bool = False,
                 arrows: bool = False,
                 navigation: bool = False,
                 ) -> None:
        """轮播

        此元素表示`Quasar的QCarousel <https://quasar.dev/vue-components/carousel#qcarousel-api>`_组件。
        它包含个别的轮播幻灯片。

        :param value: `ui.carousel_slide`或初始选择的幻灯片名称（默认：`None`，表示第一张幻灯片）
        :param on_value_change: 当选择的幻灯片更改时要执行的回调函数
        :param animated: 是否为幻灯片切换添加动画（默认：`False`）
        :param arrows: 是否显示手动幻灯片导航的箭头（默认：`False`）
        :param navigation: 是否显示手动幻灯片导航的导航点（默认：`False`）
        """
        super().__init__(tag='q-carousel', value=value, on_value_change=on_value_change)
        self._props['animated'] = animated
        self._props['arrows'] = arrows
        self._props['navigation'] = navigation

    def _value_to_model_value(self, value: Any) -> Any:
        return value.props['name'] if isinstance(value, CarouselSlide) else value

    def _handle_value_change(self, value: Any) -> None:
        super()._handle_value_change(value)
        names = [slide.props['name'] for slide in self.default_slot]
        for i, slide in enumerate(self):
            done = i < names.index(value) if value in names else False
            slide.props(f':done={done}')

    def next(self) -> None:
        """显示下一张幻灯片。"""
        self.run_method('next')

    def previous(self) -> None:
        """显示上一张幻灯片。"""
        self.run_method('previous')


class CarouselSlide(DisableableElement, default_classes='nicegui-carousel-slide'):

    def __init__(self, name: Optional[str] = None) -> None:
        """轮播幻灯片

        此元素表示`Quasar的QCarouselSlide <https://quasar.dev/vue-components/carousel#qcarouselslide-api>`_组件。
        它是`ui.carousel`元素的子元素。

        :param name: 幻灯片的名称（将是`ui.carousel`元素的值，如果为`None`则自动生成）
        """
        super().__init__(tag='q-carousel-slide')
        self.carousel = cast(ValueElement, context.slot.parent)
        name = name or f'slide_{len(self.carousel.default_slot.children)}'
        self._props['name'] = name
        if self.carousel.value is None:
            self.carousel.value = name
