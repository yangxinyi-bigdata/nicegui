import html
from typing import List, Optional, Union

from .html import Html
from .mixins.label_element import LabelElement


class ChatMessage(LabelElement):

    def __init__(self,
                 text: Union[str, List[str]] = ..., *,  # type: ignore
                 name: Optional[str] = None,
                 label: Optional[str] = None,
                 stamp: Optional[str] = None,
                 avatar: Optional[str] = None,
                 sent: bool = False,
                 text_html: bool = False,
                 ) -> None:
        """聊天消息

        基于Quasar的`聊天消息 <https://quasar.dev/vue-components/chat/>`_组件。

        :param text: 消息正文（可以是字符串列表，用于多个消息部分）
        :param name: 消息作者的名字
        :param label: 仅渲染标签标题/部分
        :param stamp: 消息的时间戳
        :param avatar: 头像的URL
        :param sent: 渲染为已发送消息（即来自当前用户）（默认：False）
        :param text_html: 将文本渲染为HTML（默认：False）
        """
        super().__init__(tag='q-chat-message', label=label)

        if text is ...:
            text = []
        if isinstance(text, str):
            text = [text]
        if not text_html:
            text = [html.escape(part) for part in text]
            text = [part.replace('\n', '<br />') for part in text]

        if name is not None:
            self._props['name'] = name
        if stamp is not None:
            self._props['stamp'] = stamp
        if avatar is not None:
            self._props['avatar'] = avatar
        self._props['sent'] = sent

        with self:
            for line in text:
                Html(line)
