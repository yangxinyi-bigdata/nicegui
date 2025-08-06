from ..context import context
from ..helpers import require_top_level_layout
from .mixins.value_element import ValueElement


class Header(ValueElement, component='header.js', default_classes='nicegui-header'):

    def __init__(self, *,
                 value: bool = True,
                 fixed: bool = True,
                 bordered: bool = False,
                 elevated: bool = False,
                 wrap: bool = True,
                 add_scroll_padding: bool = True,
                 ) -> None:
        """页头

        此元素基于Quasar的`QHeader <https://quasar.dev/layout/header-and-footer#qheader-api>`_组件。

        与其他布局元素一样，页头不能嵌套在其他元素内部。

        注意：页头会自动放置在DOM中其他布局元素之上以提高可访问性。
        要更改顺序，请使用`move`方法。

        :param value: 页头是否已打开（默认：`True`）
        :param fixed: 页头是否固定在页面顶部（默认：`True`）
        :param bordered: 页头是否应有边框（默认：`False`）
        :param elevated: 页头是否应有阴影（默认：`False`）
        :param wrap: 页头是否应换行其内容（默认：`True`）
        :param add_scroll_padding: 是否自动防止链接目标被页头隐藏（默认：`True`）
        """
        require_top_level_layout(self)
        with context.client.layout:
            super().__init__(value=value, on_value_change=None)
        self._props['bordered'] = bordered
        self._props['elevated'] = elevated
        self._props['add_scroll_padding'] = add_scroll_padding
        if wrap:
            self._classes.append('wrap')
        code = list(self.client.layout.props['view'])
        code[1] = 'H' if fixed else 'h'
        self.client.layout.props['view'] = ''.join(code)

        self.move(target_index=0)

    def toggle(self):
        """切换页头"""
        self.value = not self.value

    def show(self):
        """显示页头"""
        self.value = True

    def hide(self):
        """隐藏页头"""
        self.value = False
