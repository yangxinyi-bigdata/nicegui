from __future__ import annotations

import inspect
import re
import weakref
from copy import copy
from pathlib import Path
from typing import TYPE_CHECKING, Any, Callable, ClassVar, Dict, Iterator, List, Optional, Sequence, Union, cast

from typing_extensions import Self

from . import core, events, helpers, json, storage
from .awaitable_response import AwaitableResponse, NullResponse
from .classes import Classes
from .context import context
from .dependencies import (
    Component,
    Library,
    register_dynamic_resource,
    register_library,
    register_resource,
    register_vue_component,
)
from .elements.mixins.visibility import Visibility
from .event_listener import EventListener
from .props import Props
from .slot import Slot
from .style import Style
from .tailwind import Tailwind
from .version import __version__

if TYPE_CHECKING:
    from .client import Client

# https://www.w3.org/TR/xml/#sec-common-syn
TAG_START_CHAR = r':|[A-Z]|_|[a-z]|[\u00C0-\u00D6]|[\u00D8-\u00F6]|[\u00F8-\u02FF]|[\u0370-\u037D]|[\u037F-\u1FFF]|[\u200C-\u200D]|[\u2070-\u218F]|[\u2C00-\u2FEF]|[\u3001-\uD7FF]|[\uF900-\uFDCF]|[\uFDF0-\uFFFD]|[\U00010000-\U000EFFFF]'
TAG_CHAR = TAG_START_CHAR + r'|-|\.|[0-9]|\u00B7|[\u0300-\u036F]|[\u203F-\u2040]'
TAG_PATTERN = re.compile(fr'^({TAG_START_CHAR})({TAG_CHAR})*$')


