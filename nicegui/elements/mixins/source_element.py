from pathlib import Path
from typing import Any, Callable, Optional, cast

from typing_extensions import Self

from ... import core
from ...binding import BindableProperty, bind, bind_from, bind_to
from ...element import Element
from ...helpers import is_file


class SourceElement(Element):
    """源元素混入

    为元素提供源数据管理功能的混入类。
    支持文件源、URL源和源数据绑定。
    自动处理静态文件和媒体文件的路由管理。
    """
    source = BindableProperty(
        on_change=lambda sender, source: cast(Self, sender)._handle_source_change(source))  # pylint: disable=protected-access

    SOURCE_IS_MEDIA_FILE: bool = False
    """源是否为媒体文件，决定使用add_media_file还是add_static_file"""

    def __init__(self, *, source: Any, **kwargs: Any) -> None:
        """初始化源元素

        :param source: 源数据，可以是文件路径、URL或其他数据源
        """
        super().__init__(**kwargs)
        self.auto_route: Optional[str] = None
        self.source = source
        self._set_props(source)

    def bind_source_to(self,
                       target_object: Any,
                       target_name: str = 'source',
                       forward: Optional[Callable[[Any], Any]] = None,
                       ) -> Self:
        """将此元素的源绑定到目标对象的target_name属性。

        绑定是单向的，从此元素到目标。
        更新会立即发生，并在值变化时进行。

        :param target_object: 要绑定到的对象。
        :param target_name: 要绑定到的属性名称。
        :param forward: 在应用到目标之前应用于值的函数（默认：恒等函数）。
        """
        bind_to(self, 'source', target_object, target_name, forward)
        return self

    def bind_source_from(self,
                         target_object: Any,
                         target_name: str = 'source',
                         backward: Optional[Callable[[Any], Any]] = None,
                         ) -> Self:
        """将此元素的源从目标对象的target_name属性绑定。

        绑定是单向的，从目标到此元素。
        更新会立即发生，并在值变化时进行。

        :param target_object: 要绑定来源的对象。
        :param target_name: 要绑定来源的属性名称。
        :param backward: 在应用到元素之前应用于值的函数（默认：恒等函数）。
        """
        bind_from(self, 'source', target_object, target_name, backward)
        return self

    def bind_source(self,
                    target_object: Any,
                    target_name: str = 'source', *,
                    forward: Optional[Callable[[Any], Any]] = None,
                    backward: Optional[Callable[[Any], Any]] = None,
                    ) -> Self:
        """将此元素的源绑定到目标对象的target_name属性。

        绑定是双向的，从此元素到目标和从目标到此元素。
        更新会立即发生，并在值变化时进行。
        反向绑定在初始同步时具有优先权。

        :param target_object: 要绑定到的对象。
        :param target_name: 要绑定到的属性名称。
        :param forward: 在应用到目标之前应用于值的函数（默认：恒等函数）。
        :param backward: 在应用到元素之前应用于值的函数（默认：恒等函数）。
        """
        bind(self, 'source', target_object, target_name, forward=forward, backward=backward)
        return self

    def set_source(self, source: Any) -> None:
        """设置此元素的源。

        :param source: 新源。
        """
        self.source = source

    def _handle_source_change(self, source: Any) -> None:
        """当元素源变化时调用。

        :param source: 新源。
        """
        self._set_props(source)
        self.update()

    def _set_props(self, source: Any) -> None:
        """设置源属性，处理文件路由和路径验证

        :param source: 要设置的源数据
        :raises FileNotFoundError: 当文件路径不存在时
        """
        if is_file(source):
            if self.auto_route:
                core.app.remove_route(self.auto_route)
            if self.SOURCE_IS_MEDIA_FILE:
                source = core.app.add_media_file(local_file=source)
            else:
                source = core.app.add_static_file(local_file=source)
            self.auto_route = source
        if isinstance(source, Path) and not source.exists():
            raise FileNotFoundError(f'文件未找到：{source}')
        self._props['src'] = source

    def _handle_delete(self) -> None:
        """处理元素删除时的清理工作，移除自动创建的路由"""
        if self.auto_route:
            core.app.remove_route(self.auto_route)
        return super()._handle_delete()
