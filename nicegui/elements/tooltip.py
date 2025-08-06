from .mixins.text_element import TextElement


class Tooltip(TextElement):

    def __init__(self, text: str = '') -> None:
        """工具提示

        此元素基于Quasar的`QTooltip <https://quasar.dev/vue-components/tooltip>`_组件。
        可以将其放置在另一个元素中，在悬停时显示附加信息。

        除了传递字符串作为第一个参数外，您还可以在工具提示内嵌套其他元素。

        :param text: 工具提示的内容（默认：''）
        """
        super().__init__(tag='q-tooltip', text=text)
