from nicegui import ui

from ..windows import bash_window, python_window
from . import doc, run_documentation

doc.title('配置与部署')


@doc.demo('URL', '''
    您可以通过 `app.urls` 访问 NiceGUI 应用可用的所有 URL 列表。
    URL 在 `app.on_startup` 中不可用，因为服务器尚未运行。
    相反，您可以在页面函数中访问它们，或使用 `app.urls.on_change` 注册回调。
''')
def urls_demo():
    from nicegui import app

    # @ui.page('/')
    # def index():
    #     for url in app.urls:
    #         ui.link(url, target=url)
    # END OF DEMO
    ui.link('https://nicegui.io', target='https://nicegui.io')


doc.intro(run_documentation)


@doc.demo('原生模式', '''
    您可以通过在 `ui.run` 函数中指定 `native=True` 来为 NiceGUI 启用原生模式。
    要自定义初始窗口大小和显示模式，请分别使用 `window_size` 和 `fullscreen` 参数。
    此外，您可以通过 `app.native.window_args` 和 `app.native.start_args` 提供额外的关键字参数。
    选择内部使用的 [pywebview 模块](https://pywebview.flowrl.com/api) 为 `webview.create_window` 和 `webview.start` 函数定义的任何参数。
    请注意，这些关键字参数将优先于 `ui.run` 中定义的参数。

    此外，您可以通过 `app.native.settings` 更改 `webview.settings`。

    在原生模式下，`app.native.main_window` 对象允许您访问底层窗口。
    它是 [pywebview 的 Window](https://pywebview.flowrl.com/api/#webview-window) 的异步版本。
''', tab=lambda: ui.label('NiceGUI'))
def native_mode_demo():
    from nicegui import app

    app.native.window_args['resizable'] = False
    app.native.start_args['debug'] = True
    app.native.settings['ALLOW_DOWNLOADS'] = True

    ui.label('app running in native mode')
    # ui.button('enlarge', on_click=lambda: app.native.main_window.resize(1000, 700))
    #
    # ui.run(native=True, window_size=(400, 300), fullscreen=False)
    # END OF DEMO
    ui.button('enlarge', on_click=lambda: ui.notify('window will be set to 1000x700 in native mode'))


# Currently, options passed via app.native are not used if they are set behind a main guard
# See discussion at: https://github.com/zauberzeug/nicegui/pull/4627
doc.text('', '''
    请注意，原生应用在单独的
    [进程](https://docs.python.org/3/library/multiprocessing.html#multiprocessing.Process)中运行。
    因此，在[主保护](https://docs.python.org/3/library/__main__.html#idiomatic-usage)下运行的代码中的任何配置更改都会被原生应用忽略。
    以下示例显示了工作配置和非工作配置之间的区别。
''')


@doc.ui
def native_main_guard():
    with ui.row().classes('w-full items-stretch'):
        with python_window('good_example.py', classes='max-w-lg w-full'):
            ui.markdown('''
                ```python
                from nicegui import app, ui

                app.native.window_args['resizable'] = False  # works

                if __name__ == '__main__':
                    ui.run(native=True, reload=False)
                ```
            ''')
        with python_window('bad_example.py', classes='max-w-lg w-full'):
            ui.markdown('''
                ```python
                from nicegui import app, ui

                if __name__ == '__main__':
                    app.native.window_args['resizable'] = False  # ignored

                    ui.run(native=True, reload=False)
                ```
            ''')


# Show a helpful workaround until issue is fixed upstream.
# For more info see: https://github.com/r0x0r/pywebview/issues/1078
doc.text('', '''
    如果 webview 在查找所需库时遇到问题，您可能会收到与 "WebView2Loader.dll" 相关的错误。
    要解决此问题，请尝试将 DLL 文件向上移动一个目录，例如：

    * 从 `.venv/Lib/site-packages/webview/lib/x64/WebView2Loader.dll`
    * 到 `.venv/Lib/site-packages/webview/lib/WebView2Loader.dll`
''')


