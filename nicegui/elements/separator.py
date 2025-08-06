from ..element import Element


class Separator(Element, default_classes='nicegui-separator'):

    def __init__(self) -> None:
        """分隔符

        此元素基于Quasar的`QSeparator <https://quasar.dev/vue-components/separator>`_组件。

        它用作卡片、菜单和其他组件容器的分隔符，类似于HTML的<hr>标签。
        """
        super().__init__('q-separator')
