from typing import Optional, Union

from ..element import Element


class Grid(Element, default_classes='nicegui-grid'):

    def __init__(self,
                 *,
                 rows: Optional[Union[int, str]] = None,
                 columns: Optional[Union[int, str]] = None,
                 ) -> None:
        """网格元素

        提供一个将其子元素排列在网格中的容器。

        :param rows: 网格中的行数或带有grid-template-rows CSS属性的字符串（例如'auto 1fr'）
        :param columns: 网格中的列数或带有grid-template-columns CSS属性的字符串（例如'auto 1fr'）
        """
        super().__init__('div')

        if isinstance(rows, int):
            self._style['grid-template-rows'] = f'repeat({rows}, minmax(0, 1fr))'
        elif isinstance(rows, str):
            self._style['grid-template-rows'] = rows

        if isinstance(columns, int):
            self._style['grid-template-columns'] = f'repeat({columns}, minmax(0, 1fr))'
        elif isinstance(columns, str):
            self._style['grid-template-columns'] = columns
