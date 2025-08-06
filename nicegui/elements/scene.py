import asyncio
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Literal, Optional, Tuple, Union

from typing_extensions import Self

from .. import binding
from ..dataclasses import KWONLY_SLOTS
from ..element import Element
from ..events import (
    GenericEventArguments,
    Handler,
    SceneClickEventArguments,
    SceneClickHit,
    SceneDragEventArguments,
    handle_event,
)
from .scene_object3d import Object3D


@dataclass(**KWONLY_SLOTS)
class SceneCamera:
    type: Literal['perspective', 'orthographic']
    params: Dict[str, float]
    x: float = 0
    y: float = -3
    z: float = 5
    look_at_x: float = 0
    look_at_y: float = 0
    look_at_z: float = 0
    up_x: float = 0
    up_y: float = 0
    up_z: float = 1


@dataclass(**KWONLY_SLOTS)
class SceneObject:
    id: str = 'scene'


class Scene(Element,
            component='scene.js',
            dependencies=[
                'lib/three/three.module.js',
                'lib/three/modules/BufferGeometryUtils.js',
                'lib/three/modules/CSS2DRenderer.js',
                'lib/three/modules/CSS3DRenderer.js',
                'lib/three/modules/DragControls.js',
                'lib/three/modules/GLTFLoader.js',
                'lib/three/modules/OrbitControls.js',
                'lib/three/modules/STLLoader.js',
                'lib/tween/tween.umd.js',
            ],
            default_classes='nicegui-scene'):
    # pylint: disable=import-outside-toplevel
    from .scene_objects import AxesHelper as axes_helper
    from .scene_objects import Box as box
    from .scene_objects import Curve as curve
    from .scene_objects import Cylinder as cylinder
    from .scene_objects import Extrusion as extrusion
    from .scene_objects import Gltf as gltf
    from .scene_objects import Group as group
    from .scene_objects import Line as line
    from .scene_objects import PointCloud as point_cloud
    from .scene_objects import QuadraticBezierTube as quadratic_bezier_tube
    from .scene_objects import Ring as ring
    from .scene_objects import Sphere as sphere
    from .scene_objects import SpotLight as spot_light
    from .scene_objects import Stl as stl
    from .scene_objects import Text as text
    from .scene_objects import Text3d as text3d
    from .scene_objects import Texture as texture

    def __init__(self,
                 width: int = 400,
                 height: int = 300,
                 grid: Union[bool, Tuple[int, int]] = True,
                 camera: Optional[SceneCamera] = None,
                 on_click: Optional[Handler[SceneClickEventArguments]] = None,
                 click_events: List[str] = ['click', 'dblclick'],  # noqa: B006
                 on_drag_start: Optional[Handler[SceneDragEventArguments]] = None,
                 on_drag_end: Optional[Handler[SceneDragEventArguments]] = None,
                 drag_constraints: str = '',
                 background_color: str = '#eee',
                 ) -> None:
        """3D场景

        使用`three.js <https://threejs.org/>`_显示3D场景。
        目前NiceGUI支持立方体、球体、圆柱体/圆锥体、拉伸体、直线、曲线和纹理网格。
        对象可以被平移、旋转，并以不同的颜色、不透明度或线框模式显示。
        它们也可以被分组以应用联合运动。

        :param width: 画布宽度
        :param height: 画布高度
        :param grid: 是否显示网格（布尔值或`Three.js的GridHelper <https://threejs.org/docs/#api/en/helpers/GridHelper>`_的``size``和``divisions``元组，默认：100x100）
        :param camera: 相机定义，``ui.scene.perspective_camera``（默认）或``ui.scene.orthographic_camera``的实例
        :param on_click: 点击3D对象时执行的回调函数（使用``click_events``指定要订阅的事件）
        :param click_events: 要订阅的JavaScript点击事件列表（默认：``['click', 'dblclick']``）
        :param on_drag_start: 拖动3D对象时执行的回调函数
        :param on_drag_end: 放置3D对象时执行的回调函数
        :param drag_constraints: 用于约束拖动对象位置的逗号分隔JavaScript表达式（例如``'x = 0, z = y / 2'``）
        :param background_color: 场景背景颜色（默认："#eee"）
        """
        super().__init__()
        self._props['width'] = width
        self._props['height'] = height
        self._props['grid'] = grid
        self._props['background_color'] = background_color
        self.camera = camera or self.perspective_camera()
        self._props['camera_type'] = self.camera.type
        self._props['camera_params'] = self.camera.params
        self.objects: Dict[str, Object3D] = {}
        self.stack: List[Union[Object3D, SceneObject]] = [SceneObject()]
        self._click_handlers = [on_click] if on_click else []
        self._props['click_events'] = click_events[:]
        self._drag_start_handlers = [on_drag_start] if on_drag_start else []
        self._drag_end_handlers = [on_drag_end] if on_drag_end else []
        self.on('init', self._handle_init)
        self.on('click3d', self._handle_click)
        self.on('dragstart', self._handle_drag)
        self.on('dragend', self._handle_drag)
        self._props['drag_constraints'] = drag_constraints

    def on_click(self, callback: Handler[SceneClickEventArguments]) -> Self:
        """添加点击3D对象时要调用的回调函数。"""
        self._click_handlers.append(callback)
        return self

    def on_drag_start(self, callback: Handler[SceneDragEventArguments]) -> Self:
        """添加拖动3D对象时要调用的回调函数。"""
        self._drag_start_handlers.append(callback)
        return self

    def on_drag_end(self, callback: Handler[SceneDragEventArguments]) -> Self:
        """添加放置3D对象时要调用的回调函数。"""
        self._drag_end_handlers.append(callback)
        return self

    @staticmethod
    def perspective_camera(*, fov: float = 75, near: float = 0.1, far: float = 1000) -> SceneCamera:
        """创建透视相机。

        :param fov: 垂直视野角度（度）
        :param near: 近裁剪平面
        :param far: 远裁剪平面
        """
        return SceneCamera(type='perspective', params={'fov': fov, 'near': near, 'far': far})

    @staticmethod
    def orthographic_camera(*, size: float = 10, near: float = 0.1, far: float = 1000) -> SceneCamera:
        """创建正交相机。

        尺寸定义了视锥体的垂直尺寸，即顶部和底部裁剪平面之间的距离。
        左右裁剪平面设置为使纵横比匹配视口。

        :param size: 视锥体的垂直尺寸
        :param near: 近裁剪平面
        :param far: 远裁剪平面
        """
        return SceneCamera(type='orthographic', params={'size': size, 'near': near, 'far': far})

    def __enter__(self) -> Self:
        Object3D.current_scene = self
        super().__enter__()
        return self

    def __getattribute__(self, name: str) -> Any:
        attribute = super().__getattribute__(name)
        if isinstance(attribute, type) and issubclass(attribute, Object3D):
            Object3D.current_scene = self
        return attribute

    def _handle_init(self, e: GenericEventArguments) -> None:
        with self.client.individual_target(e.args['socket_id']):
            self.move_camera(duration=0)
            self.run_method('init_objects', [obj.data for obj in self.objects.values()])

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

    def _handle_drag(self, e: GenericEventArguments) -> None:
        arguments = SceneDragEventArguments(
            sender=self,
            client=self.client,
            type=e.args['type'],
            object_id=e.args['object_id'],
            object_name=e.args['object_name'],
            x=e.args['x'],
            y=e.args['y'],
            z=e.args['z'],
        )
        if arguments.type == 'dragend':
            self.objects[arguments.object_id].move(arguments.x, arguments.y, arguments.z)

        for handler in (self._drag_start_handlers if arguments.type == 'dragstart' else self._drag_end_handlers):
            handle_event(handler, arguments)

    def __len__(self) -> int:
        return len(self.objects)

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
        :param look_at_x: 相机观察点x位置
        :param look_at_y: 相机观察点y位置
        :param look_at_z: 相机观察点z位置
        :param up_x: 相机上向量的x分量
        :param up_y: 相机上向量的y分量
        :param up_z: 相机上向量的z分量
        :param duration: 移动持续时间（秒）（默认：`0.5`）
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

    async def get_camera(self) -> Dict[str, Any]:
        """获取当前相机参数。

        与`camera`属性不同，
        此方法的结果包括用户在浏览器中导航场景导致的当前相机姿态。
        """
        return await self.run_method('get_camera')

    def _handle_delete(self) -> None:
        binding.remove(list(self.objects.values()))
        super()._handle_delete()

    def delete_objects(self, predicate: Callable[[Object3D], bool] = lambda _: True) -> None:
        """从场景中移除对象。

        :param predicate: 对于应该删除的对象返回`True`的函数
        """
        for obj in list(self.objects.values()):
            if predicate(obj) and obj.id in self.objects:  # NOTE: object might have been deleted already by its parent
                obj.delete()

    def clear(self) -> None:
        """从场景中移除所有对象。"""
        super().clear()
        self.delete_objects()
