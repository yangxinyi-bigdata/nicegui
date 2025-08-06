import io
from typing import Union

from .. import json, optional_features
from ..logging import log
from .javascript import run_javascript

try:
    from PIL import Image as PIL_Image
    optional_features.register('pillow')
except ImportError:
    pass


async def read() -> str:
    """从剪贴板读取文本。

    注意：此函数仅在安全上下文（HTTPS 或 localhost）中工作。
    """
    result = await run_javascript('''
        if (navigator.clipboard) {
            return navigator.clipboard.readText()
        }
        else {
            console.error('Clipboard API is only available in secure contexts (HTTPS or localhost).')
        }
    ''')
    if result is None:
        log.warning('Clipboard API is only available in secure contexts (HTTPS or localhost).')
    return result or ''


def write(text: str) -> None:
    """向剪贴板写入文本。

    注意：此函数仅在安全上下文（HTTPS 或 localhost）中工作。

    :param text: 要写入的文本
    """
    run_javascript(f'''
        if (navigator.clipboard) {{
            navigator.clipboard.writeText({json.dumps(text)})
        }}
        else {{
            console.error('Clipboard API is only available in secure contexts (HTTPS or localhost).')
        }}
    ''')


async def read_image() -> Union['PIL_Image.Image', None]:
    """从剪贴板读取 PIL 图像。

    注意：此函数仅在安全上下文（HTTPS 或 localhost）中工作，并且需要安装 Pillow。

    *在版本 2.10.0 中添加*
    """
    if not optional_features.has('pillow'):
        log.warning('Pillow is not installed, so we cannot read images from the clipboard.')
        return None
    content = await run_javascript('''
        if (navigator.clipboard) {
            const items = await navigator.clipboard.read();
            for (const item of items) {
                if (item.types.length > 0 && /^image/.test(item.types[0])) {
                    return await item.getType(item.types[0]);
                }
            }
        }
        else {
            console.error('Clipboard API is only available in secure contexts (HTTPS or localhost).');
        }
    ''', timeout=5)
    if not content:
        return None
    buffer = io.BytesIO(content)
    return PIL_Image.open(buffer)
