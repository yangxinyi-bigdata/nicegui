import asyncio
import time
from typing import Optional

from .. import json
from .button import Button as button
from .markdown import Markdown as markdown
from .markdown import remove_indentation
from .mixins.content_element import ContentElement
from .timer import Timer as timer


class Code(ContentElement, component='code.js', default_classes='nicegui-code'):

    def __init__(self, content: str = '', *, language: Optional[str] = 'python') -> None:
        """代码显示

        此元素显示带有语法高亮的代码块。

        在安全环境（HTTPS或localhost）中，会显示一个复制按钮用于将代码复制到剪贴板。

        :param content: 要显示的代码
        :param language: 代码语言（默认："python"）
        """
        super().__init__(content=remove_indentation(content))

        with self:
            self.markdown = markdown().classes('overflow-auto h-full') \
                .bind_content_from(self, 'content', lambda content: f'```{language}\n{content}\n```')
            self.copy_button = button(icon='content_copy', on_click=self.show_checkmark) \
                .props('round flat size=sm').classes('absolute right-2 top-2 opacity-20 hover:opacity-80') \
                .on('click', js_handler=f'() => navigator.clipboard.writeText({json.dumps(self.content)})')

        self._last_scroll: float = 0.0
        self.markdown.on('scroll', self._handle_scroll)
        with self:
            timer(0.1, self._update_copy_button)

    async def show_checkmark(self) -> None:
        """显示检查标记图标3秒钟。"""
        self.copy_button.props('icon=check')
        await asyncio.sleep(3.0)
        self.copy_button.props('icon=content_copy')

    def _handle_scroll(self) -> None:
        self._last_scroll = time.time()

    def _update_copy_button(self) -> None:
        self.copy_button.set_visibility(time.time() > self._last_scroll + 1.0)

    def _handle_content_change(self, content: str) -> None:
        pass  # handled by markdown element