@doc.demo('环境变量', '''
    您可以设置以下环境变量来配置 NiceGUI：

    - `MATPLOTLIB`（默认：true）可以设置为 `false` 以避免可能昂贵的 Matplotlib 导入。
        这将使 `ui.pyplot` 和 `ui.line_plot` 不可用。
    - `NICEGUI_STORAGE_PATH`（默认：本地 ".nicegui"）可以设置为更改存储文件的位置。
    - `MARKDOWN_CONTENT_CACHE_SIZE`（默认：1000）：在内存中缓存的 Markdown 内容片段的最大数量。
    - `RST_CONTENT_CACHE_SIZE`（默认：1000）：在内存中缓存的 ReStructuredText 内容片段的最大数量。
    - `NICEGUI_REDIS_URL`（默认：None，表示本地文件存储）：用于共享持久存储的 Redis 服务器的 URL。
    - `NICEGUI_REDIS_KEY_PREFIX`（默认："nicegui:"）：Redis 键的前缀。
''')
def env_var_demo():
    from nicegui.elements import markdown

    ui.label(f'Markdown content cache size is {markdown.prepare_content.cache_info().maxsize}')


@doc.demo('后台任务', '''
    `background_tasks.create()` 允许您在后台运行异步函数并返回任务对象。
    默认情况下，任务将在关闭期间自动取消。
    您可以使用 `@background_tasks.await_on_shutdown` 装饰器（在版本 2.16.0 中添加）来防止这种情况。
    这对于即使应用关闭时也需要完成的任务很有用。
''')
def background_tasks_demo():
    # import aiofiles
    import asyncio
    from nicegui import background_tasks

    results = {'answer': '?'}

    async def compute() -> None:
        await asyncio.sleep(1)
        results['answer'] = 42

    @background_tasks.await_on_shutdown
    async def backup() -> None:
        await asyncio.sleep(1)
        # async with aiofiles.open('backup.json', 'w') as f:
        #     await f.write(f'{results["answer"]}')
        # print('backup.json written', flush=True)

    ui.label().bind_text_from(results, 'answer', lambda x: f'answer: {x}')
    ui.button('Compute', on_click=lambda: background_tasks.create(compute()))
    ui.button('Backup', on_click=lambda: background_tasks.create(backup()))


doc.text('自定义 Vue 组件', '''
    您可以通过子类化 `ui.element` 并实现相应的 Vue 组件来创建自定义组件。
    ["自定义 Vue 组件"示例](https://github.com/zauberzeug/nicegui/tree/main/examples/custom_vue_component)
    演示了如何创建发出事件并从服务器接收更新的自定义计数器组件。

    ["签名板"示例](https://github.com/zauberzeug/nicegui/blob/main/examples/signature_pad)
    展示了如何使用 `package.json` 文件为自定义组件定义依赖项。
    这允许您在组件中通过 NPM 使用第三方库。

    最后但同样重要的是，["Node 模块集成"示例](https://github.com/zauberzeug/nicegui/blob/main/examples/node_module_integration)
    演示了如何创建 package.json 文件和 webpack.config.js 文件来将自定义 Vue 组件与其依赖项捆绑在一起。
''')

doc.text('服务器托管', '''
    要在服务器上部署您的 NiceGUI 应用，您需要在云基础设施上执行您的 `main.py`（或任何包含 `ui.run(...)` 的文件）。
    例如，您可以通过 [pip 安装 NiceGUI python 包](https://pypi.org/project/nicegui/) 并使用 systemd 或类似服务来启动主脚本。
    在大多数情况下，您将使用 `ui.run` 命令将端口设置为 80（如果要使用 HTTPS 则设置为 443），以便从外部轻松访问。

    一个方便的替代方案是使用我们的[预构建多架构 Docker 镜像](https://hub.docker.com/r/zauberzeug/nicegui)，其中包含所有必要的依赖项。
    使用此命令，您可以在公共端口 80 上启动当前目录中的 `main.py` 脚本：
''')


@doc.ui
def docker_run():
    with bash_window(classes='max-w-lg w-full h-44'):
        ui.markdown('''
            ```bash
            docker run -it --restart always \\
            -p 80:8080 \\
            -e PUID=$(id -u) \\
            -e PGID=$(id -g) \\
            -v $(pwd)/:/app/ \\
            zauberzeug/nicegui:latest
            ```
        ''')


doc.text('', '''
    演示假设 `main.py` 在 `ui.run` 命令中使用端口 8080（这是默认值）。
    `-d` 告诉 docker 在后台运行，`--restart always` 确保容器在应用崩溃或服务器重启时重新启动。
    当然，这也可以写在 Docker compose 文件中：
''')


@doc.ui
def docker_compose():
    with python_window('docker-compose.yml', classes='max-w-lg w-full h-60'):
        ui.markdown('''
            ```yaml
            app:
                image: zauberzeug/nicegui:latest
                restart: always
                ports:
                    - 80:8080
                environment:
                    - PUID=1000 # change this to your user id
                    - PGID=1000 # change this to your group id
                volumes:
                    - ./:/app/
            ```
        ''')


