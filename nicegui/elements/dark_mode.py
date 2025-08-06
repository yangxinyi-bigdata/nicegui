from typing import Optional

from .. import core, helpers
from ..events import Handler, ValueChangeEventArguments
from .mixins.value_element import ValueElement


class DarkMode(ValueElement, component='dark_mode.js'):
    VALUE_PROP = 'value'

    def __init__(self, value: Optional[bool] = False, *, on_change: Optional[Handler[ValueChangeEventArguments]] = None) -> None:
        """深色模式

        您可以使用此元素在页面上启用、禁用或切换深色模式。
        值`None`表示自动模式，使用客户端的系统偏好设置。

        请注意，此元素会覆盖`ui.run`函数和页面装饰器的`dark`参数。

        :param value: 是否启用深色模式。如果为None，则将深色模式设置为自动。
        :param on_change: 值变化时调用的回调函数。
        """
        super().__init__(value=value, on_value_change=on_change)

        # HACK: this is a temporary warning to inform users about issue #3753
        if core.app.is_started:
            self._check_for_issue_3753()
        else:
            core.app.on_startup(self._check_for_issue_3753)

    def _check_for_issue_3753(self) -> None:
        if self.client.page.resolve_dark() is None and core.app.config.tailwind:
            helpers.warn_once(
                '`ui.dark_mode` is not supported on pages with `dark=None` while running with `tailwind=True` (the default). '
                'See https://github.com/zauberzeug/nicegui/issues/3753 for more information.'
            )

    def enable(self) -> None:
        """启用深色模式。"""
        self.value = True

    def disable(self) -> None:
        """禁用深色模式。"""
        self.value = False

    def toggle(self) -> None:
        """切换深色模式。

        如果深色模式设置为自动，此方法将引发ValueError。
        """
        if self.value is None:
            raise ValueError('Cannot toggle dark mode when it is set to auto.')
        self.value = not self.value

    def auto(self) -> None:
        """将深色模式设置为自动。

        这将使用客户端的系统偏好设置。
        """
        self.value = None
