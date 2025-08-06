from typing import Dict, Optional

from typing_extensions import Self

from ..awaitable_response import AwaitableResponse
from ..element import Element
from ..events import (
    GenericEventArguments,
    Handler,
    JsonEditorChangeEventArguments,
    JsonEditorSelectEventArguments,
    handle_event,
)


class JsonEditor(Element, component='json_editor.js', dependencies=['lib/vanilla-jsoneditor/standalone.js']):

    def __init__(self,
                 properties: Dict, *,
                 on_select: Optional[Handler[JsonEditorSelectEventArguments]] = None,
                 on_change: Optional[Handler[JsonEditorChangeEventArguments]] = None,
                 schema: Optional[Dict] = None,
                 ) -> None:
        """JSON编辑器

        使用`JSONEditor <https://github.com/josdejong/svelte-jsoneditor>`_创建JSON编辑器的元素。
        可以通过更改`properties`属性将更新推送到编辑器。
        数据更改后，调用`update`方法刷新编辑器。

        :param properties: JSONEditor属性字典
        :param on_select: 当部分内容被选中时调用的回调函数
        :param on_change: 当内容更改时调用的回调函数
        :param schema: 用于验证正在编辑的数据的可选`JSON schema <https://json-schema.org/>`_（*在版本2.8.0中添加*）
        """
        super().__init__()
        self._props['properties'] = properties
        self._update_method = 'update_editor'

        if schema:
            self._props['schema'] = schema

        if on_select:
            self.on_select(on_select)

        if on_change:
            self.on_change(on_change)

    def on_change(self, callback: Handler[JsonEditorChangeEventArguments]) -> Self:
        """添加内容更改时要调用的回调函数。"""
        def handle_on_change(e: GenericEventArguments) -> None:
            handle_event(callback, JsonEditorChangeEventArguments(sender=self, client=self.client, **e.args))
        self.on('content_change', handle_on_change, ['content', 'errors'])
        return self

    def on_select(self, callback: Handler[JsonEditorSelectEventArguments]) -> Self:
        """添加部分内容被选中时要调用的回调函数。"""
        def handle_on_select(e: GenericEventArguments) -> None:
            handle_event(callback, JsonEditorSelectEventArguments(sender=self, client=self.client, **e.args))
        self.on('content_select', handle_on_select, ['selection'])
        return self

    @property
    def properties(self) -> Dict:
        """属性字典。"""
        return self._props['properties']

    def run_editor_method(self, name: str, *args, timeout: float = 1) -> AwaitableResponse:
        """运行JSONEditor实例的方法。

        有关方法列表，请参见`JSONEditor README <https://github.com/josdejong/svelte-jsoneditor/>`_。

        如果函数被等待，则返回方法调用的结果。
        否则，方法会在不等待响应的情况下执行。

        :param name: 方法名称（前缀":"表示参数是JavaScript表达式）
        :param args: 传递给方法的参数（Python对象或JavaScript表达式）
        :param timeout: 超时时间（秒）（默认：1秒）

        :return: 可以等待以获取方法调用结果的AwaitableResponse
        """
        return self.run_method('run_editor_method', name, *args, timeout=timeout)
