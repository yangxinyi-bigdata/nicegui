from nicegui import app, ui

from . import (
    clipboard_documentation,
    doc,
    generic_events_documentation,
    keyboard_documentation,
    refreshable_documentation,
    run_javascript_documentation,
    storage_documentation,
    timer_documentation,
)

doc.title('动作与*事件*')

doc.intro(timer_documentation)
doc.intro(keyboard_documentation)


@doc.demo('UI 更新', '''
    NiceGUI 会尝试自动同步 UI 元素的状态与客户端，
    例如当标签文本、输入值或元素的样式/类/属性发生变化时。
    在其他情况下，您可以显式调用 `element.update()` 或 `ui.update(*elements)` 来更新。
    演示代码展示了 `ui.echart` 的两种方法，在这种情况下很难自动检测 `options` 字典的变化。
''')
def ui_updates_demo():
    from random import random

    chart = ui.echart({
        'xAxis': {'type': 'value'},
        'yAxis': {'type': 'value'},
        'series': [{'type': 'line', 'data': [[0, 0], [1, 1]]}],
    })

    def add():
        chart.options['series'][0]['data'].append([random(), random()])
        chart.update()

    def clear():
        chart.options['series'][0]['data'].clear()
        ui.update(chart)

    with ui.row():
        ui.button('Add', on_click=add)
        ui.button('Clear', on_click=clear)


doc.intro(refreshable_documentation)


@doc.demo('异步事件处理器', '''
    大多数元素也支持异步事件处理器。

    注意：您也可以将 `functools.partial` 传递到 `on_click` 属性中来包装带参数的异步函数。
''')
def async_handlers_demo():
    import asyncio

    async def async_task():
        ui.notify('Asynchronous task started')
        await asyncio.sleep(5)
        ui.notify('Asynchronous task finished')

    ui.button('start async task', on_click=async_task)


doc.intro(generic_events_documentation)


@doc.demo('运行 CPU 密集型任务', '''
    NiceGUI 提供了一个 `cpu_bound` 函数，用于在单独的进程中运行 CPU 密集型任务。
    这对于长时间运行的计算很有用，否则会阻塞事件循环并使 UI 无响应。
    该函数返回一个可以等待的 future 对象。

    注意：
    该函数需要将传递函数的整个状态传输到进程，这是通过 pickle 完成的。
    建议创建自由函数或静态方法，这些方法将所有数据作为简单参数获取（即没有类或 UI 逻辑）
    并返回结果，而不是将其写入类属性或全局变量。
''')
def cpu_bound_demo():
    import time

    from nicegui import run

    def compute_sum(a: float, b: float) -> float:
        time.sleep(1)  # simulate a long-running computation
        return a + b

    async def handle_click():
        result = await run.cpu_bound(compute_sum, 1, 2)
        ui.notify(f'Sum is {result}')

    # ui.button('Compute', on_click=handle_click)
    # END OF DEMO
    async def mock_click():
        import asyncio
        await asyncio.sleep(1)
        ui.notify('Sum is 3')
    ui.button('Compute', on_click=mock_click)


@doc.demo('运行 I/O 密集型任务', '''
    NiceGUI 提供了一个 `io_bound` 函数，用于在单独的线程中运行 I/O 密集型任务。
    这对于长时间运行的 I/O 操作很有用，否则会阻塞事件循环并使 UI 无响应。
    该函数返回一个可以等待的 future 对象。
''')
def io_bound_demo():
    import httpx

    from nicegui import run

    async def handle_click():
        URL = 'https://httpbin.org/delay/1'
        response = await run.io_bound(httpx.get, URL, timeout=3)
        ui.notify(f'Downloaded {len(response.content)} bytes')

    ui.button('Download', on_click=handle_click)


doc.intro(run_javascript_documentation)
doc.intro(clipboard_documentation)


@doc.demo('事件', '''
    您可以为以下事件注册要调用的协程或函数：

    - `app.on_startup`: 当 NiceGUI 启动或重启时调用
    - `app.on_shutdown`: 当 NiceGUI 关闭或重启时调用
    - `app.on_connect`: 为每个连接的客户端调用（可选参数：nicegui.Client）
    - `app.on_disconnect`: 为每个断开连接的客户端调用（可选参数：nicegui.Client）
    - `app.on_exception`: 当发生异常时调用（可选参数：exception）

    当 NiceGUI 关闭或重启时，所有仍在执行的任务将自动取消。
''')
def lifecycle_demo():
    from datetime import datetime

    from nicegui import app

    # dt = datetime.now()

    def handle_connection():
        global dt
        dt = datetime.now()
    app.on_connect(handle_connection)

    label = ui.label()
    ui.timer(1, lambda: label.set_text(f'Last new connection: {dt:%H:%M:%S}'))
    # END OF DEMO
    global dt
    dt = datetime.now()


@doc.auto_execute
@doc.demo('自定义错误页面', '''
    您可以使用 `@app.on_page_exception` 来定义自定义错误页面。

    处理器必须是一个同步函数，它像普通页面函数一样创建页面。
    它可以将异常作为参数，但这不是必需的。
    它会覆盖默认的"悲伤面孔"错误页面，除非错误被重新引发。

    以下示例展示了如何创建一个只处理特定异常的自定义错误页面处理器。
    对于所有其他异常，仍然使用默认的错误页面处理器。

    注意：在生产环境中显示 traceback 可能不是一个好主意，因为它可能泄露敏感信息。

    *在版本 2.20.0 中添加*
''')
def error_page_demo():
    from nicegui import app
    import traceback

    @app.on_page_exception
    def timeout_error_page(exception: Exception) -> None:
        if not isinstance(exception, TimeoutError):
            raise exception
        with ui.column().classes('absolute-center items-center gap-8'):
            ui.icon('sym_o_timer', size='xl')
            ui.label(f'{exception}').classes('text-2xl')
            ui.code(traceback.format_exc(chain=False))

    @ui.page('/raise_timeout_error')
    def raise_timeout_error():
        raise TimeoutError('This took too long')

    @ui.page('/raise_runtime_error')
    def raise_runtime_error():
        raise RuntimeError('Something is wrong')

    ui.link('Raise timeout error (custom error page)', '/raise_timeout_error')
    ui.link('Raise runtime error (default error page)', '/raise_runtime_error')


@doc.demo(app.shutdown)
def shutdown_demo():
    from nicegui import app

    # ui.button('shutdown', on_click=app.shutdown)
    #
    # ui.run(reload=False)
    # END OF DEMO
    ui.button('shutdown', on_click=lambda: ui.notify(
        'Nah. We do not actually shutdown the documentation server. Try it in your own app!'))


doc.intro(storage_documentation)
