from nicegui import ui

from . import doc


@doc.demo(ui.column)
def main_demo() -> None:
    with ui.column():
        ui.label('label 1')
        ui.label('label 2')
        ui.label('label 3')


@doc.demo('瀑布流或 Pinterest 风格布局', '''
    要创建瀑布流/Pinterest 布局，不能使用普通的 `ui.column`。
    但可以通过几个 TailwindCSS 类来实现。
''')
def masonry() -> None:
    with ui.element('div').classes('columns-3 w-full gap-2'):
        for i, height in enumerate([50, 50, 50, 150, 100, 50]):
            tailwind = f'mb-2 p-2 h-[{height}px] bg-blue-100 break-inside-avoid'
            with ui.card().classes(tailwind):
                ui.label(f'Card #{i+1}')


doc.reference(ui.column)
