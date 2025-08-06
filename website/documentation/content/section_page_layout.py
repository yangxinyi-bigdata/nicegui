from nicegui import ui

from . import (
    card_documentation,
    carousel_documentation,
    column_documentation,
    context_menu_documentation,
    dialog_documentation,
    doc,
    expansion_documentation,
    fullscreen_documentation,
    grid_documentation,
    list_documentation,
    menu_documentation,
    slide_item_documentation,
    notification_documentation,
    notify_documentation,
    pagination_documentation,
    row_documentation,
    scroll_area_documentation,
    separator_documentation,
    skeleton_documentation,
    space_documentation,
    splitter_documentation,
    stepper_documentation,
    tabs_documentation,
    teleport_documentation,
    timeline_documentation,
    tooltip_documentation,
)

doc.title('页面*布局*')


@doc.demo('自动上下文', '''
    为了允许编写直观的 UI 描述，NiceGUI 会自动跟踪元素创建的上下文。
    这意味着没有明确的 `parent` 参数。
    而是使用 `with` 语句来定义父上下文。
    它也会传递给事件处理器和计时器。

    在演示中，标签"Card content"被添加到卡片中。
    并且因为 `ui.button` 也被添加到卡片中，标签"Click!"也将在这个上下文中创建。
    标签"Tick!"在一秒后添加一次，也被添加到卡片中。

    这个设计决策允许轻松创建模块化组件，在 UI 中移动后仍能继续工作。
    例如，您可以将标签和按钮移动到其他地方，也许将它们包装在另一个容器中，代码仍然可以工作。
''')
def auto_context_demo():
    with ui.card():
        ui.label('Card content')
        ui.button('Add label', on_click=lambda: ui.label('Click!'))
        ui.timer(1.0, lambda: ui.label('Tick!'), once=True)


doc.intro(card_documentation)
doc.intro(column_documentation)
doc.intro(row_documentation)
doc.intro(grid_documentation)
doc.intro(list_documentation)
doc.intro(slide_item_documentation)
doc.intro(fullscreen_documentation)


@doc.demo('清空容器', '''
    要从行、列或卡片容器中删除所有元素，可以调用
    ```py
    container.clear()
    ```

    或者，您可以通过调用来删除单个元素

    - `container.remove(element: Element)`,
    - `container.remove(index: int)`, 或
    - `element.delete()`。
''')
def clear_containers_demo():
    container = ui.row()

    def add_face():
        with container:
            ui.icon('face')
    add_face()

    ui.button('Add', on_click=add_face)
    ui.button('Remove', on_click=lambda: container.remove(0) if list(container) else None)
    ui.button('Clear', on_click=container.clear)


doc.intro(teleport_documentation)
doc.intro(expansion_documentation)
doc.intro(scroll_area_documentation)
doc.intro(separator_documentation)
doc.intro(space_documentation)
doc.intro(skeleton_documentation)
doc.intro(splitter_documentation)
doc.intro(tabs_documentation)
doc.intro(stepper_documentation)
doc.intro(timeline_documentation)
doc.intro(carousel_documentation)
doc.intro(pagination_documentation)
doc.intro(menu_documentation)
doc.intro(context_menu_documentation)
doc.intro(tooltip_documentation)
doc.intro(notify_documentation)
doc.intro(notification_documentation)
doc.intro(dialog_documentation)
