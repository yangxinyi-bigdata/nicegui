import inspect
import os
import platform
import signal
import urllib
from enum import Enum
from pathlib import Path
from typing import Any, Awaitable, Callable, Iterator, List, Optional, Union

from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.responses import FileResponse

from .. import background_tasks, helpers
from ..client import Client
from ..logging import log
from ..native import NativeConfig
from ..observables import ObservableSet
from ..server import Server
from ..staticfiles import CacheControlledStaticFiles
from ..storage import Storage
from .app_config import AppConfig
from .range_response import get_range_response


class State(Enum):
    STOPPED = 0
    STARTING = 1
    STARTED = 2
    STOPPING = 3


class App(FastAPI):
    from ..timer import Timer as timer  # pylint: disable=import-outside-toplevel

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs, docs_url=None, redoc_url=None, openapi_url=None)
        self.native = NativeConfig()
        self.storage = Storage()
        self.urls = ObservableSet()
        self._state: State = State.STOPPED
        self.config = AppConfig()

        self._startup_handlers: List[Union[Callable[..., Any], Awaitable]] = []
        self._shutdown_handlers: List[Union[Callable[..., Any], Awaitable]] = []
        self._connect_handlers: List[Union[Callable[..., Any], Awaitable]] = []
        self._disconnect_handlers: List[Union[Callable[..., Any], Awaitable]] = []
        self._exception_handlers: List[Callable[..., Any]] = [log.exception]
        self._page_exception_handler: Optional[Callable[..., Any]] = None

    @property
    def is_starting(self) -> bool:
        """返回 NiceGUI 是否正在启动。"""
        return self._state == State.STARTING

    @property
    def is_started(self) -> bool:
        """返回 NiceGUI 是否已启动。"""
        return self._state == State.STARTED

    @property
    def is_stopping(self) -> bool:
        """返回 NiceGUI 是否正在停止。"""
        return self._state == State.STOPPING

    @property
    def is_stopped(self) -> bool:
        """返回 NiceGUI 是否已停止。"""
        return self._state == State.STOPPED

    def start(self) -> None:
        """启动 NiceGUI。（仅供内部使用。）"""
        self._state = State.STARTING
        for t in self._startup_handlers:
            Client.auto_index_client.safe_invoke(t)
        self.on_shutdown(self.storage.on_shutdown)
        self.on_shutdown(background_tasks.teardown)
        self._state = State.STARTED

    async def stop(self) -> None:
        """停止 NiceGUI。（仅供内部使用。）"""
        self._state = State.STOPPING
        with Client.auto_index_client:
            for t in self._shutdown_handlers:
                if isinstance(t, Awaitable):
                    await t
                else:
                    result = t(self) if len(inspect.signature(t).parameters) == 1 else t()
                    if helpers.is_coroutine_function(t):
                        await result
        self._state = State.STOPPED

    def on_connect(self, handler: Union[Callable, Awaitable]) -> None:
        """每次新客户端连接到 NiceGUI 时调用。

        回调有一个可选的 `nicegui.Client` 参数。
        """
        self._connect_handlers.append(handler)

    def on_disconnect(self, handler: Union[Callable, Awaitable]) -> None:
        """每次新客户端从 NiceGUI 断开连接时调用。

        回调有一个可选的 `nicegui.Client` 参数。
        """
        self._disconnect_handlers.append(handler)

    def on_startup(self, handler: Union[Callable, Awaitable]) -> None:
        """当 NiceGUI 启动或重新启动时调用。

        需要在 `ui.run()` 之前调用。
        """
        if self.is_started:
            raise RuntimeError('Unable to register another startup handler. NiceGUI has already been started.')
        self._startup_handlers.append(handler)

    def on_shutdown(self, handler: Union[Callable, Awaitable]) -> None:
        """当 NiceGUI 关闭或重新启动时调用。

        当 NiceGUI 关闭或重新启动时，所有仍在执行的任务将自动取消。
        """
        self._shutdown_handlers.append(handler)

    def on_exception(self, handler: Callable) -> None:
        """发生异常时调用。

        回调有一个可选的 `Exception` 参数。
        """
        self._exception_handlers.append(handler)

    def handle_exception(self, exception: Exception) -> None:
        """通过调用所有注册的异常处理程序来处理异常。"""
        for handler in self._exception_handlers:
            result = handler() if not inspect.signature(handler).parameters else handler(exception)
            if helpers.is_coroutine_function(handler):
                background_tasks.create(result, name=f'exception {handler.__name__}')

    def on_page_exception(self, handler: Callable) -> None:
        """页面中发生异常时调用，允许创建自定义错误页面。

        回调可以接受一个可选的 ``Exception`` 作为参数。
        在回调中创建的所有 UI 元素都显示在错误页面上。
        目前不支持异步处理程序。

        *在 2.20.0 版本中添加*
        """
        self._page_exception_handler = handler

    def shutdown(self) -> None:
        """关闭 NiceGUI。

        这将以编程方式停止服务器。
        """
        if self.native.main_window:
            self.native.main_window.destroy()
        if self.config.reload:
            os.kill(os.getppid(), getattr(signal, 'CTRL_C_EVENT' if platform.system() == 'Windows' else 'SIGINT'))
        else:
            Server.instance.should_exit = True

    def add_static_files(self,
                         url_path: str,
                         local_directory: Union[str, Path],
                         *,
                         follow_symlink: bool = False,
                         max_cache_age: int = 3600) -> None:
        """添加静态文件目录。

        `add_static_files()` 使本地目录在指定端点处可用，例如 `'/static'`。
        这对于向前端提供图像等本地数据很有用。
        否则浏览器将无法访问这些文件。
        请只放入非安全关键文件，因为每个人都可以访问它们。

        要使单个文件可访问，您可以使用 `add_static_file()`。
        对于应该流式传输的媒体文件，您可以使用 `add_media_files()` 或 `add_media_file()`。

        :param url_path: 以斜杠 "/" 开头的字符串，标识文件应该提供服务的路径
        :param local_directory: 包含要作为静态内容提供的文件的本地文件夹
        :param follow_symlink: 是否遵循符号链接（默认：False）
        :param max_cache_age: 在 Cache-Control 标头中设置的 max-age 值（*在 2.8.0 版本中添加*）
        """
        if url_path == '/':
            raise ValueError('''Path cannot be "/", because it would hide NiceGUI's internal "/_nicegui" route.''')
        if max_cache_age < 0:
            raise ValueError('''Value of max_cache_age must be a positive integer or 0.''')

        handler = CacheControlledStaticFiles(
            directory=local_directory, follow_symlink=follow_symlink, max_cache_age=max_cache_age)

        @self.get(url_path.rstrip('/') + '/{path:path}')  # NOTE: prevent double slashes in route pattern
        async def static_file(request: Request, path: str = '') -> Response:
            return await handler.get_response(path, request.scope)

    def add_static_file(self, *,
                        local_file: Union[str, Path],
                        url_path: Optional[str] = None,
                        single_use: bool = False,
                        strict: bool = True,
                        max_cache_age: int = 3600) -> str:
        """添加单个静态文件。

        允许本地文件在线访问并启用缓存。
        如果未指定 `url_path`，将生成一个路径。

        要使整个文件夹的文件可访问，请使用 `add_static_files()`。
        对于应该流式传输的媒体文件，您可以使用 `add_media_files()` 或 `add_media_file()`。

        弃用警告：
        如果 ``strict`` 为 ``True``，在 3.0 版本中不存在的文件将引发 ``FileNotFoundError`` 而不是 ``ValueError``。

        :param local_file: 要作为静态内容提供的本地文件
        :param url_path: 以斜杠 "/" 开头的字符串，标识文件应该提供服务的路径（默认：None -> 自动生成的 URL 路径）
        :param single_use: 是否在文件下载一次后删除路由（默认：False）
        :param strict: 如果文件不存在是否引发 ``ValueError``（默认：False，*在 2.12.0 版本中添加*）
        :param max_cache_age: 在 Cache-Control 标头中设置的 max-age 值（*在 2.8.0 版本中添加*）
        :return: 可用于访问文件的编码 URL
        """
        if max_cache_age < 0:
            raise ValueError('''Value of max_cache_age must be a positive integer or 0.''')

        file = Path(local_file).resolve()
        if strict and not file.is_file():
            raise ValueError(f'File not found: {file}')  # DEPRECATED: will raise a ``FileNotFoundError`` in version 3.0
        path = f'/_nicegui/auto/static/{helpers.hash_file_path(file)}/{file.name}' if url_path is None else url_path

        @self.get(path)
        def read_item() -> FileResponse:
            if single_use:
                self.remove_route(path)
            return FileResponse(file, headers={'Cache-Control': f'public, max-age={max_cache_age}'})

        return urllib.parse.quote(path)

    def add_media_files(self, url_path: str, local_directory: Union[str, Path]) -> None:
        """添加媒体文件目录。

        `add_media_files()` 允许从指定端点流式传输本地文件，例如 `'/media'`。
        这应该用于媒体文件以支持适当的流式传输。
        否则浏览器将无法逐步访问和加载文件或跳转到流中的不同位置。
        请只放入非安全关键文件，因为每个人都可以访问它们。

        要使单个文件通过流式传输可访问，您可以使用 `add_media_file()`。
        对于小型静态文件，您可以使用 `add_static_files()` 或 `add_static_file()`。

        :param url_path: 以斜杠 "/" 开头的字符串，标识文件应该提供服务的路径
        :param local_directory: 包含要作为媒体内容提供的文件的本地文件夹
        """
        @self.get(url_path.rstrip('/') + '/{filename:path}')  # NOTE: prevent double slashes in route pattern
        def read_item(request: Request, filename: str, nicegui_chunk_size: int = 8192) -> Response:
            filepath = Path(local_directory) / filename
            if not filepath.is_file():
                raise HTTPException(status_code=404, detail='Not Found')
            return get_range_response(filepath, request, chunk_size=nicegui_chunk_size)

    def add_media_file(self, *,
                       local_file: Union[str, Path],
                       url_path: Optional[str] = None,
                       single_use: bool = False,
                       strict: bool = True) -> str:
        """添加单个媒体文件。

        允许本地文件被流式传输。
        如果未指定 `url_path`，将生成一个路径。

        要使整个媒体文件夹通过流式传输可访问，请使用 `add_media_files()`。
        对于小型静态文件，您可以使用 `add_static_files()` 或 `add_static_file()`。

        弃用警告：
        如果 ``strict`` 为 ``True``，在 3.0 版本中不存在的文件将引发 ``FileNotFoundError`` 而不是 ``ValueError``。

        :param local_file: 要作为媒体内容提供的本地文件
        :param url_path: 以斜杠 "/" 开头的字符串，标识文件应该提供服务的路径（默认：None -> 自动生成的 URL 路径）
        :param single_use: 是否在媒体文件下载一次后删除路由（默认：False）
        :param strict: 如果文件不存在是否引发 ``ValueError``（默认：False，*在 2.12.0 版本中添加*）
        :return: 可用于访问文件的编码 URL
        """
        file = Path(local_file).resolve()
        if strict and not file.is_file():
            raise ValueError(f'File not found: {file}')  # DEPRECATED: will raise a ``FileNotFoundError`` in version 3.0
        path = f'/_nicegui/auto/media/{helpers.hash_file_path(file)}/{file.name}' if url_path is None else url_path

        @self.get(path)
        def read_item(request: Request, nicegui_chunk_size: int = 8192) -> Response:
            if single_use:
                self.remove_route(path)
            return get_range_response(file, request, chunk_size=nicegui_chunk_size)

        return urllib.parse.quote(path)

    def remove_route(self, path: str) -> None:
        """删除具有给定路径的路由。"""
        self.routes[:] = [r for r in self.routes if getattr(r, 'path', None) != path]

    def reset(self) -> None:
        """将应用程序重置为其初始状态。（对测试有用。）"""
        self.storage.clear()
        self._startup_handlers.clear()
        self._shutdown_handlers.clear()
        self._connect_handlers.clear()
        self._disconnect_handlers.clear()
        self._exception_handlers[:] = [log.exception]
        self.config = AppConfig()

    @staticmethod
    def clients(path: str) -> Iterator[Client]:
        """迭代所有具有匹配路径的连接客户端。

        当使用 `@ui.page("/path")` 时，每个客户端都会获得此页面的私有视图。
        更新必须单独发送给每个客户端，此迭代器简化了此过程。

        *在 2.7.0 版本中添加*

        :param path: 用于过滤客户端的字符串
        """
        for client in Client.instances.values():
            if client.page.path == path:
                yield client
