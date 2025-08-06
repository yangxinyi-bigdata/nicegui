from nicegui import events, ui

from ..windows import browser_window, python_window
from . import (
    add_style_documentation,
    colors_documentation,
    dark_mode_documentation,
    doc,
    element_filter_documentation,
    query_documentation,
)

doc.title('样式与外观')


@doc.demo('样式', '''
    NiceGUI 使用 [Quasar Framework](https://quasar.dev/)，因此具有其全部设计能力。
    每个 NiceGUI 元素都提供一个 `props` 方法，其内容被[传递给 Quasar 组件](https://justpy.io/quasar_tutorial/introduction/#props-of-quasar-components)：
    查看所有样式属性，请查看 [Quasar 文档](https://quasar.dev/vue-components/button#design)。
    带有前导 `:` 的属性可以包含在客户端上计算的 JavaScript 表达式。
    您也可以使用 `classes` 方法应用 [Tailwind CSS](https://v3.tailwindcss.com/) 实用类。

    如果您确实需要应用 CSS，可以使用 `style` 方法。这里的分隔符是 `;` 而不是空格。

    所有三个函数还提供 `remove` 和 `replace` 参数，以防在特定样式中不想要预定义的外观。
''')
def design_demo():
    ui.radio(['x', 'y', 'z'], value='x').props('inline color=green')
    ui.button(icon='touch_app').props('outline round').classes('shadow-lg')
    ui.label('Stylish!').style('color: #6E93D6; font-size: 200%; font-weight: 300')


doc.text('尝试为 NiceGUI 元素添加样式！', '''
    尝试一下
    [Tailwind CSS 类](https://v3.tailwindcss.com/)、
    [Quasar 属性](https://justpy.io/quasar_tutorial/introduction/#props-of-quasar-components)
    和 CSS 样式如何影响 NiceGUI 元素。
''')


@doc.ui
def styling_demo():
    with ui.row():
        ui.label('Select an element from those available and start styling it!').classes('mx-auto my-auto')
        select_element = ui.select({
            ui.label: 'ui.label',
            ui.checkbox: 'ui.checkbox',
            ui.switch: 'ui.switch',
            ui.input: 'ui.input',
            ui.textarea: 'ui.textarea',
            ui.button: 'ui.button',
        }, value=ui.button, on_change=lambda: live_demo_ui.refresh()).props('dense')

    @ui.refreshable
    def live_demo_ui():
        with ui.column().classes('w-full items-stretch gap-8 no-wrap min-[1500px]:flex-row'):
            with python_window(classes='w-full max-w-[44rem]'):
                with ui.column().classes('w-full gap-2'):
                    ui.markdown(f'''
                        ```py
                        from nicegui import ui

                        element = {select_element.options[select_element.value]}('element')
                        ```
                    ''').classes('mb-[-0.25em]')
                    with ui.row().classes('items-center gap-0 w-full'):
                        def handle_classes(e: events.ValueChangeEventArguments):
                            try:
                                element.classes(replace=e.value)
                            except ValueError:
                                pass
                        ui.markdown("`element.classes('`")
                        ui.input(on_change=handle_classes).classes('text-mono grow').props('dense hide-bottom-space')
                        ui.markdown("`')`")
                    with ui.row().classes('items-center gap-0 w-full'):
                        def handle_props(e: events.ValueChangeEventArguments):
                            element.props.clear()
                            if isinstance(element, (ui.button, ui.input, ui.textarea)):
                                element.props['label'] = 'element'
                            if isinstance(element, ui.button):
                                element.props['color'] = 'primary'
                            try:
                                element.props(e.value)
                            except ValueError:
                                pass
                            element.update()
                        ui.markdown("`element.props('`")
                        ui.input(on_change=handle_props).classes('text-mono grow').props('dense hide-bottom-space')
                        ui.markdown("`')`")
                    with ui.row().classes('items-center gap-0 w-full'):
                        def handle_style(e: events.ValueChangeEventArguments):
                            try:
                                element.style(replace=e.value)
                            except ValueError:
                                pass
                        ui.markdown("`element.style('`")
                        ui.input(on_change=handle_style).classes('text-mono grow').props('dense hide-bottom-space')
                        ui.markdown("`')`")
                    ui.markdown('''
                        ```py
                        ui.run()
                        ```
                    ''')
            with browser_window(classes='w-full max-w-[44rem] min-[1500px]:max-w-[20rem] min-h-[10rem] browser-window'):
                element: ui.element = select_element.value('element')
    live_demo_ui()


@doc.demo('Tailwind CSS', '''
    [Tailwind CSS](https://v3.tailwindcss.com/) 是一个用于快速构建自定义用户界面的 CSS 框架。
    NiceGUI 提供了一个流畅的、自动补全友好的界面，用于向 UI 元素添加 Tailwind 类。

    您可以通过浏览 `tailwind` 属性的方法来发现可用的类。
    构建器模式允许您将多个类链接在一起（如"标签 A"所示）。
    您也可以使用类列表调用 `tailwind` 属性（如"标签 B"所示）。

    尽管这与使用 `classes` 方法非常相似，但由于自动补全功能，它对 Tailwind 类来说更方便。

    最后但同样重要的是，您还可以预定义样式并将其应用于多个元素（标签 C 和 D）。

    请注意，有时 Tailwind 会被 Quasar 样式覆盖，例如当使用 `ui.button('Button').tailwind('bg-red-500')` 时。
    这是一个已知的限制，我们无法完全控制。
    但我们尝试提供像 `color` 参数这样的解决方案：`ui.button('Button', color='red-500')`。
''')
def tailwind_demo():
    from nicegui import Tailwind
    ui.label('Label A').tailwind.font_weight('extrabold').text_color('blue-600').background_color('orange-200')
    ui.label('Label B').tailwind('drop-shadow', 'font-bold', 'text-green-600')

    red_style = Tailwind().text_color('red-600').font_weight('bold')
    label_c = ui.label('Label C')
    red_style.apply(label_c)
    ui.label('Label D').tailwind(red_style)


