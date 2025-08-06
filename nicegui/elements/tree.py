from typing import Any, Dict, Iterator, List, Literal, Optional, Set

from typing_extensions import Self

from ..events import GenericEventArguments, Handler, ValueChangeEventArguments, handle_event
from .mixins.filter_element import FilterElement


class Tree(FilterElement):

    def __init__(self,
                 nodes: List[Dict], *,
                 node_key: str = 'id',
                 label_key: str = 'label',
                 children_key: str = 'children',
                 on_select: Optional[Handler[ValueChangeEventArguments]] = None,
                 on_expand: Optional[Handler[ValueChangeEventArguments]] = None,
                 on_tick: Optional[Handler[ValueChangeEventArguments]] = None,
                 tick_strategy: Optional[Literal['leaf', 'leaf-filtered', 'strict']] = None,
                 ) -> None:
        """树形结构

        使用Quasar的`QTree <https://quasar.dev/vue-components/tree>`_组件显示分层数据。

        如果使用ID，请确保它们在整个树中是唯一的。

        要使用复选框和``on_tick``，请将``tick_strategy``参数设置为"leaf"、"leaf-filtered"或"strict"。

        :param nodes: 节点对象的分层次列表
        :param node_key: 每个节点对象中保存其唯一ID的属性名称（默认："id"）
        :param label_key: 每个节点对象中保存其标签的属性名称（默认："label"）
        :param children_key: 每个节点对象中保存其子节点列表的属性名称（默认："children"）
        :param on_select: 节点选择更改时调用的回调函数
        :param on_expand: 节点展开更改时调用的回调函数
        :param on_tick: 节点被勾选或取消勾选时调用的回调函数
        :param tick_strategy: 是否以及如何使用复选框（"leaf"、"leaf-filtered"或"strict"；默认：``None``）
        """
        super().__init__(tag='q-tree', filter=None)
        self._props['nodes'] = nodes
        self._props['node-key'] = node_key
        self._props['label-key'] = label_key
        self._props['children-key'] = children_key
        if on_select:
            self._props['selected'] = None
        if on_expand:
            self._props['expanded'] = []
        if on_tick or tick_strategy:
            self._props['ticked'] = []
            self._props['tick-strategy'] = tick_strategy or 'leaf'
        self._select_handlers = [on_select] if on_select else []
        self._expand_handlers = [on_expand] if on_expand else []
        self._tick_handlers = [on_tick] if on_tick else []

        # https://github.com/zauberzeug/nicegui/issues/1385
        self._props.add_warning('default-expand-all',
                                'The prop "default-expand-all" is not supported by `ui.tree`. '
                                'Use ".expand()" instead.')

        def update_prop(name: str, value: Any) -> None:
            if self._props[name] != value:
                self._props[name] = value
                self.update()

        def handle_selected(e: GenericEventArguments) -> None:
            update_prop('selected', e.args)
            for handler in self._select_handlers:
                handle_event(handler, ValueChangeEventArguments(sender=self, client=self.client, value=e.args))
        self.on('update:selected', handle_selected)

        def handle_expanded(e: GenericEventArguments) -> None:
            update_prop('expanded', e.args)
            for handler in self._expand_handlers:
                handle_event(handler, ValueChangeEventArguments(sender=self, client=self.client, value=e.args))
        self.on('update:expanded', handle_expanded)

        def handle_ticked(e: GenericEventArguments) -> None:
            update_prop('ticked', e.args)
            for handler in self._tick_handlers:
                handle_event(handler, ValueChangeEventArguments(sender=self, client=self.client, value=e.args))
        self.on('update:ticked', handle_ticked)

    def on_select(self, callback: Handler[ValueChangeEventArguments]) -> Self:
        """添加选择更改时调用的回调函数。"""
        self._props.setdefault('selected', None)
        self._select_handlers.append(callback)
        return self

    def select(self, node_key: Optional[str]) -> Self:
        """选择给定的节点。

        :param node_key: 要选择的节点键
        """
        self._props.setdefault('selected', None)
        if self._props['selected'] != node_key:
            self._props['selected'] = node_key
            self.update()
        return self

    def deselect(self) -> Self:
        """移除节点选择。"""
        return self.select(None)

    def on_expand(self, callback: Handler[ValueChangeEventArguments]) -> Self:
        """添加展开更改时调用的回调函数。"""
        self._props.setdefault('expanded', [])
        self._expand_handlers.append(callback)
        return self

    def on_tick(self, callback: Handler[ValueChangeEventArguments]) -> Self:
        """添加节点被勾选或取消勾选时调用的回调函数。"""
        self._props.setdefault('ticked', [])
        self._props.setdefault('tick-strategy', 'leaf')
        self._tick_handlers.append(callback)
        return self

    def tick(self, node_keys: Optional[List[str]] = None) -> Self:
        """勾选给定的节点。

        :param node_keys: 要勾选的节点键列表，或``None``以勾选所有节点（默认：``None``）
        """
        self._props.setdefault('ticked', [])
        self._props['ticked'][:] = self._find_node_keys(node_keys).union(self._props['ticked'])
        self.update()
        return self

    def untick(self, node_keys: Optional[List[str]] = None) -> Self:
        """移除给定节点的勾选。

        :param node_keys: 要取消勾选的节点键列表，或``None``以取消勾选所有节点（默认：``None``）
        """
        self._props.setdefault('ticked', [])
        self._props['ticked'][:] = set(self._props['ticked']).difference(self._find_node_keys(node_keys))
        self.update()
        return self

    def expand(self, node_keys: Optional[List[str]] = None) -> Self:
        """展开给定的节点。

        :param node_keys: 要展开的节点键列表（默认：所有节点）
        """
        self._props.setdefault('expanded', [])
        self._props['expanded'][:] = self._find_node_keys(node_keys).union(self._props['expanded'])
        self.update()
        return self

    def collapse(self, node_keys: Optional[List[str]] = None) -> Self:
        """折叠给定的节点。

        :param node_keys: 要折叠的节点键列表（默认：所有节点）
        """
        self._props.setdefault('expanded', [])
        self._props['expanded'][:] = set(self._props['expanded']).difference(self._find_node_keys(node_keys))
        self.update()
        return self

    def _find_node_keys(self, node_keys: Optional[List[str]] = None) -> Set[str]:
        if node_keys is not None:
            return set(node_keys)

        CHILDREN_KEY = self._props['children-key']
        NODE_KEY = self._props['node-key']

        def iterate_nodes(nodes: List[Dict]) -> Iterator[Dict]:
            for node in nodes:
                yield node
                yield from iterate_nodes(node.get(CHILDREN_KEY, []))
        return {node[NODE_KEY] for node in iterate_nodes(self._props['nodes'])}
