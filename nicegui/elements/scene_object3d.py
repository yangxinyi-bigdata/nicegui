from __future__ import annotations

import math
import uuid
from typing import TYPE_CHECKING, Any, List, Literal, Optional, Union

from typing_extensions import Self

if TYPE_CHECKING:
    from .scene import Scene, SceneObject


class Object3D:
    current_scene: Optional[Scene] = None

    def __init__(self, type_: str, *args: Any) -> None:
        self.type = type_
        self.id = str(uuid.uuid4())
        self.name: Optional[str] = None
        assert self.current_scene is not None
        self.scene: Scene = self.current_scene
        self.scene.objects[self.id] = self
        self.parent: Union[Object3D, SceneObject] = self.scene.stack[-1]
        self.args: List = list(args)
        self.color: Optional[str] = '#ffffff'
        self.opacity: float = 1.0
        self.side_: str = 'front'
        self.visible_: bool = True
        self.draggable_: bool = False
        self.x: float = 0
        self.y: float = 0
        self.z: float = 0
        self.R: List[List[float]] = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
        self.sx: float = 1
        self.sy: float = 1
        self.sz: float = 1
        self._create()

    def with_name(self, name: str) -> Self:
        """设置对象的名称。"""
        self.name = name
        self._name()
        return self

    @property
    def data(self) -> List[Any]:
        """要发送到前端的数据。"""
        return [
            self.type, self.id, self.parent.id, self.args,
            self.name,
            self.color, self.opacity, self.side_,
            self.x, self.y, self.z,
            self.R,
            self.sx, self.sy, self.sz,
            self.visible_,
            self.draggable_,
        ]

    def __enter__(self) -> Self:
        self.scene.stack.append(self)
        return self

    def __exit__(self, *_) -> None:
        self.scene.stack.pop()

    def _create(self) -> None:
        self.scene.run_method('create', self.type, self.id, self.parent.id, *self.args)

    def _name(self) -> None:
        self.scene.run_method('name', self.id, self.name)

    def _material(self) -> None:
        self.scene.run_method('material', self.id, self.color, self.opacity, self.side_)

    def _move(self) -> None:
        self.scene.run_method('move', self.id, self.x, self.y, self.z)

    def _rotate(self) -> None:
        self.scene.run_method('rotate', self.id, self.R)

    def _scale(self) -> None:
        self.scene.run_method('scale', self.id, self.sx, self.sy, self.sz)

    def _visible(self) -> None:
        self.scene.run_method('visible', self.id, self.visible_)

    def _draggable(self) -> None:
        self.scene.run_method('draggable', self.id, self.draggable_)

    def _delete(self) -> None:
        self.scene.run_method('delete', self.id)

    def material(self,
                 color: Optional[str] = '#ffffff',
                 opacity: float = 1.0,
                 side: Literal['front', 'back', 'both'] = 'front',
                 ) -> Self:
        """设置对象的颜色和不透明度。

        :param color: CSS颜色字符串（默认：'#ffffff'）
        :param opacity: 0.0到1.0之间的不透明度（默认：1.0）
        :param side: 'front'、'back'或'double'（默认：'front'）
        """
        if self.color != color or self.opacity != opacity or self.side_ != side:
            self.color = color
            self.opacity = opacity
            self.side_ = side
            self._material()
        return self

    def move(self, x: float = 0.0, y: float = 0.0, z: float = 0.0) -> Self:
        """移动对象。

        :param x: x坐标
        :param y: y坐标
        :param z: z坐标
        """
        if self.x != x or self.y != y or self.z != z:
            self.x = x
            self.y = y
            self.z = z
            self._move()
        return self

    @staticmethod
    def rotation_matrix_from_euler(r_x: float, r_y: float, r_z: float) -> List[List[float]]:
        """从欧拉角创建旋转矩阵。

        :param r_x: 绕x轴的旋转（弧度）
        :param r_y: 绕y轴的旋转（弧度）
        :param r_z: 绕z轴的旋转（弧度）
        """
        sx, cx = math.sin(r_x), math.cos(r_x)
        sy, cy = math.sin(r_y), math.cos(r_y)
        sz, cz = math.sin(r_z), math.cos(r_z)
        return [
            [cz * cy, -sz * cx + cz * sy * sx, sz * sx + cz * sy * cx],
            [sz * cy, cz * cx + sz * sy * sx, -cz * sx + sz * sy * cx],
            [-sy, cy * sx, cy * cx],
        ]

    def rotate(self, r_x: float, r_y: float, r_z: float) -> Self:
        """旋转对象。

        :param r_x: 绕x轴的旋转（弧度）
        :param r_y: 绕y轴的旋转（弧度）
        :param r_z: 绕z轴的旋转（弧度）
        """
        return self.rotate_R(self.rotation_matrix_from_euler(r_x, r_y, r_z))

    def rotate_R(self, R: List[List[float]]) -> Self:
        """旋转对象。

        :param R: 3x3旋转矩阵
        """
        if self.R != R:
            self.R = R
            self._rotate()
        return self

    def scale(self, sx: float = 1.0, sy: Optional[float] = None, sz: Optional[float] = None) -> Self:
        """缩放对象。

        :param sx: x轴的缩放因子
        :param sy: y轴的缩放因子（默认：`sx`）
        :param sz: z轴的缩放因子（默认：`sx`）
        """
        if sy is None:
            sy = sx
        if sz is None:
            sz = sx
        if self.sx != sx or self.sy != sy or self.sz != sz:
            self.sx = sx
            self.sy = sy
            self.sz = sz
            self._scale()
        return self

    def visible(self, value: bool = True) -> Self:
        """设置对象的可见性。

        :param value: 对象是否应该可见（默认：`True`）
        """
        if self.visible_ != value:
            self.visible_ = value
            self._visible()
        return self

    def draggable(self, value: bool = True) -> Self:
        """设置对象是否应该可拖动。

        :param value: 对象是否应该可拖动（默认：`True`）
        """
        if self.draggable_ != value:
            self.draggable_ = value
            self._draggable()
        return self

    def attach(self, parent: Object3D) -> None:
        """将对象附加到父对象。

        对象的位置和旋转被保留，以便对象不在空间中移动。

        但请注意，缩放不会被保留。
        如果父对象或对象本身被缩放，对象的形状和位置可能会改变。

        *在版本2.7.0中添加*
        """
        self.detach()
        self.parent = parent
        self._move_into_parent(parent)
        self.scene.run_method('attach', self.id, parent.id, self.x, self.y, self.z, self.R)

    def _move_into_parent(self, parent: Union[Object3D, SceneObject]) -> None:
        if not isinstance(parent, Object3D):
            return
        if isinstance(parent.parent, Object3D):
            self._move_into_parent(parent.parent)
        M1: List[List[float]] = [
            [self.R[0][0], self.R[0][1], self.R[0][2], self.x],
            [self.R[1][0], self.R[1][1], self.R[1][2], self.y],
            [self.R[2][0], self.R[2][1], self.R[2][2], self.z],
            [0, 0, 0, 1],
        ]
        M2_inv: List[List[float]] = [
            [parent.R[0][0], parent.R[1][0], parent.R[2][0],
             - parent.R[0][0] * parent.x
             - parent.R[1][0] * parent.y
             - parent.R[2][0] * parent.z],
            [parent.R[0][1], parent.R[1][1], parent.R[2][1],
             - parent.R[0][1] * parent.x
             - parent.R[1][1] * parent.y
             - parent.R[2][1] * parent.z],
            [parent.R[0][2], parent.R[1][2], parent.R[2][2],
             - parent.R[0][2] * parent.x
             - parent.R[1][2] * parent.y
             - parent.R[2][2] * parent.z],
            [0, 0, 0, 1],
        ]
        M: List[List[float]] = [
            [
                M2_inv[0][0] * M1[0][0] + M2_inv[0][1] * M1[1][0] + M2_inv[0][2] * M1[2][0],
                M2_inv[0][0] * M1[0][1] + M2_inv[0][1] * M1[1][1] + M2_inv[0][2] * M1[2][1],
                M2_inv[0][0] * M1[0][2] + M2_inv[0][1] * M1[1][2] + M2_inv[0][2] * M1[2][2],
                M2_inv[0][0] * M1[0][3] + M2_inv[0][1] * M1[1][3] + M2_inv[0][2] * M1[2][3] + M2_inv[0][3],
            ],
            [
                M2_inv[1][0] * M1[0][0] + M2_inv[1][1] * M1[1][0] + M2_inv[1][2] * M1[2][0],
                M2_inv[1][0] * M1[0][1] + M2_inv[1][1] * M1[1][1] + M2_inv[1][2] * M1[2][1],
                M2_inv[1][0] * M1[0][2] + M2_inv[1][1] * M1[1][2] + M2_inv[1][2] * M1[2][2],
                M2_inv[1][0] * M1[0][3] + M2_inv[1][1] * M1[1][3] + M2_inv[1][2] * M1[2][3] + M2_inv[1][3],
            ],
            [
                M2_inv[2][0] * M1[0][0] + M2_inv[2][1] * M1[1][0] + M2_inv[2][2] * M1[2][0],
                M2_inv[2][0] * M1[0][1] + M2_inv[2][1] * M1[1][1] + M2_inv[2][2] * M1[2][1],
                M2_inv[2][0] * M1[0][2] + M2_inv[2][1] * M1[1][2] + M2_inv[2][2] * M1[2][2],
                M2_inv[2][0] * M1[0][3] + M2_inv[2][1] * M1[1][3] + M2_inv[2][2] * M1[2][3] + M2_inv[2][3],
            ],
            [
                0, 0, 0, 1,
            ],
        ]
        self.x = M[0][3]
        self.y = M[1][3]
        self.z = M[2][3]
        self.R = [
            [M[0][0], M[0][1], M[0][2]],
            [M[1][0], M[1][1], M[1][2]],
            [M[2][0], M[2][1], M[2][2]],
        ]

    def detach(self) -> None:
        """从其父组对象中移除对象。

        对象的位置和旋转被保留，以便对象不在空间中移动。

        但请注意，缩放不会被保留。
        如果父对象或对象本身被缩放，对象的形状和位置可能会改变。

        *在版本2.7.0中添加*
        """
        self._move_out_of_parent(self.parent)
        self.parent = self.scene.stack[0]
        self.scene.run_method('detach', self.id, self.x, self.y, self.z, self.R)

    def _move_out_of_parent(self, parent: Union[Object3D, SceneObject]) -> None:
        if not isinstance(parent, Object3D):
            return
        M1: List[List[float]] = [
            [self.R[0][0], self.R[0][1], self.R[0][2], self.x],
            [self.R[1][0], self.R[1][1], self.R[1][2], self.y],
            [self.R[2][0], self.R[2][1], self.R[2][2], self.z],
            [0, 0, 0, 1],
        ]
        M2: List[List[float]] = [
            [parent.R[0][0], parent.R[0][1], parent.R[0][2], parent.x],
            [parent.R[1][0], parent.R[1][1], parent.R[1][2], parent.y],
            [parent.R[2][0], parent.R[2][1], parent.R[2][2], parent.z],
            [0, 0, 0, 1],
        ]
        M: List[List[float]] = [
            [
                M2[0][0] * M1[0][0] + M2[0][1] * M1[1][0] + M2[0][2] * M1[2][0],
                M2[0][0] * M1[0][1] + M2[0][1] * M1[1][1] + M2[0][2] * M1[2][1],
                M2[0][0] * M1[0][2] + M2[0][1] * M1[1][2] + M2[0][2] * M1[2][2],
                M2[0][0] * M1[0][3] + M2[0][1] * M1[1][3] + M2[0][2] * M1[2][3] + M2[0][3],
            ],
            [
                M2[1][0] * M1[0][0] + M2[1][1] * M1[1][0] + M2[1][2] * M1[2][0],
                M2[1][0] * M1[0][1] + M2[1][1] * M1[1][1] + M2[1][2] * M1[2][1],
                M2[1][0] * M1[0][2] + M2[1][1] * M1[1][2] + M2[1][2] * M1[2][2],
                M2[1][0] * M1[0][3] + M2[1][1] * M1[1][3] + M2[1][2] * M1[2][3] + M2[1][3],
            ],
            [
                M2[2][0] * M1[0][0] + M2[2][1] * M1[1][0] + M2[2][2] * M1[2][0],
                M2[2][0] * M1[0][1] + M2[2][1] * M1[1][1] + M2[2][2] * M1[2][1],
                M2[2][0] * M1[0][2] + M2[2][1] * M1[1][2] + M2[2][2] * M1[2][2],
                M2[2][0] * M1[0][3] + M2[2][1] * M1[1][3] + M2[2][2] * M1[2][3] + M2[2][3],
            ],
            [
                0, 0, 0, 1,
            ],
        ]
        self.x = M[0][3]
        self.y = M[1][3]
        self.z = M[2][3]
        self.R = [
            [M[0][0], M[0][1], M[0][2]],
            [M[1][0], M[1][1], M[1][2]],
            [M[2][0], M[2][1], M[2][2]],
        ]
        if isinstance(parent.parent, Object3D):
            self._move_out_of_parent(parent.parent)

    @property
    def children(self) -> List[Object3D]:
        """对象的子对象列表。

        *在版本2.4.0中添加*
        """
        return [object for object in self.scene.objects.values() if object.parent == self]

    def delete(self) -> None:
        """删除对象。"""
        for child in self.children:
            child.delete()
        del self.scene.objects[self.id]
        self._delete()
