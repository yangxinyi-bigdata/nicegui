from typing import Any, Optional

from ..element import Element
from .label import Label


class Log(Element, default_classes='nicegui-log'):

    def __init__(self, max_lines: Optional[int] = None) -> None:
        """日志视图

        创建一个日志视图，允许添加新行而无需将整个历史记录重新传输到客户端。

        :param max_lines: 删除最旧行之前的最大行数（默认：`None`）
        """
        super().__init__()
        self.max_lines = max_lines

    def push(self, line: Any, *,
             classes: Optional[str] = None,
             style: Optional[str] = None,
             props: Optional[str] = None) -> None:
        """向日志添加新行。

        :param line: 要添加的行（可以包含换行符）
        :param classes: 应用于行的类（*在版本2.18.0中添加*）
        :param style: 应用于行的样式（*在版本2.18.0中添加*）
        :param props: 应用于行的属性（*在版本2.18.0中添加*）
        """
        for text in str(line).splitlines():
            with self:
                label = Label(text)
                if classes is not None:
                    label.classes(replace=classes)
                if style is not None:
                    label.style(replace=style)
                if props is not None:
                    label.props.clear()
                    label.props(props)
        while self.max_lines is not None and len(self.default_slot.children) > self.max_lines:
            self.remove(0)