doc.text('', '''
    Docker 镜像中还有其他方便的功能，如非 root 用户执行和信号传递。
    更多细节，我们建议查看我们的 [Docker 示例](https://github.com/zauberzeug/nicegui/tree/main/examples/docker_image)。

    要使用 [HTTPS](https://fastapi.tiangolo.com/deployment/https/) 加密为您的应用程序提供服务，您可以通过多种方式提供 SSL 证书。
    例如，您可以直接将证书提供给 [Uvicorn](https://www.uvicorn.org/)（NiceGUI 基于它），方法是将相关的[选项](https://www.uvicorn.org/#command-line-options)传递给 `ui.run()`。
    如果同时提供了证书和密钥文件，应用程序将自动通过 HTTPS 提供服务：
''')


@doc.ui
def uvicorn_ssl():
    with python_window('main.py', classes='max-w-lg w-full'):
        ui.markdown('''
            ```python
            from nicegui import ui

            ui.run(
                port=443,
                ssl_certfile="<path_to_certfile>",
                ssl_keyfile="<path_to_keyfile>",
            )
            ```
        ''')


doc.text('', '''
    在生产环境中，我们还喜欢使用像 [Traefik](https://doc.traefik.io/traefik/) 或 [NGINX](https://www.nginx.com/) 这样的反向代理来为我们处理这些细节。
    查看我们的开发 [docker-compose.yml](https://github.com/zauberzeug/nicegui/blob/main/docker-compose.yml) 作为基于 traefik 的示例，或
    [这个示例 nginx.conf 文件](https://github.com/zauberzeug/nicegui/blob/main/examples/nginx_https/nginx.conf) 展示了如何使用 NGINX 处理 SSL 证书并
    反向代理到您的 NiceGUI 应用。

    您也可以查看[我们使用自定义 FastAPI 应用的演示](https://github.com/zauberzeug/nicegui/tree/main/examples/fastapi)。
    这将允许您进行非常灵活的部署，如 [FastAPI 文档](https://fastapi.tiangolo.com/deployment/) 中所述。
    请注意，需要额外的步骤来允许多个工作进程。
''')

doc.text('打包安装', '''
    NiceGUI 应用也可以使用基于 [PyInstaller](https://www.pyinstaller.org/) 的 `nicegui-pack` 捆绑成可执行文件。
    这允许您将应用作为可以在任何计算机上执行的单个文件分发。

    只需确保在主脚本中使用 `reload=False` 调用 `ui.run` 以禁用自动重新加载功能。
    运行下面的 `nicegui-pack` 命令将在 `dist` 文件夹中创建一个可执行文件 `myapp`：
''')


@doc.ui
def pyinstaller():
    with ui.row().classes('w-full items-stretch'):
        with python_window(classes='max-w-lg w-full'):
            ui.markdown('''
                ```python
                from nicegui import native, ui

                ui.label('Hello from PyInstaller')

                ui.run(reload=False, port=native.find_open_port())
                ```
            ''')
        with bash_window(classes='max-w-lg w-full'):
            ui.markdown('''
                ```bash
                nicegui-pack --onefile --name "myapp" main.py
                ```
            ''')


