from typing import Any, Callable, Optional, cast

from typing_extensions import Self

from ...binding import BindableProperty, bind, bind_from, bind_to
from ...element import Element


class FilterElement(Element):
    """过滤元素混入

    为元素提供过滤功能管理的混入类。
    支持过滤器绑定和动态更新。
    """
    FILTER_PROP = 'filter'
    filter = BindableProperty(
        on_change=lambda sender, filter: cast(Self, sender)._handle_filter_change(filter))  # pylint: disable=protected-access

    def __init__(self, *, filter: Optional[str] = None, **kwargs: Any) -> None:  # pylint: disable=redefined-builtin
        """初始化过滤元素

        :param filter: 过滤器字符串
        """
        super().__init__(**kwargs)
        self.filter = filter
        self._props[self.FILTER_PROP] = filter

    def bind_filter_to(self,
                       target_object: Any,
                       target_name: str = 'filter',
                       forward: Optional[Callable[[Any], Any]] = None,
                       ) -> Self:
        """将此元素的过滤器绑定到目标对象的target_name属性。

        绑定是单向的，从此元素到目标。
        更新会立即发生，并在值变化时进行。

        :param target_object: 要绑定到的对象。
        :param target_name: 要绑定到的属性名称。
        :param forward: 在应用到目标之前应用于值的函数（默认：恒等函数）。
        """
        bind_to(self, 'filter', target_object, target_name, forward)
        return self

    def bind_filter_from(self,
                         target_object: Any,
                         target_name: str = 'filter',
                         backward: Optional[Callable[[Any], Any]] = None,
                         ) -> Self:
        """将此元素的过滤器从目标对象的target_name属性绑定。

        绑定是单向的，从目标到此元素。
        更新会立即发生，并在值变化时进行。

        :param target_object: 要绑定来源的对象。
        :param target_name: 要绑定来源的属性名称。
        :param backward: 在应用到元素之前应用于值的函数（默认：恒等函数）。
        """
        bind_from(self, 'filter', target_object, target_name, backward)
        return self

    def bind_filter(self,
                    target_object: Any,
                    target_name: str = 'filter', *,
                    forward: Optional[Callable[[Any], Any]] = None,
                    backward: Optional[Callable[[Any], Any]] = None,
                    ) -> Self:
        """将此元素的过滤器绑定到目标对象的target_name属性。

        绑定是双向的，从此元素到目标和从目标到此元素。
        更新会立即发生，并在值变化时进行。
        反向绑定在初始同步时具有优先权。

        :param target_object: 要绑定到的对象。
        :param target_name: 要绑定到的属性名称。
        :param forward: 在应用到目标之前应用于值的函数（默认：恒等函数）。
        :param backward: 在应用到元素之前应用于值的函数（默认：恒等函数）。
        """
        bind(self, 'filter', target_object, target_name, forward=forward, backward=backward)
        return self

    def set_filter(self, filter_: str) -> None:
        """设置此元素的过滤器。

        :param filter_: 新过滤器。
        """
        self.filter = filter_

    def _handle_filter_change(self, filter_: str) -> None:
        """当元素过滤器变化时调用。

        :param filter_: 新过滤器。
        """
        self._props[self.FILTER_PROP] = filter_
        self.update()
