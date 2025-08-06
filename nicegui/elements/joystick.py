from typing import Any, Optional

from typing_extensions import Self

from ..element import Element
from ..events import GenericEventArguments, Handler, JoystickEventArguments, handle_event


class Joystick(Element,
               component='joystick.vue',
               dependencies=['lib/nipplejs/nipplejs.js'],
               default_classes='nicegui-joystick'):

    def __init__(self, *,
                 on_start: Optional[Handler[JoystickEventArguments]] = None,
                 on_move: Optional[Handler[JoystickEventArguments]] = None,
                 on_end: Optional[Handler[JoystickEventArguments]] = None,
                 throttle: float = 0.05,
                 **options: Any) -> None:
        """虚拟摇杆

        基于`nipple.js <https://yoannmoi.net/nipplejs/>`_创建虚拟摇杆。

        :param on_start: 用户触摸摇杆时的回调函数
        :param on_move: 用户移动摇杆时的回调函数
        :param on_end: 用户释放摇杆时的回调函数
        :param throttle: 移动事件的节流间隔，以秒为单位（默认：0.05）
        :param options: 应该传递给`底层nipple.js库 <https://github.com/yoannmoinet/nipplejs#options>`_的参数，如`color`
        """
        super().__init__()
        self._props['options'] = options
        self.active = False

        self._start_handlers = [on_start] if on_start else []
        self._move_handlers = [on_move] if on_move else []
        self._end_handlers = [on_end] if on_end else []

        def handle_start() -> None:
            self.active = True
            args = JoystickEventArguments(sender=self, client=self.client, action='start')
            for handler in self._start_handlers:
                handle_event(handler, args)

        def handle_move(e: GenericEventArguments) -> None:
            if self.active:
                args = JoystickEventArguments(sender=self,
                                              client=self.client,
                                              action='move',
                                              x=float(e.args['data']['vector']['x']),
                                              y=float(e.args['data']['vector']['y']))
                for handler in self._move_handlers:
                    handle_event(handler, args)

        def handle_end() -> None:
            self.active = False
            args = JoystickEventArguments(sender=self,
                                          client=self.client,
                                          action='end')
            for handler in self._end_handlers:
                handle_event(handler, args)

        self.on('start', handle_start, [])
        self.on('move', handle_move, ['data'], throttle=throttle)
        self.on('end', handle_end, [])

    def on_start(self, callback: Handler[JoystickEventArguments]) -> Self:
        """添加用户触摸摇杆时要调用的回调函数。"""
        self._start_handlers.append(callback)
        return self

    def on_move(self, callback: Handler[JoystickEventArguments]) -> Self:
        """添加用户移动摇杆时要调用的回调函数。"""
        self._move_handlers.append(callback)
        return self

    def on_end(self, callback: Handler[JoystickEventArguments]) -> Self:
        """添加用户释放摇杆时要调用的回调函数。"""
        self._end_handlers.append(callback)
        return self
