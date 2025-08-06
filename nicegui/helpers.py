from __future__ import annotations

import asyncio
import functools
import hashlib
import os
import socket
import struct
import threading
import time
import webbrowser
from collections.abc import Callable
from inspect import Parameter, signature
from pathlib import Path
from typing import TYPE_CHECKING, Any, Optional, Set, Tuple, Union

from .context import context
from .logging import log

if TYPE_CHECKING:
    from .element import Element

_shown_warnings: Set[str] = set()


def warn_once(message: str, *, stack_info: bool = False) -> None:
    """只打印一次警告消息。"""
    if message not in _shown_warnings:
        log.warning(message, stack_info=stack_info)
        _shown_warnings.add(message)


def is_pytest() -> bool:
    """检查代码是否在 pytest 中运行。"""
    return 'PYTEST_CURRENT_TEST' in os.environ


def is_coroutine_function(obj: Any) -> bool:
    """检查对象是否是协程函数。

    需要此函数是因为 functools.partial 不是协程函数，但其 func 属性是。
    注意：对于协程对象，它将返回 false。
    """
    while isinstance(obj, functools.partial):
        obj = obj.func
    return asyncio.iscoroutinefunction(obj)


def expects_arguments(func: Callable) -> bool:
    """检查函数是否需要非可变参数且没有默认值。"""
    return any(p.default is Parameter.empty and
               p.kind is not Parameter.VAR_POSITIONAL and
               p.kind is not Parameter.VAR_KEYWORD
               for p in signature(func).parameters.values())


def is_file(path: Optional[Union[str, Path]]) -> bool:
    """检查路径是否为存在的文件。"""
    if not path:
        return False
    if isinstance(path, str) and path.strip().startswith('data:'):
        return False  # NOTE: avoid passing data URLs to Path
    try:
        return Path(path).is_file()
    except OSError:
        return False


def hash_file_path(path: Path, *, max_time: Optional[float] = None) -> str:
    """基于给定路径的字符串表示形式以及可选的给定文件最后修改时间来哈希该路径。"""
    hasher = hashlib.sha256(path.as_posix().encode())
    if max_time is not None:
        hasher.update(struct.pack('!d', max_time))
    return hasher.hexdigest()[:32]


def is_port_open(host: str, port: int) -> bool:
    """通过检查是否可以建立 TCP 连接来检查端口是否开放。"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((host, port))
    except (ConnectionRefusedError, TimeoutError):
        return False
    except Exception:
        return False
    else:
        return True
    finally:
        sock.close()


def schedule_browser(protocol: str, host: str, port: int) -> Tuple[threading.Thread, threading.Event]:
    """非阻塞地等待端口开放，然后启动网页浏览器。

    此函数启动一个线程以实现非阻塞。
    该线程然后使用 `is_port_open` 来检查端口何时开放。
    当连接确认时，使用 `webbrowser.open` 启动网页浏览器。

    该线程创建为守护线程，以免干扰 Ctrl+C。

    如果需要停止此线程，可以通过设置返回的 Event 来实现。
    该线程将在下一个循环中停止而不打开浏览器。

    :return: 由实际线程对象和用于停止线程的事件组成的元组。
    """
    cancel = threading.Event()

    def in_thread(protocol: str, host: str, port: int) -> None:
        while not is_port_open(host, port):
            if cancel.is_set():
                return
            time.sleep(0.1)
        webbrowser.open(f'{protocol}://{host}:{port}/')

    host = host if host != '0.0.0.0' else '127.0.0.1'
    thread = threading.Thread(target=in_thread, args=(protocol, host, port), daemon=True)
    thread.start()
    return thread, cancel


def kebab_to_camel_case(string: str) -> str:
    """将 kebab-case 字符串转换为 camelCase。"""
    return ''.join(word.capitalize() if i else word for i, word in enumerate(string.split('-')))


def event_type_to_camel_case(string: str) -> str:
    """将事件类型字符串转换为 camelCase。"""
    return '.'.join(kebab_to_camel_case(part) if part != '-' else part for part in string.split('.'))


def require_top_level_layout(element: Element) -> None:
    """检查元素是否为顶级布局元素。"""
    parent = context.slot.parent
    if parent != parent.client.content:
        raise RuntimeError(
            f'Found top level layout element "{element.__class__.__name__}" inside element "{parent.__class__.__name__}". '
            'Top level layout elements can not be nested but must be direct children of the page content.',
        )
