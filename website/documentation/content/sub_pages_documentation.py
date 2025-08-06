from nicegui import PageArguments, ui
from typing import Callable, Dict, Any

from . import doc


class FakeSubPages(ui.column):

    def __init__(self, routes: Dict[str, Callable], *, data: Dict[str, Any] = {}) -> None:
        super().__init__()
        self.routes = routes
        self.data = data

    def init(self) -> None:
        self._render('/')
        self.move()  # move to end

    def link(self, text: str, route: str) -> None:
        ui.label(text).classes('nicegui-link cursor-pointer').on('click', lambda: self._render(route))

    def _render(self, route: str) -> None:
        self.clear()
        with self:
            ui.timer(0, lambda: self.routes[route](**self.data), once=True)  # NOTE: timer for sync and async functions


class FakeArguments:

    def __init__(self, **kwargs: Any) -> None:
        self.query_parameters = kwargs


@doc.demo('子页面', '''
    子页面提供基于 URL 的不同视图之间的导航。
    这允许您轻松构建单页面应用程序（SPA）。
    `ui.sub_pages` 元素本身充当当前活动子页面的容器。
    您只需要为每个视图构建器函数提供路由。
    当 URL 更改时，NiceGUI 负责替换内容而不会触发完整的页面重新加载。

    **注意：这是一个实验性功能，API 可能会发生变化。**
''')
def main_demo() -> None:
    from uuid import uuid4

    # @ui.page('/')
    # @ui.page('/{_:path}')  # NOTE: our page should catch all paths
    # def index():
    #     ui.label(f'This ID {str(uuid4())[:6]} changes only on reload.')
    #     ui.separator()
    #     ui.sub_pages({'/': main, '/other': other})

    def main():
        ui.label('Main page content')
        # ui.link('Go to other page', '/other')
        sub_pages.link('Go to other page', '/other')  # HIDE

    def other():
        ui.label('Another page content')
        # ui.link('Go to main page', '/')
        sub_pages.link('Go to main page', '/')  # HIDE

    # END OF DEMO
    ui.label(f'This ID {str(uuid4())[:6]} changes only on reload.')
    ui.separator()
    sub_pages = FakeSubPages({'/': main, '/other': other})
    sub_pages.init()


@doc.demo('向子页面传递参数', '''
    如果子页面需要来自其父页面的数据，可以将 `data` 字典传递给 `ui.sub_pages` 元素。
    数据将作为子页面函数中的关键字参数或作为 `PageArguments.data` 对象可用。
''')
def parameters_demo():
    # @ui.page('/')
    # @ui.page('/{_:path}') # NOTE: our page should catch all paths
    # def index():
    #     with ui.row():
    #         ui.label('Title:')
    #         title = ui.label()
    #     ui.separator()
    #     ui.sub_pages({
    #        '/': main,
    #        '/other': other,
    #     }, data={'title': title})

    def main(title: ui.label):
        title.text = 'Main page content'
        # ui.button('Go to other page', on_click=lambda: ui.navigate.to('/other'))
        sub_pages.link('Go to other page', '/other')  # HIDE

    def other(title: ui.label):
        title.text = 'Other page content'
        # ui.button('Go to main page', on_click=ui.navigate.to('/'))
        sub_pages.link('Go to main page', '/')  # HIDE

    # END OF DEMO
    with ui.row():
        ui.label('Title:')
        title = ui.label()
    ui.separator()
    sub_pages = FakeSubPages({'/': main, '/other': other}, data={'title': title})
    sub_pages.init()


@doc.demo('异步子页面', '''
    子页面也适用于异步构建器函数。
''')
def async_demo():
    import asyncio

    # @ui.page('/')
    # @ui.page('/{_:path}')
    # def index():
    #     with ui.row():
    #         ui.link('main', '/')
    #         ui.link('other', '/other')
    #     ui.sub_pages({'/': main, '/other': lambda: other('other page')})

    async def main():
        ui.label('main page').classes('font-bold')
        await asyncio.sleep(2)
        ui.label('after 2 sec')

    async def other(title: str):
        ui.label(title).classes('font-bold')
        await asyncio.sleep(1)
        ui.label('after 1 sec')

    # END OF DEMO
    sub_pages = FakeSubPages({'/': main, '/other': lambda: other('other page')})
    with ui.row():
        sub_pages.link('main', '/')
        sub_pages.link('other', '/other')
    sub_pages.init()


