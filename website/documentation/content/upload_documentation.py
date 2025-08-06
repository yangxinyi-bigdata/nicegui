from nicegui import ui

from . import doc


@doc.demo(ui.upload)
def main_demo() -> None:
    ui.upload(on_upload=lambda e: ui.notify(f'Uploaded {e.name}')).classes('max-w-full')


@doc.demo('上传限制', '''
    在这个演示中，上传被限制为最大文件大小 1 MB。
    当文件被拒绝时，会显示通知。
''')
def upload_restrictions() -> None:
    ui.upload(on_upload=lambda e: ui.notify(f'Uploaded {e.name}'),
              on_rejected=lambda: ui.notify('Rejected!'),
              max_file_size=1_000_000).classes('max-w-full')


@doc.demo('显示文件内容', '''
    在这个演示中，上传的 markdown 文件在对话框中显示。
''')
def show_file_content() -> None:
    from nicegui import events

    with ui.dialog().props('full-width') as dialog:
        with ui.card():
            content = ui.markdown()

    def handle_upload(e: events.UploadEventArguments):
        text = e.content.read().decode('utf-8')
        content.set_content(text)
        dialog.open()

    ui.upload(on_upload=handle_upload).props('accept=.md').classes('max-w-full')


@doc.demo('上传大文件', '''
    大文件上传可能会遇到问题，这是由于底层 Starlette 库中设置的默认文件大小参数造成的。
    为了确保大文件的顺利上传，建议将 Starlette 的 `MultiPartParser` 类中的 `spool_max_size` 参数从默认的 `1024 * 1024` (1 MB) 增加到与预期文件大小相符的更高限制。

    这个演示将 Starlette Multiparser 保留在 RAM 中的 `max_file_size` 增加到 5 MB。
    这种更改允许系统通过将文件保留在 RAM 中更有效地处理大文件，从而避免需要将数据写入磁盘上的临时文件并防止上传"卡顿"。

    但是，在允许用户上传大文件并将其保留在 RAM 中时，请注意对服务器的潜在影响。
''')
def uploading_large_files() -> None:
    from starlette.formparsers import MultiPartParser

    MultiPartParser.spool_max_size = 1024 * 1024 * 5  # 5 MB

    ui.upload(on_upload=lambda e: ui.notify(f'Uploaded {e.name}')).classes('max-w-full')


doc.reference(ui.upload)
