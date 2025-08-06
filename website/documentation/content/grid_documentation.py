from nicegui import ui

from . import doc


@doc.demo(ui.grid)
def main_demo() -> None:
    with ui.grid(columns=2):
        ui.label('Name:')
        ui.label('Tom')

        ui.label('Age:')
        ui.label('42')

        ui.label('Height:')
        ui.label('1.80m')


@doc.demo('自定义网格布局', '''
    这个演示展示了如何通过传递带有 grid-template-columns CSS 属性的字符串来创建自定义网格布局。
    您可以使用任何有效的 CSS 尺寸，如 'auto'、'1fr'、'80px' 等。

    - 'auto' 将使列与其内容一样宽。
    - '1fr' 或 '2fr' 将使相应的列填充剩余空间，分数比为 1:2。
    - '80px' 将使列宽为 80 像素。
''')
def custom_demo() -> None:
    with ui.grid(columns='auto 80px 1fr 2fr').classes('w-full gap-0'):
        for _ in range(3):
            ui.label('auto').classes('border p-1')
            ui.label('80px').classes('border p-1')
            ui.label('1fr').classes('border p-1')
            ui.label('2fr').classes('border p-1')


@doc.demo('跨多列的单元格', '''
    这个演示展示了如何让单元格跨越多列。

    请注意，[Tailwind 中没有跨越 15 列的类](https://v3.tailwindcss.com/docs/grid-column#arbitrary-values)，
    但我们可以使用方括号设置[任意值](https://v3.tailwindcss.com/docs/grid-column#arbitrary-values)。
    或者您可以使用相应的 CSS 定义：`.style('grid-column: span 15 / span 15')`。
''')
def span_demo() -> None:
    with ui.grid(columns=16).classes('w-full gap-0'):
        ui.label('full').classes('col-span-full border p-1')
        ui.label('8').classes('col-span-8 border p-1')
        ui.label('8').classes('col-span-8 border p-1')
        ui.label('12').classes('col-span-12 border p-1')
        ui.label('4').classes('col-span-4 border p-1')
        ui.label('15').classes('col-[span_15] border p-1')
        ui.label('1').classes('col-span-1 border p-1')


doc.reference(ui.grid)
