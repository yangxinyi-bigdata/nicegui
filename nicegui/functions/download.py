from pathlib import Path
from typing import Optional, Union

from .. import core, helpers
from ..context import context
from ..logging import log


class Download:
    """下载函数

    这些函数允许您下载文件、URL 或原始数据。

    *在版本 2.14.0 中添加*
    """

    def __call__(self, src: Union[str, Path, bytes], filename: Optional[str] = None, media_type: str = '') -> None:
        """下载

        触发文件、URL 或字节下载的函数。

        :param src: 相对目标 URL、文件的本地路径或应下载的原始数据
        :param filename: 要下载的文件名（默认：服务器上的文件名）
        :param media_type: 要下载的文件的媒体类型（默认：""）
        """
        if isinstance(src, bytes):
            self.content(src, filename, media_type)
        elif helpers.is_file(src):
            self.file(src, filename, media_type)
        else:
            src = str(src)
            self.from_url(src, filename, media_type)

    def file(self, path: Union[str, Path], filename: Optional[str] = None, media_type: str = '') -> None:
        """从本地路径下载文件

        触发文件下载的函数。

        *在版本 2.14.0 中添加*

        :param path: 文件的本地路径
        :param filename: 要下载的文件名（默认：服务器上的文件名）
        :param media_type: 要下载的文件的媒体类型（默认：""）
        """
        src = core.app.add_static_file(local_file=path, single_use=True)
        context.client.download(src, filename, media_type)

    def from_url(self, url: str, filename: Optional[str] = None, media_type: str = '') -> None:
        """从相对 URL 下载

        触发从相对 URL 下载的函数。

        注意：
        此函数仅适用于相对 URL。
        对于绝对 URL，浏览器会忽略下载指令，并尝试在新标签页中查看文件（如果可能），
        例如图像、PDF 等。
        因此，下载可能仅适用于某些文件类型，如 .zip、.db 等。
        此外，浏览器会忽略 filename 和 media_type 参数，
        而是尊重源服务器的头部信息。
        请将绝对 URL 替换为相对 URL，或使用 ``ui.navigate.to(url, new_tab=True)`` 代替。

        *在版本 2.14.0 中添加*

        *在版本 2.19.0 中更新：添加了跨源下载警告*

        :param url: URL
        :param filename: 要下载的文件名（默认：服务器上的文件名）
        :param media_type: 要下载的文件的媒体类型（默认：""）
        """
        is_relative = url.startswith('/') or url.startswith('./') or url.startswith('../')
        if not is_relative:
            log.warning('Using `ui.download.from_url` with absolute URLs is not recommended.\n'
                        'Please refer to the documentation for more details.')
        context.client.download(url, filename, media_type)

    def content(self, content: Union[bytes, str], filename: Optional[str] = None, media_type: str = '') -> None:
        """下载原始字节或字符串内容

        触发原始数据下载的函数。

        *在版本 2.14.0 中添加*

        :param content: 原始字节或字符串
        :param filename: 要下载的文件名（默认：服务器上的文件名）
        :param media_type: 要下载的文件的媒体类型（默认：""）
        """
        if isinstance(content, str):
            content = content.encode('utf-8')
        context.client.download(content, filename, media_type)


download = Download()
