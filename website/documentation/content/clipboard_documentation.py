from nicegui import ui

from . import doc


@doc.demo('读写剪贴板', '''
    以下演示展示了如何使用 `ui.clipboard.read()`、`ui.clipboard.write()` 和 `ui.clipboard.read_image()` 与剪贴板交互。

    由于自动索引页面可以同时被多个浏览器标签页访问，因此不支持在此页面上读取剪贴板。
    这仅在用 `ui.page` 装饰的页面构建器函数中才可能实现，如本演示所示。

    请注意，您的浏览器可能会请求访问剪贴板的权限，或者可能完全不支持此功能。
''')
def main_demo() -> None:
    # @ui.page('/')
    # async def index():
    with ui.column():  # HIDE
        ui.button('写入文本', on_click=lambda: ui.clipboard.write('嗨！'))

        async def read() -> None:
            ui.notify(await ui.clipboard.read())
        ui.button('读取文本', on_click=read)

        async def read_image() -> None:
            img = await ui.clipboard.read_image()
            if not img:
                ui.notify('您必须先复制图像到剪贴板。')
            else:
                image.set_source(img)
        ui.button('读取图像', on_click=read_image)
        image = ui.image().classes('w-72')


@doc.demo('客户端剪贴板', '''
    为了避免到服务器的往返，您也可以直接使用客户端剪贴板API。
    这可能会被更多浏览器支持，因为剪贴板访问是由用户操作直接触发的。
''')
def client_side_clipboard() -> None:
    ui.button('写入').on('click', js_handler='''
        () => navigator.clipboard.writeText("哈！")
    ''')
    ui.button('读取').on('click', js_handler='''
        async () => emitEvent("clipboard", await navigator.clipboard.readText())
    ''')
    ui.on('clipboard', lambda e: ui.notify(e.args))
