from typing import Literal, Optional

from typing_extensions import Self

from ..events import ClickEventArguments, Handler, handle_event
from .mixins.color_elements import BackgroundColorElement
from .mixins.disableable_element import DisableableElement
from .mixins.icon_element import IconElement
from .mixins.label_element import LabelElement
from .mixins.value_element import ValueElement


class Fab(ValueElement, LabelElement, IconElement, BackgroundColorElement, DisableableElement):

    def __init__(self,
                 icon: str, *,
                 value: bool = False,
                 label: str = '',
                 color: Optional[str] = 'primary',
                 direction: Literal['up', 'down', 'left', 'right'] = 'right',
                 ) -> None:
        """浮动操作按钮（FAB）

        可用于触发操作的浮动操作按钮。
        此元素基于Quasar的`QFab <https://quasar.dev/vue-components/floating-action-button#qfab-api>`_组件。

        :param icon: 在FAB上显示的图标
        :param value: FAB是否已打开（默认：``False``）
        :param label: FAB的可选标签
        :param color: FAB的背景颜色（默认："primary"）
        :param direction: FAB的方向（"up", "down", "left", "right"，默认："right"）
        """
        super().__init__(tag='q-fab', value=value, label=label, background_color=color, icon=icon)
        self._props['direction'] = direction

    def open(self) -> None:
        """打开FAB。"""
        self.value = True

    def close(self) -> None:
        """关闭FAB。"""
        self.value = False

    def toggle(self) -> None:
        """切换FAB。"""
        self.value = not self.value


class FabAction(LabelElement, IconElement, BackgroundColorElement, DisableableElement):

    def __init__(self, icon: str, *,
                 label: str = '',
                 on_click: Optional[Handler[ClickEventArguments]] = None,
                 color: Optional[str] = 'primary',
                 auto_close: bool = True,
                 ) -> None:
        """浮动操作按钮操作

        可添加到浮动操作按钮（FAB）的操作。
        此元素基于Quasar的`QFabAction <https://quasar.dev/vue-components/floating-action-button#qfabaction-api>`_组件。

        **在版本2.22.0中添加**

        :param icon: 在操作按钮上显示的图标
        :param label: 操作按钮的可选标签
        :param color: 操作按钮的背景颜色（默认："primary"）
        :param auto_close: 点击事件后是否应关闭FAB（默认：``True``）
        """
        super().__init__(tag='q-fab-action', label=label, background_color=color, icon=icon)
        self.fab = next((e for e in self.ancestors() if isinstance(e, Fab)), None)
        if self.fab and not auto_close:
            self.on('click', self.fab.open)

        if on_click:
            self.on_click(on_click)

    def on_click(self, callback: Handler[ClickEventArguments]) -> Self:
        """添加点击操作元素时要调用的回调函数。"""
        self.on('click', lambda _: handle_event(callback, ClickEventArguments(sender=self, client=self.client)), [])
        return self
