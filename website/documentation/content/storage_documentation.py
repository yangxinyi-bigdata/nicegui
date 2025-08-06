from collections import Counter
from datetime import datetime

from nicegui import ui

from . import doc

counter = Counter()  # type: ignore
start = datetime.now().strftime(r'%H:%M, %d %B %Y')


doc.title('Storage')


@doc.demo('存储', '''
    NiceGUI 为应用程序内的数据持久化提供了简单的机制。
    它具有五种内置的存储类型：

    - `app.storage.tab`：
        存储在服务器端内存中，此字典对每个非重复的标签页会话是唯一的，可以保存任意对象。
        重新启动服务器时数据将丢失，直到 <https://github.com/zauberzeug/nicegui/discussions/2841> 实现。
        此存储仅在 [页面构建器函数](/documentation/page) 内可用，
        并且需要已建立的连接，可通过 [`await client.connected()`](/documentation/page#wait_for_client_connection) 获取。
    - `app.storage.client`：
        同样存储在服务器端内存中，此字典对每个客户端连接是唯一的，可以保存任意对象。
        当页面重新加载或用户导航到另一个页面时，数据将被丢弃。
        与存储在 `app.storage.tab` 中的数据不同，后者可以在服务器上保留数天，
        `app.storage.client` 有助于缓存资源密集型对象，例如您需要保持活动状态的流或数据库连接，
        用于动态站点更新，但希望在用户离开页面或关闭浏览器时立即丢弃。
        此存储仅在 [页面构建器函数](/documentation/page) 内可用。
    - `app.storage.user`：
        存储在服务器端，每个字典都与浏览器会话 cookie 中保存的唯一标识符相关联。
        此存储对每个用户是唯一的，可以在其所有浏览器标签页中访问。
        `app.storage.browser['id']` 用于标识用户。
        此存储仅在 [页面构建器函数](/documentation/page) 内可用，
        并且需要 `ui.run()` 中的 `storage_secret` 参数来签署浏览器会话 cookie。
    - `app.storage.general`：
        同样存储在服务器端，此字典提供所有用户都可以访问的共享存储空间。
    - `app.storage.browser`：
        与以前的类型不同，此字典直接存储为浏览器会话 cookie，在同一用户的所有浏览器标签页之间共享。
        但是，由于其在减少数据负载、增强安全性和提供更大存储容量方面的优势，通常首选 `app.storage.user`。
        默认情况下，NiceGUI 在 `app.storage.browser['id']` 中保存浏览器会话的唯一标识符。
        此存储仅在 [页面构建器函数](/documentation/page) 内可用，
        并且需要 `ui.run()` 中的 `storage_secret` 参数来签署浏览器会话 cookie。

    下表将帮助您选择存储。

    | 存储类型                   | `client` | `tab`  | `browser` | `user` | `general` |
    |----------------------------|----------|--------|-----------|--------|-----------|
    | 位置                       | 服务器   | 服务器 | 浏览器   | 服务器 | 服务器    |
    | 跨标签页                   | 否       | 否     | 是       | 是    | 是       |
    | 跨浏览器                   | 否       | 否     | 否        | 否     | 是       |
    | 跨服务器重启               | 否       | 是     | 否        | 是    | 是       |
    | 跨页面重新加载             | 否       | 是     | 是       | 是    | 是       |
    | 需要页面构建器函数         | 是       | 是     | 是       | 是    | 否        |
    | 需要客户端连接             | 否       | 是     | 否        | 否     | 否        |
    | 仅在响应前写入             | 否       | 否     | 是       | 否     | 否        |
    | 需要可序列化数据           | 否       | 否     | 是       | 是    | 是       |
    | 需要 `storage_secret`      | 否       | 否     | 是       | 是    | 否        |
''')
def storage_demo():
    from nicegui import app

    # @ui.page('/')
    # def index():
    #     app.storage.user['count'] = app.storage.user.get('count', 0) + 1
    #     with ui.row():
    #        ui.label('your own page visits:')
    #        ui.label().bind_text_from(app.storage.user, 'count')
    #
    # ui.run(storage_secret='private key to secure the browser session cookie')
    # END OF DEMO
    app.storage.user['count'] = app.storage.user.get('count', 0) + 1
    with ui.row():
        ui.label('your own page visits:')
        ui.label().bind_text_from(app.storage.user, 'count')


@doc.demo('计算页面访问次数', '''
    在这里，我们使用自动可用的浏览器存储会话 ID 来计算唯一页面访问次数。
''')
def page_visits():
    from collections import Counter
    from datetime import datetime

    from nicegui import app

    # counter = Counter()
    # start = datetime.now().strftime('%H:%M, %d %B %Y')
    #
    # @ui.page('/')
    # def index():
    #     counter[app.storage.browser['id']] += 1
    #     ui.label(f'{len(counter)} unique views ({sum(counter.values())} overall) since {start}')
    #
    # ui.run(storage_secret='private key to secure the browser session cookie')
    # END OF DEMO
    counter[app.storage.browser['id']] += 1
    ui.label(f'{len(counter)} unique views ({sum(counter.values())} overall) since {start}')


