from nicegui import ui

from ..windows import bash_window, python_window
from . import doc

doc.text('项目结构', '''
    NiceGUI 包提供了一个 [pytest 插件](https://docs.pytest.org/en/stable/how-to/writing_plugins.html)
    可以通过 `pytest_plugins = ['nicegui.testing.plugin']` 激活。
    这使得专门的 [fixtures](https://docs.pytest.org/en/stable/explanation/fixtures.html) 可用于测试您的 NiceGUI 用户界面。
    使用 [`screen` fixture](/documentation/screen) 您可以通过无头浏览器运行测试（较慢）
    使用 [`user` fixture](/documentation/user) 在 Python 中完全模拟（较快）。
    如果您只想要一种测试 fixture，
    您也可以使用插件 `nicegui.testing.user_plugin` 或 `nicegui.testing.screen_plugin`。

    有多种方法可以构建您的项目和测试。
    在此我们只介绍两种我们发现有用的方法，
    一种是用于[小型应用和实验](/documentation/project_structure#simple)
    另一种是用于[大型项目的模块化方法](/documentation/project_structure#modular)。
    您可以在 [pytest 文档](https://docs.pytest.org/en/stable/contents.html) 中找到更多信息。
''')

doc.text('简单', '''
    对于小型应用和实验，您可以将测试放在单独的文件中，
    就像我们在示例中所做的那样
    [聊天应用](https://github.com/zauberzeug/nicegui/tree/main/examples/chat_app)
    [待办事项列表](https://github.com/zauberzeug/nicegui/tree/main/examples/todo_list/) 和
    [身份验证](https://github.com/zauberzeug/nicegui/tree/main/examples/authentication)。
    为了在测试中正确重新初始化您的 `main.py`，
    您在代码旁边放置一个空的 `__init__.py` 文件以使其成为一个包
    并使用 `module_under_test` 标记器为每个测试自动重新加载您的主文件。
    还不要忘记 `pytest.ini` 文件
    来为用户 fixture 启用 [`asyncio_mode = auto`](/documentation/user#async_execution) 选项
    并确保在您的 `main.py` 中正确保护 `ui.run()` 调用
    以防止服务器在测试期间启动：
''')


@doc.ui
def simple_project_code():
    with ui.row(wrap=False).classes('gap-4 items-stretch'):
        with python_window(classes='w-[400px]'):
            ui.markdown('''
                ```python
                from nicegui import ui

                def hello() -> None:
                    ui.notify('Hello World!')

                ui.button('Click me', on_click=hello)

                if __name__ in {'__main__', '__mp_main__'}:
                    ui.run()
                ```
            ''')

        with python_window(classes='w-[400px]', title='test_app.py'):
            ui.markdown('''
                ```python
                import pytest
                from nicegui import ui
                from nicegui.testing import User
                from . import main

                pytest_plugins = ['nicegui.testing.user_plugin']

                @pytest.mark.module_under_test(main)
                async def test_click(user: User) -> None:
                    await user.open('/')
                    await user.should_see('Click me')
                    user.find(ui.button).click()
                    await user.should_see('Hello World!')
                ```
            ''')


@doc.ui
def simple_project_bash():
    with bash_window(classes='max-w-[820px] w-full h-42'):
        ui.markdown('''
            ```bash
            $ ls
            __init__.py         main.py        test_app.py       pytest.ini

            $ pytest
            ==================== test session starts =====================
            test_app.py .                                     [100%]
            ===================== 1 passed in 0.51 s ======================
            ```
        ''')


doc.text('模块化', '''
    一种更模块化的方法是为您的代码创建一个包，其中包含一个空的 `__init__.py`
    和一个单独的 `tests` 文件夹用于您的测试。
    在您的包中，`startup.py` 文件可用于注册页面和执行所有必要的应用初始化。
    根级别的 `main.py` 然后只导入启动例程并调用 `ui.run()`。
    根目录中的一个空的 `conftest.py` 文件使包及其 `startup` 例程可用于测试。
    还不要忘记 `pytest.ini` 文件
    来为用户 fixture 启用 [`asyncio_mode = auto`](/documentation/user#async_execution) 选项。
''')


@doc.ui
def modular_project():
    with ui.row(wrap=False).classes('gap-4 items-stretch'):
        with python_window(classes='w-[400px]'):
            ui.markdown('''
                ```python
                from nicegui import ui, app
                from app.startup import startup

                app.on_startup(startup)

                ui.run()
                ```
            ''')

        with python_window(classes='w-[400px]', title='app/startup.py'):
            ui.markdown('''
                ```python
                from nicegui import ui

                def hello() -> None:
                    ui.notify('Hello World!')

                def startup() -> None:
                    @ui.page('/')
                    def index():
                        ui.button('Click me', on_click=hello)
                ```
            ''')

    with ui.row(wrap=False).classes('gap-4 items-stretch'):
        with python_window(classes='w-[400px]', title='tests/test_app.py'):
            ui.markdown('''
                ```python
                from nicegui import ui
                from nicegui.testing import User
                from app.startup import startup

                pytest_plugins = ['nicegui.testing.user_plugin']

                async def test_click(user: User) -> None:
                    startup()
                    await user.open('/')
                    await user.should_see('Click me')
                    user.find(ui.button).click()
                    await user.should_see('Hello World!')
                ```
                ''')

        with bash_window(classes='w-[400px]'):
            ui.markdown('''
                ```bash
                $ tree
                .
                ├── main.py
                ├── pytest.ini
                ├── app
                │   ├── __init__.py
                │   └── startup.py
                └── tests
                    ├── __init__.py
                    ├── conftest.py
                    └── test_app.py
                ```
            ''')


doc.text('', '''
    您还可以在 `conftest.py` 中定义自己的 fixtures，调用 `startup` 例程。
    Pytest 有一些魔法可以自动在您的测试中找到并使用这个专门的 fixture。
    这样您可以使您的测试保持干净和简单。
    查看 [pytests 示例](https://github.com/zauberzeug/nicegui/tree/main/examples/pytests)
    了解此设置的完整演示。
''')


@doc.ui
def custom_user_fixture():
    with ui.row(wrap=False).classes('gap-4 items-stretch'):
        with python_window(classes='w-[400px]', title='tests/test_app.py'):
            ui.markdown('''
                ```python
                from nicegui import ui
                from nicegui.testing import User

                async def test_click(user: User) -> None:
                    await user.open('/')
                    await user.should_see('Click me')
                    user.find(ui.button).click()
                    await user.should_see('Hello World!')
                ```
            ''')

        with python_window(classes='w-[400px]', title='conftest.py'):
            ui.markdown('''
                ```python
                import pytest
                from nicegui.testing import User
                from app.startup import startup

                pytest_plugins = ['nicegui.testing.user_plugin']

                @pytest.fixture
                def user(user: User) -> User:
                    startup()
                    return user
                ```
            ''')
