from typing import Any, Awaitable, Callable, Dict, Optional, Union

from typing_extensions import Self

from ... import background_tasks, helpers
from .value_element import ValueElement

ValidationFunction = Callable[[Any], Union[Optional[str], Awaitable[Optional[str]]]]
ValidationDict = Dict[str, Callable[[Any], bool]]


class ValidationElement(ValueElement):
    """验证元素混入

    为元素提供数据验证功能的混入类。
    支持同步和异步验证函数，以及验证规则字典。
    自动管理错误消息显示和验证状态。
    """

    def __init__(self, validation: Optional[Union[ValidationFunction, ValidationDict]], **kwargs: Any) -> None:
        """初始化验证元素

        :param validation: 验证函数或验证规则字典（``None``表示禁用验证）
        """
        self._validation = validation
        self._auto_validation = True
        self._error: Optional[str] = None
        super().__init__(**kwargs)
        self._props['error'] = None if validation is None else False  # 注意：为错误消息保留底部空间

    @property
    def validation(self) -> Optional[Union[ValidationFunction, ValidationDict]]:
        """验证函数或验证函数字典。"""
        return self._validation

    @validation.setter
    def validation(self, validation: Optional[Union[ValidationFunction, ValidationDict]]) -> None:
        """设置验证函数或验证函数字典。

        :param validation: 验证函数或验证函数字典（``None``表示禁用验证）
        """
        self._validation = validation
        self.validate(return_result=False)

    @property
    def error(self) -> Optional[str]:
        """来自验证函数的最新错误消息。"""
        return self._error

    @error.setter
    def error(self, error: Optional[str]) -> None:
        """设置错误消息。

        :param error: 可选的错误消息
        """
        new_error_prop = None if self.validation is None else (error is not None)
        if self._error == error and self._props['error'] == new_error_prop:
            return
        self._error = error
        self._props['error'] = new_error_prop
        self._props['error-message'] = error
        self.update()

    def validate(self, *, return_result: bool = True) -> bool:
        """验证当前值并在必要时设置错误消息。

        对于异步验证函数，``return_result``必须设置为``False``，返回值将为``True``，
        独立于在后台评估的验证结果。

        *在版本2.7.0中更新：添加了对异步验证函数的支持。*

        :param return_result: 是否返回验证结果（默认：``True``）
        :return: 验证是否成功（异步验证函数总是返回``True``）
        """
        if helpers.is_coroutine_function(self._validation):
            async def await_error():
                assert callable(self._validation)
                result = self._validation(self.value)
                assert isinstance(result, Awaitable)
                self.error = await result
            if return_result:
                raise NotImplementedError('validate方法无法为异步验证函数返回结果。')
            background_tasks.create(await_error(), name=f'validate {self.id}')
            return True

        if callable(self._validation):
            result = self._validation(self.value)
            assert not isinstance(result, Awaitable)
            self.error = result
            return self.error is None

        if isinstance(self._validation, dict):
            for message, check in self._validation.items():
                if not check(self.value):
                    self.error = message
                    return False

        self.error = None
        return True

    def without_auto_validation(self) -> Self:
        """禁用值变化时的自动验证。"""
        self._auto_validation = False
        return self

    def _handle_value_change(self, value: Any) -> None:
        super()._handle_value_change(value)
        if self._auto_validation:
            self.validate(return_result=False)
