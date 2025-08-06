from typing import Optional

from typing_extensions import Self

from ..element import Element
from ..events import ColorPickEventArguments, GenericEventArguments, Handler, handle_event
from .menu import Menu


class ColorPicker(Menu):

    def __init__(self, *,
                 on_pick: Optional[Handler[ColorPickEventArguments]] = None,
                 value: bool = False,
                 ) -> None:
        """颜色选择器

        此元素基于Quasar的`QMenu <https://quasar.dev/vue-components/menu>`_和
        `QColor <https://quasar.dev/vue-components/color-picker>`_组件。

        :param on_pick: 选择颜色时执行的回调函数
        :param value: 菜单是否已打开（默认：`False`）
        """
        super().__init__(value=value)
        self._pick_handlers = [on_pick] if on_pick else []
        with self:
            def handle_change(e: GenericEventArguments):
                for handler in self._pick_handlers:
                    handle_event(handler, ColorPickEventArguments(sender=self, client=self.client, color=e.args))
            self.q_color = Element('q-color').on('change', handle_change)

    def set_color(self, color: str) -> None:
        """设置选择器的颜色。

        :param color: 要设置的颜色
        """
        self.q_color.props(f'model-value="{color}"')

    def on_pick(self, callback: Handler[ColorPickEventArguments]) -> Self:
        """添加一个在选择颜色时调用的回调函数。"""
        self._pick_handlers.append(callback)
        return self
