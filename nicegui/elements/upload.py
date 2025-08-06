from typing import Dict, List, Optional, cast

from fastapi import Request
from starlette.datastructures import UploadFile
from typing_extensions import Self

from ..events import Handler, MultiUploadEventArguments, UiEventArguments, UploadEventArguments, handle_event
from ..nicegui import app
from .mixins.disableable_element import DisableableElement
from .mixins.label_element import LabelElement


class Upload(LabelElement, DisableableElement, component='upload.js'):

    def __init__(self, *,
                 multiple: bool = False,
                 max_file_size: Optional[int] = None,
                 max_total_size: Optional[int] = None,
                 max_files: Optional[int] = None,
                 on_begin_upload: Optional[Handler[UiEventArguments]] = None,
                 on_upload: Optional[Handler[UploadEventArguments]] = None,
                 on_multi_upload: Optional[Handler[MultiUploadEventArguments]] = None,
                 on_rejected: Optional[Handler[UiEventArguments]] = None,
                 label: str = '',
                 auto_upload: bool = False,
                 ) -> None:
        """文件上传

        基于Quasar的`QUploader <https://quasar.dev/vue-components/uploader>`_组件。

        上传事件处理器按以下顺序调用：

        1. ``on_begin_upload``：客户端开始向服务器上传一个或多个文件。
        2. ``on_upload``：单个文件的上传完成。
        3. ``on_multi_upload``：所有选定文件的上传完成。

        以下事件处理器在文件选择过程中已经被调用：

        - ``on_rejected``：一个或多个文件被拒绝。

        :param multiple: 允许一次上传多个文件（默认：`False`）
        :param max_file_size: 最大文件大小（字节）（默认：`0`）
        :param max_total_size: 所有文件的最大总大小（字节）（默认：`0`）
        :param max_files: 最大文件数量（默认：`0`）
        :param on_begin_upload: 上传开始时执行的回调函数（*在版本2.14.0中添加*）
        :param on_upload: 为每个上传的文件执行的回调函数
        :param on_multi_upload: 多个文件上传后执行的回调函数
        :param on_rejected: 当一个或多个文件在文件选择过程中被拒绝时执行的回调函数
        :param label: 上传器的标签（默认：`''`）
        :param auto_upload: 选择文件时自动上传（默认：`False`）
        """
        super().__init__(label=label)
        self._props['multiple'] = multiple
        self._props['auto-upload'] = auto_upload
        self._props['url'] = f'/_nicegui/client/{self.client.id}/upload/{self.id}'

        if max_file_size is not None:
            self._props['max-file-size'] = max_file_size

        if max_total_size is not None:
            self._props['max-total-size'] = max_total_size

        if max_files is not None:
            self._props['max-files'] = max_files

        if multiple and on_multi_upload:
            self._props['batch'] = True

        self._begin_upload_handlers = [on_begin_upload] if on_begin_upload else []
        self._upload_handlers = [on_upload] if on_upload else []
        self._multi_upload_handlers = [on_multi_upload] if on_multi_upload else []

        @app.post(self._props['url'])
        async def upload_route(request: Request) -> Dict[str, str]:
            for begin_upload_handler in self._begin_upload_handlers:
                handle_event(begin_upload_handler, UiEventArguments(sender=self, client=self.client))
            form = await request.form()
            uploads = [cast(UploadFile, data) for data in form.values()]
            self.handle_uploads(uploads)
            return {'upload': 'success'}

        if on_rejected:
            self.on_rejected(on_rejected)

    def handle_uploads(self, uploads: List[UploadFile]) -> None:
        """处理上传的文件。

        此方法主要用于内部使用和在测试中模拟文件上传。
        """
        for upload in uploads:
            for upload_handler in self._upload_handlers:
                handle_event(upload_handler, UploadEventArguments(
                    sender=self,
                    client=self.client,
                    content=upload.file,
                    name=upload.filename or '',
                    type=upload.content_type or '',
                ))
        multi_upload_args = MultiUploadEventArguments(
            sender=self,
            client=self.client,
            contents=[upload.file for upload in uploads],
            names=[upload.filename or '' for upload in uploads],
            types=[upload.content_type or '' for upload in uploads],
        )
        for multi_upload_handler in self._multi_upload_handlers:
            handle_event(multi_upload_handler, multi_upload_args)

    def on_begin_upload(self, callback: Handler[UiEventArguments]) -> Self:
        """添加上传开始时调用的回调函数。"""
        self._begin_upload_handlers.append(callback)
        return self

    def on_upload(self, callback: Handler[UploadEventArguments]) -> Self:
        """添加文件上传时调用的回调函数。"""
        self._upload_handlers.append(callback)
        return self

    def on_multi_upload(self, callback: Handler[MultiUploadEventArguments]) -> Self:
        """添加多个文件上传完成时调用的回调函数。"""
        self._multi_upload_handlers.append(callback)
        return self

    def on_rejected(self, callback: Handler[UiEventArguments]) -> Self:
        """添加文件选择过程中一个或多个文件被拒绝时调用的回调函数。"""
        self.on('rejected', lambda: handle_event(callback, UiEventArguments(sender=self, client=self.client)), args=[])
        return self

    def reset(self) -> None:
        """清除上传队列。"""
        self.run_method('reset')

    def _handle_delete(self) -> None:
        app.remove_route(self._props['url'])
        super()._handle_delete()
