from __future__ import annotations

from typing import Generic, Iterator, List, Optional, Type, TypeVar, Union, overload

from typing_extensions import Self

from .context import context
from .element import Element
from .elements.choice_element import ChoiceElement
from .elements.mixins.content_element import ContentElement
from .elements.mixins.source_element import SourceElement
from .elements.mixins.text_element import TextElement
from .elements.notification import Notification
from .elements.select import Select

T = TypeVar('T', bound=Element)


class ElementFilter(Generic[T]):
    DEFAULT_LOCAL_SCOPE = False

    @overload
    def __init__(self: ElementFilter[Element], *,
                 marker: Union[str, List[str], None] = None,
                 content: Union[str, List[str], None] = None,
                 local_scope: bool = DEFAULT_LOCAL_SCOPE,
                 ) -> None:
        ...

    @overload
    def __init__(self, *,
                 kind: Type[T],
                 marker: Union[str, List[str], None] = None,
                 content: Union[str, List[str], None] = None,
                 local_scope: bool = DEFAULT_LOCAL_SCOPE,
                 ) -> None:
        ...

    def __init__(self, *,
                 kind: Optional[Type[T]] = None,
                 marker: Union[str, List[str], None] = None,
                 content: Union[str, List[str], None] = None,
                 local_scope: bool = DEFAULT_LOCAL_SCOPE,
                 ) -> None:
        """ElementFilter

        有时候搜索当前页面的 Python 元素树会很方便。
        ``ElementFilter()`` 允许通过元素类型、标记和内容进行强大的过滤。
        它还提供了一个流畅的接口来应用更多过滤器，如排除元素或在特定父元素内过滤元素。
        过滤器可以用作迭代器来迭代找到的元素，并且总是在迭代时应用，而不是在实例化时应用。

        元素在满足以下所有条件时被产生：

        - 元素是指定的类型（如果指定）。
        - 元素不是任何排除的类型。
        - 元素具有所有指定的标记。
        - 元素没有任何排除的标记。
        - 元素包含所有指定的内容。
        - 元素没有任何排除的内容。

        - 其祖先包括通过 ``within`` 定义的所有指定实例。
        - 其祖先不包括通过 ``not_within`` 定义的任何指定实例。
        - 其祖先包括通过 ``within`` 定义的所有指定类型。
        - 其祖先不包括通过 ``not_within`` 定义的任何指定类型。
        - 其祖先包括通过 ``within`` 定义的所有指定标记。
        - 其祖先不包括通过 ``not_within`` 定义的任何指定标记。

        元素"内容"包括其文本、标签、图标、占位符、值、消息、内容、源。
        像 "Hello World!" 中的 "Hello" 这样的部分匹配就足以进行内容过滤。

        :param kind: 按元素类型过滤；迭代器将是 ``kind`` 类型
        :param marker: 按元素标记过滤；可以是字符串列表或单个字符串，其中标记由空格分隔
        :param content: 过滤在其内容属性之一（如 ``.text``、``.value``、``.source`` 等）中包含 ``content`` 的元素；可以是单个字符串或必须全部匹配的字符串列表
        :param local_scope: 如果为 `True`，则只返回当前范围内的元素；默认搜索整个页面（此默认行为可以通过 ``ElementFilter.DEFAULT_LOCAL_SCOPE = True`` 更改）
        """
        self._kind = kind
        self._markers = marker.split() if isinstance(marker, str) else marker or []
        self._contents = [content] if isinstance(content, str) else content or []

        self._within_kinds: List[Type[Element]] = []
        self._within_instances: List[Element] = []
        self._within_markers: List[str] = []

        self._not_within_kinds: List[Type[Element]] = []
        self._not_within_instances: List[Element] = []
        self._not_within_markers: List[str] = []

        self._exclude_kinds: List[Type[Element]] = []
        self._exclude_markers: List[str] = []
        self._exclude_content: List[str] = []

        self._scope = context.slot.parent if local_scope else context.client.layout

    def __iter__(self) -> Iterator[T]:
        for element in self._scope.descendants():
            if self._kind and not isinstance(element, self._kind):
                continue
            if self._exclude_kinds and isinstance(element, tuple(self._exclude_kinds)):
                continue

            if any(marker not in element._markers for marker in self._markers):
                continue
            if any(marker in element._markers for marker in self._exclude_markers):
                continue

            if self._contents or self._exclude_content:
                element_contents = [content for content in (
                    element.props.get('text'),
                    element.props.get('label'),
                    element.props.get('icon'),
                    element.props.get('placeholder'),
                    element.props.get('value'),
                    element.props.get('error-message'),
                    element.text if isinstance(element, TextElement) else None,
                    element.content if isinstance(element, ContentElement) else None,
                    element.source if isinstance(element, SourceElement) else None,
                ) if content]
                if isinstance(element, Notification):
                    element_contents.append(element.message)
                if isinstance(element, ChoiceElement):
                    if isinstance(element, Select):
                        values = element.value if element.multiple else [element.value]
                        labels = [value if isinstance(element.options, list) else element.options.get(value, '')
                                  for value in values]
                        element_contents.extend(labels)
                    if not isinstance(element, Select) or element.is_showing_popup:
                        element_contents.extend(element._labels)  # pylint: disable=protected-access
                if any(all(needle not in str(haystack) for haystack in element_contents) for needle in self._contents):
                    continue
                if any(needle in str(haystack) for haystack in element_contents for needle in self._exclude_content):
                    continue

            ancestors = set(element.ancestors())
            if self._within_instances and not ancestors.issuperset(self._within_instances):
                continue
            if self._not_within_instances and not ancestors.isdisjoint(self._not_within_instances):
                continue
            if self._within_kinds and not all(any(isinstance(ancestor, kind) for ancestor in ancestors) for kind in self._within_kinds):
                continue
            if self._not_within_kinds and any(isinstance(ancestor, tuple(self._not_within_kinds)) for ancestor in ancestors):
                continue
            ancestor_markers = {marker for ancestor in ancestors for marker in ancestor._markers}
            if self._within_markers and not ancestor_markers.issuperset(self._within_markers):
                continue
            if self._not_within_markers and not ancestor_markers.isdisjoint(self._not_within_markers):
                continue

            yield element  # type: ignore

    def within(self, *,
               kind: Optional[Type[Element]] = None,
               marker: Optional[str] = None,
               instance: Union[Element, List[Element], None] = None,
               ) -> Self:
        """过滤在父层次结构中具有特定匹配的元素。"""
        if kind is not None:
            assert issubclass(kind, Element)
            self._within_kinds.append(kind)
        if marker is not None:
            self._within_markers.extend(marker.split())
        if instance is not None:
            self._within_instances.extend(instance if isinstance(instance, list) else [instance])
        return self

    def exclude(self, *,
                kind: Optional[Type[Element]] = None,
                marker: Optional[str] = None,
                content: Optional[str] = None,
                ) -> Self:
        """排除具有特定元素类型、标记或内容的元素。"""
        if kind is not None:
            assert issubclass(kind, Element)
            self._exclude_kinds.append(kind)
        if marker is not None:
            self._exclude_markers.append(marker)
        if content is not None:
            self._exclude_content.append(content)
        return self

    def not_within(self, *,
                   kind: Optional[Type[Element]] = None,
                   marker: Optional[str] = None,
                   instance: Union[Element, List[Element], None] = None,
                   ) -> Self:
        """排除具有特定类型或标记的父元素的元素。"""
        if kind is not None:
            assert issubclass(kind, Element)
            self._not_within_kinds.append(kind)
        if marker is not None:
            self._not_within_markers.extend(marker.split())
        if instance is not None:
            self._not_within_instances.extend(instance if isinstance(instance, list) else [instance])
        return self

    def classes(self, add: Optional[str] = None, *, remove: Optional[str] = None, replace: Optional[str] = None) -> Self:
        """应用、移除或替换 HTML 类。

        这允许使用 `Tailwind <https://v3.tailwindcss.com/>`_ 或 `Quasar <https://quasar.dev/>`_ 类修改元素的外观或布局。

        如果不需要预定义的类，移除或替换类可能会有帮助。

        :param add: 以空格分隔的类字符串
        :param remove: 要从元素中移除的以空格分隔的类字符串
        :param replace: 用于替换现有类的以空格分隔的类字符串
        """
        for element in self:
            element.classes(add, remove=remove, replace=replace)
        return self

    def style(self, add: Optional[str] = None, *, remove: Optional[str] = None, replace: Optional[str] = None) -> Self:
        """应用、移除或替换 CSS 定义。

        如果不需要预定义的样式，移除或替换样式可能会有帮助。

        :param add: 要添加到元素的以分号分隔的样式列表
        :param remove: 要从元素中移除的以分号分隔的样式列表
        :param replace: 用于替换现有样式的以分号分隔的样式列表
        """
        for element in self:
            element.style(add, remove=remove, replace=replace)
        return self

    def props(self, add: Optional[str] = None, *, remove: Optional[str] = None) -> Self:
        """添加或移除属性。

        这允许使用 `Quasar <https://quasar.dev/>`_ 属性修改元素的外观或布局。
        由于属性只是作为 HTML 属性应用，它们可以用于任何 HTML 元素。

        如果没有指定值，布尔属性假定为 ``True``。

        :param add: 要添加的以空格分隔的布尔值或键值对列表
        :param remove: 要移除的以空格分隔的属性键列表
        """
        for element in self:
            element.props(add, remove=remove)
        return self
