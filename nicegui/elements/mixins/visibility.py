from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable, Optional, cast

from typing_extensions import Self

from ...binding import BindableProperty, bind, bind_from, bind_to

if TYPE_CHECKING:
    from ...element import Element


class Visibility:
    """可见性混入

    为元素提供可见性管理功能的混入类。
    支持可见性绑定和隐藏时事件忽略控制。
    通过CSS 'hidden' 类控制元素可见性。
    """
    visible = BindableProperty(
        on_change=lambda sender, visible: cast(Self, sender)._handle_visibility_change(visible))  # pylint: disable=protected-access

    def __init__(self, **kwargs: Any) -> None:
        """初始化可见性混入
        """
        super().__init__(**kwargs)
        self.visible = True
        self.ignores_events_when_hidden = True

    @property
    def is_ignoring_events(self) -> bool:
        """返回元素当前是否正在忽略事件。"""
        return not self.visible and self.ignores_events_when_hidden

    def bind_visibility_to(self,
                           target_object: Any,
                           target_name: str = 'visible',
                           forward: Optional[Callable[[Any], Any]] = None,
                           ) -> Self:
        """将此元素的可见性绑定到目标对象的target_name属性。

        绑定是单向的，从此元素到目标。
        更新会立即发生，并在值变化时进行。

        :param target_object: 要绑定到的对象。
        :param target_name: 要绑定到的属性名称。
        :param forward: 在应用到目标之前应用于值的函数（默认：恒等函数）。
        """
        bind_to(self, 'visible', target_object, target_name, forward)
        return self

    def bind_visibility_from(self,
                             target_object: Any,
                             target_name: str = 'visible',
                             backward: Optional[Callable[[Any], Any]] = None, *,
                             value: Any = None) -> Self:
        """将此元素的可见性从目标对象的target_name属性绑定。

        绑定是单向的，从目标到此元素。
        更新会立即发生，并在值变化时进行。

        :param target_object: 要绑定来源的对象。
        :param target_name: 要绑定来源的属性名称。
        :param backward: 在应用到元素之前应用于值的函数（默认：恒等函数）。
        :param value: 如果指定，只有当目标值等于此值时元素才可见。
        """
        if value is not None:
            def backward(x):  # pylint: disable=function-redefined
                return x == value
        bind_from(self, 'visible', target_object, target_name, backward)
        return self

    def bind_visibility(self,
                        target_object: Any,
                        target_name: str = 'visible', *,
                        forward: Optional[Callable[[Any], Any]] = None,
                        backward: Optional[Callable[[Any], Any]] = None,
                        value: Any = None,
                        ) -> Self:
        """将此元素的可见性绑定到目标对象的target_name属性。

        绑定是双向的，从此元素到目标和从目标到此元素。
        更新会立即发生，并在值变化时进行。
        反向绑定在初始同步时具有优先权。

        :param target_object: 要绑定到的对象。
        :param target_name: 要绑定到的属性名称。
        :param forward: 在应用到目标之前应用于值的函数（默认：恒等函数）。
        :param backward: 在应用到元素之前应用于值的函数（默认：恒等函数）。
        :param value: 如果指定，只有当目标值等于此值时元素才可见。
        """
        if value is not None:
            def backward(x):  # pylint: disable=function-redefined
                return x == value
        bind(self, 'visible', target_object, target_name, forward=forward, backward=backward)
        return self

    def set_visibility(self, visible: bool) -> None:
        """设置此元素的可见性。

        :param visible: 元素是否应该可见。
        """
        self.visible = visible

    def _handle_visibility_change(self, visible: str) -> None:
        """当元素可见性变化时调用。

        :param visible: 元素是否应该可见。
        """
        element: Element = cast('Element', self)
        classes = element.classes  # pylint: disable=no-member
        if visible and 'hidden' in classes:
            classes.remove('hidden')
            element.update()  # pylint: disable=no-member
        if not visible and 'hidden' not in classes:
            classes.append('hidden')
            element.update()  # pylint: disable=no-member
