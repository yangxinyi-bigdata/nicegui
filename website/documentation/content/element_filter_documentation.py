from nicegui import ElementFilter, ui

from . import doc


@doc.demo(ElementFilter)
def main_demo() -> None:
    from nicegui import ElementFilter

    with ui.card():
        ui.button('button A')
        ui.label('label A')

    with ui.card().mark('important'):
        ui.button('button B')
        ui.label('label B')

    ElementFilter(kind=ui.label).within(marker='important').classes('text-xl')


@doc.demo('查找具有文本属性的所有元素', '''
    `text` 属性由名为 `TextElement` 的混入类提供。
    如果我们按这样的混入类过滤，ElementFilter 本身将提供一个类型化的可迭代对象。
''')
def text_element() -> None:
    from nicegui import ElementFilter
    from nicegui.elements.mixins.text_element import TextElement

    with ui.card():
        ui.button('button')
        ui.icon('home')
        ui.label('label A')
        ui.label('label B')
        ui.html('HTML')

    # ui.label(', '.join(b.text for b in ElementFilter(kind=TextElement)))
    # END OF DEMO
    ui.label(', '.join(b.text for b in ElementFilter(kind=TextElement, local_scope=True)))


@doc.demo('标记', '''
    标记是用字符串标记元素的简单方法，该字符串可以被 `ElementFilter` 查询。
''')
def marker_demo() -> None:
    from nicegui import ElementFilter

    with ui.card().mark('red'):
        ui.label('label A')
    with ui.card().mark('strong'):
        ui.label('label B')
    with ui.card().mark('red strong'):
        ui.label('label C')

    # ElementFilter(marker='red').classes('bg-red-200')
    # ElementFilter(marker='strong').classes('text-bold')
    # ElementFilter(marker='red strong').classes('bg-red-600 text-white')
    # END OF DEMO
    ElementFilter(marker='red', local_scope=True).classes('bg-red-200')
    ElementFilter(marker='strong', local_scope=True).classes('text-bold')
    ElementFilter(marker='red strong', local_scope=True).classes('bg-red-600 text-white')


@doc.auto_execute
@doc.demo('在其他页面上查找元素', '''
    您可以使用 `app.clients` 迭代器将元素过滤器应用于特定页面的所有客户端。
''')
def multicasting():
    from nicegui import app
    import time

    @ui.page('/log')
    def page():
        ui.log()

    def log_time():
        for client in app.clients('/log'):
            with client:
                for log in ElementFilter(kind=ui.log):
                    log.push(f'{time.strftime("%H:%M:%S")}')

    ui.button('Log current time', on_click=log_time)
    ui.link('Open log', '/log', new_tab=True)


doc.reference(ElementFilter)
