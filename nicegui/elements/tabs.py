from __future__ import annotations

from typing import Any, Optional, Union

from ..context import context
from ..events import Handler, ValueChangeEventArguments
from .mixins.disableable_element import DisableableElement
from .mixins.icon_element import IconElement
from .mixins.label_element import LabelElement
from .mixins.value_element import ValueElement


class Tabs(ValueElement):

    def __init__(self, *,
                 value: Union[Tab, TabPanel, None] = None,
                 on_change: Optional[Handler[ValueChangeEventArguments]] = None,
                 ) -> None:
        """选项卡

        此元素表示`Quasar的QTabs <https://quasar.dev/vue-components/tabs#qtabs-api>`_组件。
        它包含单个选项卡。

        :param value: `ui.tab`、`ui.tab_panel`或要初始选择的选项卡的名称
        :param on_change: 所选选项卡更改时执行的回调函数
        """
        super().__init__(tag='q-tabs', value=value, on_value_change=on_change)

    def _value_to_model_value(self, value: Any) -> Any:
        return value.props['name'] if isinstance(value, (Tab, TabPanel)) else value


class Tab(LabelElement, IconElement, DisableableElement):

    def __init__(self, name: str, label: Optional[str] = None, icon: Optional[str] = None) -> None:
        """选项卡

        此元素表示`Quasar的QTab <https://quasar.dev/vue-components/tabs#qtab-api>`_组件。
        它是`ui.tabs`元素的子元素。

        :param name: 选项卡的名称（将成为`ui.tabs`元素的值）
        :param label: 选项卡的标签（默认：`None`，表示与`name`相同）
        :param icon: 选项卡的图标（默认：`None`）
        """
        if label is None:
            label = name
        super().__init__(tag='q-tab', label=label, icon=icon)
        self._props['name'] = name
        self.tabs = context.slot.parent


class TabPanels(ValueElement):

    def __init__(self,
                 tabs: Optional[Tabs] = None, *,
                 value: Union[Tab, TabPanel, str, None] = None,
                 on_change: Optional[Handler[ValueChangeEventArguments]] = None,
                 animated: bool = True,
                 keep_alive: bool = True,
                 ) -> None:
        """选项卡面板

        此元素表示`Quasar的QTabPanels <https://quasar.dev/vue-components/tab-panels#qtabpanels-api>`_组件。
        它包含单个选项卡面板。

        为避免切换选项卡时动态元素出现问题，
        此元素使用Vue的`keep-alive <https://vuejs.org/guide/built-ins/keep-alive.html>`_组件。
        如果客户端性能有问题，您可以禁用此功能。

        :param tabs: 控制此元素的可选`ui.tabs`元素
        :param value: `ui.tab`、`ui.tab_panel`或要初始可见的选项卡面板的名称
        :param on_change: 可见选项卡面板更改时执行的回调函数
        :param animated: 选项卡面板是否应该有动画（默认：`True`）
        :param keep_alive: 是否在内容上使用Vue的keep-alive组件（默认：`True`）
        """
        super().__init__(tag='q-tab-panels', value=value, on_value_change=on_change)
        if tabs is not None:
            tabs.bind_value(self, 'value')
        self._props['animated'] = animated
        self._props['keep-alive'] = keep_alive

    def _value_to_model_value(self, value: Any) -> Any:
        return value.props['name'] if isinstance(value, (Tab, TabPanel)) else value


class TabPanel(DisableableElement, default_classes='nicegui-tab-panel'):

    def __init__(self, name: Union[Tab, str]) -> None:
        """选项卡面板

        此元素表示`Quasar的QTabPanel <https://quasar.dev/vue-components/tab-panels#qtabpanel-api>`_组件。
        它是`TabPanels`元素的子元素。

        :param name: `ui.tab`或选项卡元素的名称
        """
        super().__init__(tag='q-tab-panel')
        self._props['name'] = name.props['name'] if isinstance(name, Tab) else name
