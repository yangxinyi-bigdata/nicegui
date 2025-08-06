import importlib.util
from typing import TYPE_CHECKING, Any, Dict, List, Literal, Optional, Tuple, Union

from typing_extensions import Self

from .. import optional_features
from ..element import Element
from ..events import (
    GenericEventArguments,
    Handler,
    TableSelectionEventArguments,
    ValueChangeEventArguments,
    handle_event,
)
from ..helpers import warn_once
from .mixins.filter_element import FilterElement

if importlib.util.find_spec('pandas'):
    optional_features.register('pandas')
    if TYPE_CHECKING:
        import pandas as pd

if importlib.util.find_spec('polars'):
    optional_features.register('polars')
    if TYPE_CHECKING:
        import polars as pl


class Table(FilterElement, component='table.js'):

    def __init__(self,
                 *,
                 rows: List[Dict],
                 columns: Optional[List[Dict]] = None,
                 column_defaults: Optional[Dict] = None,
                 row_key: str = 'id',
                 title: Optional[str] = None,
                 selection: Literal[None, 'single', 'multiple'] = None,
                 pagination: Optional[Union[int, dict]] = None,
                 on_select: Optional[Handler[TableSelectionEventArguments]] = None,
                 on_pagination_change: Optional[Handler[ValueChangeEventArguments]] = None,
                 ) -> None:
        """表格

        基于Quasar的`QTable <https://quasar.dev/vue-components/table>`_组件的表格。

        :param rows: 行对象列表
        :param columns: 列对象列表（默认为第一行的列 *自2.0.0版本起*）
        :param column_defaults: 可选的默认列属性，*2.0.0版本添加*
        :param row_key: 包含标识行的唯一数据的列名（默认："id"）
        :param title: 表格标题
        :param selection: 选择类型（"single"或"multiple"；默认：`None`）
        :param pagination: 对应分页对象的字典或每页行数（`None`隐藏分页，0表示"无限"；默认：`None`）
        :param on_select: 选择更改时调用的回调函数
        :param on_pagination_change: 分页更改时调用的回调函数

        如果选择为'single'或'multiple'，则可以访问包含选定行的`selected`属性。
        """
        super().__init__()

        if columns is None:
            first_row = rows[0] if rows else {}
            columns = [{'name': key, 'label': str(key).upper(), 'field': key, 'sortable': True} for key in first_row]

        self._column_defaults = column_defaults
        self._use_columns_from_df = False
        self._props['columns'] = self._normalize_columns(columns)
        self._props['rows'] = rows
        self._props['row-key'] = row_key
        self._props['title'] = title
        self._props['hide-pagination'] = pagination is None
        self._props['pagination'] = pagination if isinstance(pagination, dict) else {'rowsPerPage': pagination or 0}
        self._props['selection'] = selection or 'none'
        self._props['selected'] = []
        self._props['fullscreen'] = False
        self._selection_handlers = [on_select] if on_select else []
        self._pagination_change_handlers = [on_pagination_change] if on_pagination_change else []

        def handle_selection(e: GenericEventArguments) -> None:
            if e.args['added']:
                if self.selection == 'single':
                    self.selected.clear()
                self.selected.extend(e.args['rows'])
            else:
                self.selected = [row for row in self.selected if row[self.row_key] not in e.args['keys']]
            self.update()
            arguments = TableSelectionEventArguments(sender=self, client=self.client, selection=self.selected)
            for handler in self._selection_handlers:
                handle_event(handler, arguments)
        self.on('selection', handle_selection, ['added', 'rows', 'keys'])

        def handle_pagination_change(e: GenericEventArguments) -> None:
            self.pagination = e.args
            self.update()
            arguments = ValueChangeEventArguments(sender=self, client=self.client, value=self.pagination)
            for handler in self._pagination_change_handlers:
                handle_event(handler, arguments)
        self.on('update:pagination', handle_pagination_change)

    def on_select(self, callback: Handler[TableSelectionEventArguments]) -> Self:
        """添加一个在选择更改时调用的回调函数。"""
        self._selection_handlers.append(callback)
        return self

    def on_pagination_change(self, callback: Handler[ValueChangeEventArguments]) -> Self:
        """添加一个在分页更改时调用的回调函数。"""
        self._pagination_change_handlers.append(callback)
        return self

    def _normalize_columns(self, columns: List[Dict]) -> List[Dict]:
        return [{**self._column_defaults, **column} for column in columns] if self._column_defaults else columns

    @classmethod
    def from_pandas(cls,
                    df: 'pd.DataFrame', *,
                    columns: Optional[List[Dict]] = None,
                    column_defaults: Optional[Dict] = None,
                    row_key: str = 'id',
                    title: Optional[str] = None,
                    selection: Optional[Literal['single', 'multiple']] = None,
                    pagination: Optional[Union[int, dict]] = None,
                    on_select: Optional[Handler[TableSelectionEventArguments]] = None) -> Self:
        """从Pandas DataFrame创建表格。

        注意：
        如果DataFrame包含`datetime64[ns]`、`timedelta64[ns]`、`complex128`或`period[M]`类型的不可序列化列，
        它们将被转换为字符串。
        要使用不同的转换，请在将DataFrame传递给此方法之前手动转换。
        有关更多信息，请参阅`issue 1698 <https://github.com/zauberzeug/nicegui/issues/1698>`_。

        *2.0.0版本添加*

        :param df: Pandas DataFrame
        :param columns: 列对象列表（默认为dataframe的列）
        :param column_defaults: 可选的默认列属性
        :param row_key: 包含标识行的唯一数据的列名（默认："id"）
        :param title: 表格标题
        :param selection: 选择类型（"single"或"multiple"；默认：`None`）
        :param pagination: 对应分页对象的字典或每页行数（`None`隐藏分页，0表示"无限"；默认：`None`）
        :param on_select: 选择更改时调用的回调函数
        :return: 表格元素
        """
        rows, columns_from_df = cls._pandas_df_to_rows_and_columns(df)
        table = cls(
            rows=rows,
            columns=columns or columns_from_df,
            column_defaults=column_defaults,
            row_key=row_key,
            title=title,
            selection=selection,
            pagination=pagination,
            on_select=on_select,
        )
        table._use_columns_from_df = columns is None
        return table

    @classmethod
    def from_polars(cls,
                    df: 'pl.DataFrame', *,
                    columns: Optional[List[Dict]] = None,
                    column_defaults: Optional[Dict] = None,
                    row_key: str = 'id',
                    title: Optional[str] = None,
                    selection: Optional[Literal['single', 'multiple']] = None,
                    pagination: Optional[Union[int, dict]] = None,
                    on_select: Optional[Handler[TableSelectionEventArguments]] = None) -> Self:
        """从Polars DataFrame创建表格。

        注意：
        如果DataFrame包含非UTF-8数据类型，它们将被转换为字符串。
        要使用不同的转换，请在将DataFrame传递给此方法之前手动转换。

        *2.7.0版本添加*

        :param df: Polars DataFrame
        :param columns: 列对象列表（默认为dataframe的列）
        :param column_defaults: 可选的默认列属性
        :param row_key: 包含标识行的唯一数据的列名（默认："id"）
        :param title: 表格标题
        :param selection: 选择类型（"single"或"multiple"；默认：`None`）
        :param pagination: 对应分页对象的字典或每页行数（`None`隐藏分页，0表示"无限"；默认：`None`）
        :param on_select: 选择更改时调用的回调函数
        :return: 表格元素
        """
        rows, columns_from_df = cls._polars_df_to_rows_and_columns(df)
        table = cls(
            rows=rows,
            columns=columns or columns_from_df,
            column_defaults=column_defaults,
            row_key=row_key,
            title=title,
            selection=selection,
            pagination=pagination,
            on_select=on_select,
        )
        table._use_columns_from_df = columns is None
        return table

    def update_from_pandas(self,
                           df: 'pd.DataFrame', *,
                           clear_selection: bool = True,
                           columns: Optional[List[Dict]] = None,
                           column_defaults: Optional[Dict] = None) -> None:
        """从Pandas DataFrame更新表格。

        有关不可序列化列转换的更多信息，请参阅`from_pandas()`。

        如果未提供`columns`且列是从DataFrame推断的，
        则列将更新以匹配新的DataFrame。

        :param df: Pandas DataFrame
        :param clear_selection: 是否清除选择（默认：True）
        :param columns: 列对象列表（默认为dataframe的列）
        :param column_defaults: 可选的默认列属性
        """
        rows, columns_from_df = self._pandas_df_to_rows_and_columns(df)
        self._update_table(rows, columns_from_df, clear_selection, columns, column_defaults)

    def update_from_polars(self,
                           df: 'pl.DataFrame', *,
                           clear_selection: bool = True,
                           columns: Optional[List[Dict]] = None,
                           column_defaults: Optional[Dict] = None) -> None:
        """从Polars DataFrame更新表格。

        :param df: Polars DataFrame
        :param clear_selection: 是否清除选择（默认：True）
        :param columns: 列对象列表（默认为dataframe的列）
        :param column_defaults: 可选的默认列属性
        """
        rows, columns_from_df = self._polars_df_to_rows_and_columns(df)
        self._update_table(rows, columns_from_df, clear_selection, columns, column_defaults)

    def _update_table(self,
                      rows: List[Dict],
                      columns_from_df: List[Dict],
                      clear_selection: bool,
                      columns: Optional[List[Dict]],
                      column_defaults: Optional[Dict]) -> None:
        """更新表格的辅助函数。"""
        self.rows[:] = rows
        if column_defaults is not None:
            self._column_defaults = column_defaults
        if columns or self._use_columns_from_df:
            self.columns[:] = self._normalize_columns(columns or columns_from_df)
        if clear_selection:
            self.selected.clear()
        self.update()

    @staticmethod
    def _pandas_df_to_rows_and_columns(df: 'pd.DataFrame') -> Tuple[List[Dict], List[Dict]]:
        import pandas as pd  # pylint: disable=import-outside-toplevel

        def is_special_dtype(dtype):
            return (pd.api.types.is_datetime64_any_dtype(dtype) or
                    pd.api.types.is_timedelta64_dtype(dtype) or
                    pd.api.types.is_complex_dtype(dtype) or
                    pd.api.types.is_object_dtype(dtype) or
                    isinstance(dtype, (pd.PeriodDtype, pd.IntervalDtype)))
        special_cols = df.columns[df.dtypes.apply(is_special_dtype)]
        if not special_cols.empty:
            df = df.copy()
            df[special_cols] = df[special_cols].astype(str)

        if isinstance(df.columns, pd.MultiIndex):
            raise ValueError('MultiIndex columns are not supported. '
                             'You can convert them to strings using something like '
                             '`df.columns = ["_".join(col) for col in df.columns.values]`.')

        return df.to_dict('records'), [{'name': col, 'label': col, 'field': col} for col in df.columns]

    @staticmethod
    def _polars_df_to_rows_and_columns(df: 'pl.DataFrame') -> Tuple[List[Dict], List[Dict]]:
        return df.to_dicts(), [{'name': col, 'label': col, 'field': col} for col in df.columns]

    @property
    def rows(self) -> List[Dict]:
        """行列表。"""
        return self._props['rows']

    @rows.setter
    def rows(self, value: List[Dict]) -> None:
        self._props['rows'] = value
        self.update()

    @property
    def columns(self) -> List[Dict]:
        """列列表。"""
        return self._props['columns']

    @columns.setter
    def columns(self, value: List[Dict]) -> None:
        self._props['columns'] = self._normalize_columns(value)
        self.update()

    @property
    def column_defaults(self) -> Optional[Dict]:
        """默认列属性。"""
        return self._column_defaults

    @column_defaults.setter
    def column_defaults(self, value: Optional[Dict]) -> None:
        self._column_defaults = value
        self.columns = self.columns  # re-normalize columns

    @property
    def row_key(self) -> str:
        """包含标识行的唯一数据的列名。"""
        return self._props['row-key']

    @row_key.setter
    def row_key(self, value: str) -> None:
        self._props['row-key'] = value
        self.update()

    @property
    def selected(self) -> List[Dict]:
        """选中的行列表。"""
        return self._props['selected']

    @selected.setter
    def selected(self, value: List[Dict]) -> None:
        self._props['selected'] = value
        self.update()

    @property
    def selection(self) -> Literal[None, 'single', 'multiple']:
        """选择类型。

        *2.11.0版本添加*
        """
        return None if self._props['selection'] == 'none' else self._props['selection']

    @selection.setter
    def selection(self, value: Literal[None, 'single', 'multiple']) -> None:
        self._props['selection'] = value or 'none'
        self.update()

    def set_selection(self, value: Literal[None, 'single', 'multiple']) -> None:
        """设置选择类型。

        *2.11.0版本添加*
        """
        self.selection = value

    @property
    def pagination(self) -> dict:
        """分页对象。"""
        return self._props['pagination']

    @pagination.setter
    def pagination(self, value: dict) -> None:
        self._props['pagination'] = value
        self.update()

    @property
    def is_fullscreen(self) -> bool:
        """表格是否处于全屏模式。"""
        return self._props['fullscreen']

    @is_fullscreen.setter
    def is_fullscreen(self, value: bool) -> None:
        """设置全屏模式。"""
        self._props['fullscreen'] = value
        self.update()

    def set_fullscreen(self, value: bool) -> None:
        """Set fullscreen mode."""
        self.is_fullscreen = value

    def toggle_fullscreen(self) -> None:
        """切换全屏模式。"""
        self.is_fullscreen = not self.is_fullscreen

    def add_rows(self, rows: List[Dict], *args: Any) -> None:
        """向表格添加行。"""
        if isinstance(rows, dict):  # DEPRECATED
            warn_once('Calling add_rows() with variable-length arguments is deprecated. '
                      'This option will be removed in NiceGUI 3.0. '
                      'Pass a list instead or use add_row() for a single row.')
            rows = [rows, *args]
        self.rows.extend(rows)
        self.update()

    def add_row(self, row: Dict) -> None:
        """向表格添加单行。"""
        self.add_rows([row])

    def remove_rows(self, rows: List[Dict], *args: Any) -> None:
        """从表格中移除行。"""
        if isinstance(rows, dict):  # DEPRECATED
            warn_once('Calling remove_rows() with variable-length arguments is deprecated. '
                      'This option will be removed in NiceGUI 3.0. '
                      'Pass a list instead or use remove_row() for a single row.')
            rows = [rows, *args]
        keys = [row[self.row_key] for row in rows]
        self.rows[:] = [row for row in self.rows if row[self.row_key] not in keys]
        self.selected[:] = [row for row in self.selected if row[self.row_key] not in keys]
        self.update()

    def remove_row(self, row: Dict) -> None:
        """从表格中移除单行。"""
        self.remove_rows([row])

    def update_rows(self, rows: List[Dict], *, clear_selection: bool = True) -> None:
        """更新表格中的行。

        :param rows: 要更新的行列表
        :param clear_selection: 是否清除选择（默认：True）
        """
        self.rows[:] = rows
        if clear_selection:
            self.selected.clear()
        self.update()

    async def get_filtered_sorted_rows(self, *, timeout: float = 1) -> List[Dict]:
        """异步返回表格的过滤和排序后的行。"""
        return await self.get_computed_prop('filteredSortedRows', timeout=timeout)

    async def get_computed_rows(self, *, timeout: float = 1) -> List[Dict]:
        """异步返回表格的计算行。"""
        return await self.get_computed_prop('computedRows', timeout=timeout)

    async def get_computed_rows_number(self, *, timeout: float = 1) -> int:
        """异步返回表格的计算行数。"""
        return await self.get_computed_prop('computedRowsNumber', timeout=timeout)

    class row(Element):

        def __init__(self) -> None:
            """行元素

            此元素基于Quasar的`QTr <https://quasar.dev/vue-components/table#qtr-api>`_组件。
            """
            super().__init__('q-tr')

    class header(Element):

        def __init__(self) -> None:
            """表头元素

            此元素基于Quasar的`QTh <https://quasar.dev/vue-components/table#qth-api>`_组件。
            """
            super().__init__('q-th')

    class cell(Element):

        def __init__(self) -> None:
            """单元格元素

            此元素基于Quasar的`QTd <https://quasar.dev/vue-components/table#qtd-api>`_组件。
            """
            super().__init__('q-td')
