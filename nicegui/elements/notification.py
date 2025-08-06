import asyncio
from typing import Any, Dict, Literal, Optional, Union

from typing_extensions import Self

from ..context import context
from ..element import Element
from ..events import Handler, UiEventArguments, handle_event

NotificationPosition = Literal[
    'top-left',
    'top-right',
    'bottom-left',
    'bottom-right',
    'top',
    'bottom',
    'left',
    'right',
    'center',
]

NotificationType = Optional[Literal[
    'positive',
    'negative',
    'warning',
    'info',
    'ongoing',
]]


class Notification(Element, component='notification.js'):

    def __init__(self,
                 message: Any = '', *,
                 position: NotificationPosition = 'bottom',
                 close_button: Union[bool, str] = False,
                 type: NotificationType = None,  # pylint: disable=redefined-builtin
                 color: Optional[str] = None,
                 multi_line: bool = False,
                 icon: Optional[str] = None,
                 spinner: bool = False,
                 timeout: Optional[float] = 5.0,
                 on_dismiss: Optional[Handler[UiEventArguments]] = None,
                 options: Optional[Dict] = None,
                 **kwargs: Any,
                 ) -> None:
        """通知元素

        在屏幕上显示通知。
        与`ui.notify`不同，此元素允许在通知显示后更新通知消息和其他属性。
        通知可以使用`dismiss()`移除。

        :param message: 通知的内容
        :param position: 屏幕上的位置（"top-left"、"top-right"、"bottom-left"、"bottom-right"、"top"、"bottom"、"left"、"right"或"center"，默认："bottom"）
        :param close_button: 用于解除通知的按钮的可选标签（默认：`False`）
        :param type: 可选类型（"positive"、"negative"、"warning"、"info"或"ongoing"）
        :param color: 可选颜色名称
        :param multi_line: 启用多行通知
        :param icon: 要在通知中显示的图标的可选名称（默认：`None`）
        :param spinner: 在通知中显示旋转器（默认：False）
        :param timeout: 通知被解除的可选超时时间（秒）（默认：5.0）
        :param on_dismiss: 通知被解除时调用的可选回调函数
        :param options: 包含所有选项的可选字典（覆盖所有其他参数）

        注意：您可以根据`Quasar的Notify API <https://quasar.dev/quasar-plugins/notify#notify-api>`_传递其他关键字参数。
        """
        with context.client.layout:
            super().__init__()
        self._update_method = 'update_notification'
        if options:
            self._props['options'] = options
        else:
            self._props['options'] = {
                'message': str(message),
                'position': position,
                'multiLine': multi_line,
                'spinner': spinner,
                'closeBtn': close_button,
                'timeout': (timeout or 0) * 1000,
                'group': False,
            }
            if type is not None:
                self._props['options']['type'] = type
            if color is not None:
                self._props['options']['color'] = color
            if icon is not None:
                self._props['options']['icon'] = icon
            self._props['options'].update(kwargs)

        if on_dismiss:
            self.on_dismiss(on_dismiss)

        async def handle_dismiss() -> None:
            if self.client.is_auto_index_client:
                self.dismiss()
                await asyncio.sleep(1.0)  # NOTE: sent dismiss message to all browsers before deleting the element
            if not self._deleted:
                self.clear()
                self.delete()
        self.on('dismiss', handle_dismiss)

    @property
    def message(self) -> str:
        """通知消息文本。"""
        return self._props['options']['message']

    @message.setter
    def message(self, value: Any) -> None:
        self._props['options']['message'] = str(value)
        self.update()

    @property
    def position(self) -> NotificationPosition:
        """屏幕上的位置。"""
        return self._props['options']['position']

    @position.setter
    def position(self, value: NotificationPosition) -> None:
        self._props['options']['position'] = value
        self.update()

    @property
    def type(self) -> NotificationType:
        """通知的类型。"""
        return self._props['options'].get('type')

    @type.setter
    def type(self, value: NotificationType) -> None:
        if value is None:
            self._props['options'].pop('type', None)
        else:
            self._props['options']['type'] = value
        self.update()

    @property
    def color(self) -> Optional[str]:
        """通知的颜色。"""
        return self._props['options'].get('color')

    @color.setter
    def color(self, value: Optional[str]) -> None:
        if value is None:
            self._props['options'].pop('color', None)
        else:
            self._props['options']['color'] = value
        self.update()

    @property
    def multi_line(self) -> bool:
        """通知是否为多行。"""
        return self._props['options']['multiLine']

    @multi_line.setter
    def multi_line(self, value: bool) -> None:
        self._props['options']['multiLine'] = value
        self.update()

    @property
    def icon(self) -> Optional[str]:
        """通知的图标。"""
        return self._props['options'].get('icon')

    @icon.setter
    def icon(self, value: Optional[str]) -> None:
        if value is None:
            self._props['options'].pop('icon', None)
        else:
            self._props['options']['icon'] = value
        self.update()

    @property
    def spinner(self) -> bool:
        """通知是否为旋转器。"""
        return self._props['options']['spinner']

    @spinner.setter
    def spinner(self, value: bool) -> None:
        self._props['options']['spinner'] = value
        self.update()

    @property
    def timeout(self) -> float:
        """通知的超时时间（秒）。

        *在版本2.13.0中添加*
        """
        return self._props['options']['timeout'] / 1000

    @timeout.setter
    def timeout(self, value: Optional[float]) -> None:
        self._props['options']['timeout'] = (value or 0) * 1000
        self.update()

    @property
    def close_button(self) -> Union[bool, str]:
        """通知是否有关闭按钮。"""
        return self._props['options']['closeBtn']

    @close_button.setter
    def close_button(self, value: Union[bool, str]) -> None:
        self._props['options']['closeBtn'] = value
        self.update()

    def on_dismiss(self, callback: Handler[UiEventArguments]) -> Self:
        """添加通知被解除时调用的回调函数。"""
        self.on('dismiss', lambda _: handle_event(callback, UiEventArguments(sender=self, client=self.client)), [])
        return self

    def dismiss(self) -> None:
        """解除通知。"""
        self.run_method('dismiss')

    def set_visibility(self, visible: bool) -> None:
        raise NotImplementedError('Use `dismiss()` to remove the notification. See #3670 for more information.')
