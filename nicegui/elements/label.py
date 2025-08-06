from .mixins.text_element import TextElement


class Label(TextElement):

    def __init__(self, text: str = '') -> None:
        """标签

        显示一些文本。

        :param text: 标签的内容
        """
        super().__init__(tag='div', text=text)