@doc.demo('Tailwind CSS 层', '''
    Tailwind CSS 的 `@layer` 指令允许您定义可在 HTML 中使用的自定义类。
    NiceGUI 通过允许您向 `components` 层添加自定义类来支持此功能。
    这样，您可以定义自己的类并在 UI 元素中使用它们。
    在下面的示例中，我们定义了一个自定义类 `blue-box` 并将其应用于两个标签。
    请注意，样式标签的类型是 `text/tailwindcss` 而不是 `text/css`。
''')
def tailwind_layers():
    ui.add_head_html('''
        <style type="text/tailwindcss">
            @layer components {
                .blue-box {
                    @apply bg-blue-500 p-12 text-center shadow-lg rounded-lg text-white;
                }
            }
        </style>
    ''')

    with ui.row():
        ui.label('Hello').classes('blue-box')
        ui.label('world').classes('blue-box')


doc.intro(element_filter_documentation)
doc.intro(query_documentation)
doc.intro(colors_documentation)


@doc.demo('CSS 变量', '''
    您可以通过设置 CSS 变量来自定义 NiceGUI 的外观。
    目前，以下变量及其默认值可用：

    - `--nicegui-default-padding: 1rem`
    - `--nicegui-default-gap: 1rem`

''')
def css_variables_demo():
    # ui.add_css('''
    #     :root {
    #         --nicegui-default-padding: 0.5rem;
    #         --nicegui-default-gap: 3rem;
    #     }
    # ''')
    # with ui.card():
    #     ui.label('small padding')
    #     ui.label('large gap')
    # END OF DEMO
    with ui.card().classes('p-[0.5rem] gap-[3rem]'):
        ui.label('small padding')
        ui.label('large gap')


@doc.demo("覆盖 Tailwind 的默认样式", '''
    Tailwind 重置 HTML 元素的默认样式，如此示例中 `h2` 元素的字体大小。
    您可以通过添加类型为 `text/tailwindcss` 的样式标签来覆盖这些默认值。
    没有此类型，样式将被评估得太早，并被 Tailwind 覆盖。
''')
def overwrite_tailwind_style_demo():
    ui.add_head_html('''
        <style type="text/tailwindcss">
            h2 {
                font-size: 150%;
            }
        </style>
    ''')
    ui.html('<h2>Hello world!</h2>')


doc.intro(dark_mode_documentation)
doc.intro(add_style_documentation)


@doc.demo('使用其他 Vue UI 框架', '''
    **这是一个实验性功能。**
    **许多 NiceGUI 元素可能会损坏，API 可能会发生变化。**

    NiceGUI 默认使用 [Quasar Framework](https://quasar.dev/)。
    但是，您也可以尝试使用其他 Vue UI 框架，
    如 [Element Plus](https://element-plus.org/en-US/) 或 [Vuetify](https://vuetifyjs.com/en/)。
    为此，您需要将框架的 JavaScript 和 CSS 文件添加到 HTML 文档的头部，
    并通过扩展或替换 `app.config.vue_config_script` 来相应地配置 NiceGUI。

    *在 NiceGUI 2.21.0 中添加*
''')
def other_vue_ui_frameworks_demo():
    from nicegui import app

    # ui.add_body_html('''
    #     <link rel="stylesheet" href="//unpkg.com/element-plus/dist/index.css" />
    #     <script defer src="https://unpkg.com/element-plus"></script>
    # ''')
    # app.config.vue_config_script += '''
    #     app.use(ElementPlus);
    # '''

    with ui.element('el-button').on('click', lambda: ui.notify('Hi!')):
        ui.html('Element Plus button')

    ui.button('Quasar button', on_click=lambda: ui.notify('Ho!'))

    # END OF DEMO
    ui.add_css('''
        el-button {
            border: 1px solid #dcdfe6;
            border-radius: 4px;
            color: #606266;
            cursor: pointer;
            font-weight: 500;
            font-size: 14px;
            height: 32px;
            line-height: 1;
            padding: 8px 15px;
        }
        el-button:hover {
            background-color: rgb(235.9,245.3,255);
            border-color: rgb(197.7,225.9,255);
            color: rgb(64,158,255);
        }
        el-button:active {
            border-color: rgb(64,158,255);
        }
        body.dark el-button {
            border-color: #4c4d4f;
            color: #cfd3dc;
        }
        body.dark el-button:hover {
            background-color: rgb(24.4, 33.8, 43.5);
            border-color: rgb(33.2, 61.4, 90.5);
            color: rgb(64, 158, 255);
        }
        body.dark el-button:active {
            border-color: rgb(64, 158, 255);
        }
    ''')
