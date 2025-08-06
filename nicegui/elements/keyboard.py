from typing import List, Literal, Optional

from typing_extensions import Self

from ..binding import BindableProperty
from ..element import Element
from ..events import (
    GenericEventArguments,
    Handler,
    KeyboardAction,
    KeyboardKey,
    KeyboardModifiers,
    KeyEventArguments,
    handle_event,
)


class Keyboard(Element, component='keyboard.js'):
    active = BindableProperty()

    def __init__(self,
                 on_key: Optional[Handler[KeyEventArguments]] = None, *,
                 active: bool = True,
                 repeating: bool = True,
                 ignore: List[Literal['input', 'select', 'button', 'textarea']] =
                     ['input', 'select', 'button', 'textarea'],  # noqa: B006
                 ) -> None:
        """虚拟键盘

        添加全局键盘事件跟踪。

        ``on_key``回调函数接收一个具有以下属性的``KeyEventArguments``对象：

        - ``sender``: ``Keyboard``元素
        - ``client``: 客户端对象
        - ``action``: 具有以下属性的``KeyboardAction``对象：
            - ``keydown``: 是否按下按键
            - ``keyup``: 是否释放按键
            - ``repeat``: 是否为重复的按键事件
        - ``key``: 具有以下属性的``KeyboardKey``对象：
            - ``name``: 按键名称（例如"a", "Enter", "ArrowLeft"；可能值列表请参见`此处 <https://developer.mozilla.org/en-US/docs/Web/API/UI_Events/Keyboard_event_key_values>`_）
            - ``code``: 按键代码（例如"KeyA", "Enter", "ArrowLeft"）
            - ``location``: 按键位置（0表示标准键，1表示左侧键，2表示右侧键，3表示数字键盘键）
        - ``modifiers``: 具有以下属性的``KeyboardModifiers``对象：
            - ``alt``: 是否按下alt键
            - ``ctrl``: 是否按下ctrl键
            - ``meta``: 是否按下meta键
            - ``shift``: 是否按下shift键

        为方便起见，``KeyboardKey``对象还具有以下属性：
            - ``is_cursorkey``: 是否为光标（箭头）键
            - ``number``: 数字键的整数值（0-9，其他键为``None``）
            - ``backspace``, ``tab``, ``enter``, ``shift``, ``control``, ``alt``, ``pause``, ``caps_lock``, ``escape``, ``space``,
              ``page_up``, ``page_down``, ``end``, ``home``, ``arrow_left``, ``arrow_up``, ``arrow_right``, ``arrow_down``,
              ``print_screen``, ``insert``, ``delete``, ``meta``,
              ``f1``, ``f2``, ``f3``, ``f4``, ``f5``, ``f6``, ``f7``, ``f8``, ``f9``, ``f10``, ``f11``, ``f12``: 是否为相应的键

        :param on_key: 键盘事件发生时要执行的回调函数。
        :param active: 布尔标志，指示是否应执行回调函数（默认：``True``）
        :param repeating: 布尔标志，指示是否应重复发送按住的键（默认：``True``）
        :param ignore: 当这些元素类型之一获得焦点时忽略按键（默认：``['input', 'select', 'button', 'textarea']``）
        """
        super().__init__()
        self._key_handlers = [on_key] if on_key else []
        self.active = active
        self._props['events'] = ['keydown', 'keyup']
        self._props['repeating'] = repeating
        self._props['ignore'] = ignore[:]
        self.on('key', self._handle_key)

    def _handle_key(self, e: GenericEventArguments) -> None:
        if not self.active:
            return

        action = KeyboardAction(
            keydown=e.args['action'] == 'keydown',
            keyup=e.args['action'] == 'keyup',
            repeat=e.args['repeat'],
        )
        modifiers = KeyboardModifiers(
            alt=e.args['altKey'],
            ctrl=e.args['ctrlKey'],
            meta=e.args['metaKey'],
            shift=e.args['shiftKey'],
        )
        key = KeyboardKey(
            name=e.args['key'],
            code=e.args['code'],
            location=e.args['location'],
        )
        arguments = KeyEventArguments(
            sender=self,
            client=self.client,
            action=action,
            modifiers=modifiers,
            key=key,
        )
        for handler in self._key_handlers:
            handle_event(handler, arguments)

    def on_key(self, handler: Handler[KeyEventArguments]) -> Self:
        """添加键盘事件发生时要调用的回调函数。"""
        self._key_handlers.append(handler)
        return self
