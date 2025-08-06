from typing import Dict, List, Optional, Union

from ..events import Handler, ValueChangeEventArguments
from .mixins.disableable_element import DisableableElement
from .mixins.value_element import ValueElement


class Date(ValueElement, DisableableElement):

    def __init__(self,
                 value: Optional[
                     Union[str, Dict[str, str], List[str], List[Union[str, Dict[str, str]]]]
                 ] = None,
                 *,
                 mask: str = 'YYYY-MM-DD',
                 on_change: Optional[Handler[ValueChangeEventArguments]] = None) -> None:
        """日期输入框

        此元素基于Quasar的`QDate <https://quasar.dev/vue-components/date>`_组件。
        日期是按`mask`参数定义格式的字符串。

        您也可以使用`range`或`multiple`属性来选择日期范围或多个日期：：

            ui.date({'from': '2023-01-01', 'to': '2023-01-05'}).props('range')
            ui.date(['2023-01-01', '2023-01-02', '2023-01-03']).props('multiple')
            ui.date([{'from': '2023-01-01', 'to': '2023-01-05'}, '2023-01-07']).props('multiple range')

        :param value: 初始日期
        :param mask: 日期字符串的格式（默认：'YYYY-MM-DD'）
        :param on_change: 更改日期时执行的回调函数
        """
        super().__init__(tag='q-date', value=value, on_value_change=on_change)
        self._props['mask'] = mask
