from nicegui import ui

from ...style import link_target
from . import doc


@doc.demo(ui.link)
def main_demo() -> None:
    ui.link('NiceGUI on GitHub', 'https://github.com/zauberzeug/nicegui')


@doc.demo('在大页面中导航', '''
    要跳转到页面内的特定位置，您可以使用 `ui.link_target('target_name')` 放置可链接的锚点，
    或者简单地传递一个 NiceGUI 元素作为链接目标。
''')
def same_page_links():
    navigation = ui.row()
    # ui.link_target('target_A')
    link_target('target_A', '-10px')  # HIDE
    ui.label(
        'Lorem ipsum dolor sit amet, consectetur adipiscing elit, '
        'sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.'
    )
    link_target('target_B', '70px')  # HIDE
    label_B = ui.label(
        'Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. '
        'Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. '
        'Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'
    )
    with navigation:
        ui.link('Goto A', '#target_A')
        # ui.link('Goto B', label_B)
        ui.link('Goto B', '#target_B')  # HIDE


@doc.auto_execute
@doc.demo('链接到其他页面', '''
    您可以通过提供路径或函数引用作为链接目标来链接到其他页面。
''')
def link_to_other_page():
    @ui.page('/some_other_page')
    def my_page():
        ui.label('This is another page')

    ui.label('Go to other page')
    ui.link('... with path', '/some_other_page')
    ui.link('... with function reference', my_page)


@doc.demo('从图像和其他元素链接', '''
    通过在链接内嵌套元素，您可以使整个元素可点击。
    这适用于所有元素，但对于非交互元素最有用，比如
    [ui.image](/documentation/image)、[ui.avatar](/documentation/image) 等。
''')
def link_from_elements():
    with ui.link(target='https://github.com/zauberzeug/nicegui'):
        ui.image('https://picsum.photos/id/41/640/360').classes('w-64')


doc.reference(ui.link)
