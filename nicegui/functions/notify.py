from typing import Any, Literal, Optional, Union

from ..context import context

ARG_MAP = {
    'close_button': 'closeBtn',
    'multi_line': 'multiLine',
}


# pylint: disable=unused-argument
def notify(message: Any, *,
           position: Literal[
               'top-left',
               'top-right',
               'bottom-left',
               'bottom-right',
               'top',
               'bottom',
               'left',
               'right',
               'center',
           ] = 'bottom',
           close_button: Union[bool, str] = False,
           type: Optional[Literal[  # pylint: disable=redefined-builtin
               'positive',
               'negative',
               'warning',
               'info',
               'ongoing',
           ]] = None,
           color: Optional[str] = None,
           multi_line: bool = False,
           **kwargs: Any,
           ) -> None:
    """通知

    在屏幕上显示通知。

    :param message: 通知的内容
    :param position: 屏幕上的位置（"top-left", "top-right", "bottom-left", "bottom-right", "top", "bottom", "left", "right" 或 "center"，默认："bottom"）
    :param close_button: 用于关闭通知的按钮的可选标签（默认：`False`）
    :param type: 可选类型（"positive", "negative", "warning", "info" 或 "ongoing"）
    :param color: 可选颜色名称
    :param multi_line: 启用多行通知

    注意：您可以根据 `Quasar 的 Notify API <https://quasar.dev/quasar-plugins/notify#notify-api>`_ 传递其他关键字参数。
    """
    options = {ARG_MAP.get(key, key): value for key, value in locals().items() if key != 'kwargs' and value is not None}
    options['message'] = str(message)
    options.update(kwargs)
    client = context.client
    client.outbox.enqueue_message('notify', options, client.id)
