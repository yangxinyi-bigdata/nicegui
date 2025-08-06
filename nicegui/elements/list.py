from ..element import Element


class List(Element):

    def __init__(self) -> None:
        """列表

        基于Quasar的`QList <https://quasar.dev/vue-components/list-and-list-items#qlist-api>`_组件的列表元素。
        它为``ui.item``元素提供容器。
        """
        super().__init__('q-list')
