from typing import Any, Callable, Optional, cast

from typing_extensions import Self

from ...binding import BindableProperty, bind, bind_from, bind_to
from ...element import Element


class TextElement(Element):
    """文本元素混入

    为元素提供文本内容管理功能的混入类。
    支持文本绑定和动态更新。
    """
    text = BindableProperty(
        on_change=lambda sender, text: cast(Self, sender)._handle_text_change(text))  # pylint: disable=protected-access

    def __init__(self, *, text: str, **kwargs: Any) -> None:
        """初始化文本元素

        :param text: 元素的文本内容
        """
        super().__init__(**kwargs)
        self.text = text
        self._text_to_model_text(text)

    def bind_text_to(self,
                     target_object: Any,
                     target_name: str = 'text',
                     forward: Optional[Callable[[Any], Any]] = None,
                     ) -> Self:
        """将此元素的文本绑定到目标对象的target_name属性。

        绑定是单向的，从此元素到目标。
        更新会立即发生，并在值变化时进行。

        :param target_object: 要绑定到的对象。
        :param target_name: 要绑定到的属性名称。
        :param forward: 在应用到目标之前应用于值的函数（默认：恒等函数）。
        """
        bind_to(self, 'text', target_object, target_name, forward)
        return self

    def bind_text_from(self,
                       target_object: Any,
                       target_name: str = 'text',
                       backward: Optional[Callable[[Any], Any]] = None,
                       ) -> Self:
        """将此元素的文本从目标对象的target_name属性绑定。

        绑定是单向的，从目标到此元素。
        更新会立即发生，并在值变化时进行。

        :param target_object: 要绑定来源的对象。
        :param target_name: 要绑定来源的属性名称。
        :param backward: 在应用到元素之前应用于值的函数（默认：恒等函数）。
        """
        bind_from(self, 'text', target_object, target_name, backward)
        return self

    def bind_text(self,
                  target_object: Any,
                  target_name: str = 'text', *,
                  forward: Optional[Callable[[Any], Any]] = None,
                  backward: Optional[Callable[[Any], Any]] = None,
                  ) -> Self:
        """将此元素的文本绑定到目标对象的target_name属性。

        绑定是双向的，从此元素到目标和从目标到此元素。
        更新会立即发生，并在值变化时进行。
        反向绑定在初始同步时具有优先权。

        :param target_object: 要绑定到的对象。
        :param target_name: 要绑定到的属性名称。
        :param forward: 在应用到目标之前应用于值的函数（默认：恒等函数）。
        :param backward: 在应用到元素之前应用于值的函数（默认：恒等函数）。
        """
        bind(self, 'text', target_object, target_name, forward=forward, backward=backward)
        return self

    def set_text(self, text: str) -> None:
        """设置此元素的文本。

        :param text: 新文本。
        """
        self.text = text

    def _handle_text_change(self, text: str) -> None:
        """当元素文本变化时调用。

        :param text: 新文本。
        """
        self._text_to_model_text(text)
        self.update()

    def _text_to_model_text(self, text: str) -> None:
        """将文本转换为模型文本格式

        :param text: 要转换的文本
        """
        self._text = text
