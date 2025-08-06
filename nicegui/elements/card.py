from typing import Literal, Optional

from typing_extensions import Self

from ..element import Element


class Card(Element, default_classes='nicegui-card'):

    def __init__(self, *,
                 align_items: Optional[Literal['start', 'end', 'center', 'baseline', 'stretch']] = None,
                 ) -> None:
        """卡片

        此元素基于Quasar的`QCard <https://quasar.dev/vue-components/card>`_组件。
        它提供了一个带有阴影的容器。

        注意：
        与此元素不同，
        原始的QCard默认没有内边距，并且会隐藏嵌套元素的外边框和阴影。
        如果您想要原始行为，请使用`tight`方法。

        *2.0.0版本更新：不再隐藏嵌套元素的外边框和阴影。*

        :param align_items: 卡片中项目的对齐方式（"start"、"end"、"center"、"baseline"或"stretch"；默认：`None`）
        """
        super().__init__('q-card')
        if align_items:
            self._classes.append(f'items-{align_items}')

    def tight(self) -> Self:
        """移除嵌套元素之间的内边距和间隙。"""
        return self.classes('nicegui-card-tight')


class CardSection(Element):

    def __init__(self) -> None:
        """卡片部分

        此元素基于Quasar的`QCardSection <https://quasar.dev/vue-components/card#qcardsection-api>`_组件。
        """
        super().__init__('q-card-section')


class CardActions(Element):

    def __init__(self) -> None:
        """卡片操作区域

        此元素基于Quasar的`QCardActions <https://quasar.dev/vue-components/card#qcardactions-api>`_组件。
        """
        super().__init__('q-card-actions')
