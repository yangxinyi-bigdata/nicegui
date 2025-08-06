from nicegui import ui

from . import doc


@doc.demo(ui.input)
def main_demo() -> None:
    ui.input(label='Text', placeholder='start typing',
             on_change=lambda e: result.set_text('you typed: ' + e.value),
             validation={'Input too long': lambda value: len(value) < 20})
    result = ui.label()


@doc.demo('自动完成', '''
    `autocomplete` 功能在您输入时提供建议，使输入更容易、更快速。
    参数 `options` 是一个字符串列表，包含将出现的可用选项。
''')
def autocomplete_demo():
    options = ['AutoComplete', 'NiceGUI', 'Awesome']
    ui.input(label='Text', placeholder='start typing', autocomplete=options)


@doc.demo('可清除', '''
    来自 [Quasar](https://quasar.dev/) 的 `clearable` 属性为输入框添加一个清除文本的按钮。
''')
def clearable():
    i = ui.input(value='some text').props('clearable')
    ui.label().bind_text_from(i, 'value')


@doc.demo('样式设置', '''
    Quasar 有很多 [改变外观的属性](https://quasar.dev/vue-components/input)。
    甚至可以使用 `input-style` 和 `input-class` 属性来设置底层输入框的样式，
    并使用提供的插槽来添加自定义元素。
''')
def styling():
    ui.input(placeholder='start typing').props('rounded outlined dense')
    ui.input('styling', value='some text') \
        .props('input-style="color: blue" input-class="font-mono"')
    with ui.input(value='custom clear button').classes('w-64') as i:
        ui.button(color='orange-8', on_click=lambda: i.set_value(None), icon='delete') \
            .props('flat dense').bind_visibility_from(i, 'value')


@doc.demo('输入验证', '''
    您可以通过两种方式验证输入：

    - 传递一个返回错误消息或 `None` 的可调用对象，或
    - 传递一个字典，将错误消息映射到返回 `True`（如果输入有效）的可调用对象。

    *自版本 2.7.0 起：*
    可调用验证函数也可以是异步协程。
    在这种情况下，验证在后台异步执行。

    您可以使用输入元素的 `validate` 方法手动触发验证。
    如果输入有效，它返回 `True`，否则返回错误消息。
    对于异步验证函数，必须通过设置 `return_result=False` 显式禁用返回值。
''')
def validation():
    ui.input('Name', validation=lambda value: 'Too short' if len(value) < 5 else None)
    ui.input('Name', validation={'Too short': lambda value: len(value) >= 5})


doc.reference(ui.input)