class Element(Visibility):
    component: Optional[Component] = None
    libraries: ClassVar[List[Library]] = []
    extra_libraries: ClassVar[List[Library]] = []
    exposed_libraries: ClassVar[List[Library]] = []
    _default_props: ClassVar[Dict[str, Any]] = {}
    _default_classes: ClassVar[List[str]] = []
    _default_style: ClassVar[Dict[str, str]] = {}

    def __init__(self, tag: Optional[str] = None, *, _client: Optional[Client] = None) -> None:
        """通用元素

        这个类是所有其他 UI 元素的基类。
        但您可以使用它来创建任意 HTML 标签的元素。

        :param tag: 元素的 HTML 标签
        :param _client: 此元素的客户端（仅供内部使用）
        """
        super().__init__()
        client = _client or context.client
        self._client = weakref.ref(client)
        self.id = client.next_element_id
        client.next_element_id += 1
        self.tag = tag if tag else self.component.tag if self.component else 'div'
        if not TAG_PATTERN.match(self.tag):
            raise ValueError(f'Invalid HTML tag: {self.tag}')
        self._classes: Classes[Self] = Classes(self._default_classes, element=cast(Self, self))
        self._style: Style[Self] = Style(self._default_style, element=cast(Self, self))
        self._props: Props[Self] = Props(self._default_props, element=cast(Self, self))
        self._markers: List[str] = []
        self._event_listeners: Dict[str, EventListener] = {}
        self._text: Optional[str] = None
        self.slots: Dict[str, Slot] = {}
        self.default_slot = self.add_slot('default')
        self._update_method: Optional[str] = None
        self._deleted: bool = False

        client.elements[self.id] = self
        self.parent_slot: Optional[Slot] = None
        slot_stack = context.slot_stack
        if slot_stack:
            self.parent_slot = slot_stack[-1]
            self.parent_slot.children.append(self)

        self.tailwind = Tailwind(self)

        client.outbox.enqueue_update(self)
        if self.parent_slot:
            client.outbox.enqueue_update(self.parent_slot.parent)

    def __init_subclass__(cls, *,
                          component: Union[str, Path, None] = None,
                          dependencies: List[Union[str, Path]] = [],  # noqa: B006
                          libraries: List[Union[str, Path]] = [],  # noqa: B006  # DEPRECATED
                          exposed_libraries: List[Union[str, Path]] = [],  # noqa: B006  # DEPRECATED
                          extra_libraries: List[Union[str, Path]] = [],  # noqa: B006  # DEPRECATED
                          default_classes: Optional[str] = None,
                          default_style: Optional[str] = None,
                          default_props: Optional[str] = None,
                          ) -> None:
        super().__init_subclass__()
        base = Path(inspect.getfile(cls)).parent

        def glob_absolute_paths(file: Union[str, Path]) -> List[Path]:
            path = Path(file)
            if not path.is_absolute():
                path = base / path
            return sorted(path.parent.glob(path.name), key=lambda p: p.stem)

        if libraries:
            helpers.warn_once(f'The `libraries` parameter for subclassing "{cls.__name__}" is deprecated. '
                              'It will be removed in NiceGUI 3.0. '
                              'Use `dependencies` instead.')
        if exposed_libraries:
            helpers.warn_once(f'The `exposed_libraries` parameter for subclassing "{cls.__name__}" is deprecated. '
                              'It will be removed in NiceGUI 3.0. '
                              'Use `dependencies` instead.')
        if extra_libraries:
            helpers.warn_once(f'The `extra_libraries` parameter for subclassing "{cls.__name__}" is deprecated. '
                              'It will be removed in NiceGUI 3.0. '
                              'Use `dependencies` instead.')

        cls.component = copy(cls.component)
        cls.libraries = copy(cls.libraries)
        cls.extra_libraries = copy(cls.extra_libraries)
        cls.exposed_libraries = copy(cls.exposed_libraries)
        if component:
            max_time = max((path.stat().st_mtime for path in glob_absolute_paths(component)), default=None)
            for path in glob_absolute_paths(component):
                cls.component = register_vue_component(path, max_time=max_time)
        for library in libraries:
            max_time = max((path.stat().st_mtime for path in glob_absolute_paths(library)), default=None)
            for path in glob_absolute_paths(library):
                cls.libraries.append(register_library(path, max_time=max_time))
        for library in extra_libraries:
            max_time = max((path.stat().st_mtime for path in glob_absolute_paths(library)), default=None)
            for path in glob_absolute_paths(library):
                cls.extra_libraries.append(register_library(path, max_time=max_time))
        for library in exposed_libraries + dependencies:
            max_time = max((path.stat().st_mtime for path in glob_absolute_paths(library)), default=None)
            for path in glob_absolute_paths(library):
                cls.exposed_libraries.append(register_library(path, expose=True, max_time=max_time))

        cls._default_props = copy(cls._default_props)
        cls._default_classes = copy(cls._default_classes)
        cls._default_style = copy(cls._default_style)
        cls.default_classes(default_classes)
        cls.default_style(default_style)
        cls.default_props(default_props)

    @property
    def client(self) -> Client:
        """此元素所属的客户端。"""
        client = self._client()
        if client is None:
            raise RuntimeError('The client this element belongs to has been deleted.')
        return client

    def add_resource(self, path: Union[str, Path]) -> None:
        """向元素添加资源。

        :param path: 资源路径（例如包含 CSS 和 JavaScript 文件的文件夹）
        """
        path_ = Path(path)
        resource = register_resource(path_, max_time=path_.stat().st_mtime)
        self._props['resource_path'] = f'/_nicegui/{__version__}/resources/{resource.key}'

    def add_dynamic_resource(self, name: str, function: Callable) -> None:
        """向元素添加一个动态资源，该资源返回函数的结果。

        :param name: 资源名称
        :param function: 返回资源响应的函数
        """
        register_dynamic_resource(name, function)
        self._props['dynamic_resource_path'] = f'/_nicegui/{__version__}/dynamic_resources'

    def add_slot(self, name: str, template: Optional[str] = None) -> Slot:
        """向元素添加插槽。

        NiceGUI 使用来自 Vue 的插槽概念：
        元素可以有多个插槽，每个插槽可能有许多子元素。
        大多数元素只有一个插槽，例如 `ui.card` (QCard) 只有一个默认插槽。
        但更复杂的元素如 `ui.table` (QTable) 可以有更多插槽，如 "header"、"body" 等。
        如果您通过 `with ui.row(): ...` 嵌套 NiceGUI 元素，您将新元素放在行的默认插槽内。
        但如果您使用 `with table.add_slot(...): ...`，您将进入不同的插槽。

        插槽堆栈帮助 NiceGUI 跟踪当前用于新元素的插槽。
        `parent` 字段持有对其元素的引用。
        每当通过 `with` 表达式进入元素时，其默认插槽也会自动进入。

        :param name: 插槽名称
        :param template: 插槽的 Vue 模板
        :return: 插槽
        """
        self.slots[name] = Slot(self, name, template)
        return self.slots[name]

    def __enter__(self) -> Self:
        self.default_slot.__enter__()
        return self

    def __exit__(self, *_) -> None:
        self.default_slot.__exit__(*_)

    def __iter__(self) -> Iterator[Element]:
        for slot in self.slots.values():
            yield from slot

    def _collect_slot_dict(self) -> Dict[str, Any]:
        return {
            name: {
                'ids': [child.id for child in slot],
                **({'template': slot.template} if slot.template is not None else {}),
            }
            for name, slot in self.slots.items()
            if slot != self.default_slot
        }

    def _to_dict(self) -> Dict[str, Any]:
        return {
            'tag': self.tag,
            **({'text': self._text} if self._text is not None else {}),
            **{
                key: value
                for key, value in {
                    'class': self._classes,
                    'style': self._style,
                    'props': self._props,
                    'slots': self._collect_slot_dict(),
                    'children': [child.id for child in self.default_slot.children],
                    'events': [listener.to_dict() for listener in self._event_listeners.values()],
                    'update_method': self._update_method,
                    'component': {
                        'key': self.component.key,
                        'name': self.component.name,
                        'tag': self.component.tag
                    } if self.component else None,
                    'libraries': [
                        {
                            'key': library.key,
                            'name': library.name,
                        } for library in self.libraries
                    ],
                }.items()
                if value
            },
        }

    @property
    def classes(self) -> Classes[Self]:
        """元素的类。"""
        return self._classes

    @classmethod
    def default_classes(cls,
                        add: Optional[str] = None, *,
                        remove: Optional[str] = None,
                        toggle: Optional[str] = None,
                        replace: Optional[str] = None) -> type[Self]:
        """应用、移除、切换或替换默认 HTML 类。

        这允许使用 `Tailwind <https://v3.tailwindcss.com/>`_ 或 `Quasar <https://quasar.dev/>`_ 类修改元素的外观或布局。

        如果不需要预定义的类，移除或替换类会很有帮助。
        此类的所有元素将共享这些 HTML 类。
        这些必须在元素实例化之前定义。

        :param add: 以空白分隔的类字符串
        :param remove: 要从元素中移除的以空白分隔的类字符串
        :param toggle: 要切换的以空白分隔的类字符串（*在版本 2.7.0 中新增*）
        :param replace: 用于替代现有类的以空白分隔的类字符串
        """
        cls._default_classes = Classes.update_list(cls._default_classes, add, remove, toggle, replace)
        return cls

    @property
    def style(self) -> Style[Self]:
        """元素的样式。"""
        return self._style

    @classmethod
    def default_style(cls,
                      add: Optional[str] = None, *,
                      remove: Optional[str] = None,
                      replace: Optional[str] = None) -> type[Self]:
        """应用、移除或替换默认 CSS 定义。

        如果不需要预定义样式，移除或替换样式会很有帮助。
        此类的所有元素将共享这些 CSS 定义。
        这些必须在元素实例化之前定义。

        :param add: 要添加到元素的以分号分隔的样式列表
        :param remove: 要从元素中移除的以分号分隔的样式列表
        :param replace: 用于替代现有样式的以分号分隔的样式列表
        """
        if replace is not None:
            cls._default_style.clear()
        for key in Style.parse(remove):
            cls._default_style.pop(key, None)
        cls._default_style.update(Style.parse(add))
        cls._default_style.update(Style.parse(replace))
        return cls

    @property
    def props(self) -> Props[Self]:
        """元素的属性。"""
        return self._props

    @classmethod
    def default_props(cls,
                      add: Optional[str] = None, *,
                      remove: Optional[str] = None) -> type[Self]:
        """添加或移除默认属性。

        这允许使用 `Quasar <https://quasar.dev/>`_ 属性修改元素的外观或布局。
        由于属性只是作为 HTML 属性应用，它们可以与任何 HTML 元素一起使用。
        此类的所有元素将共享这些属性。
        这些必须在元素实例化之前定义。

        如果未指定值，布尔属性假定为 ``True``。

        :param add: 要添加的布尔值或 key=value 对的以空白分隔的列表
        :param remove: 要移除的属性键的以空白分隔的列表
        """
        for key in Props.parse(remove):
            if key in cls._default_props:
                del cls._default_props[key]
        for key, value in Props.parse(add).items():
            cls._default_props[key] = value
        return cls

    def mark(self, *markers: str) -> Self:
        """替换元素的标记。

        标记用于通过 `ElementFilter </documentation/element_filter>`_ 查询来识别元素，
        这在测试中大量使用，
        但也可以用于减少全局变量的数量或传递依赖项。

        :param markers: 字符串列表或包含以空白分隔的标记的单个字符串；替换现有标记
        """
        self._markers = [word for marker in markers for word in marker.split()]
        return self

    def tooltip(self, text: str) -> Self:
        """向元素添加工具提示。

        :param text: 工具提示的文本
        """
        from .elements.tooltip import Tooltip  # pylint: disable=import-outside-toplevel, cyclic-import
        with self:
            Tooltip(text)
        return self

    def on(self,
           type: str,  # pylint: disable=redefined-builtin
           handler: Optional[events.Handler[events.GenericEventArguments]] = None,
           args: Union[None, Sequence[str], Sequence[Optional[Sequence[str]]]] = None,
           *,
           throttle: float = 0.0,
           leading_events: bool = True,
           trailing_events: bool = True,
           js_handler: Optional[str] = '(...args) => emit(...args)',  # DEPRECATED: None will be removed in version 3.0
           ) -> Self:
        """订阅事件。

        事件处理器可以是 Python 函数、JavaScript 函数或两者的组合：

        - 如果您想在服务器上处理带有所有（可序列化）事件参数的事件，
          使用 Python ``handler``。
        - 如果您想在客户端处理事件而不向服务器发送任何内容，
          使用 ``js_handler`` 和处理事件的 JavaScript 函数。
        - 如果您想在服务器上处理事件参数的子集或转换版本，
          使用 ``js_handler`` 和使用 ``emit()`` 发送转换参数的 JavaScript 函数，并
          使用 Python ``handler`` 在服务器端处理这些参数。
          ``js_handler`` 也可以决定选择性地向服务器发送参数，
          在这种情况下，Python ``handler`` 不会总是被调用。

        请注意，参数 ``throttle``、``leading_events`` 和 ``trailing_events`` 只在
        向服务器发送事件时相关。

        *在版本 2.18.0 中更新：两个处理器可以同时指定。*

        :param type: 事件名称（例如 "click"、"mousedown" 或 "update:model-value"）
        :param handler: 事件发生时调用的回调函数
        :param args: 发送给事件处理器的事件消息中包含的参数（默认：``None`` 表示全部）
        :param throttle: 事件发生之间的最小时间（以秒为单位）（默认：0.0）
        :param leading_events: 是否在第一次事件发生时立即触发事件处理器（默认：``True``）
        :param trailing_events: 是否在最后一次事件发生后触发事件处理器（默认：``True``）
        :param js_handler: 在客户端处理事件的 JavaScript 函数（默认："(...args) => emit(...args)"）
        """
        if js_handler is None:
            helpers.warn_once('Passing `js_handler=None` to `on()` is deprecated. '
                              'Use the default "(...args) => emit(...args)" instead or remove the parameter.')
        if js_handler == '(...args) => emit(...args)':
            js_handler = None

        if handler or js_handler:
            listener = EventListener(
                element_id=self.id,
                type=helpers.event_type_to_camel_case(type),
                args=[args] if args and isinstance(args[0], str) else args,  # type: ignore
                handler=handler,
                js_handler=js_handler,
                throttle=throttle,
                leading_events=leading_events,
                trailing_events=trailing_events,
                request=storage.request_contextvar.get(),
            )
            self._event_listeners[listener.id] = listener
            self.update()
        return self

    def _handle_event(self, msg: Dict) -> None:
        listener = self._event_listeners[msg['listener_id']]
        storage.request_contextvar.set(listener.request)
        args = events.GenericEventArguments(sender=self, client=self.client, args=msg['args'])
        events.handle_event(listener.handler, args)

    def update(self) -> None:
        """在客户端更新元素。"""
        if self.is_deleted:
            return
        self.client.outbox.enqueue_update(self)

    def run_method(self, name: str, *args: Any, timeout: float = 1) -> AwaitableResponse:
        """在客户端运行方法。

        如果函数被等待，将返回方法调用的结果。
        否则，方法将在不等待响应的情况下执行。

        :param name: 方法名称
        :param args: 传递给方法的参数
        :param timeout: 等待响应的最大时间（默认：1 秒）
        """
        if not core.loop:
            return NullResponse()
        return self.client.run_javascript(f'return runMethod({self.id}, "{name}", {json.dumps(args)})', timeout=timeout)

    def get_computed_prop(self, prop_name: str, *, timeout: float = 1) -> AwaitableResponse:
        """返回计算属性。

        应该等待此函数以正确返回计算属性。

        :param prop_name: 计算属性的名称
        :param timeout: 等待响应的最大时间（默认：1 秒）
        """
        if not core.loop:
            return NullResponse()
        return self.client.run_javascript(f'return getComputedProp({self.id}, "{prop_name}")', timeout=timeout)

    def ancestors(self, *, include_self: bool = False) -> Iterator[Element]:
        """遍历元素的祖先。

        :param include_self: 是否在遍历中包含元素本身
        """
        if include_self:
            yield self
        if self.parent_slot:
            yield from self.parent_slot.parent.ancestors(include_self=True)

    def descendants(self, *, include_self: bool = False) -> Iterator[Element]:
        """遍历元素的后代。

        :param include_self: 是否在遍历中包含元素本身
        """
        if include_self:
            yield self
        for child in self:
            yield from child.descendants(include_self=True)

    def clear(self) -> None:
        """移除所有子元素。"""
        self.client.remove_elements(self.descendants())
        for slot in self.slots.values():
            slot.children.clear()
        self.update()

    def move(self,
             target_container: Optional[Element] = None,
             target_index: int = -1, *,
             target_slot: Optional[str] = None) -> None:
        """将元素移动到另一个容器。

        :param target_container: 要移动元素到的容器（默认：父容器）
        :param target_index: 目标插槽内的索引（默认：追加到末尾）
        :param target_slot: 目标容器内的插槽（默认：默认插槽）
        """
        assert self.parent_slot is not None
        self.parent_slot.children.remove(self)
        self.parent_slot.parent.update()
        target_container = target_container or self.parent_slot.parent

        if target_slot is None:
            self.parent_slot = target_container.default_slot
        elif target_slot in target_container.slots:
            self.parent_slot = target_container.slots[target_slot]
        else:
            raise ValueError(f'Slot "{target_slot}" does not exist in the target container. '
                             f'Add it first using `add_slot("{target_slot}")`.')

        target_index = target_index if target_index >= 0 else len(self.parent_slot.children)
        self.parent_slot.children.insert(target_index, self)

        target_container.update()

    def remove(self, element: Union[Element, int]) -> None:
        """移除子元素。

        :param element: 元素实例或其 ID
        """
        if isinstance(element, int):
            children = list(self)
            element = children[element]
        self.client.remove_elements(element.descendants(include_self=True))
        assert element.parent_slot is not None
        element.parent_slot.children.remove(element)
        self.update()

    def delete(self) -> None:
        """删除元素及其所有子元素。"""
        assert self.parent_slot is not None
        self.parent_slot.parent.remove(self)

    def _handle_delete(self) -> None:
        """元素被删除时调用。

        此方法可以在子类中重写以执行清理任务。
        """

    @property
    def is_deleted(self) -> bool:
        """元素是否已被删除。"""
        return self._deleted

    def __str__(self) -> str:
        result = self.tag if type(self) is Element else self.__class__.__name__  # pylint: disable=unidiomatic-typecheck

        def shorten(content: Any, length: int = 20) -> str:
            text = str(content).replace('\n', ' ').replace('\r', ' ')
            return text[:length].strip() + '...' if len(text) > length else text

        additions = []
        if self._markers:
            additions.append(f'markers={", ".join(self._markers)}')
        if self._text:
            additions.append(f'text={shorten(self._text)}')
        if hasattr(self, 'content') and self.content:  # pylint: disable=no-member
            additions.append(f'content={shorten(self.content)}')  # pylint: disable=no-member
        IGNORED_PROPS = {'loopback', 'color', 'view', 'innerHTML', 'dynamic_resource_path'}
        additions += [
            f'{key}={shorten(value)}'
            for key, value in self._props.items()
            if not key.startswith('_') and key not in IGNORED_PROPS and value
        ]
        if not self.visible:
            additions.append(f'visible={self.visible}')
        if additions:
            result += f' [{", ".join(additions)}]'

        for child in self.default_slot.children:
            for line in str(child).split('\n'):
                result += f'\n {line}'

        return result

    @property
    def html_id(self) -> str:
        """HTML DOM 中元素的 ID。

        *在版本 2.16.0 中新增*
        """
        return f'c{self.id}'
