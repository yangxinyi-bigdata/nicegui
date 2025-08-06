from nicegui import ui

from . import doc


@doc.demo(ui.download)
def main_demo() -> None:
    ui.button('本地文件', on_click=lambda: ui.download.file('main.py'))
    ui.button('从URL', on_click=lambda: ui.download.from_url('/logo.png'))
    ui.button('内容', on_click=lambda: ui.download.content('你好世界', 'hello.txt'))


@doc.demo(ui.download.from_url)
def from_url_demo() -> None:
    ui.button('下载', on_click=lambda: ui.download.from_url('/logo.png'))


@doc.demo(ui.download.content)
def content_demo() -> None:
    ui.button('下载', on_click=lambda: ui.download.content('你好世界', 'hello.txt'))


@doc.demo(ui.download.file)
def file_demo() -> None:
    ui.button('下载', on_click=lambda: ui.download.file('main.py'))
