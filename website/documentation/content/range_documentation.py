from nicegui import ui

from . import doc


@doc.demo(ui.range)
def main_demo() -> None:
    min_max_range = ui.range(min=0, max=100, value={'min': 20, 'max': 80})
    ui.label().bind_text_from(min_max_range, 'value',
                              backward=lambda v: f'min: {v["min"]}, max: {v["max"]}')


@doc.demo('自定义标签', '''
    您可以通过单独设置或为整个范围设置来自定义范围及其标签的颜色。
''')
def customize_labels():
    ui.label('为整个范围着色')
    ui.range(min=0, max=100, value={'min': 20, 'max': 80}) \
        .props('label snap color="secondary"')

    ui.label('自定义标签的颜色')
    ui.range(min=0, max=100, value={'min': 40, 'max': 80}) \
        .props('label-always snap label-color="secondary" right-label-text-color="black"')


@doc.demo('更改范围限制', '''
    此演示展示了如何通过点击按钮来更改限制。
''')
def range_limits():
    def increase_limits():
        r.min -= 10
        r.max += 10

    ui.button('增加限制', on_click=increase_limits)
    r = ui.range(min=0, max=100, value={'min': 30, 'max': 70}).props('label-always')


doc.reference(ui.range)
