from typing import Optional

from ..events import Handler, ValueChangeEventArguments
from .mixins.disableable_element import DisableableElement
from .mixins.value_element import ValueElement


class Pagination(ValueElement, DisableableElement):

    def __init__(self,
                 min: int, max: int, *,  # pylint: disable=redefined-builtin
                 direction_links: bool = False,
                 value: Optional[int] = ...,  # type: ignore
                 on_change: Optional[Handler[ValueChangeEventArguments]] = None) -> None:
        """分页

        封装Quasar的`QPagination <https://quasar.dev/vue-components/pagination>`_组件的分页元素。

        :param min: 最小页码
        :param max: 最大页码
        :param direction_links: 是否显示首页/末页链接
        :param value: 初始页码（如果未提供值，默认为`min`）
        :param on_change: 值变化时要调用的回调函数
        """
        if value is ...:
            value = min
        super().__init__(tag='q-pagination', value=value, on_value_change=on_change)
        self._props['min'] = min
        self._props['max'] = max
        self._props['direction-links'] = direction_links

    @property
    def min(self) -> int:
        """最小页码"""
        return self._props['min']

    @min.setter
    def min(self, value: int) -> None:
        self._props['min'] = value
        self.update()

    @property
    def max(self) -> int:
        """最大页码"""
        return self._props['max']

    @max.setter
    def max(self, value: int) -> None:
        self._props['max'] = value
        self.update()

    @property
    def direction_links(self) -> bool:
        """是否显示首页/末页链接"""
        return self._props['direction-links']

    @direction_links.setter
    def direction_links(self, value: bool) -> None:
        self._props['direction-links'] = value
        self.update()
