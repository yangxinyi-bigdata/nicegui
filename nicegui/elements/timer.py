from contextlib import nullcontext
from typing import ContextManager

from ..client import Client
from ..element import Element
from ..logging import log
from ..timer import Timer as BaseTimer


class Timer(BaseTimer, Element, component='timer.js'):

    def _get_context(self) -> ContextManager:
        return self.parent_slot or nullcontext()

    async def _can_start(self) -> bool:
        """在允许计时器回调操作状态之前等待客户端连接。

        详情请参见 https://github.com/zauberzeug/nicegui/issues/206。
        如果客户端已连接则返回True，如果客户端未连接且计时器应该被取消则返回False。
        """
        if self.client.shared:
            return True

        # ignore served pages which do not reconnect to backend (e.g. monitoring requests, scrapers etc.)
        TIMEOUT = 60.0
        try:
            await self.client.connected(timeout=TIMEOUT)
            return True
        except TimeoutError:
            log.error(f'Timer cancelled because client is not connected after {TIMEOUT} seconds')
            return False

    def _should_stop(self) -> bool:
        return (
            self.is_deleted or
            self.client.id not in Client.instances or
            super()._should_stop()
        )

    def _cleanup(self) -> None:
        super()._cleanup()
        if not self._deleted:
            assert self.parent_slot
            self.parent_slot.parent.remove(self)

    def set_visibility(self, visible: bool) -> None:
        raise NotImplementedError('Use `activate()`, `deactivate()` or `cancel()`. See #3670 for more information.')
