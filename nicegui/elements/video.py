from pathlib import Path
from typing import Union

from .mixins.source_element import SourceElement


class Video(SourceElement, component='video.js'):
    SOURCE_IS_MEDIA_FILE = True

    def __init__(self, src: Union[str, Path], *,
                 controls: bool = True,
                 autoplay: bool = False,
                 muted: bool = False,
                 loop: bool = False,
                 ) -> None:
        """视频

        显示视频。

        :param src: 视频源的URL或本地文件路径
        :param controls: 是否显示视频控件，如播放、暂停和音量（默认：`True`）
        :param autoplay: 是否自动开始播放视频（默认：`False`）
        :param muted: 视频是否应该初始静音（默认：`False`）
        :param loop: 视频是否应该循环播放（默认：`False`）

        请参见`此处 <https://developer.mozilla.org/en-US/docs/Web/HTML/Element/video#events>`_
        获取可以使用通用事件订阅`on()`订阅的事件列表。
        """
        super().__init__(source=src)
        self._props['controls'] = controls
        self._props['autoplay'] = autoplay
        self._props['muted'] = muted
        self._props['loop'] = loop

    def set_source(self, source: Union[str, Path]) -> None:
        return super().set_source(source)

    def seek(self, seconds: float) -> None:
        """跳转到视频中的特定位置。

        :param seconds: 位置（秒）
        """
        self.run_method('seek', seconds)

    def play(self) -> None:
        """播放视频。"""
        self.run_method('play')

    def pause(self) -> None:
        """暂停视频。"""
        self.run_method('pause')
