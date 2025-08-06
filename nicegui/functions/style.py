from pathlib import Path
from typing import Union

from .. import optional_features

try:
    import sass
    optional_features.register('sass')
except ImportError:
    pass

from .. import helpers
from .html import add_head_html


def add_css(content: Union[str, Path], *, shared: bool = False) -> None:
    """向页面添加 CSS 样式定义。

    此函数可用于向 HTML 页面的头部添加 CSS 样式定义。

    *在版本 2.0.0 中添加*

    :param content: CSS 内容（字符串或文件路径）
    :param shared: 是否将代码添加到所有页面（默认：``False``，*在版本 2.14.0 中添加*）
    """
    if helpers.is_file(content):
        content = Path(content).read_text(encoding='utf-8')
    add_head_html(f'<style>{content}</style>', shared=shared)


def add_scss(content: Union[str, Path], *, indented: bool = False, shared: bool = False) -> None:
    """向页面添加 SCSS 样式定义。

    此函数可用于向 HTML 页面的头部添加 SCSS 样式定义。

    *在版本 2.0.0 中添加*

    :param content: SCSS 内容（字符串或文件路径）
    :param indented: 内容是否缩进（SASS）或不缩进（SCSS）（默认：`False`）
    :param shared: 是否将代码添加到所有页面（默认：``False``，*在版本 2.14.0 中添加*）
    """
    if not optional_features.has('sass'):
        raise ImportError('Please run "pip install libsass" to use SASS or SCSS.')

    if helpers.is_file(content):
        content = Path(content).read_text(encoding='utf-8')
    add_css(sass.compile(string=str(content).strip(), indented=indented), shared=shared)


def add_sass(content: Union[str, Path], *, shared: bool = False) -> None:
    """向页面添加 SASS 样式定义。

    此函数可用于向 HTML 页面的头部添加 SASS 样式定义。

    *在版本 2.0.0 中添加*

    :param content: SASS 内容（字符串或文件路径）
    :param shared: 是否将代码添加到所有页面（默认：``False``，*在版本 2.14.0 中添加*）
    """
    add_scss(content, indented=True, shared=shared)
