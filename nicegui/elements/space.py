from ..element import Element


class Space(Element):

    def __init__(self) -> None:
        """空间

        此元素基于Quasar的`QSpace <https://quasar.dev/vue-components/space>`_组件。

        其目的是简单地填充flexbox元素内的所有可用空间。
        """
        super().__init__('q-space')
