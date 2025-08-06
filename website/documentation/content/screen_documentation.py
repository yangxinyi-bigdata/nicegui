from nicegui import ui
from nicegui.testing import Screen

from ..windows import python_window
from . import doc


@doc.part('Screen 夹具')
def screen_fixture():
    ui.markdown('''
        `screen` 夹具启动一个真实的（无头）浏览器来与您的应用程序交互。
        仅当您有特定于浏览器的行为需要测试时才需要这样做。
        NiceGUI 本身使用此夹具进行了彻底测试，以确保每个组件都按预期工作。
        所以只在必要时使用它。
    ''').classes('bold-links arrow-links')

    with python_window(classes='w-[600px]', title='example'):
        ui.markdown('''
            ```python
            from selenium.webdriver.common.keys import Keys

            screen.open('/')
            screen.type(Keys.TAB) # to focus on the first input
            screen.type('user1')
            screen.type(Keys.TAB) # to focus the second input
            screen.type('pass1')
            screen.click('Log in')
            screen.should_contain('Hello user1!')
            screen.click('logout')
            screen.should_contain('Log in')
            ```
        ''')


@doc.part('Web 驱动程序')
def web_driver():
    ui.markdown('''
        `screen` 夹具在底层使用 Selenium。
        目前它仅使用 Chrome 驱动程序进行了测试。
        为了自动在测试中使用它，我们建议将选项 `--driver Chrome` 添加到您的 `pytest.ini` 中：
    ''').classes('bold-links arrow-links')

    with python_window(classes='w-[600px] h-42', title='pytest.ini'):
        ui.markdown('''
            ```ini
            [pytest]
            asyncio_mode = auto
            addopts = "--driver Chrome"
            ```
        ''')


doc.reference(Screen)
