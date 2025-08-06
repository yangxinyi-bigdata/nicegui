from nicegui import ui

from . import (
    doc,
    section_action_events,
    section_audiovisual_elements,
    section_binding_properties,
    section_configuration_deployment,
    section_controls,
    section_data_elements,
    section_page_layout,
    section_pages_routing,
    section_styling_appearance,
    section_testing,
    section_text_elements,
)
from ...style import subheading

doc.title('*NiceGUI* 文档', '参考、演示和更多')

doc.text('概览', '''
    NiceGUI 是一个开源的 Python 库，用于编写在浏览器中运行的图形用户界面。
    它的学习曲线非常平缓，同时仍提供高级自定义选项。
    NiceGUI 遵循后端优先的理念：
    它处理所有 Web 开发细节。
    您可以专注于编写 Python 代码。
    这使其成为各种项目的理想选择，包括短脚本、仪表板、机器人项目、
    IoT 解决方案、智能家居自动化和机器学习。
''')

doc.text('如何使用本指南', '''
    本文档解释了如何使用 NiceGUI。
    每个瓦片都详细涵盖了一个 NiceGUI 主题。
    建议先阅读整个介绍页面，然后根据需要参考其他部分。
''')

doc.text('基本概念', '''
    NiceGUI 提供 UI _元素_，如按钮、滑块、文本、图像、图表等。
    您的应用程序将这些组件组装成 _页面_。
    当用户与页面上的项目交互时，NiceGUI 会触发一个 _事件_（或 _动作_）。
    您定义代码来 _处理_ 每个事件，例如当用户单击按钮、修改值或操作滑块时要做什么。
    元素也可以绑定到 _模型_（数据对象），当模型值变化时自动更新用户界面。

    元素使用"声明式 UI"或"基于代码的 UI"在页面上排列。
    这意味着您也可以直接在代码中编写网格、卡片、选项卡、轮播、展开区域、菜单等布局结构。
    这个概念在 Flutter 和 SwiftUI 中已经流行起来。
    为了提高可读性，NiceGUI 利用 Python 的 `with ...` 语句。
    这个上下文管理器提供了一种很好的方式来缩进代码，使其类似于 UI 的布局。

    样式和外观可以通过多种方式控制。
    大多数元素接受可选参数来更改常见的样式和行为，例如按钮图标或文本颜色。
    因为 NiceGUI 是一个 Web 框架，您可以用 CSS 更改元素的几乎所有外观。
    但元素也提供 `.classes` 和 `.props` 方法来应用 Tailwind CSS 和 Quasar 属性，
    这些属性更高级，在您掌握后日常使用起来更简单。
''')

doc.text('动作、事件和任务', '''
    NiceGUI 使用 async/await 事件循环来实现并发，这既节省资源，又具有不必担心线程安全性的巨大优势。
    本节展示了如何处理用户输入和其他事件，如计时器和键盘绑定。
    它还描述了将长时间运行的任务包装在异步函数中的辅助函数，以保持 UI 响应性。
    请记住，所有 UI 更新都必须在主线程及其事件循环上进行。
''')

doc.text('实现', '''
    NiceGUI 是用由 HTTP 服务器（FastAPI）提供的 HTML 组件实现的，即使是原生窗口也是如此。
    如果您已经了解 HTML，一切都会感到非常熟悉。
    如果您不了解 HTML，那也没关系！
    NiceGUI 抽象了细节，因此您可以专注于创建美观的界面，而不必担心它们是如何实现的。
''')

