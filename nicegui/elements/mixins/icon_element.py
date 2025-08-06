from typing import Any, Callable, Optional, cast

from typing_extensions import Self

from ...binding import BindableProperty, bind, bind_from, bind_to
from ...element import Element


class IconElement(Element):
    """图标元素混入

    为元素提供图标管理功能的混入类。
    支持图标绑定和动态更新。
    """
    icon = BindableProperty(
        on_change=lambda sender, icon: cast(Self, sender)._handle_icon_change(icon))  # pylint: disable=protected-access

    def __init__(self, *, icon: Optional[str] = None, **kwargs: Any) -> None:  # pylint: disable=redefined-builtin
        """初始化图标元素

        :param icon: 图标名称
        """
        super().__init__(**kwargs)
        self.icon = icon
        if icon is not None:
            self._props['icon'] = icon

    def bind_icon_to(self,
                     target_object: Any,
                     target_name: str = 'icon',
                     forward: Optional[Callable[[Any], Any]] = None,
                     ) -> Self:
        """将此元素的图标绑定到目标对象的target_name属性。

        绑定是单向的，从此元素到目标。
        更新会立即发生，并在值变化时进行。

        :param target_object: 要绑定到的对象。
        :param target_name: 要绑定到的属性名称。
        :param forward: 在应用到目标之前应用于值的函数（默认：恒等函数）。
        """
        bind_to(self, 'icon', target_object, target_name, forward)
        return self

    def bind_icon_from(self,
                       target_object: Any,
                       target_name: str = 'icon',
                       backward: Optional[Callable[[Any], Any]] = None,
                       ) -> Self:
        """将此元素的图标从目标对象的target_name属性绑定。

        绑定是单向的，从目标到此元素。
        更新会立即发生，并在值变化时进行。

        :param target_object: 要绑定来源的对象。
        :param target_name: 要绑定来源的属性名称。
        :param backward: 在应用到元素之前应用于值的函数（默认：恒等函数）。
        """
        bind_from(self, 'icon', target_object, target_name, backward)
        return self

    def bind_icon(self,
                  target_object: Any,
                  target_name: str = 'icon', *,
                  forward: Optional[Callable[[Any], Any]] = None,
                  backward: Optional[Callable[[Any], Any]] = None,
                  ) -> Self:
        """将此元素的图标绑定到目标对象的target_name属性。

        绑定是双向的，从此元素到目标和从目标到此元素。
        更新会立即发生，并在值变化时进行。
        反向绑定在初始同步时具有优先权。

        :param target_object: 要绑定到的对象。
        :param target_name: 要绑定到的属性名称。
        :param forward: 在应用到目标之前应用于值的函数（默认：恒等函数）。
        :param backward: 在应用到元素之前应用于值的函数（默认：恒等函数）。
        """
        bind(self, 'icon', target_object, target_name, forward=forward, backward=backward)
        return self

    def set_icon(self, icon: Optional[str]) -> None:
        """设置此元素的图标。

        :param icon: 新图标。
        """
        self.icon = icon

    def _handle_icon_change(self, icon: Optional[str]) -> None:
        """当元素图标变化时调用。

        :param icon: 新图标。
        """
        if icon is not None:
            self._props['icon'] = icon
        else:
            self._props.pop('icon', None)
        self.update()
