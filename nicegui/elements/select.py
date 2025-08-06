from collections.abc import Generator, Iterable
from copy import deepcopy
from typing import Any, Callable, Dict, Iterator, List, Literal, Optional, Union

from ..events import GenericEventArguments, Handler, ValueChangeEventArguments
from .choice_element import ChoiceElement
from .mixins.disableable_element import DisableableElement
from .mixins.label_element import LabelElement
from .mixins.validation_element import ValidationDict, ValidationElement, ValidationFunction


class Select(LabelElement, ValidationElement, ChoiceElement, DisableableElement, component='select.js'):

    def __init__(self,
                 options: Union[List, Dict], *,
                 label: Optional[str] = None,
                 value: Any = None,
                 on_change: Optional[Handler[ValueChangeEventArguments]] = None,
                 with_input: bool = False,
                 new_value_mode: Optional[Literal['add', 'add-unique', 'toggle']] = None,
                 multiple: bool = False,
                 clearable: bool = False,
                 validation: Optional[Union[ValidationFunction, ValidationDict]] = None,
                 key_generator: Optional[Union[Callable[[Any], Any], Iterator[Any]]] = None,
                 ) -> None:
        """下拉选择框

        此元素基于Quasar的`QSelect <https://quasar.dev/vue-components/select>`_组件。

        选项可以指定为值列表，或者映射值到标签的字典。
        操作选项后，调用`update()`来更新UI中的选项。

        如果`with_input`为True，会显示一个输入框来过滤选项。

        如果`new_value_mode`不为None，则意味着`with_input=True`，用户可以在输入框中输入新值。
        详情请参见`Quasar文档 <https://quasar.dev/vue-components/select#the-new-value-mode-prop>`_。
        注意，在以编程方式设置`value`属性时，此模式无效。

        您可以使用`validation`参数来定义验证规则字典，
        例如``{'Too long!': lambda value: len(value) < 3}``。
        第一个失败的规则的键将作为错误消息显示。
        或者，您可以传递一个返回可选错误消息的可调用对象。
        要禁用每次值更改时的自动验证，可以使用`without_auto_validation`方法。

        :param options: 指定选项的列表 ['value1', ...] 或字典 `{'value1':'label1', ...}`
        :param label: 显示在选择框上方的标签
        :param value: 初始值
        :param on_change: 选择更改时执行的回调函数
        :param with_input: 是否显示输入框来过滤选项
        :param new_value_mode: 处理用户输入的新值（默认：None，即无新值）
        :param multiple: 是否允许多选
        :param clearable: 是否添加清除选择的按钮
        :param validation: 验证规则字典或返回可选错误消息的可调用对象（默认：None表示无验证）
        :param key_generator: 为新值生成字典键的回调函数或迭代器
        """
        self.multiple = multiple
        if multiple:
            if value is None:
                value = []
            elif not isinstance(value, list):
                value = [value]
            else:
                value = value[:]  # NOTE: avoid modifying the original list which could be the list of options (#3014)
        super().__init__(label=label, options=options, value=value, on_change=on_change, validation=validation)
        if isinstance(key_generator, Generator):
            next(key_generator)  # prime the key generator, prepare it to receive the first value
        self.key_generator = key_generator
        if new_value_mode is not None:
            if isinstance(options, dict) and new_value_mode == 'add' and key_generator is None:
                raise ValueError('new_value_mode "add" is not supported for dict options without key_generator')
            self._props['new-value-mode'] = new_value_mode
            with_input = True
        if with_input:
            self.original_options = deepcopy(options)
            self._props['use-input'] = True
            self._props['hide-selected'] = not multiple
            self._props['fill-input'] = True
            self._props['input-debounce'] = 0
        self._props['multiple'] = multiple
        self._props['clearable'] = clearable

        self._is_showing_popup = False
        self.on('popup-show', lambda e: setattr(e.sender, '_is_showing_popup', True))
        self.on('popup-hide', lambda e: setattr(e.sender, '_is_showing_popup', False))

    @property
    def is_showing_popup(self) -> bool:
        """选项弹出窗口当前是否显示。"""
        return self._is_showing_popup

    def _event_args_to_value(self, e: GenericEventArguments) -> Any:
        # pylint: disable=too-many-nested-blocks
        if self.multiple:
            if e.args is None:
                return []
            else:
                if self._props.get('new-value-mode') == 'add-unique':
                    # handle issue #4896: eliminate duplicate arguments
                    for arg1 in [a for a in e.args if isinstance(a, str)]:
                        for arg2 in [a for a in e.args if isinstance(a, dict)]:
                            if arg1 == arg2['label']:
                                e.args.remove(arg1)
                                break
                args = [self._values[arg['value']] if isinstance(arg, dict) else arg for arg in e.args]
                for arg in e.args:
                    if isinstance(arg, str):
                        self._handle_new_value(arg)
                return [arg for arg in args if arg in self._values]
        else:  # noqa: PLR5501
            if e.args is None:
                return None
            else:  # noqa: PLR5501
                if isinstance(e.args, str):
                    new_value = self._handle_new_value(e.args)
                    return new_value if new_value in self._values else None
                else:
                    return self._values[e.args['value']]

    def _value_to_model_value(self, value: Any) -> Any:
        # pylint: disable=no-else-return
        if self.multiple:
            result = []
            for item in value or []:
                try:
                    index = self._values.index(item)
                    result.append({'value': index, 'label': self._labels[index]})
                except ValueError:
                    pass
            return result
        else:
            try:
                index = self._values.index(value)
                return {'value': index, 'label': self._labels[index]}
            except ValueError:
                return None

    def _generate_key(self, value: str) -> Any:
        if isinstance(self.key_generator, Generator):
            return self.key_generator.send(value)
        if isinstance(self.key_generator, Iterable):
            return next(self.key_generator)
        if callable(self.key_generator):
            return self.key_generator(value)
        return value

    def _handle_new_value(self, value: str) -> Any:
        mode = self._props['new-value-mode']
        if isinstance(self.options, list):
            if mode == 'add':
                self.options.append(value)
            elif mode == 'add-unique':
                if value not in self.options:
                    self.options.append(value)
            elif mode == 'toggle':
                if value in self.options:
                    self.options.remove(value)
                else:
                    self.options.append(value)
            # NOTE: self._labels and self._values are updated via self.options since they share the same references
            return value
        else:
            key = value
            if mode == 'add':
                key = self._generate_key(value)
                self.options[key] = value
            elif mode == 'add-unique':
                if value not in self.options.values():
                    key = self._generate_key(value)
                    self.options[key] = value
            elif mode == 'toggle':
                if value in self.options:
                    self.options.pop(value)
                else:
                    key = self._generate_key(value)
                    self.options.update({key: value})
            self._update_values_and_labels()
            return key
