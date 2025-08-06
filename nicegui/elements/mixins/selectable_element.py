from typing import Any, Callable, List, Optional, cast

from typing_extensions import Self

from ...binding import BindableProperty, bind, bind_from, bind_to
from ...element import Element
from ...events import Handler, ValueChangeEventArguments, handle_event


class SelectableElement(Element):
    """可选择元素混入

    为元素提供选择状态管理功能的混入类。
    支持选择状态绑定和选择事件处理。
    """
    selected = BindableProperty(
        on_change=lambda sender, selected: cast(Self, sender)._handle_selection_change(selected))  # pylint: disable=protected-access

    def __init__(self, *,
                 selectable: bool,
                 selected: bool,
                 on_selection_change: Optional[Handler[ValueChangeEventArguments]] = None,
                 **kwargs: Any) -> None:
        """初始化可选择元素

        :param selectable: 元素是否可选择
        :param selected: 初始选择状态
        :param on_selection_change: 选择状态变化时的回调函数
        """
        super().__init__(**kwargs)
        if not selectable:
            return

        self._props['selectable'] = selectable

        self.selected = selected
        self._props['selected'] = selected
        self.set_selected(selected)
        self.on('update:selected', lambda e: self.set_selected(e.args))

        self._selection_change_handlers: List[Handler[ValueChangeEventArguments]] = []
        if on_selection_change:
            self.on_selection_change(on_selection_change)

    def on_selection_change(self, callback: Handler[ValueChangeEventArguments]) -> Self:
        """添加选择状态变化时要调用的回调函数。"""
        self._selection_change_handlers.append(callback)
        return self

    def bind_selected_to(self,
                         target_object: Any,
                         target_name: str = 'selected',
                         forward: Optional[Callable[[Any], Any]] = None,
                         ) -> Self:
        """将此元素的选择状态绑定到目标对象的target_name属性。

        绑定是单向的，从此元素到目标。
        更新会立即发生，并在值变化时进行。

        :param target_object: 要绑定到的对象。
        :param target_name: 要绑定到的属性名称。
        :param forward: 在应用到目标之前应用于值的函数（默认：恒等函数）。
        """
        bind_to(self, 'selected', target_object, target_name, forward)
        return self

    def bind_selected_from(self,
                           target_object: Any,
                           target_name: str = 'selected',
                           backward: Optional[Callable[[Any], Any]] = None,
                           ) -> Self:
        """将此元素的选择状态从目标对象的target_name属性绑定。

        绑定是单向的，从目标到此元素。
        更新会立即发生，并在值变化时进行。

        :param target_object: 要绑定来源的对象。
        :param target_name: 要绑定来源的属性名称。
        :param backward: 在应用到元素之前应用于值的函数（默认：恒等函数）。
        """
        bind_from(self, 'selected', target_object, target_name, backward)
        return self

    def bind_selected(self,
                      target_object: Any,
                      target_name: str = 'selected', *,
                      forward: Optional[Callable[[Any], Any]] = None,
                      backward: Optional[Callable[[Any], Any]] = None,
                      ) -> Self:
        """将此元素的选择状态绑定到目标对象的target_name属性。

        绑定是双向的，从此元素到目标和从目标到此元素。
        更新会立即发生，并在值变化时进行。
        反向绑定在初始同步时具有优先权。

        :param target_object: 要绑定到的对象。
        :param target_name: 要绑定到的属性名称。
        :param forward: 在应用到目标之前应用于值的函数（默认：恒等函数）。
        :param backward: 在应用到元素之前应用于值的函数（默认：恒等函数）。
        """
        bind(self, 'selected', target_object, target_name, forward=forward, backward=backward)
        return self

    def set_selected(self, selected: bool) -> None:
        """设置此元素的选择状态。

        :param selected: 新选择状态。
        """
        self.selected = selected

    def _handle_selection_change(self, selected: bool) -> None:
        """当元素选择状态变化时调用。

        :param selected: 新选择状态。
        """
        self._props['selected'] = selected
        self.update()
        args = ValueChangeEventArguments(sender=self, client=self.client, value=self._props['selected'])
        for handler in self._selection_change_handlers:
            handle_event(handler, args)