doc.text('运行 NiceGUI 应用程序', '''
    部署 NiceGUI 有几种选项。
    默认情况下，NiceGUI 在 localhost 上运行服务器，并将您的应用程序作为本地机器上的私人网页运行。
    以这种方式运行时，您的应用程序出现在 Web 浏览器窗口中。
    您也可以在与 Web 浏览器分离的原生窗口中运行 NiceGUI。
    或者您可以在处理许多客户端的服务器上运行 NiceGUI - 您正在阅读的这个网站就是由 NiceGUI 提供的。

    使用组件创建应用程序页面后，您调用 `ui.run()` 来启动 NiceGUI 服务器。
    `ui.run` 的可选参数设置服务器绑定的网络地址和端口、
    应用程序是否以原生模式运行、初始窗口大小和许多其他选项。
    _配置和部署_ 部分涵盖了 `ui.run()` 函数及其基于的 FastAPI 框架的选项。
''')

doc.text('自定义', '''
    如果您想在应用程序中进行更多自定义，可以使用底层的 Tailwind 类和 Quasar 组件
    来控制组件的样式或行为。
    您也可以通过子类化现有的 NiceGUI 组件或从 Quasar 导入新组件来扩展可用组件。
    所有这些都是可选的。
    开箱即用，NiceGUI 提供了制作现代、时尚、响应式用户界面所需的一切。
''')

doc.text('测试', '''
    NiceGUI 提供了一个基于 [pytest](https://docs.pytest.org/) 的全面测试框架，
    它允许您自动化用户界面的测试。
    您可以利用 `screen` 夹具，它启动一个真实的（无头）浏览器来与您的应用程序交互。
    如果您有特定于浏览器的行为需要测试，这非常有用。

    但大多数情况下，NiceGUI 新引入的 `user` 夹具更适合：
    它只在 Python 级别上模拟用户交互，因此速度极快。
    这样，经典的[测试金字塔](https://martinfowler.com/bliki/TestPyramid.html)不再适用，
    其中 UI 测试被认为是缓慢和昂贵的。
    这可以对您的开发速度、质量和信心产生巨大影响。
''')

tiles = [
    (section_text_elements, '''
        像 `ui.label`、`ui.markdown`、`ui.restructured_text` 和 `ui.html` 这样的元素可用于显示文本和其他内容。
    '''),
    (section_controls, '''
        NiceGUI 提供了多种用户交互元素，例如 `ui.button`、`ui.slider`、`ui.inputs` 等。
    '''),
    (section_audiovisual_elements, '''
        您可以使用 `ui.image`、`ui.audio`、`ui.video` 等元素来显示视听内容。
    '''),
    (section_data_elements, '''
        有几种用于显示数据的元素，例如 `ui.table`、`ui.aggrid`、`ui.highchart`、`ui.echart` 等。
    '''),
    (section_binding_properties, '''
        要自动更新 UI 元素，您可以将它们相互绑定或绑定到您的数据模型。
    '''),
    (section_page_layout, '''
        本节涵盖了基础技术以及构建 UI 的几种元素。
    '''),
    (section_styling_appearance, '''
        NiceGUI 允许通过各种方式自定义 UI 元素的外观，包括 CSS、Tailwind CSS 和 Quasar 属性。
    '''),
    (section_action_events, '''
        本节涵盖了计时器、UI 事件和 NiceGUI 应用程序的生命周期。
    '''),
    (section_pages_routing, '''
        NiceGUI 应用程序可以由多个页面和其他 FastAPI 端点组成。
    '''),
    (section_configuration_deployment, '''
        无论您想在本地还是服务器上运行应用程序，原生还是在浏览器中，我们都为您提供了支持。
    '''),
    (section_testing, '''
        编写自动化 UI 测试，在无头浏览器（慢速）中运行或在 Python 中完全模拟（快速）。
     '''),
]


@doc.extra_column
def create_tiles():
    with ui.row().classes('items-center content-between'):
        ui.label('如果您喜欢 NiceGUI，请成为')
        ui.html('<iframe src="https://github.com/sponsors/zauberzeug/button" title="Sponsor zauberzeug" height="32" width="114" style="border: 0; border-radius: 6px;"></iframe>')
    for documentation, description in tiles:
        page = doc.get_page(documentation)
        with ui.link(target=f'/documentation/{page.name}') \
                .classes('bg-[#5898d420] p-4 self-stretch rounded flex flex-col gap-2') \
                .style('box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1)'):
            if page.title:
                ui.label(page.title.replace('*', '')).classes(replace='text-2xl')
            ui.markdown(description).classes(replace='bold-links arrow-links')


