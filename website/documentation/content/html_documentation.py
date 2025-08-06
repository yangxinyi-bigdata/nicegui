from nicegui import ui

from . import doc


@doc.demo(ui.html)
def main_demo() -> None:
    ui.html('This is <strong>HTML</strong>.')


@doc.demo('生成内联元素', '''
    使用 `tag` 参数来生成除 div 以外的其他元素。
''')
def demo_inline() -> None:
    ui.html('This is <u>emphasized</u>.', tag='em')


@doc.demo(other_html_elements_title := '其他 HTML 元素', other_html_elements_description := '''
    还有一个 `html` 模块，允许您插入其他 HTML 元素，如 `<span>`、`<div>`、`<p>` 等。
    这等同于使用带有 `tag` 参数的 `ui.element` 方法。

    就像任何其他元素一样，您可以添加类、样式、属性、工具提示和事件。
    一个便利之处是关键字参数会自动添加到元素的 `props` 字典中。

    *在版本 2.5.0 中新增*
''')
def other_html_elements():
    from nicegui import html, ui

    with html.section().style('font-size: 120%'):
        html.strong('This is bold.') \
            .classes('cursor-pointer') \
            .on('click', lambda: ui.notify('Bold!'))
        html.hr()
        html.em('This is italic.').tooltip('Nice!')
        with ui.row():
            html.img().props('src=https://placehold.co/60')
            html.img(src='https://placehold.co/60')


doc.reference(ui.html)
