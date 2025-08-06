from typing import Literal, Optional

from .mixins.color_elements import TextColorElement

SpinnerTypes = Literal[
    'default',
    'audio',
    'ball',
    'bars',
    'box',
    'clock',
    'comment',
    'cube',
    'dots',
    'facebook',
    'gears',
    'grid',
    'hearts',
    'hourglass',
    'infinity',
    'ios',
    'orbit',
    'oval',
    'pie',
    'puff',
    'radio',
    'rings',
    'tail',
]


class Spinner(TextColorElement):

    def __init__(self,
                 type: Optional[SpinnerTypes] = 'default', *,  # pylint: disable=redefined-builtin
                 size: str = '1em',
                 color: Optional[str] = 'primary',
                 thickness: float = 5.0,
                 ) -> None:
        """旋转器

        此元素基于Quasar的`QSpinner <https://quasar.dev/vue-components/spinners>`_组件。

        :param type: 旋转器类型（例如"audio"、"ball"、"bars"等，默认："default"）
        :param size: 旋转器大小（例如"3em"、"10px"、"xl"等，默认："1em"）
        :param color: 旋转器颜色（Quasar、Tailwind或CSS颜色，或`None`，默认："primary"）
        :param thickness: 旋转器厚度（仅适用于"default"旋转器，默认：5.0）
        """
        super().__init__(tag='q-spinner' if type == 'default' else f'q-spinner-{type}', text_color=color)
        self._props['size'] = size
        self._props['thickness'] = thickness
