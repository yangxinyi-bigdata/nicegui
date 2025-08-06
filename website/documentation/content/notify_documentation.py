from nicegui import ui

from . import doc


@doc.demo(ui.notify)
def main_demo() -> None:
    ui.button('Say hi!', on_click=lambda: ui.notify('Hi!', close_button='OK'))


@doc.demo('通知类型', '''
    有不同的类型可用于指示通知的性质。
''')
def notify_colors():
    ui.button('negative', on_click=lambda: ui.notify('error', type='negative'))
    ui.button('positive', on_click=lambda: ui.notify('success', type='positive'))
    ui.button('warning', on_click=lambda: ui.notify('warning', type='warning'))


@doc.demo('多行通知', '''
    要允许通知文本跨越多行，只需设置 `multi_line=True` 即可。
    如果需要手动换行符（例如 `\\n`），您需要定义一个 CSS 样式并将其传递给通知，如示例所示。
''')
def multiline():
    ui.html('<style>.multi-line-notification { white-space: pre-line; }</style>')
    ui.button('show', on_click=lambda: ui.notify(
        'Lorem ipsum dolor sit amet, consectetur adipisicing elit. \n'
        'Hic quisquam non ad sit assumenda consequuntur esse inventore officia. \n'
        'Corrupti reiciendis impedit vel, '
        'fugit odit quisquam quae porro exercitationem eveniet quasi.',
        multi_line=True,
        classes='multi-line-notification',
    ))
