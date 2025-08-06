from typing import Literal, Optional

from ..element import Element
from .mixins.icon_element import IconElement


class Timeline(Element):

    def __init__(self,
                 *,
                 side: Literal['left', 'right'] = 'left',
                 layout: Literal['dense', 'comfortable', 'loose'] = 'dense',
                 color: Optional[str] = None,
                 ) -> None:
        """时间线

        此元素代表`Quasar的QTimeline <https://quasar.dev/vue-components/timeline#qtimeline-api>`_组件。

        :param side: 侧边（"left"或"right"；默认："left"）。
        :param layout: 布局（"dense"、"comfortable"或"loose"；默认："dense"）。
        :param color: 图标的颜色。
        """
        super().__init__('q-timeline')
        self._props['side'] = side
        self._props['layout'] = layout
        if color is not None:
            self._props['color'] = color


class TimelineEntry(IconElement, default_classes='nicegui-timeline-entry'):

    def __init__(self,
                 body: Optional[str] = None,
                 *,
                 side: Literal['left', 'right'] = 'left',
                 heading: bool = False,
                 tag: Optional[str] = None,
                 icon: Optional[str] = None,
                 avatar: Optional[str] = None,
                 title: Optional[str] = None,
                 subtitle: Optional[str] = None,
                 color: Optional[str] = None,
                 ) -> None:
        """时间线条目

        此元素代表`Quasar的QTimelineEntry <https://quasar.dev/vue-components/timeline#qtimelineentry-api>`_组件。

        :param body: 正文文本。
        :param side: 侧边（"left"或"right"；默认："left"）。
        :param heading: 时间线条目是否为标题。
        :param tag: 如果是标题要使用的HTML标签名称。
        :param icon: 图标名称。
        :param avatar: 头像URL。
        :param title: 标题文本。
        :param subtitle: 副标题文本。
        :param color: 时间线的颜色。
        """
        super().__init__(tag='q-timeline-entry', icon=icon)
        if body is not None:
            self._props['body'] = body
        self._props['side'] = side
        self._props['heading'] = heading
        if tag is not None:
            self._props['tag'] = tag
        if color is not None:
            self._props['color'] = color
        if avatar is not None:
            self._props['avatar'] = avatar
        if title is not None:
            self._props['title'] = title
        if subtitle is not None:
            self._props['subtitle'] = subtitle
