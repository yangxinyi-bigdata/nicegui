from typing import List, Optional, Union

from ..events import Handler, ValueChangeEventArguments
from .mixins.disableable_element import DisableableElement
from .mixins.value_element import ValueElement


class Rating(ValueElement, DisableableElement):

    def __init__(self,
                 value: Optional[float] = None,
                 max: int = 5,  # pylint: disable=redefined-builtin
                 icon: Optional[str] = None,
                 icon_selected: Optional[str] = None,
                 icon_half: Optional[str] = None,
                 color: Optional[Union[str, List[str]]] = 'primary',
                 size: Optional[str] = None,
                 on_change: Optional[Handler[ValueChangeEventArguments]] = None,
                 ) -> None:
        """评分

        此元素基于Quasar的`QRating <https://quasar.dev/vue-components/rating>`_组件。

        *在版本2.12.0中添加*

        :param value: 初始值（默认：``None``）
        :param max: 最大评分，图标数量（默认：5）
        :param icon: 要显示的图标名称（默认：star）
        :param icon_selected: 选中时要显示的图标名称（默认：与``icon``相同）
        :param icon_half: 半选时要显示的图标名称（默认：与``icon``相同）
        :param color: 图标的颜色（Quasar、Tailwind或CSS颜色或``None``，默认："primary"）
        :param size: CSS单位的大小，包括单位名称或标准尺寸名称（xs|sm|md|lg|xl），例如：16px, 2rem
        :param on_change: 选择变化时要执行的回调函数
        """
        super().__init__(tag='q-rating', value=value, on_value_change=on_change)

        self._props['max'] = max

        if icon:
            self._props['icon'] = icon

        if color:
            self._props['color'] = color

        if icon_selected:
            self._props['icon-selected'] = icon_selected

        if icon_half:
            self._props['icon-half'] = icon_half

        if size:
            self._props['size'] = size
