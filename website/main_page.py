import json
from pathlib import Path

from nicegui import ui

from . import documentation, example_card, svg
from .examples import examples
from .style import example_link, features, heading, link_target, section_heading, subtitle, title

SPONSORS = json.loads((Path(__file__).parent / 'sponsors.json').read_text(encoding='utf-8'))


def create() -> None:
    """创建主页面的内容。"""
    with ui.row().classes('w-full h-screen items-center gap-8 pr-4 no-wrap into-section'):
        svg.face(half=True).classes('stroke-black dark:stroke-white w-[200px] md:w-[230px] lg:w-[300px]')
        with ui.column().classes('gap-4 md:gap-8 pt-32'):
            title('认识 *NiceGUI*。')
            subtitle('让任何浏览器成为您 Python 代码的前端。') \
                .classes('max-w-[20rem] sm:max-w-[24rem] md:max-w-[30rem]')
            ui.link(target='#about').classes('scroll-indicator')

    with ui.row().classes('''
            dark-box min-h-screen no-wrap
            justify-center items-center flex-col md:flex-row
            py-20 px-8 lg:px-16
            gap-8 sm:gap-16 md:gap-8 lg:gap-16
        '''):
        link_target('about', '70px')
        with ui.column().classes('text-white max-w-4xl'):
            heading('通过按钮、对话框、3D 场景、图表等与 Python 交互。')
            with ui.column().classes('gap-2 bold-links arrow-links text-lg'):
                ui.markdown('''
                    NiceGUI 管理 Web 开发细节，让您专注于为各种应用编写 Python 代码，
                    包括机器人、物联网解决方案、智能家居自动化和机器学习。
                    设计为与 IoT 设置中的网络摄像头和 GPIO 引脚等连接外设流畅协作，
                    NiceGUI 简化了在一个地方管理所有代码的过程。
                    <br><br>
                    凭借平缓的学习曲线，NiceGUI 对初学者友好，
                    并为经验丰富的用户提供高级自定义功能，
                    确保基本任务的简单性和复杂项目的可行性。
                    <br><br><br>
                    可作为
                    [PyPI 包](https://pypi.org/project/nicegui/)、
                    [Docker 镜像](https://hub.docker.com/r/zauberzeug/nicegui) 和在
                    [GitHub](https://github.com/zauberzeug/nicegui) 上获取。
                ''')
        example_card.create()

    with ui.column().classes('w-full text-lg p-8 lg:p-16 max-w-[1600px] mx-auto'):
        link_target('installation')
        section_heading('安装', '*开始*使用')
        with ui.row().classes('w-full text-lg leading-tight grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-8'):
            with ui.column().classes('w-full max-w-md gap-2'):
                ui.html('<em>1.</em>').classes('text-3xl font-bold fancy-em')
                ui.markdown('创建 __main.py__').classes('text-lg')
                with documentation.python_window(classes='w-full h-52'):
                    ui.markdown('''
                        ```python\n
                        from nicegui import ui

                        ui.label('Hello NiceGUI!')

                        ui.run()
                        ```
                    ''')
            with ui.column().classes('w-full max-w-md gap-2'):
                ui.html('<em>2.</em>').classes('text-3xl font-bold fancy-em')
                ui.markdown('安装并启动').classes('text-lg')
                with documentation.bash_window(classes='w-full h-52'):
                    ui.markdown('''
                        ```bash
                        pip3 install nicegui
                        python3 main.py
                        ```
                    ''')
            with ui.column().classes('w-full max-w-md gap-2'):
                ui.html('<em>3.</em>').classes('text-3xl font-bold fancy-em')
                ui.markdown('享受！').classes('text-lg')
                with documentation.browser_window(classes='w-full h-52'):
                    ui.label('Hello NiceGUI!')
        with ui.expansion('...或使用 Docker 来运行您的 main.py').classes('w-full gap-2 bold-links arrow-links'):
            with ui.row().classes('mt-8 w-full justify-center items-center gap-8'):
                ui.markdown('''
                    使用我们的[多架构 Docker 镜像](https://hub.docker.com/repository/docker/zauberzeug/nicegui)
                    您可以在不安装任何包的情况下启动服务器。

                    该命令在当前目录中搜索 `main.py` 并使应用程序在 http://localhost:8888 上可用。
                ''').classes('max-w-xl')
                with documentation.bash_window(classes='max-w-lg w-full h-52'):
                    ui.markdown('''
                        ```bash
                        docker run -it --rm -p 8888:8080 \\
                            -v "$PWD":/app zauberzeug/nicegui
                        ```
                    ''')

    with ui.column().classes('w-full p-8 lg:p-16 bold-links arrow-links max-w-[1600px] mx-auto'):
        link_target('features')
        section_heading('功能', '*优雅地*编码')
        with ui.row().classes('w-full text-lg leading-tight grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-8'):
            features('swap_horiz', '交互', [
                '[按钮、开关、滑块、输入框等](/documentation/section_controls)',
                '[通知、对话框和菜单](/documentation/section_page_layout)',
                '[带 SVG 叠加层的交互式图像](/documentation/interactive_image)',
                '网页和[原生窗口应用程序](/documentation/section_configuration_deployment#native_mode)',
            ])
            features('space_dashboard', '布局', [
                '[导航栏、选项卡、面板等](/documentation/section_page_layout)',
                '使用行、列、网格和卡片进行分组',
                '[HTML](/documentation/html) 和 [Markdown](/documentation/markdown) 元素',
                '默认 flex 布局',
            ])
            features('insights', '可视化', [
                '[图表、图表、表格](/documentation/section_data_elements)、[音频/视频](/documentation/section_audiovisual_elements)',
                '[3D 场景](/documentation/scene)',
                '直接的[数据绑定](/documentation/section_binding_properties)',
                '内置的[数据刷新计时器](/documentation/timer)',
            ])
            features('brush', '样式', [
                '可自定义的[颜色主题](/documentation/section_styling_appearance#color_theming)',
                '自定义 CSS 和类',
                '材料设计的现代外观',
                '[Tailwind CSS](https://v3.tailwindcss.com/) 自动补全',
            ])
            features('source', '编码', [
                '多[页面](/documentation/page)路由',
                '代码更改时自动重新加载',
                '持久的[用户会话](/documentation/storage)',
                '超棒的[测试框架](/documentation/section_testing)',
            ])
            features('anchor', '基础', [
                '通用的 [Vue](https://vuejs.org/) 到 Python 桥接',
                '通过 [Quasar](https://quasar.dev/) 实现动态 GUI',
                '内容通过 [FastAPI](https://fastapi.tiangolo.com/) 提供服务',
                'Python 3.8+',
            ])

    with ui.column().classes('w-full p-8 lg:p-16 max-w-[1600px] mx-auto'):
        link_target('demos')
        section_heading('演示', '尝试*这个*')
        with ui.column().classes('w-full'):
            documentation.create_intro()

    with ui.column().classes('dark-box p-8 lg:p-16 my-16'):
        with ui.column().classes('mx-auto items-center gap-y-8 gap-x-32 lg:flex-row'):
            with ui.column().classes('gap-1 max-lg:items-center max-lg:text-center'):
                ui.markdown('浏览大量实时演示。') \
                    .classes('text-white text-2xl md:text-3xl font-medium')
                ui.html('有趣的事实：整个网站也是用 NiceGUI 编码的。') \
                    .classes('text-white text-lg md:text-xl')
            ui.link('文档', '/documentation').style('color: black !important') \
                .classes('rounded-full mx-auto px-12 py-2 bg-white font-medium text-lg md:text-xl')

    with ui.column().classes('w-full p-8 lg:p-16 max-w-[1600px] mx-auto'):
        link_target('examples')
        section_heading('深入示例', '选择您的*解决方案*')
        with ui.row().classes('w-full text-lg leading-tight grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-4'):
            for example in examples:
                example_link(example)

    with ui.column().classes('dark-box p-8 lg:p-16 my-16 bg-transparent border-y-2'):
        with ui.column().classes('mx-auto items-center gap-y-8 gap-x-32 lg:flex-row'):
            with ui.column().classes('max-lg:items-center max-lg:text-center'):
                link_target('sponsors')
                ui.markdown('NiceGUI 得到以下支持') \
                    .classes('text-2xl md:text-3xl font-medium')
                if SPONSORS['top']:
                    with ui.row(align_items='center'):
                        assert SPONSORS['total'] > 0
                        ui.markdown(f'''
                            我们的顶级{'赞助商' if len(SPONSORS['top']) == 1 else '赞助商们'}
                        ''')
                        for sponsor in SPONSORS['top']:
                            with ui.link(target=f'https://github.com/{sponsor}').classes('row items-center gap-2'):
                                ui.image(f'https://github.com/{sponsor}.png').classes('w-12 h-12 border')
                                ui.label(f'@{sponsor}')
                    ui.markdown(f'''
                        以及 {SPONSORS['total'] - len(SPONSORS['top'])} 位其他[赞助商](https://github.com/sponsors/zauberzeug)
                        和 {SPONSORS['contributors']} 位[贡献者](https://github.com/zauberzeug/nicegui/graphs/contributors)。
                    ''').classes('bold-links arrow-links')
                else:
                    ui.markdown(f'''
                        {SPONSORS['total']} 位[赞助商](https://github.com/sponsors/zauberzeug)
                        和 {SPONSORS['contributors']} 位[贡献者](https://github.com/zauberzeug/nicegui/graphs/contributors)。
                    ''').classes('bold-links arrow-links')
            with ui.link(target='https://github.com/sponsors/zauberzeug').style('color: black !important') \
                    .classes('rounded-full mx-auto px-12 py-2 border-2 border-[#3e6a94] font-medium text-lg md:text-xl'):
                with ui.row().classes('items-center gap-4'):
                    ui.icon('sym_o_favorite', color='#3e6a94')
                    ui.label('成为赞助商').classes('text-[#3e6a94]')

    with ui.row().classes('dark-box min-h-screen mt-16'):
        link_target('why', '70px')
        with ui.column().classes('''
                max-w-[1600px] m-auto
                py-20 px-8 lg:px-16
                items-center justify-center no-wrap flex-col md:flex-row gap-16
            '''):
            with ui.column().classes('gap-8'):
                heading('为什么？')
                with ui.column().classes('gap-2 text-xl text-white bold-links arrow-links'):
                    ui.markdown('''
                        我们在
                        [Zauberzeug](https://zauberzeug.com)
                        喜欢
                        [Streamlit](https://streamlit.io/)
                        但发现它在状态处理方面
                        [过于神奇](https://github.com/zauberzeug/nicegui/issues/1#issuecomment-847413651)。
                        在寻找一个替代的优秀 Python 简单图形用户界面库时，我们发现了
                        [JustPy](https://justpy.io/)。
                        虽然我们喜欢这种方法，但它对我们的日常使用来说太"底层 HTML"了。
                        但它启发我们使用
                        [Vue](https://vuejs.org/)
                        和
                        [Quasar](https://quasar.dev/)
                        作为前端。
                    ''')
                    ui.markdown('''
                        我们构建在
                        [FastAPI](https://fastapi.tiangolo.com/)
                        之上，它本身基于 ASGI 框架
                        [Starlette](https://www.starlette.io/)
                        和 ASGI Web 服务器
                        [Uvicorn](https://www.uvicorn.org/)
                        因为它们出色的性能和易用性。
                    ''')
            svg.face().classes('stroke-white shrink-0 w-[200px] md:w-[300px] lg:w-[450px]')
        with ui.column().classes('w-full p-4 items-end text-white self-end'):
            ui.link('版权声明与隐私政策', '/imprint_privacy').classes('text-sm')
