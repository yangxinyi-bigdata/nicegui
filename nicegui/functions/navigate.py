from typing import Any, Callable, Union
from urllib.parse import urlparse

from ..client import Client
from ..context import context
from ..element import Element
from .javascript import run_javascript


class Navigate:
    """导航函数

    这些函数允许您在浏览器历史记录中导航和访问外部 URL。

    *在版本 2.0.0 中添加*
    """

    def __init__(self) -> None:
        self.history = History()

    def back(self) -> None:
        """ui.navigate.back

        在浏览器历史记录中向后导航。
        这相当于在浏览器中点击后退按钮。
        """
        run_javascript('history.back()')

    def forward(self) -> None:
        """ui.navigate.forward

        在浏览器历史记录中向前导航。
        这相当于在浏览器中点击前进按钮。
        """
        run_javascript('history.forward()')

    def reload(self) -> None:
        """ui.navigate.reload

        重新加载当前页面。
        这相当于在浏览器中点击重新加载按钮。
        """
        run_javascript('history.go(0)')

    def to(self, target: Union[Callable[..., Any], str, Element], new_tab: bool = False) -> None:
        """ui.navigate.to（以前是 ui.open）

        可用于以编程方式打开不同的页面或 URL。

        使用 `new_tab` 参数时，浏览器可能会阻止新标签页。
        这是浏览器设置，应用程序无法更改。
        您可能想要使用 `ui.link` 及其 `new_tab` 参数代替。

        此功能以前可用作 `ui.open`，现已弃用。

        注意：使用`自动索引页面 </documentation/section_pages_routing#auto-index_page>`_ 时（例如没有 `@page` 装饰器），
        连接到页面的所有客户端（即浏览器）将打开目标 URL，除非指定了套接字。

        :param target: 页面函数、同一页面上的 NiceGUI 元素或字符串，是绝对 URL 或来自基本 URL 的相对路径
        :param new_tab: 是否在新标签页中打开目标（可能会被浏览器阻止）
        """
        if isinstance(target, str):
            path = target
        elif isinstance(target, Element):
            path = f'#{target.html_id}'
        elif callable(target):
            path = Client.page_routes[target]
        else:
            raise TypeError(f'Invalid target type: {type(target)}')

        if not new_tab and isinstance(target, str) and not bool(urlparse(target).netloc):
            context.client.sub_pages_router._handle_navigate(path)  # pylint: disable=protected-access
            return

        context.client.open(path, new_tab)


class History:

    def push(self, url: str) -> None:
        """将 URL 推送到浏览器导航历史记录。

        请参阅 JavaScript 的 `pushState <https://developer.mozilla.org/en-US/docs/Web/API/History/pushState>`_ 了解更多信息。

        *在版本 2.13.0 中添加*

        :param url: 相对或绝对 URL
        """
        run_javascript(f'history.pushState({{}}, "", "{url}");')

    def replace(self, url: str) -> None:
        """替换浏览器历史记录中的当前 URL。

        请参阅 JavaScript 的 `replaceState <https://developer.mozilla.org/en-US/docs/Web/API/History/replaceState>`_ 了解更多信息。

        *在版本 2.13.0 中添加*

        :param url: 相对或绝对 URL
        """
        run_javascript(f'history.replaceState({{}}, "", "{url}");')


navigate = Navigate()
