from ..awaitable_response import AwaitableResponse
from ..context import context


def run_javascript(code: str, *, timeout: float = 1.0) -> AwaitableResponse:
    """运行 JavaScript

    此函数在浏览器中执行的页面上运行任意的 JavaScript 代码。
    在调用此函数之前，客户端必须已连接。
    要通过 ID 访问客户端 Vue 组件或 HTML 元素，
    请使用 JavaScript 函数 `getElement()` 或 `getHtmlElement()`（*在版本 2.9.0 中添加*）。

    如果函数被等待，则返回 JavaScript 代码的结果。
    否则，JavaScript 代码将在不等待响应的情况下执行。

    请注意，从客户端请求数据仅支持页面函数，不支持共享的自动索引页面。

    :param code: 要运行的 JavaScript 代码
    :param timeout: 超时时间（秒）（默认：`1.0`）

    :return: 可以等待以获取 JavaScript 代码结果的 AwaitableResponse
    """
    return context.client.run_javascript(code, timeout=timeout)
