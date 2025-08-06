from nicegui import ui
from nicegui.testing import User, UserInteraction

from ..windows import python_window
from . import doc


@doc.part('用户夹具')
def user_fixture():
    ui.markdown('''
        我们建议尽可能使用 `user` 夹具而不是 [`screen` 夹具](/documentation/screen)，
        因为执行速度与单元测试一样快，并且当通过 `pytest_plugins = ['nicegui.testing.user_plugin']` 加载时不需要 Selenium 作为依赖。
        `user` 夹具去掉浏览器，并用完全在 Python 中的轻量级模拟替换它。
        有关设置的描述，请参见 [项目结构](/documentation/project_structure)。

        您可以断言"看到"特定的元素或内容，点击按钮，在输入中输入并触发事件。
        我们的目标是提供一个良好的 API 来编写像故事一样易于理解的验收测试。
        由于执行速度快，经典的 [测试金字塔](https://martinfowler.com/bliki/TestPyramid.html)，
        其中 UI 测试被认为是缓慢和昂贵的，不再适用。
    ''').classes('bold-links arrow-links')

    with python_window(classes='w-[600px]', title='example'):
        ui.markdown('''
            ```python
            await user.open('/')
            user.find('Username').type('user1')
            user.find('Password').type('pass1').trigger('keydown.enter')
            await user.should_see('Hello user1!')
            user.find('logout').click()
            await user.should_see('Log in')
            ```
        ''')

    ui.markdown('''
        **注意：** `user` 夹具相当新，仍然缺少一些功能。
        请在单独的功能请求中告诉我们
        [在 GitHub 上](https://github.com/zauberzeug/nicegui/discussions/new?category=ideas-feature-requests)。
    ''').classes('bold-links arrow-links')


@doc.part('异步执行')
def async_execution():
    ui.markdown('''
        用户模拟在与您的应用程序相同的异步上下文中运行，
        以使查询和交互尽可能简单。
        但这也意味着您的测试必须是 `async` 的。
        我们建议通过在项目根目录中创建 `pytest.ini` 文件
        或将激活直接添加到您的 `pyproject.toml` 来激活 [pytest-asyncio 自动模式](https://pytest-asyncio.readthedocs.io/en/latest/concepts.html#auto-mode)。
    ''').classes('bold-links arrow-links')

    with ui.row(wrap=False).classes('gap-4 items-center'):
        with python_window(classes='w-[300px] h-42', title='pytest.ini'):
            ui.markdown('''
                ```ini
                [pytest]
                asyncio_mode = auto
                ```
            ''')
        ui.label('or').classes('text-2xl')
        with python_window(classes='w-[300px] h-42', title='pyproject.toml'):
            ui.markdown('''
                ```toml
                [tool.pytest.ini_options]
                asyncio_mode = "auto"
                ```
            ''')


doc.text('查询', '''
    `User` 的查询功能建立在 [ElementFilter](/documentation/element_filter) 之上。
    `user.should_see(...)` 方法和 `user.find(...)` 方法
    提供参数来过滤内容、[标记](/documentation/element_filter#markers)、类型等。
    如果您不提供命名属性，字符串将与文本内容和标记匹配。
''')


@doc.ui
def querying():
    with ui.row().classes('gap-4 items-stretch'):
        with python_window(classes='w-[400px]', title='some UI code'):
            ui.markdown('''
                ```python
                with ui.row():
                    ui.label('Hello World!').mark('greeting')
                    ui.icon('star')
                with ui.row():
                    ui.label('Hello Universe!')
                    ui.input(placeholder='Type here')
                ```
            ''')

        with python_window(classes='w-[600px]', title='user assertions'):
            ui.markdown('''
                ```python
                await user.should_see('greeting')
                await user.should_see('star')
                await user.should_see('Hello Universe!')
                await user.should_see('Type here')
                await user.should_see('Hello')
                await user.should_see(marker='greeting')
                await user.should_see(kind=ui.icon)
                ```
            ''')


