from nicegui import ui

from . import doc


@doc.demo(ui.rating)
def main_demo() -> None:
    ui.rating(value=4)


@doc.demo('自定义图标', '''
    您可以自定义图标的名称和大小。
    可选地，未选中、选中或半选中的值可以有不同的图标。
''')
def customize_icons():
    ui.rating(
        value=3.5,
        size='lg',
        icon='sentiment_dissatisfied',
        icon_selected='sentiment_satisfied',
        icon_half='sentiment_neutral',
    )
    ui.rating(
        value=3.5,
        size='lg',
        icon='star',
        icon_selected='star',
        icon_half='star_half',
    )


@doc.demo('自定义颜色', '''
    您可以通过提供单一颜色或一系列不同颜色来自定义评分的颜色。
''')
def rating_color():
    ui.rating(value=3, color='red-10')
    ui.rating(value=5, color=['green-2', 'green-4', 'green-6', 'green-8', 'green-10'])


@doc.demo('最大评分', '''
    此演示展示了如何更改最大可能的评分
    以及将值绑定到滑块。
''')
def rating_scale():
    slider = ui.slider(value=5, min=0, max=10)
    ui.rating(max=10, icon='circle').bind_value(slider)


doc.reference(ui.rating)
