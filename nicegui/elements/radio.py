from typing import Any, Dict, List, Optional, Union

from ..events import GenericEventArguments, Handler, ValueChangeEventArguments
from .choice_element import ChoiceElement
from .mixins.disableable_element import DisableableElement


class Radio(ChoiceElement, DisableableElement):

    def __init__(self,
                 options: Union[List, Dict], *,
                 value: Any = None,
                 on_change: Optional[Handler[ValueChangeEventArguments]] = None,
                 ) -> None:
        """单选按钮选择

        此元素基于Quasar的`QRadio <https://quasar.dev/vue-components/radio>`_组件。

        选项可以指定为值列表，或者映射值到标签的字典。
        操作选项后，调用`update()`来更新UI中的选项。

        :param options: 指定选项的列表 ['value1', ...] 或字典 `{'value1':'label1', ...}`
        :param value: 初始值
        :param on_change: 选择更改时执行的回调函数
        """
        super().__init__(tag='q-option-group', options=options, value=value, on_change=on_change)

    def _event_args_to_value(self, e: GenericEventArguments) -> Any:
        return self._values[e.args]

    def _value_to_model_value(self, value: Any) -> Any:
        return self._values.index(value) if value in self._values else None
