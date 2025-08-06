import asyncio
from typing import Optional

from typing_extensions import Self

from ..element import Element
from ..events import (
    ClickEventArguments,
    GenericEventArguments,
    Handler,
    SceneClickEventArguments,
    SceneClickHit,
    handle_event,
)
from .scene import Scene, SceneCamera


class SceneView(Element,
                component='scene_view.js',
                dependencies=[
                    'lib/tween/tween.umd.js',
                    'lib/three/three.module.js',
                ],
                default_classes='nicegui-scene-view'):

    def __init__(self,
                 scene: Scene,
                 width: int = 400,
                 height: int = 300,
                 camera: Optional[SceneCamera] = None,
                 on_click: Optional[Handler[ClickEventArguments]] = None,
                 ) -> None:
        """场景视图

        使用`three.js <https://threejs.org/>`_显示3D场景的附加视图。
        此组件只能显示场景而不能修改它。
        但是，您可以独立移动相机。

        当前限制：不支持2D和3D文本对象，不会在场景视图中显示。

        :param scene: 将在画布上显示的场景
        :param width: 画布的宽度
        :param height: 画布的高度
        :param camera: 相机定义，``ui.scene.perspective_camera``（默认）或``ui.scene.orthographic_camera``的实例
        :param on_click: 点击3D对象时要执行的回调函数
        """
        super().__init__()
        self._props['width'] = width
        self._props['height'] = height
        self._props['scene_id'] = scene.id
        self.camera = camera or Scene.perspective_camera()
        self._props['camera_type'] = self.camera.type
        self._props['camera_params'] = self.camera.params
        self._click_handlers = [on_click] if on_click else []
        self.on('init', self._handle_init)
        self.on('click3d', self._handle_click)

    def on_click(self, callback: Handler[ClickEventArguments]) -> Self:
        """添加点击3D对象时要调用的回调函数。"""
        self._click_handlers.append(callback)
        return self

    def _handle_init(self, e: GenericEventArguments) -> None:
        with self.client.individual_target(e.args['socket_id']):
            self.move_camera(duration=0)
            self.run_method('init')

    async def initialized(self) -> None:
        """等待场景初始化完成。"""
        event = asyncio.Event()
        self.on('init', event.set, [])
        await self.client.connected()
        await event.wait()

    def _handle_click(self, e: GenericEventArguments) -> None:
        arguments = SceneClickEventArguments(
            sender=self,
            client=self.client,
            click_type=e.args['click_type'],
            button=e.args['button'],
            alt=e.args['alt_key'],
            ctrl=e.args['ctrl_key'],
            meta=e.args['meta_key'],
            shift=e.args['shift_key'],
            hits=[SceneClickHit(
                object_id=hit['object_id'],
                object_name=hit['object_name'],
                x=hit['point']['x'],
                y=hit['point']['y'],
                z=hit['point']['z'],
            ) for hit in e.args['hits']],
        )
        for handler in self._click_handlers:
            handle_event(handler, arguments)

    def move_camera(self,
                    x: Optional[float] = None,
                    y: Optional[float] = None,
                    z: Optional[float] = None,
                    look_at_x: Optional[float] = None,
                    look_at_y: Optional[float] = None,
                    look_at_z: Optional[float] = None,
                    up_x: Optional[float] = None,
                    up_y: Optional[float] = None,
                    up_z: Optional[float] = None,
                    duration: float = 0.5) -> None:
        """将相机移动到新位置。

        :param x: 相机x位置
        :param y: 相机y位置
        :param z: 相机z位置
        :param look_at_x: 相机观察目标x位置
        :param look_at_y: 相机观察目标y位置
        :param look_at_z: 相机观察目标z位置
        :param up_x: 相机上向量的x分量
        :param up_y: 相机上向量的y分量
        :param up_z: 相机上向量的z分量
        :param duration: 移动持续时间，以秒为单位（默认：`0.5`）
        """
        self.camera.x = self.camera.x if x is None else x
        self.camera.y = self.camera.y if y is None else y
        self.camera.z = self.camera.z if z is None else z
        self.camera.look_at_x = self.camera.look_at_x if look_at_x is None else look_at_x
        self.camera.look_at_y = self.camera.look_at_y if look_at_y is None else look_at_y
        self.camera.look_at_z = self.camera.look_at_z if look_at_z is None else look_at_z
        self.camera.up_x = self.camera.up_x if up_x is None else up_x
        self.camera.up_y = self.camera.up_y if up_y is None else up_y
        self.camera.up_z = self.camera.up_z if up_z is None else up_z
        self.run_method('move_camera',
                        self.camera.x, self.camera.y, self.camera.z,
                        self.camera.look_at_x, self.camera.look_at_y, self.camera.look_at_z,
                        self.camera.up_x, self.camera.up_y, self.camera.up_z, duration)
