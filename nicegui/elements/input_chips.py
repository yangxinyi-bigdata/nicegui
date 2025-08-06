from typing import Any, List, Literal, Optional, Union

from ..events import GenericEventArguments, Handler, ValueChangeEventArguments
from .mixins.disableable_element import DisableableElement
from .mixins.label_element import LabelElement
from .mixins.validation_element import ValidationDict, ValidationElement, ValidationFunction


class InputChips(LabelElement, ValidationElement, DisableableElement):

    def __init__(self,
                 label: Optional[str] = None,
                 *,
                 value: Optional[List[str]] = None,
                 on_change: Optional[Handler[ValueChangeEventArguments]] = None,
                 new_value_mode: Literal['add', 'add-unique', 'toggle'] = 'toggle',
                 clearable: bool = False,
                 validation: Optional[Union[ValidationFunction, ValidationDict]] = None,
                 ) -> None:
        """输入芯片

        管理值集合作为可视化"芯片"或标签的输入字段。
        用户可以输入来添加新芯片，并通过点击或使用键盘快捷键删除现有芯片。

        此元素基于Quasar的`QSelect <https://quasar.dev/vue-components/select>`_组件。
        与传统的下拉选择不同，此变体专注于带芯片的自由形式文本输入，
        使其非常适合标签、关键字或任何用户定义值的列表。

        您可以使用``validation``参数来定义验证规则字典，
        例如``{'Too long!': lambda value: len(value) < 3}``。
        第一个失败的规则的键将显示为错误消息。
        或者，您可以传递一个返回可选错误消息的可调用对象。
        要禁用每次值更改时的自动验证，可以使用`without_auto_validation`方法。

        *在版本2.22.0中添加*

        :param label: 在选择上方显示的标签
        :param value: 初始值
        :param on_change: 选择变化时要执行的回调函数
        :param new_value_mode: 处理用户输入的新值（默认："toggle"）
        :param clearable: 是否添加清除选择的按钮
        :param validation: 验证规则字典或返回可选错误消息的可调用对象（默认：None表示无验证）
        """
        super().__init__(tag='q-select', label=label, value=value or [], on_value_change=on_change, validation=validation)

        self._props['new-value-mode'] = new_value_mode
        self._props['use-input'] = True
        self._props['use-chips'] = True
        self._props['fill-input'] = True
        self._props['input-debounce'] = 0
        self._props['multiple'] = True
        self._props['hide-dropdown-icon'] = True
        self._props['clearable'] = clearable

    def _event_args_to_value(self, e: GenericEventArguments) -> Any:
        return e.args or []
