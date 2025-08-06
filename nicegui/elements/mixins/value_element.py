from typing import Any, Callable, List, Optional, cast

from typing_extensions import Self

from ...binding import BindableProperty, bind, bind_from, bind_to
from ...element import Element
from ...events import GenericEventArguments, Handler, ValueChangeEventArguments, handle_event


class ValueElement(Element):
    """值元素混入

    为元素提供值管理功能的混入类。
    支持值绑定、值变化事件处理和多种值更新策略。
    """
    VALUE_PROP: str = 'model-value'
    '''保存元素值的属性名称'''

    LOOPBACK: Optional[bool] = True
    '''是否直接在客户端设置新值，还是在从服务器获取更新后设置。

    - ``True``: 值通过向服务器发送变化事件来更新，服务器响应更新。
    - ``False``: 值通过直接在客户端设置VALUE_PROP来更新。
    - ``None``: 值由Vue元素自动更新。
    '''

    value = BindableProperty(
        on_change=lambda sender, value: cast(Self, sender)._handle_value_change(value))  # pylint: disable=protected-access

    def __init__(self, *,
                 value: Any,
                 on_value_change: Optional[Handler[ValueChangeEventArguments]] = None,
                 throttle: float = 0,
                 **kwargs: Any,
                 ) -> None:
        """初始化值元素

        :param value: 元素的初始值
        :param on_value_change: 值变化时的回调函数
        :param throttle: 事件节流时间（秒）
        """
        super().__init__(**kwargs)
        self._send_update_on_value_change = True
        self.set_value(value)
        self._props[self.VALUE_PROP] = self._value_to_model_value(value)
        self._props['loopback'] = self.LOOPBACK
        self._change_handlers: List[Handler[ValueChangeEventArguments]] = [on_value_change] if on_value_change else []

        def handle_change(e: GenericEventArguments) -> None:
            self._send_update_on_value_change = self.LOOPBACK is True
            self.set_value(self._event_args_to_value(e))
            self._send_update_on_value_change = True
        self.on(f'update:{self.VALUE_PROP}', handle_change, [None], throttle=throttle)

    def on_value_change(self, callback: Handler[ValueChangeEventArguments]) -> Self:
        """添加值变化时要调用的回调函数。"""
        self._change_handlers.append(callback)
        return self

    def bind_value_to(self,
                      target_object: Any,
                      target_name: str = 'value',
                      forward: Optional[Callable[[Any], Any]] = None,
                      ) -> Self:
        """将此元素的值绑定到目标对象的target_name属性。

        绑定是单向的，从此元素到目标。
        更新会立即发生，并在值变化时进行。

        :param target_object: 要绑定到的对象。
        :param target_name: 要绑定到的属性名称。
        :param forward: 在应用到目标之前应用于值的函数（默认：恒等函数）。
        """
        bind_to(self, 'value', target_object, target_name, forward)
        return self

    def bind_value_from(self,
                        target_object: Any,
                        target_name: str = 'value',
                        backward: Optional[Callable[[Any], Any]] = None,
                        ) -> Self:
        """将此元素的值从目标对象的target_name属性绑定。

        绑定是单向的，从目标到此元素。
        更新会立即发生，并在值变化时进行。

        :param target_object: 要绑定来源的对象。
        :param target_name: 要绑定来源的属性名称。
        :param backward: 在应用到元素之前应用于值的函数（默认：恒等函数）。
        """
        bind_from(self, 'value', target_object, target_name, backward)
        return self

    def bind_value(self,
                   target_object: Any,
                   target_name: str = 'value', *,
                   forward: Optional[Callable[[Any], Any]] = None,
                   backward: Optional[Callable[[Any], Any]] = None,
                   ) -> Self:
        """将此元素的值绑定到目标对象的target_name属性。

        绑定是双向的，从此元素到目标和从目标到此元素。
        更新会立即发生，并在值变化时进行。
        反向绑定在初始同步时具有优先权。

        :param target_object: 要绑定到的对象。
        :param target_name: 要绑定到的属性名称。
        :param forward: 在应用到目标之前应用于值的函数（默认：恒等函数）。
        :param backward: 在应用到元素之前应用于值的函数（默认：恒等函数）。
        """
        bind(self, 'value', target_object, target_name, forward=forward, backward=backward)
        return self

    def set_value(self, value: Any) -> None:
        """设置此元素的值。

        :param value: 要设置的值。
        """
        self.value = value

    def _handle_value_change(self, value: Any) -> None:
        """处理元素值变化

        :param value: 新值
        """
        self._props[self.VALUE_PROP] = self._value_to_model_value(value)
        if self._send_update_on_value_change:
            self.update()
        args = ValueChangeEventArguments(sender=self, client=self.client, value=self._value_to_event_value(value))
        for handler in self._change_handlers:
            handle_event(handler, args)

    def _event_args_to_value(self, e: GenericEventArguments) -> Any:
        """将事件参数转换为值

        :param e: 事件参数
        :return: 转换后的值
        """
        return e.args

    def _value_to_model_value(self, value: Any) -> Any:
        """将值转换为模型值格式

        :param value: 要转换的值
        :return: 模型值
        """
        return value

    def _value_to_event_value(self, value: Any) -> Any:
        """将值转换为事件值格式

        :param value: 要转换的值
        :return: 事件值
        """
        return value
