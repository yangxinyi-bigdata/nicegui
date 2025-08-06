from nicegui import ui

from . import doc

doc.title('通用事件')


@doc.demo('通用事件', '''
    大多数 UI 元素都带有预定义的事件。
    例如，演示中的 `ui.button`（如 "A"）有一个 `on_click` 参数，它期望一个协程或函数。
    但您也可以使用 `on` 方法来注册通用事件处理器，如 "B" 那样。
    这允许您为 JavaScript 和 Quasar 支持的任何事件注册处理器。

    例如，您可以为 `mousemove` 事件注册处理器，如 "C" 那样，即使 `ui.button` 没有 `on_mousemove` 参数。
    某些事件，如 `mousemove`，触发非常频繁。
    为避免性能问题，您可以使用 `throttle` 参数来每 `throttle` 秒只调用一次处理器（"D"）。

    通用事件处理器可以是同步或异步的，并可选择接受 `GenericEventArguments` 作为参数（"E"）。
    您还可以指定 JavaScript 或 Quasar 事件的哪些属性应该传递给处理器（"F"）。
    这可以减少需要在服务器和客户端之间传输的数据量。

    您可以在此找到有关支持的事件的更多信息：

    - <https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement#events> 用于 HTML 元素
    - <https://quasar.dev/vue-components> 用于基于 Quasar 的元素（参见各个组件页面上的 "Events" 选项卡）
''')
def generic_events_demo() -> None:
    with ui.row():
        ui.button('A', on_click=lambda: ui.notify('You clicked the button A.'))
        ui.button('B').on('click', lambda: ui.notify('You clicked the button B.'))
    with ui.row():
        ui.button('C').on('mousemove', lambda: ui.notify('You moved on button C.'))
        ui.button('D').on('mousemove', lambda: ui.notify('You moved on button D.'), throttle=0.5)
    with ui.row():
        ui.button('E').on('mousedown', lambda e: ui.notify(e))
        ui.button('F').on('mousedown', lambda e: ui.notify(e), ['ctrlKey', 'shiftKey'])


@doc.demo('指定事件属性', '''
    **字符串列表** 命名 JavaScript 事件对象的属性：
    ```py
    ui.button().on('click', handle_click, ['clientX', 'clientY'])
    ```

    **空列表** 请求_无_属性：
    ```py
    ui.button().on('click', handle_click, [])
    ```

    **值 `None`** 表示_所有_属性（默认）：
    ```py
    ui.button().on('click', handle_click, None)
    ```

    **如果事件使用多个参数调用** 如 QTable 的 "row-click" `(evt, row, index) => void`，
    您可以定义参数定义列表：
    ```py
    ui.table(...).on('rowClick', handle_click, [[], ['name'], None])
    ```
    在此示例中，"row-click" 事件将省略第一个 `evt` 参数的所有参数，
    只发送 `row` 参数的 "name" 属性并发送完整的 `index`。

    如果检索到的事件参数列表长度为 1，参数将自动解包。
    所以您可以写
    ```py
    ui.button().on('click', lambda e: print(e.args['clientX'], flush=True))
    ```
    而不是
    ```py
    ui.button().on('click', lambda e: print(e.args[0]['clientX'], flush=True))
    ```

    请注意，默认情况下发送所有参数的所有 JSON 可序列化属性。
    这是为了简化注册新事件和发现其属性。
    如果带宽是个问题，参数应该限制为服务器实际需要的。
''')
def event_attributes() -> None:
    columns = [
        {'name': 'name', 'label': 'Name', 'field': 'name'},
        {'name': 'age', 'label': 'Age', 'field': 'age'},
    ]
    rows = [
        {'name': 'Alice', 'age': 42},
        {'name': 'Bob', 'age': 23},
    ]
    ui.table(columns=columns, rows=rows, row_key='name') \
        .on('rowClick', ui.notify, [[], ['name'], None])


@doc.demo('修饰符', '''
    您还可以包含[按键修饰符](https://vuejs.org/guide/essentials/event-handling.html#key-modifiers>)（如输入框 "A" 所示），
    修饰符组合（如输入框 "B" 所示），
    和[事件修饰符](https://vuejs.org/guide/essentials/event-handling.html#mouse-button-modifiers>)（如输入框 "C" 所示）。
''')
def modifiers() -> None:
    with ui.row():
        ui.input('A').classes('w-12').on('keydown.space', lambda: ui.notify('You pressed space.'))
        ui.input('B').classes('w-12').on('keydown.y.shift', lambda: ui.notify('You pressed Shift+Y'))
        ui.input('C').classes('w-12').on('keydown.once', lambda: ui.notify('You started typing.'))


@doc.demo('自定义事件', '''
    使用 `emitEvent(...)` 从 JavaScript 发出自定义事件相当容易，可以使用 `ui.on(...)` 监听。
    如果您想在 JavaScript 中发生某些事情时调用 Python 代码，这可能会很有用。
    在此示例中，我们正在监听浏览器选项卡的 `visibilitychange` 事件。
''')
async def custom_events() -> None:
    tabwatch = ui.checkbox('Watch browser tab re-entering')
    ui.on('tabvisible', lambda: ui.notify('Welcome back!') if tabwatch.value else None)
    # ui.add_head_html('''
    #     <script>
    #     document.addEventListener('visibilitychange', () => {
    #         if (document.visibilityState === 'visible') {
    #             emitEvent('tabvisible');
    #         }
    #     });
    #     </script>
    # ''')
    # END OF DEMO
    await ui.context.client.connected()
    ui.run_javascript('''
        document.addEventListener('visibilitychange', () => {
            if (document.visibilityState === 'visible') {
                emitEvent('tabvisible');
            }
        });
    ''')


@doc.demo('纯 JavaScript 事件', '''
    您也可以使用 `on` 方法来注册纯 JavaScript 事件处理器。
    如果您想调用 JavaScript 代码而不向服务器发送任何数据，这可能会很有用。
    在此示例中，我们使用 `navigator.clipboard` API 将字符串复制到剪贴板。
''')
def pure_javascript() -> None:
    ui.button('Copy to clipboard') \
        .on('click', js_handler='''() => {
            navigator.clipboard.writeText("Hello, NiceGUI!");
        }''')
