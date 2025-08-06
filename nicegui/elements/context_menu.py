from ..element import Element


class ContextMenu(Element):

    def __init__(self) -> None:
        """右键菜单

        基于Quasar的`QMenu <https://quasar.dev/vue-components/menu>`_组件创建右键菜单。
        右键菜单应该放置在要显示它的元素内部。
        当用户右键点击元素时，它会自动打开并出现在鼠标位置。
        """
        super().__init__('q-menu')
        self._props['context-menu'] = True
        self._props['touch-position'] = True

    def open(self) -> None:
        """打开右键菜单。"""
        self.run_method('show')

    def close(self) -> None:
        """关闭右键菜单。"""
        self.run_method('hide')
