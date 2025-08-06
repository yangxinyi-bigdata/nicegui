import importlib.util
from typing import TYPE_CHECKING, Dict, List, Literal, Optional, cast

from typing_extensions import Self

from .. import helpers, optional_features
from ..awaitable_response import AwaitableResponse
from ..element import Element

if importlib.util.find_spec('pandas'):
    optional_features.register('pandas')
    if TYPE_CHECKING:
        import pandas as pd

if importlib.util.find_spec('polars'):
    optional_features.register('polars')
    if TYPE_CHECKING:
        import polars as pl


class AgGrid(Element,
             component='aggrid.js',
             dependencies=['lib/aggrid/ag-grid-community.min.js'],
             default_classes='nicegui-aggrid'):

    def __init__(self,
                 options: Dict, *,
                 html_columns: List[int] = [],  # noqa: B006
                 theme: Optional[str] = 'balham',
                 auto_size_columns: bool = True,
                 ) -> None:
        """AG表格

        一个使用`AG Grid <https://www.ag-grid.com/>`_创建表格的元素。

        可以使用``run_grid_method``和``run_row_method``方法与客户端的AG Grid实例进行交互。

        :param options: AG Grid选项字典
        :param html_columns: 应该渲染为HTML的列列表（默认：``[]``）
        :param theme: AG Grid主题（默认："balham"）
        :param auto_size_columns: 是否自动调整列大小以适应表格宽度（默认：``True``）
        """
        super().__init__()
        self._props['options'] = options
        self._props['html_columns'] = html_columns[:]
        self._props['auto_size_columns'] = auto_size_columns
        if theme:
            self._classes.append(f'ag-theme-{theme}')
        self._update_method = 'update_grid'

    @classmethod
    def from_pandas(cls,
                    df: 'pd.DataFrame', *,
                    html_columns: List[int] = [],  # noqa: B006
                    theme: Optional[str] = 'balham',
                    auto_size_columns: bool = True,
                    options: Dict = {}) -> Self:  # noqa: B006
        """从Pandas DataFrame创建AG表格。

        注意：
        如果DataFrame包含不可序列化的列，类型为``datetime64[ns]``、``timedelta64[ns]``、``complex128``或``period[M]``，
        它们将被转换为字符串。
        要使用不同的转换，请在将DataFrame传递给此方法之前手动转换。
        有关更多信息，请参见`issue 1698 <https://github.com/zauberzeug/nicegui/issues/1698>`_。

        :param df: Pandas DataFrame
        :param html_columns: 应该渲染为HTML的列列表（默认：``[]``，*在版本2.19.0中添加*）
        :param theme: AG Grid主题（默认："balham"）
        :param auto_size_columns: 是否自动调整列大小以适应表格宽度（默认：``True``）
        :param options: 额外的AG Grid选项字典
        :return: AG表格元素
        """
        import pandas as pd  # pylint: disable=import-outside-toplevel

        def is_special_dtype(dtype):
            return (pd.api.types.is_datetime64_any_dtype(dtype) or
                    pd.api.types.is_timedelta64_dtype(dtype) or
                    pd.api.types.is_complex_dtype(dtype) or
                    isinstance(dtype, pd.PeriodDtype))
        special_cols = df.columns[df.dtypes.apply(is_special_dtype)]
        if not special_cols.empty:
            df = df.copy()
            df[special_cols] = df[special_cols].astype(str)

        if isinstance(df.columns, pd.MultiIndex):
            raise ValueError('MultiIndex columns are not supported. '
                             'You can convert them to strings using something like '
                             '`df.columns = ["_".join(col) for col in df.columns.values]`.')

        return cls({
            'columnDefs': [{'field': str(col)} for col in df.columns],
            'rowData': df.to_dict('records'),
            'suppressFieldDotNotation': True,
            **options,
        }, html_columns=html_columns, theme=theme, auto_size_columns=auto_size_columns)

    @classmethod
    def from_polars(cls,
                    df: 'pl.DataFrame', *,
                    html_columns: List[int] = [],  # noqa: B006
                    theme: Optional[str] = 'balham',
                    auto_size_columns: bool = True,
                    options: Dict = {}) -> Self:  # noqa: B006
        """从Polars DataFrame创建AG表格。

        如果DataFrame包含非UTF-8数据类型，它们将被转换为字符串。
        要使用不同的转换，请在将DataFrame传递给此方法之前手动转换。

        *在版本2.7.0中添加*

        :param df: Polars DataFrame
        :param html_columns: 应该渲染为HTML的列列表（默认：``[]``，*在版本2.19.0中添加*）
        :param theme: AG Grid主题（默认："balham"）
        :param auto_size_columns: 是否自动调整列大小以适应表格宽度（默认：``True``）
        :param options: 额外的AG Grid选项字典
        :return: AG表格元素
        """
        return cls({
            'columnDefs': [{'field': str(col)} for col in df.columns],
            'rowData': df.to_dicts(),
            'suppressFieldDotNotation': True,
            **options,
        }, html_columns=html_columns, theme=theme, auto_size_columns=auto_size_columns)

    @property
    def options(self) -> Dict:
        """选项字典。"""
        return self._props['options']

    @options.setter
    def options(self, value: Dict) -> None:
        self._props['options'] = value
        self.update()

    @property
    def html_columns(self) -> List[int]:
        """应该渲染为HTML的列列表。"""
        return self._props['html_columns']

    @html_columns.setter
    def html_columns(self, value: List[int]) -> None:
        self._props['html_columns'] = value[:]
        self.update()

    @property
    def theme(self) -> Optional[str]:
        """AG Grid主题。"""
        for class_name in self._classes:
            if class_name.startswith('ag-theme-'):
                return class_name[len('ag-theme-'):]
        return None

    @theme.setter
    def theme(self, value: Optional[str]) -> None:
        for class_name in self._classes:
            if class_name.startswith('ag-theme-'):
                self._classes.remove(class_name)
        if value:
            self._classes.append(f'ag-theme-{value}')
        self.update()

    @property
    def auto_size_columns(self) -> bool:
        """是否自动调整列大小以适应表格宽度。"""
        return self._props['auto_size_columns']

    @auto_size_columns.setter
    def auto_size_columns(self, value: bool) -> None:
        self._props['auto_size_columns'] = value
        self.update()

    def run_grid_method(self, name: str, *args, timeout: float = 1) -> AwaitableResponse:
        """运行AG Grid API方法。

        有关方法列表，请参见`AG Grid API <https://www.ag-grid.com/javascript-data-grid/grid-api/>`_。

        如果函数被等待，则返回方法调用的结果。
        否则，方法将在不等待响应的情况下执行。

        :param name: 方法名称
        :param args: 传递给方法的参数
        :param timeout: 超时时间（秒）（默认：1秒）

        :return: 可以等待以获取方法调用结果的AwaitableResponse
        """
        return self.run_method('run_grid_method', name, *args, timeout=timeout)

    def run_column_method(self, name: str, *args, timeout: float = 1) -> AwaitableResponse:  # DEPRECATED
        """此方法已弃用。请使用`run_grid_method`代替。

        有关更多信息，请参见 https://www.ag-grid.com/javascript-data-grid/column-api/
        """
        helpers.warn_once('The method `run_column_method` is deprecated. '
                          'It will be removed in NiceGUI 3.0. '
                          'Use `run_grid_method` instead.')
        return self.run_method('run_grid_method', name, *args, timeout=timeout)

    def run_row_method(self, row_id: str, name: str, *args, timeout: float = 1) -> AwaitableResponse:
        """在特定行上运行AG Grid API方法。

        有关方法列表，请参见`AG Grid行引用 <https://www.ag-grid.com/javascript-data-grid/row-object/>`_。

        如果函数被等待，则返回方法调用的结果。
        否则，方法将在不等待响应的情况下执行。

        :param row_id: 行的ID（由``getRowId``选项定义）
        :param name: 方法名称
        :param args: 传递给方法的参数
        :param timeout: 超时时间（秒）（默认：1秒）

        :return: 可以等待以获取方法调用结果的AwaitableResponse
        """
        return self.run_method('run_row_method', row_id, name, *args, timeout=timeout)

    async def get_selected_rows(self) -> List[Dict]:
        """获取当前选中的行。

        当表格配置为``rowSelection: 'multiple'``时，此方法特别有用。

        有关更多信息，请参见`AG Grid API <https://www.ag-grid.com/javascript-data-grid/row-selection/#reference-selection-getSelectedRows>`_。

        :return: 选中的行数据列表
        """
        result = await self.run_grid_method('getSelectedRows')
        return cast(List[Dict], result)

    async def get_selected_row(self) -> Optional[Dict]:
        """获取单个当前选中的行。

        当表格配置为``rowSelection: 'single'``时，此方法特别有用。

        :return: 如果有行被选中，则返回第一个选中的行数据，否则返回`None`
        """
        rows = await self.get_selected_rows()
        return rows[0] if rows else None

    async def get_client_data(
        self,
        *,
        timeout: float = 1,
        method: Literal['all_unsorted', 'filtered_unsorted', 'filtered_sorted', 'leaf'] = 'all_unsorted'
    ) -> List[Dict]:
        """从客户端获取数据，包括客户端所做的任何编辑。

        当表格配置为``'editable': True``时，此方法特别有用。

        有关更多信息，请参见`AG Grid API <https://www.ag-grid.com/javascript-data-grid/accessing-data/>`_。

        请注意，当编辑单元格时，行数据不会更新，直到单元格退出编辑模式。
        当单元格失去焦点时，这不会发生，除非设置了``stopEditingWhenCellsLoseFocus: True``。

        :param timeout: 超时时间（秒）（默认：1秒）
        :param method: 访问数据的方法，"all_unsorted"（默认）、"filtered_unsorted"、"filtered_sorted"、"leaf"

        :return: 行数据列表
        """
        API_METHODS = {
            'all_unsorted': 'forEachNode',
            'filtered_unsorted': 'forEachNodeAfterFilter',
            'filtered_sorted': 'forEachNodeAfterFilterAndSort',
            'leaf': 'forEachLeafNode',
        }
        result = await self.client.run_javascript(f'''
            const rowData = [];
            getElement({self.id}).api.{API_METHODS[method]}(node => rowData.push(node.data));
            return rowData;
        ''', timeout=timeout)
        return cast(List[Dict], result)

    async def load_client_data(self) -> None:
        """获取客户端数据并用它更新元素的行数据。

        这会将客户端在可编辑单元格中所做的编辑同步到服务器。

        请注意，当编辑单元格时，行数据不会更新，直到单元格退出编辑模式。
        当单元格失去焦点时，这不会发生，除非设置了``stopEditingWhenCellsLoseFocus: True``。
        """
        client_row_data = await self.get_client_data()
        self.options['rowData'] = client_row_data
        self.update()
