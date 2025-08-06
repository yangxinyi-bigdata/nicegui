from typing import Optional, Sequence, Union

from ..context import context
from ..events import GenericEventArguments, Handler


def on(type: str,  # pylint: disable=redefined-builtin
       handler: Optional[Handler[GenericEventArguments]] = None,
       args: Union[None, Sequence[str], Sequence[Optional[Sequence[str]]]] = None, *,
       throttle: float = 0.0,
       leading_events: bool = True,
       trailing_events: bool = True,
       ):
    """订阅全局事件。

    :param type: 事件名称
    :param handler: 事件发生时调用的回调
    :param args: 包含在发送到事件处理器的事件消息中的参数（默认：`None` 表示全部）
    :param throttle: 事件发生之间的最小时间（秒）（默认：0.0）
    :param leading_events: 是否在第一次事件发生时立即触发事件处理器（默认：`True`）
    :param trailing_events: 是否在最后一次事件发生后触发事件处理器（默认：`True`）
    """
    context.client.layout.on(type, handler, args,
                             throttle=throttle, leading_events=leading_events, trailing_events=trailing_events)
