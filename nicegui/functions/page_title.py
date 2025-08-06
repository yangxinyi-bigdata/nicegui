from .. import core, json
from ..context import context


def page_title(title: str) -> None:
    """页面标题

    为当前客户端设置页面标题。

    :param title: 页面标题
    """
    client = context.client
    client.title = title
    if core.app.native.main_window:
        core.app.native.main_window.set_title(title)
    if client.has_socket_connection:
        client.run_javascript(f'document.title = {json.dumps(title)}')
