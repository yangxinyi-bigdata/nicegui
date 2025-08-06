from typing import Union

from ..element import Element


class Teleport(Element, component='teleport.js'):

    def __init__(self, to: Union[str, Element]) -> None:
        """传送

        允许我们将内容从组件内传送到页面上任何位置的元素。

        :param to: 传送内容的目标元素的NiceGUI元素或CSS选择器
        """
        super().__init__()
        if isinstance(to, Element):
            to = f'#{to.html_id}'
        self._props['to'] = to
        self._update_method = 'update'
