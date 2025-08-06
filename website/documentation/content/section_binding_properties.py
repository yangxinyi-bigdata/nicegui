from nicegui import ui

from . import doc

date = '2023-01-01'

doc.title('*绑定*属性')


@doc.demo('绑定', '''
    NiceGUI 能够直接将 UI 元素绑定到模型。
    绑定适用于 UI 元素属性，如文本、值或可见性，以及作为（嵌套）类属性的模型属性。
    每个元素都提供 `bind_value` 和 `bind_visibility` 等方法来创建与相应属性的双向绑定。
    要定义单向绑定，请使用这些方法的 `_from` 和 `_to` 变体。
    只需将模型的属性作为参数传递给这些方法即可创建绑定。
    值将立即更新，并在其中任何一个发生变化时更新。
''')
def bindings_demo():
    class Demo:
        def __init__(self):
            self.number = 1

    demo = Demo()
    v = ui.checkbox('visible', value=True)
    with ui.column().bind_visibility_from(v, 'value'):
        ui.slider(min=1, max=3).bind_value(demo, 'number')
        ui.toggle({1: 'A', 2: 'B', 3: 'C'}).bind_value(demo, 'number')
        ui.number().bind_value(demo, 'number')


@doc.demo('转换函数', '''
    您可以使用 ``forward`` 和 ``backward`` 转换函数在将值从一个对象传播到另一个对象时进行转换。
    这些函数在源属性发生变化时被调用，
    或者在活动链接的情况下（见下文）- 在检查源属性是否发生变化时被调用。

    注意：
    NiceGUI 2.16.0 通过严格遵循深度优先搜索方法提高了绑定传播的效率，
    每个受影响的节点只更新一次，转换函数只执行一次。
    如果您从 NiceGUI 2.15.0 或更早版本迁移，转换函数可能会有额外的运行，
    特别是那些与当前传播方向相反的函数，
    这些在 NiceGUI 2.16.0 中不再运行。
    因此，您需要适当地更改代码。

    我们还想提到，为了在版本间获得最稳定的行为，
    最佳实践是转换函数没有副作用，只执行基本的转换操作。
    这样，无论 NiceGUI 选择以何种顺序和多少次调用它们都不会产生影响。
''')
def transformation_functions():
    i = ui.input(value='Lorem ipsum')
    ui.label().bind_text_from(i, 'value',
                              backward=lambda text: f'{len(text)} characters')


@doc.demo('绑定到字典', '''
    在这里，我们将标签的文本绑定到字典。
''')
def bind_dictionary():
    data = {'name': 'Bob', 'age': 17}

    ui.label().bind_text_from(data, 'name', backward=lambda n: f'Name: {n}')
    ui.label().bind_text_from(data, 'age', backward=lambda a: f'Age: {a}')

    ui.button('Turn 18', on_click=lambda: data.update(age=18))


@doc.demo('绑定到变量', '''
    在这里，我们将日期选择器的值绑定到一个普通变量。
    因此我们使用包含所有全局变量的字典 `globals()`。
    此演示基于[官方日期选择器示例](/documentation/date#input_element_with_date_picker)。
''')
def bind_variable():
    # date = '2023-01-01'

    with ui.input('Date').bind_value(globals(), 'date') as date_input:
        with ui.menu() as menu:
            ui.date(on_change=lambda: ui.notify(f'Date: {date}')).bind_value(date_input)
        with date_input.add_slot('append'):
            ui.icon('edit_calendar').on('click', menu.open).classes('cursor-pointer')


@doc.demo('绑定到存储', '''
    绑定也适用于 [`app.storage`](/documentation/storage)。
    在这里，我们在访问之间存储文本区域的值。
    该笔记也在同一用户的所有标签页之间共享。
''')
def ui_state():
    from nicegui import app

    # @ui.page('/')
    # def index():
    #     ui.textarea('This note is kept between visits')
    #         .classes('w-full').bind_value(app.storage.user, 'note')
    # END OF DEMO
    ui.textarea('This note is kept between visits').classes('w-full').bind_value(app.storage.user, 'note')


@doc.demo('可绑定属性以获得最大性能', '''
    有两种类型的绑定：

    1. "可绑定属性"自动检测写入访问并触发值传播。
        大多数 NiceGUI 元素使用这些可绑定属性，如 `ui.input` 中的 `value` 或 `ui.label` 中的 `text`。
        基本上所有带有 `bind()` 方法的属性都支持这种类型的绑定。
    2. 所有其他绑定有时被称为"活动链接"。
        如果您将标签文本绑定到某个字典条目或自定义数据模型的属性，
        NiceGUI 的绑定模块必须主动检查值是否发生变化。
        这是在每 0.1 秒运行一次的 `refresh_loop()` 中完成的。
        间隔可以通过 `ui.run()` 中的 `binding_refresh_interval` 进行配置。

    "可绑定属性"非常高效，只要值不变化就不会消耗任何资源。
    但是"活动链接"需要每秒检查所有绑定值 10 次。
    这可能会变得昂贵，特别是如果您绑定到复杂对象如列表或字典时。

    因为不阻塞主线程太长时间至关重要，
    如果 `refresh_loop()` 的某一步骤花费太长时间，我们会显示警告。
    您可以通过 `binding.MAX_PROPAGATION_TIME` 配置阈值，默认为 0.01 秒。
    但通常警告是性能或内存问题的有价值指标。
    如果您的 CPU 忙于更新绑定很长一段时间，
    主线程上就不会发生其他任何事情，UI 就会"挂起"。

    以下演示展示了如何为像第一个演示中的 `Demo` 类定义和使用可绑定属性。
    `number` 属性现在是一个 `BindableProperty`，
    这允许 NiceGUI 检测写入访问并立即触发值传播。
''')
def bindable_properties():
    from nicegui import binding

    class Demo:
        number = binding.BindableProperty()

        def __init__(self):
            self.number = 1

    demo = Demo()
    ui.slider(min=1, max=3).bind_value(demo, 'number')
    ui.toggle({1: 'A', 2: 'B', 3: 'C'}).bind_value(demo, 'number')
    ui.number(min=1, max=3).bind_value(demo, 'number')


@doc.demo('可绑定数据类', '''
    `bindable_dataclass` 装饰器提供了一种创建具有可绑定属性的类的便捷方法。
    它扩展了 Python 标准 `dataclasses.dataclass` 装饰器的功能，
    通过自动使所有数据类字段可绑定。
    这消除了手动将每个字段声明为 `BindableProperty` 的需要，
    同时保留了常规数据类的所有好处。

    *在版本 2.11.0 中添加*
''')
def bindable_dataclass():
    from nicegui import binding

    @binding.bindable_dataclass
    class Demo:
        number: int = 1

    demo = Demo()
    ui.slider(min=1, max=3).bind_value(demo, 'number')
    ui.toggle({1: 'A', 2: 'B', 3: 'C'}).bind_value(demo, 'number')
    ui.number(min=1, max=3).bind_value(demo, 'number')
