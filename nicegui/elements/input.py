from typing import Any, List, Optional, Union

from ..events import Handler, ValueChangeEventArguments
from .icon import Icon
from .mixins.disableable_element import DisableableElement
from .mixins.label_element import LabelElement
from .mixins.validation_element import ValidationDict, ValidationElement, ValidationFunction


class Input(LabelElement, ValidationElement, DisableableElement, component='input.js'):
    VALUE_PROP: str = 'value'
    LOOPBACK = False

    def __init__(self,
                 label: Optional[str] = None, *,
                 placeholder: Optional[str] = None,
                 value: str = '',
                 password: bool = False,
                 password_toggle_button: bool = False,
                 on_change: Optional[Handler[ValueChangeEventArguments]] = None,
                 autocomplete: Optional[List[str]] = None,
                 validation: Optional[Union[ValidationFunction, ValidationDict]] = None,
                 ) -> None:
        """文本输入框

        此元素基于Quasar的`QInput <https://quasar.dev/vue-components/input>`_组件。

        `on_change`事件在每次按键时调用，值会相应更新。
        如果您想等待用户确认输入，可以注册自定义事件回调，例如
        `ui.input(...).on('keydown.enter', ...)` 或 `ui.input(...).on('blur', ...)`。

        您可以使用`validation`参数来定义验证规则字典，
        例如 ``{'太长了！': lambda value: len(value) < 3}``。
        第一个失败的规则的键将显示为错误消息。
        或者，您可以传递一个返回可选错误消息的可调用对象。
        要禁用每次值更改时的自动验证，可以使用`without_auto_validation`方法。

        关于输入框样式的说明：
        Quasar的`QInput`组件是原生`input`元素的包装器。
        这意味着您不能直接样式化输入框，
        但可以使用`input-class`和`input-style`属性来样式化原生输入元素。
        有关更多详情，请参阅`QInput <https://quasar.dev/vue-components/input>`_文档中的"Style"属性部分。

        :param label: 文本输入框的显示标签
        :param placeholder: 如果没有输入值时显示的文本
        :param value: 文本输入框的当前值
        :param password: 是否隐藏输入内容（默认：False）
        :param password_toggle_button: 是否显示切换密码可见性的按钮（默认：False）
        :param on_change: 值更改时执行的回调函数
        :param autocomplete: 用于自动完成的可选字符串列表
        :param validation: 验证规则字典或返回可选错误消息的可调用对象（默认：None表示不验证）
        """
        super().__init__(label=label, value=value, on_value_change=on_change, validation=validation)
        if placeholder is not None:
            self._props['placeholder'] = placeholder
        self._props['type'] = 'password' if password else 'text'

        if password_toggle_button:
            with self.add_slot('append'):
                def toggle_type(_):
                    is_hidden = self._props.get('type') == 'password'
                    icon.props(f'name={"visibility" if is_hidden else "visibility_off"}')
                    self.props(f'type={"text" if is_hidden else "password"}')
                icon = Icon('visibility_off').classes('cursor-pointer').on('click', toggle_type)

        self._props['_autocomplete'] = autocomplete or []

    def set_autocomplete(self, autocomplete: Optional[List[str]]) -> None:
        """设置自动完成列表。"""
        self._props['_autocomplete'] = autocomplete
        self.update()

    def _handle_value_change(self, value: Any) -> None:
        super()._handle_value_change(value)
        if self._send_update_on_value_change:
            self.run_method('updateValue')