doc.text('', '''
    **打包提示：**

    - 构建 PyInstaller 应用时，您的主脚本可以通过使用 `ui.run(reload=False, native=True)` 使用原生窗口（而不是浏览器窗口）。
    `native` 参数可以是 `True` 或 `False`，取决于您想要原生窗口还是在用户的浏览器中启动页面 - 两者都可以在 PyInstaller 生成的应用中工作。

    - 为 `nicegui-pack` 指定 `--windowed` 将阻止终端控制台出现。
    但是，只有当您在 `ui.run` 命令中也指定了 `native=True` 时才应使用此选项。
    没有终端控制台，用户将无法通过按 Ctrl-C 退出应用。
    使用 `native=True` 选项，应用将在窗口关闭时自动关闭，正如预期的那样。

    - 为 `nicegui-pack` 指定 `--windowed` 将在 Mac 上创建一个 `.app` 文件，这可能更方便分发。
    当您双击应用运行它时，它不会显示任何控制台输出。
    您也可以使用 `./myapp.app/Contents/MacOS/myapp` 从命令行运行应用以查看控制台输出。

    - 为 `nicegui-pack` 指定 `--onefile` 将创建一个单一的可执行文件。
    虽然便于分发，但启动速度会较慢。
    这不是 NiceGUI 的错，而是 Pyinstaller 将内容压缩成单个文件，然后在运行前将所有内容解压缩到临时目录的方式。
    您可以通过从 `nicegui-pack` 命令中删除 `--onefile` 来缓解这个问题，
    并自己压缩生成的 `dist` 目录，分发它，
    您的最终用户只需解压缩一次即可开始使用，
    而不会由于 `--onefile` 标志而不断扩展文件。

    - 不同选项的用户体验总结：

        | `nicegui-pack`           | `ui.run(...)`  | 说明 |
        | :---                     | :---           | :---        |
        | `onefile`                | `native=False` | 在 `dist/` 中生成单一可执行文件，在浏览器中运行 |
        | `onefile`                | `native=True`  | 在 `dist/` 中生成单一可执行文件，在弹出窗口中运行 |
        | `onefile` 和 `windowed` | `native=True`  | 在 `dist/` 中生成单一可执行文件（在 Mac 上生成适当的 `dist/myapp.app` 包含图标），在弹出窗口中运行，不出现控制台 |
        | `onefile` 和 `windowed` | `native=False` | 避免（无法退出应用） |
        | 都不指定                |                | 创建一个 `dist/myapp` 目录，可以手动压缩并分发；使用 `dist/myapp/myapp` 运行 |

    - 如果您使用 Python 虚拟环境，请确保在虚拟环境中 `pip install pyinstaller`，
    以便使用正确的 PyInstaller，否则由于使用了错误版本的 PyInstaller，您可能会得到损坏的应用。
    这就是为什么 `nicegui-pack` 使用 `python -m PyInstaller` 而不仅仅是 `pyinstaller` 来调用 PyInstaller。
''')


@doc.ui
def install_pyinstaller():
    with bash_window(classes='max-w-lg w-full h-42 self-center'):
        ui.markdown('''
            ```bash
            python -m venv venv
            source venv/bin/activate
            pip install nicegui
            pip install pyinstaller
            ```
        ''')


doc.text('', '''
    注意：
    如果您收到错误 "TypeError: a bytes-like object is required, not 'str'"，请尝试在 `main.py` 文件顶部添加以下行：
    ```py
    import sys
    sys.stdout = open('logs.txt', 'w')
    ```
    更多信息请参见 <https://github.com/zauberzeug/nicegui/issues/681>。
''')

doc.text('', '''
    **macOS 打包**

    在主应用文件中的任何其他内容之前添加以下代码片段，以防止新进程在无限循环中生成：

    ```python
    # macOS packaging support
    from multiprocessing import freeze_support  # noqa
    freeze_support()  # noqa

    # all your other imports and code
    ```

    `# noqa` 注释指示 Pylance 或 autopep8 不要在这两行上应用任何 PEP 规则，确保它们保持在所有其他内容之上。
    这是防止进程生成的关键。
''')

doc.text('NiceGUI On Air', '''
    通过使用 `ui.run(on_air=True)`，您可以通过互联网与他人共享您的本地应用 🧞。

    访问 on-air URL 时，所有库（如 Vue、Quasar 等）都从我们的 CDN 加载。
    因此，只有原始内容和事件需要由您的本地应用传输。
    这使其即使您的应用只有很差的互联网连接（例如现场的移动机器人）也能极快地运行。

    通过设置 `on_air=True`，您将获得一个有效期为 1 小时的随机 URL。
    如果您在 <https://on-air.nicegui.io> 注册，您可以设置组织和设备名称以获得固定的 URL：
    `https://on-air.nicegui.io/<my-org>/<my_device_name>`。
    然后设备通过唯一的私有令牌识别，您可以使用它代替布尔标志：`ui.run(on_air='<your token>')`。
    如果您[赞助我们](https://github.com/sponsors/zauberzeug)，
    我们将启用多设备管理并为每个设备提供内置的密码保护。

    目前 On Air 作为技术预览版提供，可以免费使用。
    我们将逐步提高稳定性，并通过使用统计、远程终端访问等扩展服务。
    请在 [GitHub](https://github.com/zauberzeug/nicegui/discussions)、
    [Reddit](https://www.reddit.com/r/nicegui/) 或 [Discord](https://discord.gg/TEpFeAaF4f) 上告诉我们您的反馈。

    **数据隐私：**
    我们非常重视您的隐私。
    NiceGUI On Air 不记录或存储任何中继数据的内容。
''')
