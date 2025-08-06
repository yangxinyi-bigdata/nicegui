from nicegui import ui

from . import doc


@doc.auto_execute
@doc.demo(ui.page)
def main_demo() -> None:
    @ui.page('/other_page')
    def other_page():
        ui.label('Welcome to the other side')

    @ui.page('/dark_page', dark=True)
    def dark_page():
        ui.label('Welcome to the dark side')

    ui.link('Visit other page', other_page)
    ui.link('Visit dark page', dark_page)


@doc.auto_execute
@doc.demo('带路径参数的页面', '''
    页面路由可以包含参数，就像 [FastAPI](https://fastapi.tiangolo.com/tutorial/path-params/)。
    如果有类型注解，它们会自动转换为 bool、int、float 和 complex 值。
    如果页面函数期望一个 `request` 参数，请求对象会自动提供。
    `client` 参数提供对 websocket 连接、布局等的访问。
''')
def page_with_path_parameters_demo():
    @ui.page('/repeat/{word}/{count}')
    def page(word: str, count: int):
        ui.label(word * count)

    ui.link('Say hi to Santa!', '/repeat/Ho! /3')


@doc.auto_execute
@doc.demo('等待客户端连接', '''
    要等待客户端连接，您可以在装饰的页面函数中添加 `client` 参数
    并等待 `client.connected()`。
    该语句下面的所有代码都在服务器和客户端之间建立 websocket 连接后执行。

    例如，这允许您运行 JavaScript 命令；这只有在客户端连接时才可能（参见 [#112](https://github.com/zauberzeug/nicegui/issues/112)）。
    还可以在用户已经看到一些内容时执行异步操作。
''')
def wait_for_connected_demo():
    import asyncio

    @ui.page('/wait_for_connection')
    async def wait_for_connection():
        ui.label('This text is displayed immediately.')
        await ui.context.client.connected()
        await asyncio.sleep(2)
        ui.label('This text is displayed 2 seconds after the page has been fully loaded.')

    ui.link('wait for connection', wait_for_connection)


@doc.auto_execute
@doc.demo('Multicasting', '''
    The content on a page is private to the client (the browser tab) and has its own local element context.
    If you want to send updates to _all_ clients of a specific page, you can use the `app.clients` iterator.
    This is useful for modifying UI elements from a background process or from other pages.

    *Added in version 2.7.0*
''')
def multicasting():
    from nicegui import app

    @ui.page('/multicast_receiver')
    def page():
        ui.label('This page will show messages from the index page.')

    def send(message: str):
        for client in app.clients('/multicast_receiver'):
            with client:
                ui.notify(message)

    ui.button('Send message', on_click=lambda: send('Hi!'))
    ui.link('Open receiver', '/multicast_receiver', new_tab=True)


@doc.demo('Modularize with APIRouter', '''
    You can use the NiceGUI specialization of
    [FastAPI's APIRouter](https://fastapi.tiangolo.com/tutorial/bigger-applications/?h=apirouter#apirouter)
    to modularize your code by grouping pages and other routes together.
    This is especially useful if you want to reuse the same prefix for multiple pages.
    The router and its pages can be neatly tugged away in a separate module (e.g. file) and
    the router is simply imported and included in the main app.
    See our [modularization example](https://github.com/zauberzeug/nicegui/blob/main/examples/modularization/api_router_example.py)
    for a multi-file app structure using an API router.
''', tab='/sub-path')
def api_router_demo():
    # from nicegui import APIRouter, app
    #
    # router = APIRouter(prefix='/sub-path')
    #
    # @router.page('/')
    # def page():
    #     ui.label('This is content on /sub-path')
    #
    # @router.page('/sub-sub-path')
    # def page():
    #     ui.label('This is content on /sub-path/sub-sub-path')
    #
    # ui.link('Visit sub-path', '/sub-path')
    # ui.link('Visit sub-sub-path', '/sub-path/sub-sub-path')
    #
    # app.include_router(router)
    # END OF DEMO
    ui.label('This is content on /sub-path')
