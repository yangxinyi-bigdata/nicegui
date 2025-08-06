from ..context import context
from ..helpers import require_top_level_layout
from .mixins.value_element import ValueElement


class Footer(ValueElement, default_classes='nicegui-footer'):

    def __init__(self, *,
                 value: bool = True,
                 fixed: bool = True,
                 bordered: bool = False,
                 elevated: bool = False,
                 wrap: bool = True,
                 ) -> None:
        """页脚

        此元素基于Quasar的`QFooter <https://quasar.dev/layout/header-and-footer#qfooter-api>`_组件。

        与其他布局元素一样，页脚不能嵌套在其他元素内部。

        注意：页脚会自动放置在DOM中其他布局元素之下以提高可访问性。
        要更改顺序，请使用`move`方法。

        :param value: 页脚是否已打开（默认：`True`）
        :param fixed: 页脚是否固定或随内容滚动（默认：`True`）
        :param bordered: 页脚是否应有边框（默认：`False`）
        :param elevated: 页脚是否应有阴影（默认：`False`）
        :param wrap: 页脚是否应换行其内容（默认：`True`）
        """
        require_top_level_layout(self)
        with context.client.layout:
            super().__init__(tag='q-footer', value=value, on_value_change=None)
        self._props['bordered'] = bordered
        self._props['elevated'] = elevated
        if wrap:
            self._classes.append('wrap')
        code = list(self.client.layout.props['view'])
        code[9] = 'F' if fixed else 'f'
        self.client.layout.props['view'] = ''.join(code)

        self.move(target_index=-1)

    def toggle(self) -> None:
        """切换页脚"""
        self.value = not self.value

    def show(self) -> None:
        """显示页脚"""
        self.value = True

    def hide(self) -> None:
        """隐藏页脚"""
        self.value = False
