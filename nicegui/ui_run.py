import multiprocessing
import os
import sys
from pathlib import Path
from typing import Any, List, Literal, Optional, Tuple, TypedDict, Union

from fastapi.middleware.gzip import GZipMiddleware
from starlette.routing import Route
from uvicorn.main import STARTUP_FAILURE
from uvicorn.supervisors import ChangeReload, Multiprocess

import __main__

from . import core, helpers
from . import native as native_module
from .air import Air
from .client import Client
from .language import Language
from .logging import log
from .middlewares import RedirectWithPrefixMiddleware, SetCacheControlMiddleware
from .server import CustomServerConfig, Server

APP_IMPORT_STRING = 'nicegui:app'


class ContactDict(TypedDict):
    name: Optional[str]
    url: Optional[str]
    email: Optional[str]


class LicenseInfoDict(TypedDict):
    name: str
    identifier: Optional[str]
    url: Optional[str]


class DocsConfig(TypedDict):
    title: Optional[str]
    summary: Optional[str]
    description: Optional[str]
    version: Optional[str]
    terms_of_service: Optional[str]
    contact: Optional[ContactDict]
    license_info: Optional[LicenseInfoDict]


def run(*,
        host: Optional[str] = None,
        port: Optional[int] = None,
        title: str = 'NiceGUI',
        viewport: str = 'width=device-width, initial-scale=1',
        favicon: Optional[Union[str, Path]] = None,
        dark: Optional[bool] = False,
        language: Language = 'en-US',
        binding_refresh_interval: float = 0.1,
        reconnect_timeout: float = 3.0,
        message_history_length: int = 1000,
        cache_control_directives: str = 'public, max-age=31536000, immutable, stale-while-revalidate=31536000',
        fastapi_docs: Union[bool, DocsConfig] = False,
        show: bool = True,
        on_air: Optional[Union[str, Literal[True]]] = None,
        native: bool = False,
        window_size: Optional[Tuple[int, int]] = None,
        fullscreen: bool = False,
        frameless: bool = False,
        reload: bool = True,
        uvicorn_logging_level: str = 'warning',
        uvicorn_reload_dirs: str = '.',
        uvicorn_reload_includes: str = '*.py',
        uvicorn_reload_excludes: str = '.*, .py[cod], .sw.*, ~*',
        tailwind: bool = True,
        prod_js: bool = True,
        endpoint_documentation: Literal['none', 'internal', 'page', 'all'] = 'none',
        storage_secret: Optional[str] = None,
        show_welcome_message: bool = True,
        **kwargs: Any,
        ) -> None:
    """ui.run

    您可以使用可选参数调用 `ui.run()`。
    其中大多数参数仅在完全停止并重新启动应用程序后才适用，并且在自动重新加载时不适用。

    :param host: 使用此主机启动服务器 (defaults to `'127.0.0.1` in native mode, otherwise `'0.0.0.0'`)
    :param port: 使用此端口 (default: 8080 in normal mode, and an automatically determined open port in native mode)
    :param title: 页面标题 (default: `'NiceGUI'`, can be overwritten per page)
    :param viewport: 页面 meta viewport 内容 (default: `'width=device-width, initial-scale=1'`, can be overwritten per page)
    :param favicon: 图标的相对文件路径、绝对 URL (default: `None`, NiceGUI icon will be used) or emoji (e.g. `'🚀'`, works for most browsers)
    :param dark: 是否使用 Quasar 的暗色模式 (default: `False`, 使用 `None` 表示"自动"模式)
    :param language: Quasar 元素的语言 (default: `'en-US'`)
    :param binding_refresh_interval: 绑定更新之间的时间 (default: `0.1` seconds, 越大越节省 CPU)
    :param reconnect_timeout: 服务器等待浏览器重新连接的最大时间 (default: 3.0 seconds)
    :param message_history_length: 连接中断后将存储并重新发送的最大消息数 (default: 1000, use 0 to disable, *added in version 2.9.0*)
    :param cache_control_directives: 内部静态文件的缓存控制指令 (default: `'public, max-age=31536000, immutable, stale-while-revalidate=31536000'`)
    :param fastapi_docs: 启用 FastAPI 的自动文档，包括 Swagger UI、ReDoc 和 OpenAPI JSON (bool or dictionary as described `here <https://fastapi.tiangolo.com/tutorial/metadata/>`_, default: `False`, *updated in version 2.9.0*)
    :param show: 自动在浏览器标签页中打开 UI (default: `True`)
    :param on_air: 技术预览：如果设置为 `True`，则 `允许临时远程访问 <https://nicegui.io/documentation/section_configuration_deployment#nicegui_on_air>`_ (default: disabled)
    :param native: 在 800x600 大小的原生窗口中打开 UI (default: `False`, deactivates `show`, automatically finds an open port)
    :param window_size: 在具有提供大小的原生窗口中打开 UI (e.g. `(1024, 786)`, default: `None`, also activates `native`)
    :param fullscreen: 在全屏窗口中打开 UI (default: `False`, also activates `native`)
    :param frameless: 在无边框窗口中打开 UI (default: `False`, also activates `native`)
    :param reload: 在文件更改时自动重新加载 UI (default: `True`)
    :param uvicorn_logging_level: uvicorn 服务器的日志记录级别 (default: `'warning'`)
    :param uvicorn_reload_dirs: 用于监视的目录的逗号分隔列表字符串 (default is current working directory only)
    :param uvicorn_reload_includes: 在修改时触发重新加载的 glob 模式的逗号分隔列表字符串 (default: `'*.py'`)
    :param uvicorn_reload_excludes: 应忽略重新加载的 glob 模式的逗号分隔列表字符串 (default: `'.*, .py[cod], .sw.*, ~*'`)
    :param tailwind: 是否使用 Tailwind (experimental, default: `True`)
    :param prod_js: 是否使用 Vue 和 Quasar 依赖的生产版本 (default: `True`)
    :param endpoint_documentation: 控制哪些端点出现在自动生成的 OpenAPI 文档中 (default: 'none', options: 'none', 'internal', 'page', 'all')
    :param storage_secret: 基于浏览器的存储的秘密密钥 (default: `None`, a value is required to enable ui.storage.individual and ui.storage.browser)
    :param show_welcome_message: 是否显示欢迎消息 (default: `True`)
    :param kwargs: 附加的关键字参数将传递给 `uvicorn.run`
    """
    core.app.config.add_run_config(
        reload=reload,
        title=title,
        viewport=viewport,
        favicon=favicon,
        dark=dark,
        language=language,
        binding_refresh_interval=binding_refresh_interval,
        reconnect_timeout=reconnect_timeout,
        message_history_length=message_history_length,
        cache_control_directives=cache_control_directives,
        tailwind=tailwind,
        prod_js=prod_js,
        show_welcome_message=show_welcome_message,
    )
    core.app.config.endpoint_documentation = endpoint_documentation
    if not helpers.is_pytest():
        core.app.add_middleware(GZipMiddleware)
    core.app.add_middleware(RedirectWithPrefixMiddleware)
    core.app.add_middleware(SetCacheControlMiddleware)

    for route in core.app.routes:
        if not isinstance(route, Route):
            continue
        if route.path.startswith('/_nicegui') and hasattr(route, 'methods'):
            route.include_in_schema = endpoint_documentation in {'internal', 'all'}
        if route.path == '/' or route.path in Client.page_routes.values():
            route.include_in_schema = endpoint_documentation in {'page', 'all'}

    if fastapi_docs:
        if not core.app.docs_url:
            core.app.docs_url = '/docs'
        if not core.app.redoc_url:
            core.app.redoc_url = '/redoc'
        if not core.app.openapi_url:
            core.app.openapi_url = '/openapi.json'
        if isinstance(fastapi_docs, dict):
            core.app.title = fastapi_docs.get('title') or title
            core.app.summary = fastapi_docs.get('summary')
            core.app.description = fastapi_docs.get('description') or ''
            core.app.version = fastapi_docs.get('version') or '0.1.0'
            core.app.terms_of_service = fastapi_docs.get('terms_of_service')
            contact = fastapi_docs.get('contact')
            license_info = fastapi_docs.get('license_info')
            core.app.contact = dict(contact) if contact else None
            core.app.license_info = dict(license_info) if license_info else None
        core.app.setup()

    if on_air:
        core.air = Air('' if on_air is True else on_air)

    if multiprocessing.current_process().name != 'MainProcess':
        return

    if reload and not hasattr(__main__, '__file__'):
        log.warning('disabling auto-reloading because is is only supported when running from a file')
        core.app.config.reload = reload = False

    if fullscreen:
        native = True
    if frameless:
        native = True
    if window_size:
        native = True
    if native:
        show = False
        host = host or '127.0.0.1'
        port = port or native_module.find_open_port()
        width, height = window_size or (800, 600)
        native_host = '127.0.0.1' if host == '0.0.0.0' else host
        native_module.activate(native_host, port, title, width, height, fullscreen, frameless)
    else:
        port = port or 8080
        host = host or '0.0.0.0'
    assert host is not None
    assert port is not None

    if kwargs.get('ssl_certfile') and kwargs.get('ssl_keyfile'):
        protocol = 'https'
    else:
        protocol = 'http'

    # NOTE: We save host and port in environment variables so the subprocess started in reload mode can access them.
    os.environ['NICEGUI_HOST'] = host
    os.environ['NICEGUI_PORT'] = str(port)
    os.environ['NICEGUI_PROTOCOL'] = protocol

    if show:
        helpers.schedule_browser(protocol, host, port)

    def split_args(args: str) -> List[str]:
        return [a.strip() for a in args.split(',')]

    if kwargs.get('workers', 1) > 1:
        raise ValueError('NiceGUI does not support multiple workers yet.')

    # NOTE: The following lines are basically a copy of `uvicorn.run`, but keep a reference to the `server`.

    config = CustomServerConfig(
        APP_IMPORT_STRING if reload else core.app,
        host=host,
        port=port,
        reload=reload,
        reload_includes=split_args(uvicorn_reload_includes) if reload else None,
        reload_excludes=split_args(uvicorn_reload_excludes) if reload else None,
        reload_dirs=split_args(uvicorn_reload_dirs) if reload else None,
        log_level=uvicorn_logging_level,
        **kwargs,
    )
    config.storage_secret = storage_secret
    config.method_queue = native_module.native.method_queue if native else None
    config.response_queue = native_module.native.response_queue if native else None
    Server.create_singleton(config)

    if (reload or config.workers > 1) and not isinstance(config.app, str):
        log.warning('You must pass the application as an import string to enable "reload" or "workers".')
        sys.exit(1)

    if config.should_reload:
        sock = config.bind_socket()
        ChangeReload(config, target=Server.instance.run, sockets=[sock]).run()
    elif config.workers > 1:
        sock = config.bind_socket()
        Multiprocess(config, target=Server.instance.run, sockets=[sock]).run()
    else:
        Server.instance.run()
    if config.uds:
        os.remove(config.uds)  # pragma: py-win32

    if not Server.instance.started and not config.should_reload and config.workers == 1:
        sys.exit(STARTUP_FAILURE)
