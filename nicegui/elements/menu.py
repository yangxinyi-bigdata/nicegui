from typing import Optional

from ..events import ClickEventArguments, Handler
from .context_menu import ContextMenu
from .item import Item
from .mixins.value_element import ValueElement


class Menu(ValueElement):

    def __init__(self, *, value: bool = False) -> None:
        """菜单

        基于Quasar的`QMenu <https://quasar.dev/vue-components/menu>`_组件创建菜单。
        菜单应该放置在要显示它的元素内部。

        高级提示：
        使用`auto-close`属性可以在任何点击事件上直接自动关闭菜单，无需服务器往返。

        :param value: 菜单是否已经打开（默认：`False`）
        """
        super().__init__(tag='q-menu', value=value, on_value_change=None)

        # https://github.com/zauberzeug/nicegui/issues/1738
        self._props.add_warning('touch-position',
                                'The prop "touch-position" is not supported by `ui.menu`. '
                                'Use "ui.context_menu()" instead.')

    def open(self) -> None:
        """打开菜单。"""
        self.value = True

    def close(self) -> None:
        """关闭菜单。"""
        self.value = False

    def toggle(self) -> None:
        """切换菜单状态。"""
        self.value = not self.value


class MenuItem(Item):

    def __init__(self,
                 text: str = '',
                 on_click: Optional[Handler[ClickEventArguments]] = None, *,
                 auto_close: bool = True,
                 ) -> None:
        """菜单项

        要添加到菜单中的菜单项。
        此元素基于Quasar的`QItem <https://quasar.dev/vue-components/list-and-list-items#qitem-api>`_组件。

        :param text: 菜单项的标签
        :param on_click: 选择菜单项时执行的回调函数
        :param auto_close: 点击事件后是否应关闭菜单（默认：`True`）
        """
        super().__init__(text=text, on_click=on_click)

        self._props['clickable'] = True

        self.menu = next((e for e in self.ancestors() if isinstance(e, (Menu, ContextMenu))), None)
        if self.menu and auto_close:
            self.on_click(self.menu.close)
