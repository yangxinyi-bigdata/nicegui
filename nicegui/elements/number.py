from typing import Any, Optional, Union

from ..events import GenericEventArguments, Handler, ValueChangeEventArguments
from .mixins.disableable_element import DisableableElement
from .mixins.label_element import LabelElement
from .mixins.validation_element import ValidationDict, ValidationElement, ValidationFunction


class Number(LabelElement, ValidationElement, DisableableElement):
    LOOPBACK = False

    def __init__(self,
                 label: Optional[str] = None, *,
                 placeholder: Optional[str] = None,
                 value: Optional[float] = None,
                 min: Optional[float] = None,  # pylint: disable=redefined-builtin
                 max: Optional[float] = None,  # pylint: disable=redefined-builtin
                 precision: Optional[int] = None,
                 step: Optional[float] = None,
                 prefix: Optional[str] = None,
                 suffix: Optional[str] = None,
                 format: Optional[str] = None,  # pylint: disable=redefined-builtin
                 on_change: Optional[Handler[ValueChangeEventArguments]] = None,
                 validation: Optional[Union[ValidationFunction, ValidationDict]] = None,
                 ) -> None:
        """数字输入框

        此元素基于Quasar的`QInput <https://quasar.dev/vue-components/input>`_组件。

        您可以使用`validation`参数来定义验证规则字典，
        例如``{'太小了！': lambda value: value > 3}``。
        第一个失败的规则的键将显示为错误消息。
        或者，您可以传递一个返回可选错误消息的可调用对象。
        要禁用每次值更改时的自动验证，可以使用`without_auto_validation`方法。

        :param label: 数字输入框的显示名称
        :param placeholder: 如果没有输入值时显示的文本
        :param value: 字段的初始值
        :param min: 允许的最小值
        :param max: 允许的最大值
        :param precision: 允许的小数位数（默认：无限制，负数：小数点前的位数）
        :param step: 步进按钮的步长
        :param prefix: 添加到显示值前的前缀
        :param suffix: 添加到显示值后的后缀
        :param format: 格式化显示值的字符串，如"%.2f"
        :param on_change: 值更改时执行的回调函数
        :param validation: 验证规则字典或返回可选错误消息的可调用对象（默认：None表示不验证）
        """
        self.format = format
        super().__init__(tag='q-input', label=label, value=value, on_value_change=on_change, validation=validation)
        self._props['type'] = 'number'
        if placeholder is not None:
            self._props['placeholder'] = placeholder
        if min is not None:
            self._props['min'] = min
        if max is not None:
            self._props['max'] = max
        self._precision = precision
        if step is not None:
            self._props['step'] = step
        if prefix is not None:
            self._props['prefix'] = prefix
        if suffix is not None:
            self._props['suffix'] = suffix
        self.on('blur', self.sanitize, [])

    @property
    def min(self) -> float:
        """允许的最小值。"""
        return self._props.get('min', -float('inf'))

    @min.setter
    def min(self, value: float) -> None:
        if self._props.get('min') == value:
            return
        self._props['min'] = value
        self.sanitize()
        self.update()

    @property
    def max(self) -> float:
        """允许的最大值。"""
        return self._props.get('max', float('inf'))

    @max.setter
    def max(self, value: float) -> None:
        if self._props.get('max') == value:
            return
        self._props['max'] = value
        self.sanitize()
        self.update()

    @property
    def precision(self) -> Optional[int]:
        """允许的小数位数（默认：无限制，负数：小数点前的位数）。"""
        return self._precision

    @precision.setter
    def precision(self, value: Optional[int]) -> None:
        self._precision = value
        self.sanitize()

    @property
    def out_of_limits(self) -> bool:
        """当前值是否超出允许的限制。"""
        return not self.min <= self.value <= self.max

    def sanitize(self) -> None:
        """将当前值清理为在允许的限制范围内。"""
        if self.value is None:
            return
        value = float(self.value)
        value = max(value, self.min)
        value = min(value, self.max)
        if self.precision is not None:
            value = float(round(value, self.precision))
        self.set_value(float(self.format % value) if self.format else value)
        self.update()

    def _event_args_to_value(self, e: GenericEventArguments) -> Any:
        if not e.args:
            return None
        return float(e.args)

    def _value_to_model_value(self, value: Any) -> Any:
        if value is None:
            return None
        if self.format is None:
            old_value = float(self._props.get(self.VALUE_PROP) or 0)
            if old_value == int(old_value) and value == int(value):
                return str(int(value))  # preserve integer representation
            return str(value)
        if value == '':
            return 0
        return self.format % float(value)
