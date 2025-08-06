from __future__ import annotations

import asyncio
import inspect
from functools import wraps
from pathlib import Path
from typing import TYPE_CHECKING, Any, Callable, Optional, Union

from fastapi import HTTPException, Request, Response

from . import background_tasks, binding, core, helpers
from .client import Client
from .elements.sub_pages import SubPages
from .favicon import create_favicon_route
from .language import Language
from .logging import log

if TYPE_CHECKING:
    from .api_router import APIRouter


class page:

    def __init__(self,
                 path: str, *,
                 title: Optional[str] = None,
                 viewport: Optional[str] = None,
                 favicon: Optional[Union[str, Path]] = None,
                 dark: Optional[bool] = ...,  # type: ignore
                 language: Language = ...,  # type: ignore
                 response_timeout: float = 3.0,
                 reconnect_timeout: Optional[float] = None,
                 api_router: Optional[APIRouter] = None,
                 **kwargs: Any,
                 ) -> None:
        """页面

        此装饰器标记一个函数作为页面构建器。
        每个访问给定路由的用户将看到页面的新实例。
        这意味着它是用户私有的，不与他人共享
        （这与`在页面装饰器外放置元素 <https://nicegui.io/documentation/section_pages_routing#auto-index_page>`_时的做法不同）。

        注意：

        - 被装饰函数的名称未被使用，可以是任何内容。
        - 页面路由由 `path` 参数确定并全局注册。
        - 该装饰器仅适用于自由函数和静态方法。
          实例方法或初始化器将需要 `self` 参数，而路由器无法关联该参数。
          请参阅`我们的模块化示例 <https://github.com/zauberzeug/nicegui/tree/main/examples/modularization/>`_
          以了解代码结构的策略。

        :param path: 新页面的路由（路径必须以 '/' 开头）
        :param title: 可选的页面标题
        :param viewport: 可选的视口 meta 标签内容
        :param favicon: 可选的相对文件路径或指向图标的绝对 URL（默认：`None`，将使用 NiceGUI 图标）
        :param dark: 是否使用 Quasar 的深色模式（默认为 `run` 命令的 `dark` 参数）
        :param language: 页面的语言（默认为 `run` 命令的 `language` 参数）
        :param response_timeout: 被装饰函数构建页面的最大时间（默认：3.0 秒）
        :param reconnect_timeout: 服务器等待浏览器重新连接的最大时间（默认为 `run` 命令的 `reconnect_timeout` 参数）
        :param api_router: 要使用的 APIRouter 实例，可以保留为 `None` 以使用默认值
        :param kwargs: 传递给 FastAPI 的 @app.get 方法的额外关键字参数
        """
        self._path = path
        self.title = title
        self.viewport = viewport
        self.favicon = favicon
        self.dark = dark
        self.language = language
        self.response_timeout = response_timeout
        self.kwargs = kwargs
        self.api_router = api_router or core.app.router
        self.reconnect_timeout = reconnect_timeout

        create_favicon_route(self.path, favicon)

    @property
    def path(self) -> str:
        """页面路径，包括 APIRouter 的前缀。"""
        return self.api_router.prefix + self._path

    def resolve_title(self) -> str:
        """返回页面标题。"""
        return self.title if self.title is not None else core.app.config.title

    def resolve_viewport(self) -> str:
        """返回页面的视口。"""
        return self.viewport if self.viewport is not None else core.app.config.viewport

    def resolve_dark(self) -> Optional[bool]:
        """返回页面是否应该使用深色模式。"""
        return self.dark if self.dark is not ... else core.app.config.dark

    def resolve_language(self) -> Language:
        """返回页面的语言。"""
        return self.language if self.language is not ... else core.app.config.language

    def resolve_reconnect_timeout(self) -> float:
        """返回页面的重新连接超时时间。"""
        return self.reconnect_timeout if self.reconnect_timeout is not None else core.app.config.reconnect_timeout

    def __call__(self, func: Callable[..., Any]) -> Callable[..., Any]:
        core.app.remove_route(self.path)  # NOTE make sure only the latest route definition is used
        parameters_of_decorated_func = list(inspect.signature(func).parameters.keys())

        def check_for_late_return_value(task: asyncio.Task) -> None:
            try:
                if task.result() is not None:
                    log.error(f'ignoring {task.result()}; '
                              'it was returned after the HTML had been delivered to the client')
            except asyncio.CancelledError:
                pass

        def create_error_page(e: Exception, request: Request) -> Response:
            page_exception_handler = core.app._page_exception_handler  # pylint: disable=protected-access
            if page_exception_handler is None:
                raise e
            with Client(page(''), request=request) as error_client:
                # page exception handler
                if helpers.expects_arguments(page_exception_handler):
                    page_exception_handler(e)
                else:
                    page_exception_handler()

                # FastAPI exception handlers
                for key, handler in core.app.exception_handlers.items():
                    if key == 500 or (isinstance(key, type) and isinstance(e, key)):
                        result = handler(request, e)
                        if helpers.is_coroutine_function(handler):
                            async def await_handler(result: Any) -> None:
                                await result
                            background_tasks.create(await_handler(result), name=f'exception handler {handler.__name__}')

                # NiceGUI exception handlers
                core.app.handle_exception(e)

                return error_client.build_response(request, 500)

        @wraps(func)
        async def decorated(*dec_args, **dec_kwargs) -> Response:
            request = dec_kwargs['request']
            # NOTE cleaning up the keyword args so the signature is consistent with "func" again
            dec_kwargs = {k: v for k, v in dec_kwargs.items() if k in parameters_of_decorated_func}
            with Client(self, request=request) as client:
                if any(p.name == 'client' for p in inspect.signature(func).parameters.values()):
                    dec_kwargs['client'] = client
                try:
                    result = func(*dec_args, **dec_kwargs)
                    # NOTE: after building the page, there might be sub pages that have 404 -- and initial requests should send 404 status request in such cases
                    sub_pages_elements = [e for e in client.elements.values() if isinstance(e, SubPages)]
                    if any(sub_pages.has_404 for sub_pages in sub_pages_elements):
                        raise HTTPException(404, f'{client.sub_pages_router.current_path} not found')
                except Exception as e:
                    return create_error_page(e, request)
            if helpers.is_coroutine_function(func):
                async def wait_for_result() -> Optional[Response]:
                    with client:
                        try:
                            return await result
                        except Exception as e:
                            return create_error_page(e, request)
                task = background_tasks.create(wait_for_result())
                task_wait_for_connection = background_tasks.create(
                    client._waiting_for_connection.wait(),  # pylint: disable=protected-access
                )
                try:
                    await asyncio.wait([
                        task,
                        task_wait_for_connection,
                    ], timeout=self.response_timeout, return_when=asyncio.FIRST_COMPLETED)
                except asyncio.TimeoutError as e:
                    raise TimeoutError(f'Response not ready after {self.response_timeout} seconds') from e
                if task.done():
                    result = task.result()
                else:
                    result = None
                    task.add_done_callback(check_for_late_return_value)
            if isinstance(result, Response):  # NOTE if setup returns a response, we don't need to render the page
                return result
            binding._refresh_step()  # pylint: disable=protected-access
            return client.build_response(request)

        parameters = [p for p in inspect.signature(func).parameters.values() if p.name != 'client']
        # NOTE adding request as a parameter so we can pass it to the client in the decorated function
        if 'request' not in {p.name for p in parameters}:
            request = inspect.Parameter('request', inspect.Parameter.POSITIONAL_OR_KEYWORD, annotation=Request)
            parameters.insert(0, request)
        decorated.__signature__ = inspect.Signature(parameters)  # type: ignore

        if 'include_in_schema' not in self.kwargs:
            self.kwargs['include_in_schema'] = core.app.config.endpoint_documentation in {'page', 'all'}

        self.api_router.get(self._path, **self.kwargs)(decorated)
        Client.page_routes[func] = self.path
        return func
