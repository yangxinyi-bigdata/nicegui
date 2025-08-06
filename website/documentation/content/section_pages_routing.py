import uuid

from nicegui import app, ui

from . import (
    doc,
    download_documentation,
    navigate_documentation,
    page_documentation,
    page_layout_documentation,
    page_title_documentation,
    sub_pages_documentation,
)

CONSTANT_UUID = str(uuid.uuid4())

doc.title('*页面*与路由')

doc.intro(page_documentation)


@doc.auto_execute
@doc.demo('自动索引页面', '''
    使用 `@ui.page` 装饰器创建的页面是"私有的"。
    它的内容会为每个客户端重新创建。
    因此，在右侧的演示中，私有页面上显示的 ID 在浏览器重新加载页面时会发生变化。

    没有包装在装饰页面函数中的 UI 元素被放置在路由"/"处自动生成的索引页面上。
    这个自动索引页面在启动时创建一次，并在可能连接的所有客户端之间*共享*。
    因此，每个连接的客户端将看到*相同*的元素。
    在右侧的演示中，自动索引页面上显示的 ID 在浏览器重新加载页面时保持不变。
''')
def auto_index_page():
    from uuid import uuid4

    @ui.page('/private_page')
    async def private_page():
        ui.label(f'private page with ID {uuid4()}')

    # ui.label(f'shared auto-index page with ID {uuid4()}')
    # ui.link('private page', private_page)
    # END OF DEMO
    ui.label(f'shared auto-index page with ID {CONSTANT_UUID}')
    ui.link('private page', private_page)


doc.intro(page_layout_documentation)
doc.intro(sub_pages_documentation)


@doc.auto_execute
@doc.demo('参数注入', '''
    多亏了 FastAPI，页面函数接受可选参数来提供
    [路径参数](https://fastapi.tiangolo.com/tutorial/path-params/)、
    [查询参数](https://fastapi.tiangolo.com/tutorial/query-params/) 或整个传入的
    [请求](https://fastapi.tiangolo.com/advanced/using-request-directly/)，用于访问
    正文载荷、头部、cookie 等。
''')
def parameter_demo():
    @ui.page('/icon/{icon}')
    def icons(icon: str, amount: int = 1):
        ui.label(icon).classes('text-h3')
        with ui.row():
            [ui.icon(icon).classes('text-h3') for _ in range(amount)]
    ui.link('Star', '/icon/star?amount=5')
    ui.link('Home', '/icon/home')
    ui.link('Water', '/icon/water_drop?amount=3')


doc.intro(page_title_documentation)
doc.intro(navigate_documentation)

doc.redirects['open'] = 'navigate#ui_navigate_to_(formerly_ui_open)'
doc.text('ui.open', f'''
    `ui.open` 函数已被弃用。
    请改用 [`ui.navigate.to`]({doc.redirects["open"]})。
''')

doc.intro(download_documentation)


@doc.demo(app.add_static_files)
def add_static_files_demo():
    from nicegui import app

    app.add_static_files('/examples', 'examples')
    ui.label('Some NiceGUI Examples').classes('text-h5')
    ui.link('AI interface', '/examples/ai_interface/main.py')
    ui.link('Custom FastAPI app', '/examples/fastapi/main.py')
    ui.link('Authentication', '/examples/authentication/main.py')


@doc.demo(app.add_media_files)
def add_media_files_demo():
    from pathlib import Path

    import httpx

    from nicegui import app

    media = Path('media')
    # media.mkdir(exist_ok=True)
    # r = httpx.get('https://cdn.coverr.co/videos/coverr-cloudy-sky-2765/1080p.mp4')
    # (media  / 'clouds.mp4').write_bytes(r.content)
    # app.add_media_files('/my_videos', media)
    # ui.video('/my_videos/clouds.mp4')
    # END OF DEMO
    ui.video('https://cdn.coverr.co/videos/coverr-cloudy-sky-2765/1080p.mp4')


@doc.demo('向页面添加 HTML', '''
    您可以通过调用 `ui.add_head_html` 或 `ui.add_body_html` 向页面添加 HTML。
    这对于添加自定义 CSS 样式或 JavaScript 代码很有用。
''')
def add_head_html_demo():
    ui.add_head_html('''
        <style>
            .my-red-label {
                color: Crimson;
                font-weight: bold;
            }
        </style>
    ''')
    ui.label('RED').classes('my-red-label')


@doc.auto_execute
@doc.demo('API 响应', '''
    NiceGUI 基于 [FastAPI](https://fastapi.tiangolo.com/)。
    这意味着您可以使用 FastAPI 的所有功能。
    例如，除了图形用户界面外，您还可以实现 RESTful API。
    您只需从 `nicegui` 导入 `app` 对象。
    或者您可以通过使用 `ui.run_with(app)` 在自己的 FastAPI 应用程序上运行 NiceGUI，而不是用 `ui.run()` 自动启动服务器。

    您还可以在页面函数中返回任何其他 FastAPI 响应对象。
    例如，如果满足某些条件，您可以返回 `RedirectResponse` 将用户重定向到另一个页面。
    这在我们的[身份验证演示](https://github.com/zauberzeug/nicegui/tree/main/examples/authentication/main.py)中使用。
''')
def fastapi_demo():
    import random

    from nicegui import app

    @app.get('/random/{max}')
    def generate_random_number(max: int):
        return {'min': 0, 'max': max, 'value': random.randint(0, max)}

    max = ui.number('max', value=100)
    ui.button('generate random number',
              on_click=lambda: ui.navigate.to(f'/random/{max.value:.0f}'))
