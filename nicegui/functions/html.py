from ..client import Client
from ..context import context


def add_head_html(code: str, *, shared: bool = False) -> None:
    """向页面头部添加 HTML 代码。

    :param code: 要添加的 HTML 代码
    :param shared: 如果为 True，代码将添加到所有页面
    """
    if shared:
        Client.shared_head_html += code + '\n'
    else:
        client = context.client
        if client.has_socket_connection:
            client.run_javascript(f'document.head.insertAdjacentHTML("beforeend", {code!r});')
        client._head_html += code + '\n'  # pylint: disable=protected-access


def add_body_html(code: str, *, shared: bool = False) -> None:
    """向页面主体添加 HTML 代码。

    :param code: 要添加的 HTML 代码
    :param shared: 如果为 True，代码将添加到所有页面
    """
    if shared:
        Client.shared_body_html += code + '\n'
    else:
        client = context.client
        if client.has_socket_connection:
            client.run_javascript(f'document.querySelector("#app").insertAdjacentHTML("beforebegin", {code!r});')
        client._body_html += code + '\n'  # pylint: disable=protected-access
