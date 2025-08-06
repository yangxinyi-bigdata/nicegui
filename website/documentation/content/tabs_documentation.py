from nicegui import ui

from . import doc


@doc.demo('选项卡', '''
    元素 `ui.tabs`、`ui.tab`、`ui.tab_panels` 和 `ui.tab_panel` 类似于
    [Quasar 的选项卡](https://quasar.dev/vue-components/tabs) 和
    [选项卡面板](https://quasar.dev/vue-components/tab-panels) API。

    `ui.tabs` 创建选项卡的容器。例如，这可以放在 `ui.header` 中。
    `ui.tab_panels` 创建带有实际内容的选项卡面板容器。
    每个 `ui.tab_panel` 都与一个 `ui.tab` 元素关联。
''')
def main_demo() -> None:
    with ui.tabs().classes('w-full') as tabs:
        one = ui.tab('One')
        two = ui.tab('Two')
    with ui.tab_panels(tabs, value=two).classes('w-full'):
        with ui.tab_panel(one):
            ui.label('First tab')
        with ui.tab_panel(two):
            ui.label('Second tab')


@doc.demo('名称、标签、图标', '''
    `ui.tab` 元素有一个 `label` 属性，可用于显示与 `name` 不同的文本。
    `name` 也可以代替 `ui.tab` 对象来关联 `ui.tab` 和 `ui.tab_panel`。
    另外，每个选项卡都可以有一个 `icon`。
''')
def name_and_label():
    with ui.tabs() as tabs:
        ui.tab('h', label='Home', icon='home')
        ui.tab('a', label='About', icon='info')
    with ui.tab_panels(tabs, value='h').classes('w-full'):
        with ui.tab_panel('h'):
            ui.label('Main Content')
        with ui.tab_panel('a'):
            ui.label('Infos')


@doc.demo('编程方式切换选项卡', '''
    `ui.tabs` 和 `ui.tab_panels` 元素继承自 ValueElement，它有一个 `set_value` 方法。
    这可以用于编程方式切换选项卡。
''')
def switch_tabs():
    content = {'Tab 1': 'Content 1', 'Tab 2': 'Content 2', 'Tab 3': 'Content 3'}
    with ui.tabs() as tabs:
        for title in content:
            ui.tab(title)
    with ui.tab_panels(tabs).classes('w-full') as panels:
        for title, text in content.items():
            with ui.tab_panel(title):
                ui.label(text)

    ui.button('GoTo 1', on_click=lambda: panels.set_value('Tab 1'))
    ui.button('GoTo 2', on_click=lambda: tabs.set_value('Tab 2'))


@doc.demo('Vertical tabs with splitter', '''
    Like in [Quasar's vertical tabs example](https://quasar.dev/vue-components/tabs#vertical),
    we can combine `ui.splitter` and tab elements to create a vertical tabs layout.
''')
def vertical_tabs():
    with ui.splitter(value=30).classes('w-full h-56') as splitter:
        with splitter.before:
            with ui.tabs().props('vertical').classes('w-full') as tabs:
                mail = ui.tab('Mails', icon='mail')
                alarm = ui.tab('Alarms', icon='alarm')
                movie = ui.tab('Movies', icon='movie')
        with splitter.after:
            with ui.tab_panels(tabs, value=mail) \
                    .props('vertical').classes('w-full h-full'):
                with ui.tab_panel(mail):
                    ui.label('Mails').classes('text-h4')
                    ui.label('Content of mails')
                with ui.tab_panel(alarm):
                    ui.label('Alarms').classes('text-h4')
                    ui.label('Content of alarms')
                with ui.tab_panel(movie):
                    ui.label('Movies').classes('text-h4')
                    ui.label('Content of movies')


doc.reference(ui.tabs, title='Reference for ui.tabs')
doc.reference(ui.tabs, title='Reference for ui.tab')
doc.reference(ui.tabs, title='Reference for ui.tab_panels')
doc.reference(ui.tabs, title='Reference for ui.tab_panel')
