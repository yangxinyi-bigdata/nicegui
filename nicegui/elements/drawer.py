from typing import Literal, Optional

from ..context import context
from ..helpers import require_top_level_layout
from .mixins.value_element import ValueElement

DrawerSides = Literal['left', 'right']


class Drawer(ValueElement, default_classes='nicegui-drawer'):

    def __init__(self,
                 side: DrawerSides, *,
                 value: Optional[bool] = None,
                 fixed: bool = True,
                 bordered: bool = False,
                 elevated: bool = False,
                 top_corner: bool = False,
                 bottom_corner: bool = False) -> None:
        """抽屉

        此元素基于Quasar的`QDrawer <https://quasar.dev/layout/drawer>`_组件。

        与其他布局元素一样，抽屉不能嵌套在其他元素内部。

        注意：根据位置，抽屉会自动放置在主页面容器之上或之下的DOM中以提高可访问性。
        要更改顺序，请使用`move`方法。

        值为``None``时会根据当前布局宽度自动打开或关闭抽屉（断点：>=1024 px）。
        在自动索引页面上，值将保持为``None``，直到抽屉被打开、关闭或切换。
        在其他页面上，当websocket连接建立时，将从客户端请求该值。

        :param side: 抽屉应放置在页面的哪一侧（`left`或`right`）
        :param value: 抽屉是否已打开（默认：`None`，即如果布局宽度超过阈值）
        :param fixed: 抽屉是否固定或随内容滚动（默认：`True`）
        :param bordered: 抽屉是否应有边框（默认：`False`）
        :param elevated: 抽屉是否应有阴影（默认：`False`）
        :param top_corner: 抽屉是否扩展到顶角（默认：`False`）
        :param bottom_corner: 抽屉是否扩展到底角（默认：`False`）
        """
        require_top_level_layout(self)
        with context.client.layout:
            super().__init__(tag='q-drawer', value=value, on_value_change=None)
        self._props['show-if-above'] = value is None
        self._props['side'] = side
        self._props['bordered'] = bordered
        self._props['elevated'] = elevated
        code = list(self.client.layout.props['view'])
        code[0 if side == 'left' else 2] = side[0].lower() if top_corner else 'h'
        code[4 if side == 'left' else 6] = side[0].upper() if fixed else side[0].lower()
        code[8 if side == 'left' else 10] = side[0].lower() if bottom_corner else 'f'
        self.client.layout.props['view'] = ''.join(code)

        page_container_index = self.client.layout.default_slot.children.index(self.client.page_container)
        self.move(target_index=page_container_index if side == 'left' else page_container_index + 1)

        if value is None and not self.client.is_auto_index_client:
            async def _request_value() -> None:
                self.value = await context.client.run_javascript(
                    f'!getHtmlElement({self.id}).parentElement.classList.contains("q-layout--prevent-focus")  // __IS_DRAWER_OPEN__'
                )
            self.client.on_connect(_request_value)

    def toggle(self) -> None:
        """切换抽屉"""
        if self.value is None:
            self.run_method('toggle')
        else:
            self.value = not self.value

    def show(self) -> None:
        """显示抽屉"""
        self.value = True

    def hide(self) -> None:
        """隐藏抽屉"""
        self.value = False

    def _handle_value_change(self, value: bool) -> None:
        super()._handle_value_change(value)
        self._props['show-if-above'] = value is None


class LeftDrawer(Drawer):

    def __init__(self, *,
                 value: Optional[bool] = None,
                 fixed: bool = True,
                 bordered: bool = False,
                 elevated: bool = False,
                 top_corner: bool = False,
                 bottom_corner: bool = False) -> None:
        """左侧抽屉

        此元素基于Quasar的`QDrawer <https://quasar.dev/layout/drawer>`_组件。

        与其他布局元素一样，左侧抽屉不能嵌套在其他元素内部。

        注意：左侧抽屉会自动放置在主页面容器之上的DOM中以提高可访问性。
        要更改顺序，请使用`move`方法。

        值为``None``时会根据当前布局宽度自动打开或关闭抽屉（断点：>=1024 px）。
        在自动索引页面上，值将保持为``None``，直到抽屉被打开、关闭或切换。
        在其他页面上，当websocket连接建立时，将从客户端请求该值。

        :param value: 抽屉是否已打开（默认：`None`，即如果布局宽度超过阈值）
        :param fixed: 抽屉是否固定或随内容滚动（默认：`True`）
        :param bordered: 抽屉是否应有边框（默认：`False`）
        :param elevated: 抽屉是否应有阴影（默认：`False`）
        :param top_corner: 抽屉是否扩展到顶角（默认：`False`）
        :param bottom_corner: 抽屉是否扩展到底角（默认：`False`）
        """
        super().__init__('left',
                         value=value,
                         fixed=fixed,
                         bordered=bordered,
                         elevated=elevated,
                         top_corner=top_corner,
                         bottom_corner=bottom_corner)


class RightDrawer(Drawer):

    def __init__(self, *,
                 value: Optional[bool] = None,
                 fixed: bool = True,
                 bordered: bool = False,
                 elevated: bool = False,
                 top_corner: bool = False,
                 bottom_corner: bool = False) -> None:
        """右侧抽屉

        此元素基于Quasar的`QDrawer <https://quasar.dev/layout/drawer>`_组件。

        与其他布局元素一样，右侧抽屉不能嵌套在其他元素内部。

        注意：右侧抽屉会自动放置在主页面容器之下的DOM中以提高可访问性。
        要更改顺序，请使用`move`方法。

        值为``None``时会根据当前布局宽度自动打开或关闭抽屉（断点：>=1024 px）。
        在自动索引页面上，值将保持为``None``，直到抽屉被打开、关闭或切换。
        在其他页面上，当websocket连接建立时，将从客户端请求该值。

        :param value: 抽屉是否已打开（默认：`None`，即如果布局宽度超过阈值）
        :param fixed: 抽屉是否固定或随内容滚动（默认：`True`）
        :param bordered: 抽屉是否应有边框（默认：`False`）
        :param elevated: 抽屉是否应有阴影（默认：`False`）
        :param top_corner: 抽屉是否扩展到顶角（默认：`False`）
        :param bottom_corner: 抽屉是否扩展到底角（默认：`False`）
        """
        super().__init__('right',
                         value=value,
                         fixed=fixed,
                         bordered=bordered,
                         elevated=elevated,
                         top_corner=top_corner,
                         bottom_corner=bottom_corner)
