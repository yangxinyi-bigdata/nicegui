from typing import Any, Dict, List, Optional, Union

from ..events import GenericEventArguments, Handler, ValueChangeEventArguments
from .choice_element import ChoiceElement
from .mixins.disableable_element import DisableableElement


class Toggle(ChoiceElement, DisableableElement):

    def __init__(self,
                 options: Union[List, Dict], *,
                 value: Any = None,
                 on_change: Optional[Handler[ValueChangeEventArguments]] = None,
                 clearable: bool = False,
                 ) -> None:
        """切换按钮

        此元素基于Quasar的`QBtnToggle <https://quasar.dev/vue-components/button-toggle>`_组件。

        选项可以指定为值列表，或映射值到标签的字典。
        操作选项后，调用`update()`来更新UI中的选项。

        :param options: 指定选项的列表['value1', ...]或字典`{'value1':'label1', ...}`
        :param value: 初始值
        :param on_change: 选择变化时要执行的回调函数
        :param clearable: 是否可以通过点击选中的选项来清除切换按钮
        """
        super().__init__(tag='q-btn-toggle', options=options, value=value, on_change=on_change)
        self._props['clearable'] = clearable

    def _event_args_to_value(self, e: GenericEventArguments) -> Any:
        return self._values[e.args] if e.args is not None else None

    def _value_to_model_value(self, value: Any) -> Any:
        return self._values.index(value) if value in self._values else None