doc.text('用户交互', '''
    `user.find(...)` 返回一个 `UserInteraction` 对象，该对象提供输入文本、
    清除输入、点击按钮和在找到的元素上触发事件的方法。
    此演示展示如何在输入第一个字母后触发 "keydown.tab" 事件来自动完成输入字段。

    *在版本 2.7.0 中添加：触发事件*
''')


@doc.ui
def trigger_events():
    with ui.row().classes('gap-4 items-stretch'):
        with python_window(classes='w-[500px]', title='some UI code'):
            ui.markdown('''
                ```python
                fruits = ['apple', 'banana', 'cherry']
                ui.input(label='fruit', autocomplete=fruits)
                ```
            ''')
        with python_window(classes='w-[500px]', title='user assertions'):
            ui.markdown('''
                ```python
                await user.open('/')
                user.find('fruit').type('a').trigger('keydown.tab')
                await user.should_see('apple')
                ```
            ''')


doc.text('选择选项', '''
    要在 `ui.select` 中选择项目，只需

    - 使用 `user.find()` 定位 `ui.select` 元素，
    - 使用 `click()` 打开下拉菜单，
    - 再次使用 `user.find()` 定位您要选择的特定_选项_，以及
    - 第二次使用 `click()` 选择所需的选项。

    对于多选元素，为每个项目重复点击和选择步骤。
''')


@doc.ui
def selecting_options_in_a_select():
    with ui.row().classes('gap-4 items-stretch'):
        with python_window(classes='w-[500px]', title='UI code'):
            ui.markdown('''
                ```python
                ui.select(
                    ['Apple', 'Banana', 'Cherry'],
                    label='Fruits',
                    multiple=True,
                    on_change=lambda e: ui.notify(', '.join(e.value)),
                )
                ```
            ''')

        with python_window(classes='w-[500px]', title='user assertions'):
            ui.markdown('''
                ```python
                user.find('Fruits').click()
                user.find('Apple').click()
                user.find('Banana').click()
                await user.should_see('Apple, Banana')
                ```
            ''')


doc.text('使用 ElementFilter', '''
    使用 [`ElementFilter`](/documentation/element_filter) 可能是可取的，以便

    - 保持元素的顺序以检查它们在页面上的顺序，以及
    - 更细粒度的过滤选项，例如 `ElementFilter(...).within(...)`。

    通过进入 `user` 上下文并迭代 `ElementFilter`，
    您可以保持匹配元素的自然文档顺序：
''')


@doc.ui
def using_an_elementfilter():
    with ui.row().classes('gap-4 items-stretch'):
        with python_window(classes='w-[400px]', title='UI code'):
            ui.markdown('''
                ```python
                ui.label('1').mark('number')
                ui.label('2').mark('number')
                ui.label('3').mark('number')
                ```
            ''')

        with python_window(classes='w-[600px]', title='user assertions'):
            ui.markdown('''
                ```python
                with user:
                    elements = list(ElementFilter(marker='number'))
                    assert len(elements) == 3
                    assert elements[0].text == '1'
                    assert elements[1].text == '2'
                    assert elements[2].text == '3'
                ```
            ''')


doc.text('复杂元素', '''
    有些元素具有复杂的可视化和交互行为（`ui.upload`、`ui.table`、...）。
    这些元素的每个方面都不能用 `should_see` 和 `UserInteraction` 测试。
    尽管如此，您可以用 `user.find(...)` 抓取它们并在元素本身上进行测试。
''')


@doc.ui
def upload_table():
    with ui.row().classes('gap-4 items-stretch'):
        with python_window(classes='w-[500px]', title='some UI code'):
            ui.markdown('''
                ```python
                def receive_file(e: events.UploadEventArguments):
                    content = e.content.read().decode('utf-8')
                    reader = csv.DictReader(content.splitlines())
                    ui.table(
                        columns=[{
                            'name': h,
                            'label': h.capitalize(),
                            'field': h,
                        } for h in reader.fieldnames or []],
                        rows=list(reader),
                    )

                ui.upload(on_upload=receive_file)
                ```
            ''')

        with python_window(classes='w-[500px]', title='user assertions'):
            ui.markdown('''
                ```python
                upload = user.find(ui.upload).elements.pop()
                upload.handle_uploads([UploadFile(
                    BytesIO(b'name,age\\nAlice,30\\nBob,28'),
                    filename='data.csv',
                    headers=Headers(raw=[(b'content-type', b'text/csv')]),
                )])
                table = user.find(ui.table).elements.pop()
                assert table.columns == [
                    {'name': 'name', 'label': 'Name', 'field': 'name'},
                    {'name': 'age', 'label': 'Age', 'field': 'age'},
                ]
                assert table.rows == [
                    {'name': 'Alice', 'age': '30'},
                    {'name': 'Bob', 'age': '28'},
                ]
                ```
            ''')