@doc.ui
def map_of_nicegui():
    ui.separator().classes('mt-6')
    subheading('NiceGUI 地图', anchor_name='map-of-nicegui')
    ui.add_css('''
        .map-of-nicegui a code {
            font-weight: bold;
        }
    ''')
    ui.markdown('''
        此概览显示了 NiceGUI 的结构。
        它是 NiceGUI 命名空间及其内容的地图。
        它并不详尽，但能让您很好地了解可用的功能。
        一个持续的目标是使这张地图更完整，并添加缺失的文档链接。

        #### `ui`

        UI 元素和运行 NiceGUI 应用程序的其他基本要素。

        - [`ui.element`](/documentation/element): 所有 UI 元素的基类
            - 自定义：
                - `.props()` 和 [`.default_props()`](/documentation/element#default_props): 添加 Quasar 属性和常规 HTML 属性
                - `.classes()` 和 [`.default_classes()`](/documentation/element#default_classes): 添加 Quasar、Tailwind 和自定义 HTML 类
                - [`.tailwind`](/documentation/section_styling_appearance#tailwind_css): 添加 Tailwind 类的便捷 API
                - `.style()` 和 [`.default_style()`](/documentation/element#default_style): 添加 CSS 样式定义
                - [`.tooltip()`](/documentation/tooltip): 为元素添加工具提示
                - [`.mark()`](/documentation/element_filter#markers): 标记元素以便使用 [ElementFilter](/documentation/element_filter) 查询
            - 交互：
                - [`.on()`](/documentation/generic_events): 添加 Python 和 JavaScript 事件处理器
                - `.update()`: 向客户端发送更新（大多数情况下自动完成）
                - `.run_method()`: 在客户端运行方法
                - `.get_computed_prop()`: 获取在客户端计算的属性值
            - 层次结构：
                - `with ...:` 以声明方式嵌套元素
                - `__iter__`: 所有子元素的迭代器
                - `ancestors`: 元素的父元素、祖父元素等的迭代器
                - `descendants`: 所有子元素、孙元素等的迭代器
                - `slots`: 命名插槽的字典
                - `add_slot`: 用 NiceGUI 元素填充新插槽或用模板字符串填充作用域插槽
                - [`clear`](/documentation/section_page_layout#clear_containers): 删除所有子元素
                - [`move`](/documentation/element#move_elements): 将元素移动到新的父元素
                - `remove`: 删除子元素
                - `delete`: 删除元素及其所有子元素
                - `is_deleted`: 元素是否已被删除
        - 元素：
            - [`ui.aggrid`](/documentation/aggrid)
            - [`ui.audio`](/documentation/audio)
            - [`ui.avatar`](/documentation/avatar)
            - [`ui.badge`](/documentation/badge)
            - [`ui.button`](/documentation/button)
            - [`ui.button_group`](/documentation/button_group)
            - [`ui.card`](/documentation/card), `ui.card_actions`, `ui.card_section`
            - [`ui.carousel`](/documentation/carousel), `ui.carousel_slide`
            - [`ui.chat_message`](/documentation/chat_message)
            - [`ui.checkbox`](/documentation/checkbox)
            - [`ui.chip`](/documentation/chip)
            - [`ui.circular_progress`](/documentation/circular_progress)
            - [`ui.code`](/documentation/code)
            - [`ui.codemirror`](/documentation/codemirror)
            - [`ui.color_input`](/documentation/color_input)
            - [`ui.color_picker`](/documentation/color_picker)
            - [`ui.column`](/documentation/column)
            - [`ui.context_menu`](/documentation/context_menu)
            - [`ui.date`](/documentation/date)
            - [`ui.dialog`](/documentation/dialog)
            - [`ui.dropdown_button`](/documentation/button_dropdown)
            - [`ui.echart`](/documentation/echart)
            - [`ui.editor`](/documentation/editor)
            - [`ui.expansion`](/documentation/expansion)
            - [`ui.fab`](/documentation/fab), `ui.fab_action`
            - [`ui.grid`](/documentation/grid)
            - [`ui.highchart`](/documentation/highchart)
            - [`ui.html`](/documentation/html)
            - [`ui.icon`](/documentation/icon)
            - [`ui.image`](/documentation/image)
            - [`ui.input`](/documentation/input)
            - [`ui.input_chips`](/documentation/input_chips)
            - [`ui.interactive_image`](/documentation/interactive_image)
            - `ui.item`, `ui.item_label`, `ui.item_section`
            - [`ui.joystick`](/documentation/joystick)
            - [`ui.json_editor`](/documentation/json_editor)
            - [`ui.knob`](/documentation/knob)
            - [`ui.label`](/documentation/label)
            - [`ui.leaflet`](/documentation/leaflet)
            - [`ui.line_plot`](/documentation/line_plot)
            - [`ui.linear_progress`](/documentation/linear_progress)
            - [`ui.link`](/documentation/link), `ui.link_target`
            - [`ui.list`](/documentation/list)
            - [`ui.log`](/documentation/log)
            - [`ui.markdown`](/documentation/markdown)
            - [`ui.matplotlib`](/documentation/matplotlib)
            - [`ui.menu`](/documentation/menu), `ui.menu_item`
            - [`ui.mermaid`](/documentation/mermaid)
            - [`ui.notification`](/documentation/notification)
            - [`ui.number`](/documentation/number)
            - [`ui.pagination`](/documentation/pagination)
            - [`ui.plotly`](/documentation/plotly)
            - [`ui.pyplot`](/documentation/pyplot)
            - [`ui.radio`](/documentation/radio)
            - [`ui.rating`](/documentation/rating)
            - [`ui.range`](/documentation/range)
            - [`ui.restructured_text`](/documentation/restructured_text)
            - [`ui.row`](/documentation/row)
            - [`ui.scene`](/documentation/scene), [`ui.scene_view`](/documentation/scene#scene_view)
            - [`ui.scroll_area`](/documentation/scroll_area)
            - [`ui.select`](/documentation/select)
            - [`ui.separator`](/documentation/separator)
            - [`ui.skeleton`](/documentation/skeleton)
            - [`ui.slide_item`](/documentation/slide_item)
            - [`ui.slider`](/documentation/slider)
            - [`ui.space`](/documentation/space)
            - [`ui.spinner`](/documentation/spinner)
            - [`ui.splitter`](/documentation/splitter)
            - [`ui.stepper`](/documentation/stepper), `ui.step`, `ui.stepper_navigation`
            - [`ui.sub_pages`](/documentation/sub_pages)
            - [`ui.switch`](/documentation/switch)
            - [`ui.tabs`](/documentation/tabs), `ui.tab`, `ui.tab_panels`, `ui.tab_panel`
            - [`ui.table`](/documentation/table)
            - [`ui.textarea`](/documentation/textarea)
            - [`ui.time`](/documentation/time)
            - [`ui.timeline`](/documentation/timeline), `ui.timeline_entry`
            - [`ui.toggle`](/documentation/toggle)
            - [`ui.tooltip`](/documentation/tooltip)
            - [`ui.tree`](/documentation/tree)
            - [`ui.upload`](/documentation/upload)
            - [`ui.video`](/documentation/video)
        - 特殊布局 [元素](/documentation/page_layout)：
            - `ui.header`
            - `ui.footer`
            - `ui.drawer`, `ui.left_drawer`, `ui.right_drawer`
            - `ui.page_sticky`
        - 特殊函数和对象：
            - [`ui.add_body_html`](/documentation/section_pages_routing#add_html_to_the_page) 和
                [`ui.add_head_html`](/documentation/section_pages_routing#add_html_to_the_page): 向页面主体和头部添加 HTML
            - [`ui.add_css`](/documentation/add_style#add_css_style_definitions_to_the_page),
                [`ui.add_sass`](/documentation/add_style#add_sass_style_definitions_to_the_page) 和
                [`ui.add_scss`](/documentation/add_style#add_scss_style_definitions_to_the_page): 向页面添加 CSS、SASS 和 SCSS
            - [`ui.clipboard`](/documentation/clipboard): 与浏览器剪贴板交互
            - [`ui.colors`](/documentation/colors): 为页面定义主色主题
            - `ui.context`: 获取当前 UI 上下文，包括 `client` 和 `request` 对象
            - [`ui.dark_mode`](/documentation/dark_mode): 获取和设置页面上的深色模式
            - [`ui.download`](/documentation/download): 向客户端下载文件
            - [`ui.fullscreen`](/documentation/fullscreen): 进入、退出和切换全屏模式
            - [`ui.keyboard`](/documentation/keyboard): 定义键盘事件处理器
            - [`ui.navigate`](/documentation/navigate): 让浏览器导航到另一个位置
            - [`ui.notify`](/documentation/notification): 显示通知
            - [`ui.on`](/documentation/generic_events#custom_events): 注册事件处理器
            - [`ui.page_title`](/documentation/page_title): 更改当前页面标题
            - [`ui.query`](/documentation/query): 查询客户端上的 HTML 元素以修改属性、类和样式定义
            - [`ui.run`](/documentation/run) 和 `ui.run_with`: 运行应用程序（独立或附加到 FastAPI 应用程序）
            - [`ui.run_javascript`](/documentation/run#run_custom_javascript_on_the_client_side): 在客户端运行自定义 JavaScript（可以使用 `getElement()`、`getHtmlElement()` 和 `emitEvent()`）
            - [`ui.teleport`](/documentation/teleport): 将元素传送到 HTML DOM 中的不同位置
            - [`ui.timer`](/documentation/timer): 定期运行函数或在延迟后运行一次
            - `ui.update`: 向客户端发送多个元素的更新
        - 装饰器：
            - [`ui.page`](/documentation/page): 定义页面（与自动生成的"自动索引页面"相对）
            - [`ui.refreshable`](/documentation/refreshable), `ui.refreshable_method`: 定义可刷新的 UI 容器
                （可以使用 [`ui.state`](/documentation/refreshable#refreshable_ui_with_reactive_state)）

        #### `app`

        应用程序范围的存储、挂载点和生命周期钩子。

        - [`app.storage`](/documentation/storage):
            - `app.storage.tab`: 存储在服务器的内存中，每个标签页唯一
            - `app.storage.client`: 存储在服务器的内存中，每个连接到页面的客户端唯一
            - `app.storage.user`: 存储在服务器的文件中，每个浏览器唯一
            - `app.storage.general`: 存储在服务器的文件中，在整个应用程序中共享
            - `app.storage.browser`: 存储在浏览器的本地存储中，每个浏览器唯一
        - [生命周期钩子](/documentation/section_action_events#events):
            - `app.on_connect()`: 客户端连接时调用
            - `app.on_disconnect()`: 客户端断开连接时调用
            - `app.on_startup()`: 应用程序启动时调用
            - `app.on_shutdown()`: 应用程序关闭时调用
            - `app.on_exception()`: 发生异常时调用
            - `app.on_page_exception()`: 构建页面时发生异常时调用
        - [`app.shutdown()`](/documentation/section_action_events#shut_down_nicegui): 关闭应用程序
        - 静态文件：
            - [`app.add_static_files()`](/documentation/section_pages_routing#add_a_directory_of_static_files),
                `app.add_static_file()`: 提供静态文件
            - [`app.add_media_files()`](/documentation/section_pages_routing#add_directory_of_media_files),
                `app.add_media_file()`: 提供媒体文件（支持流式传输）
        - [`app.native`](/documentation/section_configuration_deployment#native_mode): 在原生模式下运行时配置应用程序

        #### `html`

        [纯 HTML 元素](/documentation/html#other_html_elements)：

        `a`,
        `abbr`,
        `acronym`,
        `address`,
        `area`,
        `article`,
        `aside`,
        `audio`,
        `b`,
        `basefont`,
        `bdi`,
        `bdo`,
        `big`,
        `blockquote`,
        `br`,
        `button`,
        `canvas`,
        `caption`,
        `cite`,
        `code`,
        `col`,
        `colgroup`,
        `data`,
        `datalist`,
        `dd`,
        `del_`,
        `details`,
        `dfn`,
        `dialog`,
        `div`,
        `dl`,
        `dt`,
        `em`,
        `embed`,
        `fieldset`,
        `figcaption`,
        `figure`,
        `footer`,
        `form`,
        `h1`,
        `header`,
        `hgroup`,
        `hr`,
        `i`,
        `iframe`,
        `img`,
        `input_`,
        `ins`,
        `kbd`,
        `label`,
        `legend`,
        `li`,
        `main`,
        `map_`,
        `mark`,
        `menu`,
        `meter`,
        `nav`,
        `object_`,
        `ol`,
        `optgroup`,
        `option`,
        `output`,
        `p`,
        `param`,
        `picture`,
        `pre`,
        `progress`,
        `q`,
        `rp`,
        `rt`,
        `ruby`,
        `s`,
        `samp`,
        `search`,
        `section`,
        `select`,
        `small`,
        `source`,
        `span`,
        `strong`,
        `sub`,
        `summary`,
        `sup`,
        `svg`,
        `table`,
        `tbody`,
        `td`,
        `template`,
        `textarea`,
        `tfoot`,
        `th`,
        `thead`,
        `time`,
        `tr`,
        `track`,
        `u`,
        `ul`,
        `var`,
        `video`,
        `wbr`

        #### `background_tasks`

        在后台运行异步函数。

        - `create()`: 创建后台任务
        - `create_lazy()`: 防止两个同名任务同时运行
        - `await_on_shutdown`: 标记一个协程函数在关闭时等待（默认情况下所有后台任务都被取消）

        #### `run`

        在单独的线程和进程中运行 IO 和 CPU 密集型函数。

        - [`run.cpu_bound()`](/documentation/section_action_events#running_cpu-bound_tasks): 在单独的进程中运行 CPU 密集型函数
        - [`run.io_bound()`](/documentation/section_action_events#running_i_o-bound_tasks): 在单独的线程中运行 IO 密集型函数

        #### `binding`

        [将对象的属性相互绑定](/documentation/section_binding_properties)。

        - [`binding.BindableProperty`](/documentation/section_binding_properties#bindable_properties_for_maximum_performance): 用于最大性能的可绑定属性
        - [`binding.bindable_dataclass()`](/documentation/section_binding_properties#bindable_dataclass): 创建具有可绑定属性的数据类
        - `binding.bind()`, `binding.bind_from()`, `binding.bind_to()`: 绑定两个属性的方法

        #### `observables`

        可观察集合，当其内容变化时通知观察者。

        - `ObservableCollection`: 基类
        - `ObservableDict`: 可观察字典
        - `ObservableList`: 可观察列表
        - `ObservableSet`: 可观察集合

        #### `testing`

        编写自动化 UI 测试，在无头浏览器（慢速）中运行或在 Python 中完全模拟（快速）。

        - [`Screen`](/documentation/section_testing#screen_fixture) 夹具：启动真实的（无头）浏览器来与您的应用程序交互
        - [`User`](/documentation/section_testing#user_fixture) 夹具：在 Python 级别模拟用户交互（快速）
    ''').classes('map-of-nicegui arrow-links bold-links')
