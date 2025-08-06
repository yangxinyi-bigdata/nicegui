from __future__ import annotations

import time
from pathlib import Path
from typing import List, Optional, Tuple, Union, cast

from typing_extensions import Self

from .. import optional_features
from ..events import GenericEventArguments, Handler, MouseEventArguments, handle_event
from ..logging import log
from .image import pil_to_base64
from .mixins.content_element import ContentElement
from .mixins.source_element import SourceElement

try:
    from PIL.Image import Image as PIL_Image
    optional_features.register('pillow')
except ImportError:
    pass


class InteractiveImage(SourceElement, ContentElement, component='interactive_image.js'):
    CONTENT_PROP = 'content'
    PIL_CONVERT_FORMAT = 'PNG'

    def __init__(self,
                 source: Union[str, Path, 'PIL_Image'] = '', *,  # noqa: UP037
                 content: str = '',
                 size: Optional[Tuple[float, float]] = None,
                 on_mouse: Optional[Handler[MouseEventArguments]] = None,
                 events: List[str] = ['click'],  # noqa: B006
                 cross: Union[bool, str] = False,
                 ) -> None:
        """交互式图像

        创建一个带有SVG覆盖层的图像，处理鼠标事件并返回图像坐标。
        这也是无闪烁图像更新的最佳选择。
        如果源URL变化速度超过浏览器加载图像的速度，一些图像将被跳过。
        因此，重复更新图像源将自动适应可用带宽。
        参见`OpenCV摄像头示例 <https://github.com/zauberzeug/nicegui/tree/main/examples/opencv_webcam/main.py>`_。

        鼠标事件处理程序被调用时包含鼠标事件参数：

        - `type`（JavaScript事件的名称），
        - `image_x` 和 `image_y`（以像素为单位的图像坐标），
        - `button` 和 `buttons`（来自JavaScript事件的鼠标按钮编号），以及
        - `alt`、`ctrl`、`meta` 和 `shift`（来自JavaScript事件的修饰键）。

        您也可以传递宽度和高度的元组而不是图像源。
        这将创建一个具有给定大小的空图像。

        :param source: 图像的源；可以是URL、本地文件路径、base64字符串或仅是图像大小
        :param content: 应该覆盖的SVG内容；视口与图像具有相同的尺寸
        :param size: 图像的大小（宽度、高度），以像素为单位；仅在未设置`source`时使用
        :param on_mouse: 鼠标事件的回调函数（包含以像素为单位的图像坐标`image_x`和`image_y`）
        :param events: 要订阅的JavaScript事件列表（默认：`['click']`）
        :param cross: 是否显示十字准线或颜色字符串（默认：`False`）
        """
        super().__init__(source=source, content=content)
        self._props['events'] = events[:]
        self._props['cross'] = cross
        self._props['size'] = size

        if on_mouse:
            self.on_mouse(on_mouse)

    def set_source(self, source: Union[str, Path, 'PIL_Image']) -> None:  # noqa: UP037
        return super().set_source(source)

    def on_mouse(self, on_mouse: Handler[MouseEventArguments]) -> Self:
        """添加鼠标事件发生时要调用的回调函数。"""
        def handle_mouse(e: GenericEventArguments) -> None:
            args = cast(dict, e.args)
            arguments = MouseEventArguments(
                sender=self,
                client=self.client,
                type=args.get('mouse_event_type', ''),
                image_x=args.get('image_x', 0.0),
                image_y=args.get('image_y', 0.0),
                button=args.get('button', 0),
                buttons=args.get('buttons', 0),
                alt=args.get('altKey', False),
                ctrl=args.get('ctrlKey', False),
                meta=args.get('metaKey', False),
                shift=args.get('shiftKey', False),
            )
            handle_event(on_mouse, arguments)
        self.on('mouse', handle_mouse)
        return self

    def _set_props(self, source: Union[str, Path, 'PIL_Image']) -> None:  # noqa: UP037
        if optional_features.has('pillow') and isinstance(source, PIL_Image):
            source = pil_to_base64(source, self.PIL_CONVERT_FORMAT)
        super()._set_props(source)

    def force_reload(self) -> None:
        """强制图像从源重新加载。"""
        if self._props['src'].startswith('data:'):
            log.warning('ui.interactive_image: force_reload() only works with network sources (not base64)')
            return
        self._props['t'] = time.time()
        self.update()

    def add_layer(self, *, content: str = '') -> InteractiveImageLayer:
        """添加一个具有自己内容的新图层。

        *在版本2.17.0中添加*
        """
        with self:
            layer = InteractiveImageLayer(source=self.source, content=content, size=self._props['size']) \
                .classes('nicegui-interactive-image-layer')
            self.on('loaded', lambda e: layer.run_method('updateViewbox', e.args['width'], e.args['height']))
            return layer


class InteractiveImageLayer(SourceElement, ContentElement, component='interactive_image.js'):
    CONTENT_PROP = 'content'
    PIL_CONVERT_FORMAT = 'PNG'

    def __init__(self, *, source: str, content: str, size: Optional[Tuple[float, float]]) -> None:
        """交互式图像图层

        在向``InteractiveImage``添加图层时创建此元素。

        *在版本2.17.0中添加*
        """
        super().__init__(source=source, content=content)
        self._props['size'] = size

    def _set_props(self, source: Union[str, Path, 'PIL_Image']) -> None:  # noqa: UP037
        if optional_features.has('pillow') and isinstance(source, PIL_Image):
            source = pil_to_base64(source, self.PIL_CONVERT_FORMAT)
        super()._set_props(source)
