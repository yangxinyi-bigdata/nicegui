from nicegui import ui

from . import doc


@doc.demo(ui.avatar)
def main_demo() -> None:
    ui.avatar('favorite_border', text_color='grey-11', square=True)
    ui.avatar('img:https://nicegui.io/logo_square.png', color='blue-2')


@doc.demo('照片', '''
    要使用照片作为头像，您可以在`ui.avatar`内使用`ui.image`。
''')
def photos() -> None:
    with ui.avatar():
        ui.image('https://robohash.org/robot?bgset=bg2')


doc.reference(ui.avatar)
