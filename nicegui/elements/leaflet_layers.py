from dataclasses import dataclass, field
from typing import Any, Dict, List, Tuple, Union

from typing_extensions import Self

from ..dataclasses import KWONLY_SLOTS
from .leaflet_layer import Layer


@dataclass(**KWONLY_SLOTS)
class GenericLayer(Layer):
    name: str
    args: List[Any] = field(default_factory=list)

    def to_dict(self) -> Dict:
        return {
            'type': self.name,
            'args': self.args,
        }


@dataclass(**KWONLY_SLOTS)
class TileLayer(Layer):
    url_template: str
    options: Dict = field(default_factory=dict)

    def to_dict(self) -> Dict:
        return {
            'type': 'tileLayer',
            'args': [self.url_template, self.options],
        }


@dataclass(**KWONLY_SLOTS)
class WmsLayer(Layer):
    url_template: str
    options: Dict = field(default_factory=dict)

    def to_dict(self) -> Dict:
        return {
            'type': 'tileLayer.wms',
            'args': [self.url_template, self.options],
        }


@dataclass(**KWONLY_SLOTS)
class ImageOverlay(Layer):
    url: str
    bounds: List[List[float]]
    options: Dict = field(default_factory=dict)

    def to_dict(self) -> Dict:
        return {
            'type': 'imageOverlay',
            'args': [self.url, self.bounds, self.options],
        }


@dataclass(**KWONLY_SLOTS)
class VideoOverlay(Layer):
    url: Union[str, List[str]]
    bounds: List[List[float]]
    options: Dict = field(default_factory=dict)

    def to_dict(self) -> Dict:
        return {
            'type': 'videoOverlay',
            'args': [self.url, self.bounds, self.options],
        }


@dataclass(**KWONLY_SLOTS)
class Marker(Layer):
    latlng: Tuple[float, float]
    options: Dict = field(default_factory=dict)

    def to_dict(self) -> Dict:
        return {
            'type': 'marker',
            'args': [{'lat': self.latlng[0], 'lng': self.latlng[1]}, self.options],
        }

    def draggable(self, value: bool = True) -> Self:
        """使标记可拖动。"""
        self.options['draggable'] = value
        return self

    def move(self, lat: float, lng: float) -> None:
        """将标记移动到新位置。

        :param lat: 纬度
        :param lng: 经度
        """
        self.latlng = (lat, lng)
        self.run_method('setLatLng', (lat, lng))
