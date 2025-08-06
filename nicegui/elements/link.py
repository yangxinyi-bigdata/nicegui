from typing import Any, Callable, Union

from ..client import Client
from ..element import Element
from .mixins.text_element import TextElement


class Link(TextElement, component='link.js', default_classes='nicegui-link'):

    def __init__(self,
                 text: str = '',
                 target: Union[Callable[..., Any], str, Element] = '#',
                 new_tab: bool = False,
                 ) -> None:
        """链接

        创建超链接。

        要跳转到页面内的特定位置，您可以使用`ui.link_target("name")`放置可链接的锚点，
        并使用`ui.link(target="#name")`链接到该锚点。

        :param text: 显示文本
        :param target: 页面函数、同一页面上的NiceGUI元素，或是绝对URL或相对路径的字符串
        :param new_tab: 在新标签页中打开链接（默认：False）
        """
        super().__init__(text=text)
        if isinstance(target, str):
            self._props['href'] = target
        elif isinstance(target, Element):
            self._props['href'] = f'#{target.html_id}'
        elif callable(target):
            self._props['href'] = Client.page_routes[target]
        self._props['target'] = '_blank' if new_tab else '_self'


class LinkTarget(Element):

    def __init__(self, name: str) -> None:
        """链接目标

        创建可以用作链接的页面内目标的锚点标签。

        :param name: 目标名称
        """
        super().__init__('a')
        self._props['name'] = name
