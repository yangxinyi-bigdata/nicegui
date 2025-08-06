import asyncio
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union, cast

from typing_extensions import Self

from .. import binding
from ..awaitable_response import AwaitableResponse, NullResponse
from ..element import Element
from ..events import GenericEventArguments
from .leaflet_layer import Layer


class Leaflet(Element, component='leaflet.js', default_classes='nicegui-leaflet'):
    # pylint: disable=import-outside-toplevel
    from .leaflet_layers import GenericLayer as generic_layer
    from .leaflet_layers import ImageOverlay as image_overlay
    from .leaflet_layers import Marker as marker
    from .leaflet_layers import TileLayer as tile_layer
    from .leaflet_layers import VideoOverlay as video_overlay
    from .leaflet_layers import WmsLayer as wms_layer

    center = binding.BindableProperty(lambda sender, value: cast(Leaflet, sender).set_center(value))
    zoom = binding.BindableProperty(lambda sender, value: cast(Leaflet, sender).set_zoom(value))

    def __init__(self,
                 center: Tuple[float, float] = (0.0, 0.0),
                 zoom: int = 13,
                 *,
                 options: Dict = {},  # noqa: B006
                 draw_control: Union[bool, Dict] = False,
                 hide_drawn_items: bool = False,
                 additional_resources: Optional[List[str]] = None,
                 ) -> None:
        """Leaflet地图

        此元素是`Leaflet <https://leafletjs.com/>`_ JavaScript库的包装器。

        :param center: 地图的初始中心位置（纬度/经度，默认：(0.0, 0.0)）
        :param zoom: 地图的初始缩放级别（默认：13）
        :param draw_control: 是否显示绘制工具栏（默认：False）
        :param options: 传递给Leaflet地图的附加选项（默认：{}）
        :param hide_drawn_items: 是否隐藏地图上绘制的项目（默认：False，*在版本2.0.0中添加*）
        :param additional_resources: 要加载的附加资源，如CSS或JS文件（默认：None，*在版本2.11.0中添加*）
        """
        super().__init__()
        self.add_resource(Path(__file__).parent / 'lib' / 'leaflet')

        self.layers: List[Layer] = []
        self.is_initialized = False

        self.center = center
        self.zoom = zoom
        self._props['center'] = center
        self._props['zoom'] = zoom
        self._props['options'] = {**options}
        self._props['draw_control'] = draw_control
        self._props['hide_drawn_items'] = hide_drawn_items
        self._props['additional_resources'] = additional_resources or []

        self.on('init', self._handle_init)
        self.on('map-moveend', self._handle_moveend)
        self.on('map-zoomend', self._handle_zoomend)

        self.tile_layer(
            url_template=r'https://{s}.tile.osm.org/{z}/{x}/{y}.png',
            options={'attribution': '&copy; <a href="https://openstreetmap.org">OpenStreetMap</a> contributors'},
        )

        self._send_update_on_value_change = True

    def __enter__(self) -> Self:
        Layer.current_leaflet = self
        return super().__enter__()

    def __getattribute__(self, name: str) -> Any:
        attribute = super().__getattribute__(name)
        if isinstance(attribute, type) and issubclass(attribute, Layer):
            Layer.current_leaflet = self
        return attribute

    def _handle_init(self, e: GenericEventArguments) -> None:
        self.is_initialized = True
        with self.client.individual_target(e.args['socket_id']):
            for layer in self.layers:
                self.run_method('add_layer', layer.to_dict(), layer.id)

    async def initialized(self, timeout: float = 3.0) -> None:
        """等待地图初始化完成。

        :param timeout: 超时时间，以秒为单位（默认：3秒）
        """
        event = asyncio.Event()
        self.on('init', event.set, [])
        await self.client.connected(timeout=timeout)
        await event.wait()

    def _handle_moveend(self, e: GenericEventArguments) -> None:
        self._send_update_on_value_change = False
        self.center = e.args['center']
        self._send_update_on_value_change = True

    def _handle_zoomend(self, e: GenericEventArguments) -> None:
        self._send_update_on_value_change = False
        self.zoom = e.args['zoom']
        self._send_update_on_value_change = True

    def run_method(self, name: str, *args: Any, timeout: float = 1) -> AwaitableResponse:
        if not self.is_initialized:
            return NullResponse()
        return super().run_method(name, *args, timeout=timeout)

    def set_center(self, center: Tuple[float, float]) -> None:
        """设置地图的中心位置。"""
        if self._props['center'] == center:
            return
        self._props['center'] = center
        if self._send_update_on_value_change:
            self.run_map_method('setView', center, self.zoom)

    def set_zoom(self, zoom: int) -> None:
        """设置地图的缩放级别。"""
        if self._props['zoom'] == zoom:
            return
        self._props['zoom'] = zoom
        if self._send_update_on_value_change:
            self.run_map_method('setView', self.center, zoom)

    def remove_layer(self, layer: Layer) -> None:
        """从地图中移除图层。"""
        self.layers.remove(layer)
        self.run_method('remove_layer', layer.id)

    def clear_layers(self) -> None:
        """从地图中移除所有图层。"""
        self.layers.clear()
        self.run_method('clear_layers')

    def run_map_method(self, name: str, *args, timeout: float = 1) -> AwaitableResponse:
        """运行Leaflet地图实例的方法。

        方法列表请参考`Leaflet文档 <https://leafletjs.com/reference.html#map-methods-for-modifying-map-state>`_。

        如果函数被等待，则返回方法调用的结果。
        否则，方法将执行而不等待响应。

        :param name: 方法名称（前缀":"表示参数是JavaScript表达式）
        :param args: 传递给方法的参数
        :param timeout: 超时时间，以秒为单位（默认：1秒）

        :return: 可以等待以获取方法调用结果的AwaitableResponse
        """
        return self.run_method('run_map_method', name, *args, timeout=timeout)

    def run_layer_method(self, layer_id: str, name: str, *args, timeout: float = 1) -> AwaitableResponse:
        """运行Leaflet图层的方法。

        如果函数被等待，则返回方法调用的结果。
        否则，方法将执行而不等待响应。

        :param layer_id: 图层的ID
        :param name: 方法名称（前缀":"表示参数是JavaScript表达式）
        :param args: 传递给方法的参数
        :param timeout: 超时时间，以秒为单位（默认：1秒）

        :return: 可以等待以获取方法调用结果的AwaitableResponse
        """
        return self.run_method('run_layer_method', layer_id, name, *args, timeout=timeout)

    def _handle_delete(self) -> None:
        binding.remove(self.layers)
        super()._handle_delete()
