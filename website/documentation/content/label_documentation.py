from nicegui import ui

from . import doc


@doc.demo(ui.label)
def main_demo() -> None:
    ui.label('some label')


@doc.demo('根据内容改变外观', '''
    您可以重写 `_handle_text_change` 方法来根据标签的内容更新其他属性。
    这种技术也适用于绑定，如下面的示例所示。
''')
def status():
    class status_label(ui.label):
        def _handle_text_change(self, text: str) -> None:
            super()._handle_text_change(text)
            if text == 'ok':
                self.classes(replace='text-positive')
            else:
                self.classes(replace='text-negative')

    model = {'status': 'error'}
    status_label().bind_text_from(model, 'status')
    ui.switch(on_change=lambda e: model.update(status='ok' if e.value else 'error'))


doc.reference(ui.label)
