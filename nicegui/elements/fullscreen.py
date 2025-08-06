from typing import Optional

from ..events import Handler, ValueChangeEventArguments
from .mixins.value_element import ValueElement


class Fullscreen(ValueElement, component='fullscreen.js'):
    LOOPBACK = None

    def __init__(self, *,
                 require_escape_hold: bool = False,
                 on_value_change: Optional[Handler[ValueChangeEventArguments]] = None) -> None:
        """全屏控制元素

        此元素基于Quasar的`AppFullscreen <https://quasar.dev/quasar-plugins/app-fullscreen>`_插件，
        提供进入、退出和切换全屏模式的方法。

        重要说明：

        * 由于安全原因，全屏模式只能从先前的用户交互（如按钮点击）进入。
        * 长按退出键要求仅在某些浏览器（如Google Chrome或Microsoft Edge）中有效。

        *在版本2.11.0中添加*

        :param require_escape_hold: 用户是否需要长按退出键来退出全屏模式
        :param on_value_change: 全屏状态变化时调用的回调函数
        """
        super().__init__(value=False, on_value_change=on_value_change)
        self._props['requireEscapeHold'] = require_escape_hold

    @property
    def require_escape_hold(self) -> bool:
        """用户是否需要长按退出键来退出全屏模式。

        此功能仅在某些浏览器（如Google Chrome或Microsoft Edge）中受支持。
        在不支持的浏览器中，此设置无效。
        """
        return self._props['requireEscapeHold']

    @require_escape_hold.setter
    def require_escape_hold(self, value: bool) -> None:
        self._props['requireEscapeHold'] = value
        self.update()

    def enter(self) -> None:
        """进入全屏模式。"""
        self.value = True

    def exit(self) -> None:
        """退出全屏模式。"""
        self.value = False

    def toggle(self) -> None:
        """切换全屏模式。"""
        self.value = not self.value

    def _handle_value_change(self, value: bool) -> None:
        super()._handle_value_change(value)
        self.run_method('enter' if value else 'exit')
