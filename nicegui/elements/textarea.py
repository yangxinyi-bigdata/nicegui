from typing import Callable, Dict, Optional, Union

from ..events import Handler, ValueChangeEventArguments
from .input import Input


class Textarea(Input, component='input.js'):

    def __init__(self,
                 label: Optional[str] = None, *,
                 placeholder: Optional[str] = None,
                 value: str = '',
                 on_change: Optional[Handler[ValueChangeEventArguments]] = None,
                 validation: Optional[Union[Callable[..., Optional[str]], Dict[str, Callable[..., bool]]]] = None,
                 ) -> None:
        """文本区域

        此元素基于Quasar的`QInput <https://quasar.dev/vue-components/input>`_组件。
        ``type``设置为``textarea``以创建多行文本输入。

        您可以使用`validation`参数来定义验证规则字典，
        例如``{'Too long!': lambda value: len(value) < 3}``。
        第一个失败的规则的键将作为错误消息显示。
        或者，您可以传递一个返回可选错误消息的可调用对象。
        要禁用每次值更改时的自动验证，可以使用`without_auto_validation`方法。

        :param label: 文本区域的显示名称
        :param placeholder: 如果没有输入值时显示的文本
        :param value: 字段的初始值
        :param on_change: 值更改时执行的回调函数
        :param validation: 验证规则字典或返回可选错误消息的可调用对象（默认：None表示无验证）
        """
        super().__init__(label, placeholder=placeholder, value=value, on_change=on_change, validation=validation)
        self._props['type'] = 'textarea'
