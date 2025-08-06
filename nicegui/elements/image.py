import base64
import io
import time
from pathlib import Path
from typing import Union

from .. import optional_features
from ..logging import log
from .mixins.source_element import SourceElement

try:
    from PIL.Image import Image as PIL_Image
    optional_features.register('pillow')
except ImportError:
    pass


class Image(SourceElement, component='image.js'):
    PIL_CONVERT_FORMAT = 'PNG'

    def __init__(self, source: Union[str, Path, 'PIL_Image'] = '') -> None:
        """图像

        显示图像。
        此元素基于Quasar的`QImg <https://quasar.dev/vue-components/img>`_组件。

        :param source: 图像的源；可以是URL、本地文件路径、base64字符串或PIL图像
        """
        super().__init__(source=source)

    def set_source(self, source: Union[str, Path, 'PIL_Image']) -> None:
        return super().set_source(source)

    def _set_props(self, source: Union[str, Path, 'PIL_Image']) -> None:
        if optional_features.has('pillow') and isinstance(source, PIL_Image):
            source = pil_to_base64(source, self.PIL_CONVERT_FORMAT)
        super()._set_props(source)

    def force_reload(self) -> None:
        """强制图像从源重新加载。"""
        if self._props['src'].startswith('data:'):
            log.warning('ui.image: force_reload() only works with network sources (not base64)')
            return
        self._props['t'] = time.time()
        self.update()


def pil_to_base64(pil_image: 'PIL_Image', image_format: str) -> str:
    """将PIL图像转换为可用作图像源的base64字符串。

    :param pil_image: PIL图像
    :param image_format: 图像格式
    :return: base64字符串
    """
    buffer = io.BytesIO()
    pil_image.save(buffer, image_format)
    base64_encoded = base64.b64encode(buffer.getvalue())
    base64_string = base64_encoded.decode('utf-8')
    return f'data:image/{image_format.lower()};base64,{base64_string}'
