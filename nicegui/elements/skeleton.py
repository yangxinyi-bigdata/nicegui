from typing import Literal, Optional

from ..element import Element


class Skeleton(Element):

    def __init__(self,
                 type: Literal[  # pylint: disable=redefined-builtin
                     'text',
                     'rect',
                     'circle',
                     'QBtn',
                     'QBadge',
                     'QChip',
                     'QToolbar',
                     'QCheckbox',
                     'QRadio',
                     'QToggle',
                     'QSlider',
                     'QRange',
                     'QInput',
                     'QAvatar',
                 ] = 'rect',
                 *,
                 tag: str = 'div',
                 animation: Literal[
                     'wave',
                     'pulse',
                     'pulse-x',
                     'pulse-y',
                     'fade',
                     'blink',
                     'none',
                 ] = 'wave',
                 animation_speed: float = 1.5,
                 square: bool = False,
                 bordered: bool = False,
                 size: Optional[str] = None,
                 width: Optional[str] = None,
                 height: Optional[str] = None,
                 ) -> None:
        """骨架屏

        此元素基于Quasar的`QSkeleton <https://quasar.dev/vue-components/skeleton>`_组件。
        它用作卡片、菜单和其他组件容器中加载内容的占位符。
        可用类型列表请参见`Quasar文档 <https://quasar.dev/vue-components/skeleton/#predefined-types>`_。

        :param type: 要显示的骨架屏类型（默认："rect"）
        :param tag: 用于此元素的HTML标签（默认："div"）
        :param animation: 骨架屏占位符的动画效果（默认："wave"）
        :param animation_speed: 动画速度，以秒为单位（默认：1.5）
        :param square: 是否移除边框半径使边框成为方形（默认：``False``）
        :param bordered: 是否向组件应用默认边框（默认：``False``）
        :param size: CSS单位的大小（覆盖``width``和``height``）
        :param width: CSS单位的宽度（如果设置了``size``则被覆盖）
        :param height: CSS单位的高度（如果设置了``size``则被覆盖）
        """
        super().__init__('q-skeleton')
        if type != 'rect':
            self._props['type'] = type
        if tag != 'div':
            self._props['tag'] = tag
        if animation != 'wave':
            self._props['animation'] = animation
        if animation_speed != 1.5:
            self._props['animation-speed'] = animation_speed
        if square:
            self._props['square'] = True
        if bordered:
            self._props['bordered'] = True
        if size:
            self._props['size'] = size
        if width:
            self._props['width'] = width
        if height:
            self._props['height'] = height
