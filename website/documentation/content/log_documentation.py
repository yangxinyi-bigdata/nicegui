from nicegui import ui

from . import doc


@doc.demo(ui.log)
def main_demo() -> None:
    from datetime import datetime

    log = ui.log(max_lines=10).classes('w-full h-20')
    ui.button('Log time', on_click=lambda: log.push(datetime.now().strftime('%X.%f')[:-5]))


@doc.demo('附加到日志记录器', '''
    您可以将 `ui.log` 元素附加到 Python 日志记录器对象，以便将日志消息推送到日志元素。
    在页面函数中使用时，当客户端断开连接时移除处理器很重要。
    否则，处理器将保持对日志元素的引用，后者将不会被垃圾回收。
''')
def logger_handler():
    import logging
    from datetime import datetime

    logger = logging.getLogger()

    class LogElementHandler(logging.Handler):
        """将消息发送到日志元素的日志记录处理器。"""

        def __init__(self, element: ui.log, level: int = logging.NOTSET) -> None:
            self.element = element
            super().__init__(level)

        def emit(self, record: logging.LogRecord) -> None:
            try:
                msg = self.format(record)
                self.element.push(msg)
            except Exception:
                self.handleError(record)

    # @ui.page('/')
    def page():
        log = ui.log(max_lines=10).classes('w-full')
        handler = LogElementHandler(log)
        logger.addHandler(handler)
        ui.context.client.on_disconnect(lambda: logger.removeHandler(handler))
        ui.button('Log time', on_click=lambda: logger.warning(datetime.now().strftime('%X.%f')[:-5]))
    page()  # HIDE


@doc.demo('样式化行', '''
    基于 `ui.log` 中的单行是 `ui.label` 实例这一事实，
    可以通过 `classes`、`style` 和 `props` 为插入的行设置样式。
    一个值得注意的用途是彩色日志。

    请注意，如果应用，这将清除当前在 `ui.label` 上设置为默认的任何现有的
    [类](element#default_classes)、
    [样式](element#default_style) 和
    [属性](element#default_props)。

    *在版本 2.18.0 中添加*
''')
def styling_lines_demo():
    log = ui.log(max_lines=10).classes('w-full h-40')
    with ui.row():
        ui.button('Normal', on_click=lambda: log.push('Text'))
        ui.button('Debug', on_click=lambda: log.push('Debug', classes='text-grey'))
        ui.button('Info', on_click=lambda: log.push('Info', classes='text-blue'))
        ui.button('Warning', on_click=lambda: log.push('Warning', classes='text-orange'))
        ui.button('Error', on_click=lambda: log.push('Error', classes='text-red'))


doc.reference(ui.log)
