from typing import Any, Callable, Optional, cast

from typing_extensions import Self

from ...binding import BindableProperty, bind, bind_from, bind_to
from ...element import Element


class LabelElement(Element):
    """标签元素混入

    为元素提供标签管理功能的混入类。
    支持标签绑定和动态更新。
    """
    label = BindableProperty(
        on_change=lambda sender, label: cast(Self, sender)._handle_label_change(label))  # pylint: disable=protected-access

    def __init__(self, *, label: Optional[str], **kwargs: Any) -> None:
        """初始化标签元素

        :param label: 标签文本
        """
        super().__init__(**kwargs)
        self.label = label
        if label is not None:
            self._props['label'] = label

    def bind_label_to(self,
                      target_object: Any,
                      target_name: str = 'label',
                      forward: Optional[Callable[[Any], Any]] = None,
                      ) -> Self:
        """将此元素的标签绑定到目标对象的target_name属性。

        绑定是单向的，从此元素到目标。
        更新会立即发生，并在值变化时进行。

        :param target_object: 要绑定到的对象。
        :param target_name: 要绑定到的属性名称。
        :param forward: 在应用到目标之前应用于值的函数（默认：恒等函数）。
        """
        bind_to(self, 'label', target_object, target_name, forward)
        return self

    def bind_label_from(self,
                        target_object: Any,
                        target_name: str = 'label',
                        backward: Optional[Callable[[Any], Any]] = None,
                        ) -> Self:
        """将此元素的标签从目标对象的target_name属性绑定。

        绑定是单向的，从目标到此元素。
        更新会立即发生，并在值变化时进行。

        :param target_object: 要绑定来源的对象。
        :param target_name: 要绑定来源的属性名称。
        :param backward: 在应用到元素之前应用于值的函数（默认：恒等函数）。
        """
        bind_from(self, 'label', target_object, target_name, backward)
        return self

    def bind_label(self,
                   target_object: Any,
                   target_name: str = 'label', *,
                   forward: Optional[Callable[[Any], Any]] = None,
                   backward: Optional[Callable[[Any], Any]] = None,
                   ) -> Self:
        """将此元素的标签绑定到目标对象的target_name属性。

        绑定是双向的，从此元素到目标和从目标到此元素。
        更新会立即发生，并在值变化时进行。
        反向绑定在初始同步时具有优先权。

        :param target_object: 要绑定到的对象。
        :param target_name: 要绑定到的属性名称。
        :param forward: 在应用到目标之前应用于值的函数（默认：恒等函数）。
        :param backward: 在应用到元素之前应用于值的函数（默认：恒等函数）。
        """
        bind(self, 'label', target_object, target_name, forward=forward, backward=backward)
        return self

    def set_label(self, label: Optional[str]) -> None:
        """设置此元素的标签。

        :param label: 新标签。
        """
        self.label = label

    def _handle_label_change(self, label: Optional[str]) -> None:
        """当元素标签变化时调用。

        :param label: 新标签。
        """
        if label is None:
            del self._props['label']
        else:
            self._props['label'] = label
        self.update()
