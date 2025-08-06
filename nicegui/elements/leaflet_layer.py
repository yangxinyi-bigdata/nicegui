from __future__ import annotations

import uuid
from abc import abstractmethod
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, ClassVar, Optional

from ..awaitable_response import AwaitableResponse
from ..dataclasses import KWONLY_SLOTS

if TYPE_CHECKING:
    from .leaflet import Leaflet


@dataclass(**KWONLY_SLOTS)
class Layer:
    current_leaflet: ClassVar[Optional[Leaflet]] = None
    leaflet: Leaflet = field(init=False)
    id: str = field(init=False)

    def __post_init__(self) -> None:
        self.id = str(uuid.uuid4())
        assert self.current_leaflet is not None
        self.leaflet = self.current_leaflet
        self.leaflet.layers.append(self)
        self.leaflet.run_method('add_layer', self.to_dict(), self.id)

    @abstractmethod
    def to_dict(self) -> dict:
        """返回图层的字典表示。"""

    def run_method(self, name: str, *args: Any, timeout: float = 1) -> AwaitableResponse:
        """运行Leaflet图层的方法。

        如果函数被等待，则返回方法调用的结果。
        否则，方法将执行而不等待响应。

        :param name: 方法名称（前缀":"表示参数是JavaScript表达式）
        :param args: 传递给方法的参数
        :param timeout: 超时时间，以秒为单位（默认：1秒）

        :return: 可以等待以获取方法调用结果的AwaitableResponse
        """
        return self.leaflet.run_method('run_layer_method', self.id, name, *args, timeout=timeout)
