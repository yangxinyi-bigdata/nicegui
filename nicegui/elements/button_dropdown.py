from typing import Optional

from typing_extensions import Self

from ..events import ClickEventArguments, Handler, ValueChangeEventArguments, handle_event
from .mixins.color_elements import BackgroundColorElement
from .mixins.disableable_element import DisableableElement
from .mixins.icon_element import IconElement
from .mixins.text_element import TextElement
from .mixins.value_element import ValueElement


class DropdownButton(IconElement, TextElement, DisableableElement, BackgroundColorElement, ValueElement):

    def __init__(self,
                 text: str = '', *,
                 value: bool = False,
                 on_value_change: Optional[Handler[ValueChangeEventArguments]] = None,
                 on_click: Optional[Handler[ClickEventArguments]] = None,
                 color: Optional[str] = 'primary',
                 icon: Optional[str] = None,
                 auto_close: Optional[bool] = False,
                 split: Optional[bool] = False,
                 ) -> None:
        """下拉按钮

        此元素基于Quasar的`QBtnDropDown <https://quasar.dev/vue-components/button-dropdown>`_组件。

        ``color``参数接受Quasar颜色、Tailwind颜色或CSS颜色。
        如果使用Quasar颜色，按钮将根据Quasar主题进行样式设置，包括文本颜色。
        请注意，像"red"这样的颜色既是Quasar颜色又是CSS颜色。
        在这种情况下，将使用Quasar颜色。

        :param text: 按钮的标签
        :param value: 下拉菜单是否打开（默认：`False`）
        :param on_value_change: 当下拉菜单打开或关闭时调用的回调函数
        :param on_click: 当按钮被按下时调用的回调函数
        :param color: 按钮的颜色（Quasar、Tailwind或CSS颜色，或`None`，默认：'primary'）
        :param icon: 要在按钮上显示的图标名称（默认：`None`）
        :param auto_close: 当点击项目时下拉菜单是否应该自动关闭（默认：`False`）
        :param split: 是否将下拉图标分割为单独的按钮（默认：`False`）
        """
        super().__init__(tag='q-btn-dropdown',
                         icon=icon, text=text, background_color=color, value=value, on_value_change=on_value_change)

        if auto_close:
            self._props['auto-close'] = True

        if split:
            self._props['split'] = True

        if on_click:
            self.on_click(on_click)

    def on_click(self, callback: Handler[ClickEventArguments]) -> Self:
        """添加当下拉按钮被点击时调用的回调函数。

        **在版本2.22.0中添加**
        """
        self.on('click', lambda _: handle_event(callback, ClickEventArguments(sender=self, client=self.client)), [])
        return self

    def _text_to_model_text(self, text: str) -> None:
        self._props['label'] = text

    def open(self) -> None:
        """打开下拉菜单。"""
        self.value = True

    def close(self) -> None:
        """关闭下拉菜单。"""
        self.value = False

    def toggle(self) -> None:
        """切换下拉菜单。"""
        self.value = not self.value