@doc.demo('存储 UI 状态', '''
    存储也可以与 [`绑定`](/documentation/section_binding_properties) 结合使用。
    在这里，我们在访问之间存储文本区域的值。
    该笔记也在同一用户的所有标签页之间共享。
''')
def ui_state():
    from nicegui import app

    # @ui.page('/')
    # def index():
    #     ui.textarea('This note is kept between visits') \
    #         .classes('w-full').bind_value(app.storage.user, 'note')
    # END OF DEMO
    ui.textarea('This note is kept between visits').classes('w-full').bind_value(app.storage.user, 'note')


@doc.demo('按浏览器标签页存储数据', '''
    在 `app.storage.tab` 中存储数据时，单个用户可以打开同一应用程序的多个标签页，每个标签页都有自己的存储数据。
    这在某些场景中可能是有益的，例如搜索或执行数据分析时。
    对于登录银行账户或访问密码管理器等场景，使用这种易失性存储也更安全。
''')
def tab_storage():
    from nicegui import app

    # @ui.page('/')
    # async def index():
    #     await ui.context.client.connected()
    with ui.column():  # HIDE
        app.storage.tab['count'] = app.storage.tab.get('count', 0) + 1
        ui.label(f'Tab reloaded {app.storage.tab["count"]} times')
        ui.button('Reload page', on_click=ui.navigate.reload)


@doc.demo('标签页存储的最大年龄', '''
    默认情况下，标签页存储保留 30 天。
    您可以通过设置 `app.storage.max_tab_storage_age` 来更改此设置。

    *在版本 2.10.0 中添加*
''')
def max_tab_storage_age():
    from nicegui import app
    from datetime import timedelta
    # app.storage.max_tab_storage_age = timedelta(minutes=1).total_seconds()
    ui.label(f'Tab storage age: {timedelta(minutes=1).total_seconds()} seconds')  # HIDE

    # @ui.page('/')
    # def index():
    #    ui.label(f'Tab storage age: {app.storage.max_tab_storage_age} seconds')


@doc.demo('短期内存', '''
    `app.storage.client` 的目标是仅在当前页面访问期间存储数据。
    与存储在 `app.storage.tab` 中的数据不同
    - 后者在页面更改甚至浏览器重启之间都会保留，只要标签页保持打开状态 -
    如果用户关闭浏览器、重新加载页面或导航到另一个页面，`app.storage.client` 中的数据将被丢弃。
    这对于资源密集型、有意短期存在或敏感的数据是有益的。
    一个例子是数据库连接，应该在用户离开页面时立即关闭。
    此外，如果您希望每次用户重新加载时返回具有默认设置的页面，此存储也很有用。
    同时，它在页面内导航期间保持数据活动状态。
    这在间隔更新站点上的元素时也很有帮助，例如实时信息流。
''')
def short_term_memory():
    from nicegui import app

    # @ui.page('/')
    # async def index():
    with ui.column():  # HIDE
        cache = app.storage.client
        cache['count'] = 0
        ui.label().bind_text_from(cache, 'count', lambda n: f'Updated {n} times')
        ui.button('Update content',
                  on_click=lambda: cache.update(count=cache['count'] + 1))
        ui.button('Reload page', on_click=ui.navigate.reload)


doc.text('缩进', '''
    默认情况下，通用和用户存储数据以无缩进的 JSON 格式存储。
    您可以通过设置 `app.storage.general.indent = True` 或 `app.storage.user.indent = True` 
    将其更改为 2 个空格的缩进。
''')


doc.text('Redis 存储', '''
    您可以使用 [Redis](https://redis.io/) 进行存储，作为默认文件存储的替代方案。
    如果您有多个 NiceGUI 实例并希望在它们之间共享数据，这很有用。

    要激活此功能，请安装 `redis` 包（`pip install nicegui[redis]`）
    并提供 `NICEGUI_REDIS_URL` 环境变量以指向您的 Redis 服务器。
    我们的 [Redis 存储示例](https://github.com/zauberzeug/nicegui/tree/main/examples/redis_storage) 显示了
    您如何使用反向代理或负载均衡器进行设置。
    为确保连接保持在最低限度，您应该使用 `--timeout <seconds>` CLI 选项启动 Redis 服务器
    或设置环境变量 `REDIS_TIMEOUT`。

    请注意，Redis 同步始终包含所有数据，而不仅仅是更改的值。

    - 对于 `app.storage.general`，这是整个字典。
    - 对于 `app.storage.user`，这是用户的所有数据。
    - 对于 `app.storage.tab`，这是为此特定标签页存储的所有数据。

    如果您有大型数据集，我们建议使用数据库。
    请参阅我们的 [数据库示例](https://github.com/zauberzeug/nicegui/blob/main/examples/sqlite_database/main.py) 了解 SQLite 的演示。
    但当然，要在多个实例之间同步，您应该用 PostgreSQL 或类似数据库替换 SQLite。

    *在版本 2.10.0 中添加*
''')
