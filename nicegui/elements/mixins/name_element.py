from typing import Any, Callable, Optional, cast

from typing_extensions import Self

from ...binding import BindableProperty, bind, bind_from, bind_to
from ...element import Element


class NameElement(Element):
    """名称元素混入

    为元素提供名称管理功能的混入类。
    支持名称绑定和动态更新。
    """
    name = BindableProperty(
        on_change=lambda sender, name: cast(Self, sender)._handle_name_change(name))  # pylint: disable=protected-access

    def __init__(self, *, name: str, **kwargs: Any) -> None:
        """初始化名称元素

        :param name: 元素名称
        """
        super().__init__(**kwargs)
        self.name = name
        self._props['name'] = name

    def bind_name_to(self,
                     target_object: Any,
                     target_name: str = 'name',
                     forward: Optional[Callable[[Any], Any]] = None,
                     ) -> Self:
        """将此元素的名称绑定到目标对象的target_name属性。

        绑定是单向的，从此元素到目标。
        更新会立即发生，并在值变化时进行。

        :param target_object: 要绑定到的对象。
        :param target_name: 要绑定到的属性名称。
        :param forward: 在应用到目标之前应用于值的函数（默认：恒等函数）。
        """
        bind_to(self, 'name', target_object, target_name, forward)
        return self

    def bind_name_from(self,
                       target_object: Any,
                       target_name: str = 'name',
                       backward: Optional[Callable[[Any], Any]] = None,
                       ) -> Self:
        """将此元素的名称从目标对象的target_name属性绑定。

        绑定是单向的，从目标到此元素。
        更新会立即发生，并在值变化时进行。

        :param target_object: 要绑定来源的对象。
        :param target_name: 要绑定来源的属性名称。
        :param backward: 在应用到元素之前应用于值的函数（默认：恒等函数）。
        """
        bind_from(self, 'name', target_object, target_name, backward)
        return self

    def bind_name(self,
                  target_object: Any,
                  target_name: str = 'name', *,
                  forward: Optional[Callable[[Any], Any]] = None,
                  backward: Optional[Callable[[Any], Any]] = None,
                  ) -> Self:
        """将此元素的名称绑定到目标对象的target_name属性。

        绑定是双向的，从此元素到目标和从目标到此元素。
        更新会立即发生，并在值变化时进行。
        反向绑定在初始同步时具有优先权。

        :param target_object: 要绑定到的对象。
        :param target_name: 要绑定到的属性名称。
        :param forward: 在应用到目标之前应用于值的函数（默认：恒等函数）。
        :param backward: 在应用到元素之前应用于值的函数（默认：恒等函数）。
        """
        bind(self, 'name', target_object, target_name, forward=forward, backward=backward)
        return self

    def set_name(self, name: str) -> None:
        """设置此元素的名称。

        :param name: 新名称。
        """
        self.name = name

    def _handle_name_change(self, name: str) -> None:
        """当元素名称变化时调用。

        :param name: 新名称。
        """
        self._props['name'] = name
        self.update()
