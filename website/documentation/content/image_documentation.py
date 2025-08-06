from nicegui import ui

from . import doc


@doc.demo(ui.image)
def main_demo() -> None:
    ui.image('https://picsum.photos/id/377/640/360')


@doc.demo('本地文件', '''
    您也可以通过传递图像文件的路径来使用本地图像。
''')
def local():
    ui.image('website/static/logo.png').classes('w-16')


@doc.demo('Base64 字符串', '''
    您也可以使用 Base64 字符串作为图像源。
''')
def base64():
    base64 = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg=='
    ui.image(base64).classes('w-2 h-2 m-auto')


@doc.demo('PIL 图像', '''
    您也可以使用 PIL 图像作为图像源。
''')
def pil():
    import numpy as np
    from PIL import Image

    image = Image.fromarray(np.random.randint(0, 255, (100, 100), dtype=np.uint8))
    ui.image(image).classes('w-32')


@doc.demo('Lottie 文件', '''
    您也可以使用带有动画的 [Lottie 文件](https://lottiefiles.com/)。
''')
def lottie():
    ui.add_body_html('<script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"></script>')

    src = 'https://assets1.lottiefiles.com/datafiles/HN7OcWNnoqje6iXIiZdWzKxvLIbfeCGTmvXmEm1h/data.json'
    ui.html(f'<lottie-player src="{src}" loop autoplay />').classes('w-full')


@doc.demo('图像链接', '''
    图像可以通过将其包装在 [ui.link](https://nicegui.io/documentation/link) 中来链接到另一个页面。
''')
def link():
    with ui.link(target='https://github.com/zauberzeug/nicegui'):
        ui.image('https://picsum.photos/id/41/640/360').classes('w-64')


@doc.demo('强制重新加载', '''
    您可以通过调用 `force_reload` 方法强制图像重新加载。
    它将在图像 URL 后面附加一个时间戳，这将使浏览器重新加载图像。
''')
def force_reload():
    img = ui.image('https://picsum.photos/640/360').classes('w-64')

    ui.button('Force reload', on_click=img.force_reload)


doc.reference(ui.image)
