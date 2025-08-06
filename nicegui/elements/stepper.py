from __future__ import annotations

from typing import Any, Optional, Union, cast

from ..context import context
from ..element import Element
from ..events import Handler, ValueChangeEventArguments
from .mixins.disableable_element import DisableableElement
from .mixins.icon_element import IconElement
from .mixins.value_element import ValueElement


class Stepper(ValueElement, default_classes='nicegui-stepper'):

    def __init__(self, *,
                 value: Union[str, Step, None] = None,
                 on_value_change: Optional[Handler[ValueChangeEventArguments]] = None,
                 keep_alive: bool = True,
                 ) -> None:
        """步骤器

        此元素代表`Quasar的QStepper <https://quasar.dev/vue-components/stepper#qstepper-api>`_组件。
        它包含单个步骤。

        为避免切换步骤时动态元素出现问题，
        此元素使用Vue的`keep-alive <https://vuejs.org/guide/built-ins/keep-alive.html>`_组件。
        如果客户端性能有问题，您可以禁用此功能。

        :param value: 初始选择的`ui.step`或步骤名称（默认：`None`，表示第一个步骤）
        :param on_value_change: 所选步骤变化时要执行的回调函数
        :param keep_alive: 是否在内容上使用Vue的keep-alive组件（默认：`True`）
        """
        super().__init__(tag='q-stepper', value=value, on_value_change=on_value_change)
        self._props['keep-alive'] = keep_alive

    def _value_to_model_value(self, value: Any) -> Any:
        return value.props['name'] if isinstance(value, Step) else value

    def _handle_value_change(self, value: Any) -> None:
        super()._handle_value_change(value)
        names = [step.props['name'] for step in self]
        for i, step in enumerate(self):
            done = i < names.index(value) if value in names else False
            step.props(f':done={done}')

    def next(self) -> None:
        """显示下一个步骤。"""
        self.run_method('next')

    def previous(self) -> None:
        """显示上一个步骤。"""
        self.run_method('previous')


class Step(IconElement, DisableableElement, default_classes='nicegui-step'):

    def __init__(self, name: str, title: Optional[str] = None, icon: Optional[str] = None) -> None:
        """步骤

        此元素代表`Quasar的QStep <https://quasar.dev/vue-components/stepper#qstep-api>`_组件。
        它是`ui.stepper`元素的子元素。

        :param name: 步骤的名称（将是`ui.stepper`元素的值）
        :param title: 步骤的标题（默认：`None`，表示与`name`相同）
        :param icon: 步骤的图标（默认：`None`）
        """
        super().__init__(tag='q-step', icon=icon)
        self._props['name'] = name
        self._props['title'] = title if title is not None else name
        self.stepper = cast(ValueElement, context.slot.parent)
        if self.stepper.value is None:
            self.stepper.value = name


class StepperNavigation(Element):

    def __init__(self, *, wrap: bool = True) -> None:
        """步骤器导航

        此元素代表`Quasar的QStepperNavigation https://quasar.dev/vue-components/stepper#qsteppernavigation-api>`_组件。

        :param wrap: 是否换行内容（默认：`True`）
        """
        super().__init__('q-stepper-navigation')

        if wrap:
            self._classes.append('wrap')
