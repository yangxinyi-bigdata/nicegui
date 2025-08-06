import asyncio
from typing import Any, Optional

from .mixins.value_element import ValueElement


class Dialog(ValueElement):

    def __init__(self, *, value: bool = False) -> None:
        """对话框

        基于Quasar的`QDialog <https://quasar.dev/vue-components/dialog>`_组件创建对话框。
        默认情况下，可以通过点击或按ESC键来关闭。
        要使其持久化，请在对话框元素上设置`.props('persistent')`。

        注意：对话框是一个元素。
        这意味着它在关闭时不会被删除，只是被隐藏。
        您应该只创建一次然后重用它，或者在关闭后用`.clear()`删除它。

        :param value: 对话框在创建时是否应该打开（默认：`False`）
        """
        super().__init__(tag='q-dialog', value=value, on_value_change=None)
        self._result: Any = None
        self._submitted: Optional[asyncio.Event] = None

    @property
    def submitted(self) -> asyncio.Event:
        """当对话框被提交时设置的事件。"""
        if self._submitted is None:
            self._submitted = asyncio.Event()
        return self._submitted

    def open(self) -> None:
        """打开对话框。"""
        self.value = True

    def close(self) -> None:
        """关闭对话框。"""
        self.value = False

    def __await__(self):
        self._result = None
        self.submitted.clear()
        self.open()
        yield from self.submitted.wait().__await__()  # pylint: disable=no-member
        result = self._result
        self.close()
        return result

    def submit(self, result: Any) -> None:
        """使用给定的结果提交对话框。"""
        self._result = result
        self.submitted.set()

    def _handle_value_change(self, value: Any) -> None:
        super()._handle_value_change(value)
        if not self.value:
            self._result = None
            self.submitted.set()
