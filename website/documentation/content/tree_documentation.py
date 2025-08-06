from nicegui import ui

from . import doc


@doc.demo(ui.tree)
def main_demo() -> None:
    ui.tree([
        {'id': 'numbers', 'children': [{'id': '1'}, {'id': '2'}]},
        {'id': 'letters', 'children': [{'id': 'A'}, {'id': 'B'}]},
    ], label_key='id', on_select=lambda e: ui.notify(e.value))


@doc.demo('带自定义标题和正文的树', '''
    作用域插槽可用于向树节点的标题和正文插入自定义内容。
    更多信息请参见 [Quasar 文档](https://quasar.dev/vue-components/tree#customize-content)。
''')
def tree_with_custom_header_and_body():
    tree = ui.tree([
        {'id': 'numbers', 'description': 'Just some numbers', 'children': [
            {'id': '1', 'description': 'The first number'},
            {'id': '2', 'description': 'The second number'},
        ]},
        {'id': 'letters', 'description': 'Some latin letters', 'children': [
            {'id': 'A', 'description': 'The first letter'},
            {'id': 'B', 'description': 'The second letter'},
        ]},
    ], label_key='id', on_select=lambda e: ui.notify(e.value))

    tree.add_slot('default-header', '''
        <span :props="props">Node <strong>{{ props.node.id }}</strong></span>
    ''')
    tree.add_slot('default-body', '''
        <span :props="props">Description: "{{ props.node.description }}"</span>
    ''')


@doc.demo('带复选框的树', '''
    通过设置 "tick-strategy" 属性，可以将树与复选框一起使用。
''')
def tree_with_checkboxes():
    ui.tree([
        {'id': 'A', 'children': [{'id': 'A1'}, {'id': 'A2'}]},
        {'id': 'B', 'children': [{'id': 'B1'}, {'id': 'B2'}]},
    ], label_key='id', tick_strategy='leaf', on_tick=lambda e: ui.notify(e.value))


@doc.demo('编程方式展开/折叠', '''
    可以使用 `expand()` 和 `collapse()` 方法编程方式切换整个树或单个节点。
    即使节点被禁用（例如用户无法点击），这也有效。
''')
def expand_programmatically():
    t = ui.tree([
        {'id': 'A', 'children': [{'id': 'A1'}, {'id': 'A2'}], 'disabled': True},
        {'id': 'B', 'children': [{'id': 'B1'}, {'id': 'B2'}]},
    ], label_key='id').expand()

    with ui.row():
        ui.button('+ all', on_click=t.expand)
        ui.button('- all', on_click=t.collapse)
        ui.button('+ A', on_click=lambda: t.expand(['A']))
        ui.button('- A', on_click=lambda: t.collapse(['A']))


@doc.demo('Select/deselect programmatically', '''
    You can select or deselect nodes with the `select()` and `deselect()` methods.
''')
def select_programmatically():
    t = ui.tree([
        {'id': 'numbers', 'children': [{'id': '1'}, {'id': '2'}]},
        {'id': 'letters', 'children': [{'id': 'A'}, {'id': 'B'}]},
    ], label_key='id').expand()

    with ui.row():
        ui.button('Select A', on_click=lambda: t.select('A'))
        ui.button('Deselect A', on_click=t.deselect)


@doc.demo('Tick/untick programmatically', '''
    After setting a `tick_strategy`, you can tick or untick nodes with the `tick()` and `untick()` methods.
    You can either specify a list of node keys or `None` to tick or untick all nodes.
''')
def tick_programmatically():
    t = ui.tree([
        {'id': 'numbers', 'children': [{'id': '1'}, {'id': '2'}]},
        {'id': 'letters', 'children': [{'id': 'A'}, {'id': 'B'}]},
    ], label_key='id', tick_strategy='leaf').expand()

    with ui.row():
        ui.button('Tick 1, 2 and B', on_click=lambda: t.tick(['1', '2', 'B']))
        ui.button('Untick 2 and B', on_click=lambda: t.untick(['2', 'B']))
    with ui.row():
        ui.button('Tick all', on_click=t.tick)
        ui.button('Untick all', on_click=t.untick)


@doc.demo('Filter nodes', '''
    You can filter nodes by setting the `filter` property.
    The tree will only show nodes that match the filter.
''')
def filter_nodes():
    t = ui.tree([
        {'id': 'fruits', 'children': [{'id': 'Apple'}, {'id': 'Banana'}]},
        {'id': 'vegetables', 'children': [{'id': 'Potato'}, {'id': 'Tomato'}]},
    ], label_key='id').expand()
    ui.input('filter').bind_value_to(t, 'filter')


doc.reference(ui.tree)
