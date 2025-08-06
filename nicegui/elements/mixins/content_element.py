from typing import Any, Callable, Optional, cast

from typing_extensions import Self

from ...binding import BindableProperty, bind, bind_from, bind_to
from ...element import Element


class ContentElement(Element):
    """内容元素混入

    为元素提供HTML内容管理功能的混入类。
    支持内容绑定和动态更新。
    """
    CONTENT_PROP = 'innerHTML'
    content = BindableProperty(
        on_change=lambda sender, content: cast(Self, sender)._handle_content_change(content))  # pylint: disable=protected-access

    def __init__(self, *, content: str, **kwargs: Any) -> None:
        """初始化内容元素

        :param content: 元素的HTML内容
        """
        super().__init__(**kwargs)
        self.content = content
        self._handle_content_change(content)

    def bind_content_to(self,
                        target_object: Any,
                        target_name: str = 'content',
                        forward: Optional[Callable[[Any], Any]] = None,
                        ) -> Self:
        """将此元素的内容绑定到目标对象的target_name属性。

        绑定是单向的，从此元素到目标。
        更新会立即发生，并在值变化时进行。

        :param target_object: 要绑定到的对象。
        :param target_name: 要绑定到的属性名称。
        :param forward: 在应用到目标之前应用于值的函数（默认：恒等函数）。
        """
        bind_to(self, 'content', target_object, target_name, forward)
        return self

    def bind_content_from(self,
                          target_object: Any,
                          target_name: str = 'content',
                          backward: Optional[Callable[[Any], Any]] = None,
                          ) -> Self:
        """将此元素的内容从目标对象的target_name属性绑定。

        绑定是单向的，从目标到此元素。
        更新会立即发生，并在值变化时进行。

        :param target_object: 要绑定来源的对象。
        :param target_name: 要绑定来源的属性名称。
        :param backward: 在应用到元素之前应用于值的函数（默认：恒等函数）。
        """
        bind_from(self, 'content', target_object, target_name, backward)
        return self

    def bind_content(self,
                     target_object: Any,
                     target_name: str = 'content', *,
                     forward: Optional[Callable[[Any], Any]] = None,
                     backward: Optional[Callable[[Any], Any]] = None,
                     ) -> Self:
        """将此元素的内容绑定到目标对象的target_name属性。

        绑定是双向的，从此元素到目标和从目标到此元素。
        更新会立即发生，并在值变化时进行。
        反向绑定在初始同步时具有优先权。

        :param target_object: 要绑定到的对象。
        :param target_name: 要绑定到的属性名称。
        :param forward: 在应用到目标之前应用于值的函数（默认：恒等函数）。
        :param backward: 在应用到元素之前应用于值的函数（默认：恒等函数）。
        """
        bind(self, 'content', target_object, target_name, forward=forward, backward=backward)
        return self

    def set_content(self, content: str) -> None:
        """设置此元素的内容。

        :param content: 新内容。
        """
        self.content = content

    def _handle_content_change(self, content: str) -> None:
        """当元素内容变化时调用。

        :param content: 新内容。
        """
        if self.CONTENT_PROP == 'innerHTML' and '</script>' in content:
            raise ValueError('HTML元素不能包含<script>标签。请使用ui.add_body_html()代替。')
        self._props[self.CONTENT_PROP] = content
        self.update()