@doc.demo('添加子页面', '''
    有时在创建 `ui.sub_pages` 元素时并不知道所有路由。
    在这种情况下，可以使用 `add` 方法在元素创建后添加路由。
    这也可以用于传递应该放置在 `ui.sub_pages` 容器下方的元素。
''')
def adding_sub_pages_demo() -> None:
    # @ui.page('/')
    # @ui.page('/{_:path}') # NOTE: our page should catch all paths
    # def index():
    #     pages = ui.sub_pages()
    #     ui.separator()
    #     footer = ui.label()
    #     pages.add('/', lambda: main(footer))
    #     pages.add('/other', lambda: other(footer))

    def main(footer: ui.label):
        footer.text = 'normal footer'
        # ui.link('Go to other page', '/other')
        sub_pages.link('Go to other page', '/other')  # HIDE

    def other(footer: ui.label):
        footer.text = 'other footer'
        # ui.link('Go to main page', '/')
        sub_pages.link('Go to main page', '/')  # HIDE

    # END OF DEMO
    sub_pages = FakeSubPages({'/': lambda: main(footer), '/other': lambda: other(footer)})
    sub_pages.init()
    ui.separator()
    footer = ui.label()


@doc.demo('使用 PageArguments', '''
    通过将参数类型提示为 `PageArguments`，
    子页面构建器函数可以获得对查询参数、路径参数等的统一访问。
''')
def page_arguments_demo():
    from nicegui import PageArguments

    # @ui.page('/')
    # @ui.page('/{_:path}') # NOTE: our page should catch all paths
    # def index():
    #     ui.link('msg=hello', '/?msg=hello')
    #     ui.link('msg=world', '/?msg=world')
    #     ui.sub_pages({'/': main})

    def main(args: PageArguments):
        ui.label(args.query_parameters.get('msg', 'no message'))

    # END OF DEMO
    sub_pages = FakeSubPages({
        '/': lambda: main(FakeArguments()),  # type: ignore
        '/?msg=hello': lambda: main(FakeArguments(msg='hello')),  # type: ignore
        '/?msg=world': lambda: main(FakeArguments(msg='world')),  # type: ignore
    })
    sub_pages.link('msg=hello', '/?msg=hello')
    sub_pages.link('msg=world', '/?msg=world')
    sub_pages.init()


@doc.demo('嵌套子页面', '''
    子页面元素可以嵌套以创建分层的页面结构。
    这些元素中的每一个通过以下方式确定它们应该处理路径的哪一部分：

    1. 从 `ui.context.client.sub_pages_router` 获取完整的 URL 路径，
    2. 移除由父元素处理的前导部分，
    3. 匹配具有最特定路径的路由，以及
    4. 将路径的剩余部分留给下一个元素（如果没有，则显示 404 错误）。
''')
def nested_sub_pages_demo():
    # @ui.page('/')
    # @ui.page('/{_:path}')  # NOTE: our page should catch all paths
    # def index():
    #     ui.link('Go to main', '/')
    #     ui.link('Go to other', '/other')
    #     ui.sub_pages({
    #         '/': main,
    #         '/other': other,
    #     }).classes('border-2 p-2')

    def main():
        ui.label('main page')

    def other():
        ui.label('sub page')
        # ui.link('Go to A', '/sub/a')
        # ui.link('Go to B', '/sub/b')
        # ui.sub_pages({
        #     '/': sub_main,
        #     '/a': sub_page_a,
        #     '/b': sub_page_b
        # }).classes('border-2 p-2')
        sub_pages = FakeSubPages({'/': sub_main, '/a': sub_page_a, '/b': sub_page_b}).classes('border-2 p-2')  # HIDE
        sub_pages.link('Go to main', '/')  # HIDE
        sub_pages.link('Go to A', '/a')  # HIDE
        sub_pages.link('Go to B', '/b')  # HIDE
        sub_pages.init()  # HIDE

    def sub_main():
        ui.label('sub main page')

    def sub_page_a():
        ui.label('sub A page')

    def sub_page_b():
        ui.label('sub B page')

    # END OF DEMO
    sub_pages = FakeSubPages({'/': main, '/other': other}).classes('border-2 p-2')
    sub_pages.link('Go to main', '/')
    sub_pages.link('Go to other', '/other')
    sub_pages.init()


doc.reference(ui.sub_pages, title='ui.sub_pages 参考')

doc.reference(PageArguments, title='PageArguments 参考')
