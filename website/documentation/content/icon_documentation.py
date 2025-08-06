from nicegui import ui

from . import doc


@doc.demo(ui.icon)
def main_demo() -> None:
    ui.icon('thumb_up', color='primary').classes('text-5xl')


@doc.demo('Material 图标和符号', r'''
    您可以使用不同套装的 Material 图标和符号。
    [Quasar 文档](https://quasar.dev/vue-components/icon\#webfont-usage)
    概述了所有可用的图标集及其名称前缀：

    * 无前缀表示 [填充图标](https://fonts.google.com/icons?icon.set=Material+Icons&icon.style=Filled)
    * "o\_" 表示 [轮廓图标](https://fonts.google.com/icons?icon.set=Material+Icons&icon.style=Outlined)
    * "r\_" 表示 [圆角图标](https://fonts.google.com/icons?icon.set=Material+Icons&icon.style=Rounded)
    * "s\_" 表示 [尖角图标](https://fonts.google.com/icons?icon.set=Material+Icons&icon.style=Sharp)
    * "sym\_o\_" 表示 [轮廓符号](https://fonts.google.com/icons?icon.set=Material+Symbols&icon.style=Outlined)
    * "sym\_r\_" 表示 [圆角符号](https://fonts.google.com/icons?icon.set=Material+Symbols&icon.style=Rounded)
    * "sym\_s\_" 表示 [尖角符号](https://fonts.google.com/icons?icon.set=Material+Symbols&icon.style=Sharp)
''')
def material_icons():
    with ui.row().classes('text-4xl'):
        ui.icon('home')
        ui.icon('o_home')
        ui.icon('r_home')
        ui.icon('sym_o_home')
        ui.icon('sym_r_home')


@doc.demo('Eva 图标', '''
    您可以在应用中使用 [Eva 图标](https://akveo.github.io/eva-icons/)。
''')
def eva_icons():
    ui.add_head_html('<link href="https://unpkg.com/eva-icons@1.1.3/style/eva-icons.css" rel="stylesheet" />')

    ui.icon('eva-github').classes('text-5xl')


@doc.demo('其他图标集', '''
    您可以使用相同的方法向应用中添加其他图标集。
    根据经验，您引用相应的 CSS，它再引用字体文件。
    这个演示展示了如何包含 [Themify 图标](https://themify.me/themify-icons)。
''')
def other_icons():
    ui.add_head_html('<link href="https://cdn.jsdelivr.net/themify-icons/0.1.2/css/themify-icons.css" rel="stylesheet" />')

    ui.icon('ti-car').classes('text-5xl')


@doc.demo('Lottie files', '''
    You can also use [Lottie files](https://lottiefiles.com/) with animations.
''', lazy=False)
def lottie():
    ui.add_body_html('<script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"></script>')

    src = 'https://assets5.lottiefiles.com/packages/lf20_MKCnqtNQvg.json'
    ui.html(f'<lottie-player src="{src}" loop autoplay />').classes('w-24')


doc.reference(ui.icon)
