from nicegui import ui

from . import doc


@doc.demo(ui.json_editor)
def main_demo() -> None:
    json = {
        'array': [1, 2, 3],
        'boolean': True,
        'color': '#82b92c',
        None: None,
        'number': 123,
        'object': {
            'a': 'b',
            'c': 'd',
        },
        'time': 1575599819000,
        'string': 'Hello World',
    }
    ui.json_editor({'content': {'json': json}},
                   on_select=lambda e: ui.notify(f'Select: {e}'),
                   on_change=lambda e: ui.notify(f'Change: {e}'))


@doc.demo('验证', '''
    您可以使用 `schema` 参数定义 [JSON schema](https://json-schema.org/) 来验证正在编辑的数据。
    在此演示中，如果数据与模式不匹配，编辑器将发出警告：

    - `id` 必须是整数
    - `name` 必须是字符串
    - `price` 必须是大于 0 的数字

    *在版本 2.8.0 中添加*
''')
def schema_demo() -> None:
    schema = {
        'type': 'object',
        'properties': {
            'id': {
                'type': 'integer',
            },
            'name': {
                'type': 'string',
            },
            'price': {
                'type': 'number',
                'exclusiveMinimum': 0,
            },
        },
        'required': ['id', 'name', 'price'],
    }
    data = {
        'id': 42,
        'name': 'Banana',
        'price': 15.0,
    }
    ui.json_editor({'content': {'json': data}}, schema=schema)


@doc.demo('运行方法', '''
    您可以使用 `run_editor_method` 方法运行 JSONEditor 实例的方法。
    此演示展示如何展开和折叠所有节点以及如何获取当前数据。

    方法名称 "expand" 前面的冒号 ":" 表示值 "path => true" 是一个 JavaScript 表达式，
    该表达式在传递给方法之前在客户端上求值。

    请注意，从客户端请求数据仅支持页面函数，不支持共享的自动索引页面。
''')
def methods_demo() -> None:
    # @ui.page('/')
    def page():
        json = {
            'Name': 'Alice',
            'Age': 42,
            'Address': {
                'Street': 'Main Street',
                'City': 'Wonderland',
            },
        }
        editor = ui.json_editor({'content': {'json': json}})

        ui.button('Expand', on_click=lambda: editor.run_editor_method(':expand', 'path => true'))
        ui.button('Collapse', on_click=lambda: editor.run_editor_method(':expand', 'path => false'))
        ui.button('Readonly', on_click=lambda: editor.run_editor_method('updateProps', {'readOnly': True}))

        async def get_data() -> None:
            data = await editor.run_editor_method('get')
            ui.notify(data)
        ui.button('Get Data', on_click=get_data)
    page()  # HIDE


doc.reference(ui.json_editor)
