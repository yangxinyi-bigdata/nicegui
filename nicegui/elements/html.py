from .mixins.content_element import ContentElement


class Html(ContentElement):

    def __init__(self, content: str = '', *, tag: str = 'div') -> None:
        """HTML元素

        在页面上渲染任意HTML，包装在指定的标签中。
        可以使用`Tailwind <https://v3.tailwindcss.com/>`_进行样式设置。
        您也可以使用`ui.add_head_html`将HTML代码添加到文档的头部，使用`ui.add_body_html`将其添加到主体中。

        :param content: 要显示的HTML代码
        :param tag: 包装内容的HTML标签（默认："div"）
        """
        super().__init__(tag=tag, content=content)
