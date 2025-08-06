from ..element import Element


class ButtonGroup(Element):

    def __init__(self) -> None:
        """按钮组

        此元素基于Quasar的`QBtnGroup <https://quasar.dev/vue-components/button-group>`_组件。
        您必须在父按钮组和子按钮上使用相同的设计属性。
        """
        super().__init__(tag='q-btn-group')
