from nicegui import ui

from . import doc


@doc.demo(ui.chat_message)
def main_demo() -> None:
    ui.chat_message('你好 NiceGUI！',
                    name='机器人',
                    stamp='现在',
                    avatar='https://robohash.org/ui')


@doc.demo('HTML文本', '''
    使用 `text_html` 参数，您可以将HTML文本发送到聊天。
''')
def html_text():
    ui.chat_message('Without <strong>HTML</strong>')
    ui.chat_message('With <strong>HTML</strong>', text_html=True)


@doc.demo('换行', '''
    您可以在聊天消息中使用换行符。
''')
def newline():
    ui.chat_message('这是一条\n长消息！')


@doc.demo('多部分消息', '''
    您可以通过传递字符串列表来发送多个消息部分。
''')
def multiple_messages():
    ui.chat_message(['你好！😀', '你好吗？']
                    )


@doc.demo('带有子元素的聊天消息', '''
    您可以向聊天消息添加子元素。
''')
def child_elements():
    with ui.chat_message():
        ui.label('猜猜我在哪里！')
        ui.image('https://picsum.photos/id/249/640/360').classes('w-64')


doc.reference(ui.chat_message)
