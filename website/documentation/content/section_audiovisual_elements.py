from nicegui import ui

from . import (
    audio_documentation,
    avatar_documentation,
    doc,
    icon_documentation,
    image_documentation,
    interactive_image_documentation,
    video_documentation,
)

doc.title('*音视频*元素')

doc.intro(image_documentation)


@doc.demo('标题和叠加层', '''
    通过在 `ui.image` 内嵌套元素，您可以创建增强效果。

    使用 [Quasar 类](https://quasar.dev/vue-components/img) 来定位和样式化标题。
    要叠加 SVG，请使 `viewBox` 与图像大小完全相同，并提供 `100%` 宽度/高度以匹配实际渲染大小。
''')
def captions_and_overlays_demo():
    with ui.image('https://picsum.photos/id/29/640/360'):
        ui.label('Nice!').classes('absolute-bottom text-subtitle2 text-center')

    with ui.image('https://cdn.stocksnap.io/img-thumbs/960w/airplane-sky_DYPWDEEILG.jpg'):
        ui.html('''
            <svg viewBox="0 0 960 638" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
            <circle cx="445" cy="300" r="100" fill="none" stroke="red" stroke-width="10" />
            </svg>
        ''').classes('w-full bg-transparent')


doc.intro(interactive_image_documentation)
doc.intro(audio_documentation)
doc.intro(video_documentation)
doc.intro(icon_documentation)
doc.intro(avatar_documentation)


@doc.demo('SVG', '''
    您可以使用 `ui.html` 元素添加可缩放矢量图形。
''')
def svg_demo():
    content = '''
        <svg viewBox="0 0 200 200" width="100" height="100" xmlns="http://www.w3.org/2000/svg">
        <circle cx="100" cy="100" r="78" fill="#ffde34" stroke="black" stroke-width="3" />
        <circle cx="80" cy="85" r="8" />
        <circle cx="120" cy="85" r="8" />
        <path d="m60,120 C75,150 125,150 140,120" style="fill:none; stroke:black; stroke-width:8; stroke-linecap:round" />
        </svg>'''
    ui.html(content)
