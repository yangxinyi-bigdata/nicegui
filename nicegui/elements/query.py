import weakref
from typing import Optional

from typing_extensions import Self

from ..classes import Classes
from ..context import context
from ..element import Element
from ..props import Props
from ..style import Style


class QueryElement(Element, component='query.js'):

    def __init__(self, selector: str) -> None:
        super().__init__()
        self._props['selector'] = selector
        self._props['classes'] = []
        self._props['style'] = {}
        self._props['props'] = {}


class Query:

    def __init__(self, selector: str) -> None:
        """查询选择器

        要操作文档正文等元素，可以使用`ui.query`函数。
        使用查询结果可以像其他UI元素一样添加类、样式和属性。
        例如，这对于更改页面背景颜色很有用（例如`ui.query('body').classes('bg-green')`）。

        :param selector: CSS选择器（例如"body"、"#my-id"、".my-class"、"div > p"）
        """
        for element in context.client.elements.values():
            if isinstance(element, QueryElement) and element.props['selector'] == selector:
                self._element = weakref.ref(element)
                break
        else:
            self._element = weakref.ref(QueryElement(selector))

    @property
    def element(self) -> QueryElement:
        """此查询所属的元素。"""
        element = self._element()
        if element is None:
            raise RuntimeError('The element this query belongs to has been deleted.')
        return element

    def classes(self,
                add: Optional[str] = None, *,
                remove: Optional[str] = None,
                toggle: Optional[str] = None,
                replace: Optional[str] = None,
                ) -> Self:
        """应用、移除、切换或替换HTML类。

        这允许使用`Tailwind <https://v3.tailwindcss.com/>`_或`Quasar <https://quasar.dev/>`_类来修改元素的外观或布局。

        如果不需要预定义的类，移除或替换类会很有帮助。

        :param add: 空格分隔的类字符串
        :param remove: 要从元素中移除的空格分隔的类字符串
        :param toggle: 要切换的空格分隔的类字符串（*在版本2.7.0中添加*）
        :param replace: 用于替换现有类的空格分隔的类字符串
        """
        element = self.element
        classes = Classes.update_list(element.props['classes'], add, remove, toggle, replace)
        new_classes = [c for c in classes if c not in element.props['classes']]
        old_classes = [c for c in element.props['classes'] if c not in classes]
        if new_classes:
            element.run_method('add_classes', new_classes)
        if old_classes:
            element.run_method('remove_classes', old_classes)
        element.props['classes'] = classes
        return self

    def style(self, add: Optional[str] = None, *, remove: Optional[str] = None, replace: Optional[str] = None) \
            -> Self:
        """应用、移除或替换CSS定义。

        如果预定义的样式不符合需求，移除或替换样式会很有帮助。

        :param add: 要添加到元素的用分号分隔的样式列表
        :param remove: 要从元素中移除的用分号分隔的样式列表
        :param replace: 用于替换现有样式的用分号分隔的样式列表
        """
        element = self.element
        old_style = Style.parse(remove)
        for key in old_style:
            element.props['style'].pop(key, None)
        if old_style:
            element.run_method('remove_style', list(old_style))
        element.props['style'].update(Style.parse(add))
        element.props['style'].update(Style.parse(replace))
        if element.props['style']:
            element.run_method('add_style', element.props['style'])
        return self

    def props(self, add: Optional[str] = None, *, remove: Optional[str] = None) -> Self:
        """添加或移除属性。

        这允许使用`Quasar <https://quasar.dev/>`_属性来修改元素的外观或布局。
        由于属性只是作为HTML属性应用，因此可以与任何HTML元素一起使用。

        如果未指定值，布尔属性假定为``True``。

        :param add: 要添加的空格分隔的布尔值或key=value对列表
        :param remove: 要移除的空格分隔的属性键列表
        """
        element = self.element
        old_props = Props.parse(remove)
        for key in old_props:
            element.props['props'].pop(key, None)
        if old_props:
            element.run_method('remove_props', list(old_props))
        new_props = Props.parse(add)
        element.props['props'].update(new_props)
        if element.props['props']:
            element.run_method('add_props', element.props['props'])
        return self
