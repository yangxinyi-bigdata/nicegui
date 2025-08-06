from typing import Dict, Optional

from .mixins.content_element import ContentElement


class Mermaid(ContentElement,
              component='mermaid.js',
              dependencies=[
                  'lib/mermaid/mermaid.esm.min.mjs',
                  'lib/mermaid/chunks/mermaid.esm.min/*.mjs',
              ]):
    CONTENT_PROP = 'content'

    def __init__(self, content: str, config: Optional[Dict] = None) -> None:
        """Mermaid图表

        渲染用Markdown启发的`Mermaid <https://mermaid.js.org/>`_语言编写的图表和图形。
        Mermaid语法也可以在Markdown元素内部使用，通过向``ui.markdown``元素提供扩展字符串'mermaid'。

        可选的配置字典在第一个图表渲染之前直接传递给mermaid。
        这可用于设置以下选项：

            ``{'securityLevel': 'loose', ...}`` - 允许在点击节点时运行JavaScript
            ``{'logLevel': 'info', ...}`` - 将调试信息记录到控制台

        有关完整选项列表，请参考Mermaid文档中的``mermaid.initialize()``方法。

        :param content: 要显示的Mermaid内容
        :param config: 要传递给``mermaid.initialize()``的配置字典
        """
        super().__init__(content=content)
        self._props['config'] = config

    def _handle_content_change(self, content: str) -> None:
        self._props[self.CONTENT_PROP] = content.strip()
        self.run_method('update', content.strip())
