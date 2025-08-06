from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Awaitable, Callable, ClassVar, Dict, Generic, List, Optional, Tuple, TypeVar, cast

from typing_extensions import Concatenate, ParamSpec, Self

from .. import background_tasks, core
from ..dataclasses import KWONLY_SLOTS
from ..element import Element
from ..helpers import is_coroutine_function

_S = TypeVar('_S')
_T = TypeVar('_T')
_P = ParamSpec('_P')


@dataclass(**KWONLY_SLOTS)
class RefreshableTarget:
    container: RefreshableContainer
    refreshable: refreshable
    instance: Any
    args: Tuple[Any, ...]
    kwargs: Dict[str, Any]

    current_target: ClassVar[Optional[RefreshableTarget]] = None
    locals: List[Any] = field(default_factory=list)
    next_index: int = 0

    def run(self, func: Callable[..., _T]) -> _T:
        """运行函数并返回结果。"""
        RefreshableTarget.current_target = self
        self.next_index = 0
        # pylint: disable=no-else-return
        if is_coroutine_function(func):
            async def wait_for_result() -> Any:
                with self.container:
                    if self.instance is None:
                        result = func(*self.args, **self.kwargs)
                    else:
                        result = func(self.instance, *self.args, **self.kwargs)
                    assert isinstance(result, Awaitable)
                    return await result
            return wait_for_result()  # type: ignore
        else:
            with self.container:
                if self.instance is None:
                    return func(*self.args, **self.kwargs)
                else:
                    return func(self.instance, *self.args, **self.kwargs)


class RefreshableContainer(Element, component='refreshable.js'):
    pass


class refreshable(Generic[_P, _T]):

    def __init__(self, func: Callable[_P, _T]) -> None:
        """可刷新的 UI 函数

        ``@ui.refreshable`` 装饰器允许您创建具有 ``refresh`` 方法的函数。
        此方法将自动删除函数创建的所有元素并重新创建它们。

        对于在类中装饰可刷新方法，有一个 ``@ui.refreshable_method`` 装饰器，
        它是等效的，但可以防止静态类型检查错误。
        """
        self.func = func
        self.instance = None
        self.targets: List[RefreshableTarget] = []

    def __get__(self, instance, _) -> Self:
        self.instance = instance
        return self

    def __getattribute__(self, __name: str) -> Any:
        attribute = object.__getattribute__(self, __name)
        if __name == 'refresh':
            def refresh(*args: Any, _instance=self.instance, **kwargs: Any) -> None:
                self.instance = _instance
                attribute(*args, **kwargs)
            return refresh
        return attribute

    def __call__(self, *args: _P.args, **kwargs: _P.kwargs) -> _T:
        self.prune()
        target = RefreshableTarget(container=RefreshableContainer(), refreshable=self, instance=self.instance,
                                   args=args, kwargs=kwargs)
        self.targets.append(target)
        return target.run(self.func)

    def refresh(self, *args: Any, **kwargs: Any) -> None:
        """刷新此函数创建的 UI 元素。

        此方法接受与函数本身相同的参数或其子集。
        它将传递给函数的参数与传递给此方法的参数结合起来。
        """
        self.prune()
        for target in self.targets:
            if target.instance != self.instance:
                continue
            target.container.clear()
            target.args = args or target.args
            target.kwargs.update(kwargs)
            try:
                result = target.run(self.func)
            except TypeError as e:
                if 'got multiple values for argument' in str(e):
                    function = str(e).split()[0].split('.')[-1]
                    parameter = str(e).split()[-1]
                    raise TypeError(f'{parameter} needs to be consistently passed to {function} '
                                    'either as positional or as keyword argument') from e
                raise
            if is_coroutine_function(self.func):
                assert isinstance(result, Awaitable)
                if core.loop and core.loop.is_running():
                    background_tasks.create(result, name=f'refresh {self.func.__name__}')
                else:
                    core.app.on_startup(result)

    def prune(self) -> None:
        """删除所有不再在具有客户端连接的页面上的目标。

        此方法在每次刷新之前自动调用。
        """
        self.targets = [target for target in self.targets if not target.container.is_deleted]


class refreshable_method(Generic[_S, _P, _T], refreshable[_P, _T]):

    def __init__(self, func: Callable[Concatenate[_S, _P], _T]) -> None:
        """可刷新的 UI 方法

        `@ui.refreshable_method` 装饰器允许您创建具有 `refresh` 方法的法。
        此方法将自动删除函数创建的所有元素并重新创建它们。
        """
        super().__init__(func)  # type: ignore


def state(value: Any) -> Tuple[Any, Callable[[Any], None]]:
    """创建一个自动更新其可刷新 UI 容器的状态变量。

    :param value: 状态变量的初始值。

    :return: 包含当前值和更新值的函数的元组。
    """
    target = cast(RefreshableTarget, RefreshableTarget.current_target)

    try:
        index = target.next_index
    except AttributeError as e:
        raise RuntimeError('ui.state() can only be used inside a @ui.refreshable function') from e

    if index >= len(target.locals):
        target.locals.append(value)
    else:
        value = target.locals[index]

    def set_value(new_value: Any) -> None:
        if target.locals[index] == new_value:
            return
        target.locals[index] = new_value
        target.refreshable.refresh(_instance=target.instance)

    target.next_index += 1

    return value, set_value