doc.text('测试下载', '''
    您可以通过检查 `user.downloads.http_responses` 来验证是否触发了下载。
    通过等待 `user.downloads.next()`，您可以获得下一个下载响应。

    *在版本 2.1.0 中添加*
''')


@doc.ui
def check_outbox():
    with ui.row().classes('gap-4 items-stretch'):
        with python_window(classes='w-[500px]', title='some UI code'):
            ui.markdown('''
                ```python
                @ui.page('/')
                def page():
                    def download():
                        ui.download(b'Hello', filename='hello.txt')

                    ui.button('Download', on_click=download)
                ```
            ''')

        with python_window(classes='w-[500px]', title='user assertions'):
            ui.markdown('''
                ```python
                await user.open('/')
                assert len(user.download.http_responses) == 0
                user.find('Download').click()
                response = await user.download.next()
                assert response.text == 'Hello'
                ```
            ''')


doc.text('多个用户', '''
    有时仅作为单个用户与 UI 交互是不够的。
    除了 `user` 夹具外，我们还提供 `create_user` 夹具，它是一个用于创建用户的工厂函数。
    `User` 实例彼此独立，可以并行与 UI 交互。
    请参阅我们的 [聊天应用示例](https://github.com/zauberzeug/nicegui/blob/main/examples/chat_app/test_chat_app.py)
    了解完整演示。
''')


@doc.ui
def multiple_users():
    with python_window(classes='w-[600px]', title='example'):
        ui.markdown('''
            ```python
            async def test_chat(create_user: Callable[[], User]) -> None:
                userA = create_user()
                await userA.open('/')
                userB = create_user()
                await userB.open('/')

                userA.find(ui.input).type('from A').trigger('keydown.enter')
                await userB.should_see('from A')
                userB.find(ui.input).type('from B').trigger('keydown.enter')
                await userA.should_see('from A')
                await userA.should_see('from B')
            ```
        ''')


doc.text('模拟 JavaScript', '''
    `User` 类有一个 `javascript_rules` 字典来模拟 JavaScript 执行。
    键是编译的正则表达式，值是返回 JavaScript 响应的函数。
    该函数将使用 JavaScript 命令上正则表达式的匹配对象调用。

    *在版本 2.14.0 中添加*
''')


@doc.ui
def simulate_javascript():
    with ui.row().classes('gap-4 items-stretch'):
        with python_window(classes='w-[500px]', title='some UI code'):
            ui.markdown('''
                ```python
                @ui.page('/')
                async def page():
                    await context.client.connected()
                    date = await ui.run_javascript('Math.sqrt(1764)')
                    ui.label(date)
                ```
            ''')

        with python_window(classes='w-[500px]', title='user assertions'):
            ui.markdown('''
                ```python
                user.javascript_rules[re.compile(r'Math.sqrt\\((\\d+)\\)')] = \\
                    lambda match: int(match.group(1))**0.5
                await user.open('/')
                await user.should_see('42')
                ```
            ''')


doc.text('与 screen 夹具的比较', '''
    通过去掉浏览器，测试执行变得比 [`screen` 夹具](/documentation/screen) 快得多。
    请参阅我们的 [pytests 示例](https://github.com/zauberzeug/nicegui/tree/main/examples/pytests)，
    它使用两个夹具实现相同的测试。
    当然，某些功能（如屏幕截图或浏览器特定行为）不可用，
    但在大多数情况下，`user` 夹具的速度使其成为首选。
''')

doc.reference(User, title='User 参考')
doc.reference(UserInteraction, title='UserInteraction 参考')
