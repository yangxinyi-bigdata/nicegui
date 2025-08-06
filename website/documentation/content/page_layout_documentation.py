from nicegui import ui

from . import doc


@doc.auto_execute
@doc.demo('页面布局', '''
    使用 `ui.header`、`ui.footer`、`ui.left_drawer` 和 `ui.right_drawer`，您可以向页面添加其他布局元素。
    `fixed` 参数控制元素是否应该滚动或保持固定在屏幕上。
    `top_corner` 和 `bottom_corner` 参数指示抽屉是否应该扩展到页面的顶部或底部。
    有关可能的属性的更多信息，请参见 <https://quasar.dev/layout/header-and-footer> 和 <https://quasar.dev/layout/drawer>。
    使用 `ui.page_sticky`，您可以在屏幕上"粘性"放置一个元素。
    有关更多信息，请参见 <https://quasar.dev/layout/page-sticky>。
''')
def page_layout_demo():
    @ui.page('/page_layout')
    def page_layout():
        ui.label('CONTENT')
        [ui.label(f'Line {i}') for i in range(100)]
        with ui.header(elevated=True).style('background-color: #3874c8').classes('items-center justify-between'):
            ui.label('HEADER')
            ui.button(on_click=lambda: right_drawer.toggle(), icon='menu').props('flat color=white')
        with ui.left_drawer(top_corner=True, bottom_corner=True).style('background-color: #d7e3f4'):
            ui.label('LEFT DRAWER')
        with ui.right_drawer(fixed=False).style('background-color: #ebf1fa').props('bordered') as right_drawer:
            ui.label('RIGHT DRAWER')
        with ui.footer().style('background-color: #3874c8'):
            ui.label('FOOTER')

    ui.link('show page with fancy layout', page_layout)


doc.reference(ui.header, title='ui.header 参考')
doc.reference(ui.left_drawer, title='ui.left_drawer 参考')
doc.reference(ui.right_drawer, title='ui.right_drawer 参考')
doc.reference(ui.footer, title='ui.footer 参考')
doc.reference(ui.page_sticky, title='ui.page_sticky 参考')
