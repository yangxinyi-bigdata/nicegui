from typing import Any, Callable, Optional, cast

from typing_extensions import Self

from ...binding import BindableProperty, bind, bind_from, bind_to
from ...element import Element


class DisableableElement(Element):
    """可禁用元素混入

    为元素提供启用/禁用状态管理功能的混入类。
    支持状态绑定和事件忽略控制。
    """
    enabled = BindableProperty(
        on_change=lambda sender, value: cast(Self, sender)._handle_enabled_change(value))  # pylint: disable=protected-access

    def __init__(self, **kwargs: Any) -> None:
        """初始化可禁用元素
        """
        super().__init__(**kwargs)
        self.enabled = True
        self.ignores_events_when_disabled = True

    @property
    def is_ignoring_events(self) -> bool:
        """返回元素当前是否正在忽略事件。"""
        if super().is_ignoring_events:
            return True
        return not self.enabled and self.ignores_events_when_disabled

    def enable(self) -> None:
        """启用元素。"""
        self.enabled = True

    def disable(self) -> None:
        """禁用元素。"""
        self.enabled = False

    def bind_enabled_to(self,
                        target_object: Any,
                        target_name: str = 'enabled',
                        forward: Optional[Callable[[Any], Any]] = None,
                        ) -> Self:
        """将此元素的启用状态绑定到目标对象的target_name属性。

        绑定是单向的，从此元素到目标。
        更新会立即发生，并在值变化时进行。

        :param target_object: 要绑定到的对象。
        :param target_name: 要绑定到的属性名称。
        :param forward: 在应用到目标之前应用于值的函数（默认：恒等函数）。
        """
        bind_to(self, 'enabled', target_object, target_name, forward)
        return self

    def bind_enabled_from(self,
                          target_object: Any,
                          target_name: str = 'enabled',
                          backward: Optional[Callable[[Any], Any]] = None,
                          ) -> Self:
        """将此元素的启用状态从目标对象的target_name属性绑定。

        绑定是单向的，从目标到此元素。
        更新会立即发生，并在值变化时进行。

        :param target_object: 要绑定来源的对象。
        :param target_name: 要绑定来源的属性名称。
        :param backward: 在应用到元素之前应用于值的函数（默认：恒等函数）。
        """
        bind_from(self, 'enabled', target_object, target_name, backward)
        return self

    def bind_enabled(self,
                     target_object: Any,
                     target_name: str = 'enabled', *,
                     forward: Optional[Callable[[Any], Any]] = None,
                     backward: Optional[Callable[[Any], Any]] = None,
                     ) -> Self:
        """将此元素的启用状态绑定到目标对象的target_name属性。

        绑定是双向的，从此元素到目标和从目标到此元素。
        更新会立即发生，并在值变化时进行。
        反向绑定在初始同步时具有优先权。

        :param target_object: 要绑定到的对象。
        :param target_name: 要绑定到的属性名称。
        :param forward: 在应用到目标之前应用于值的函数（默认：恒等函数）。
        :param backward: 在应用到元素之前应用于值的函数（默认：恒等函数）。
        """
        bind(self, 'enabled', target_object, target_name, forward=forward, backward=backward)
        return self

    def set_enabled(self, value: bool) -> None:
        """设置元素的启用状态。

        :param value: 启用状态。
        """
        self.enabled = value

    def _handle_enabled_change(self, enabled: bool) -> None:
        """当元素启用或禁用时调用。

        :param enabled: 新状态。
        """
        self._props['disable'] = not enabled
        self.update()
