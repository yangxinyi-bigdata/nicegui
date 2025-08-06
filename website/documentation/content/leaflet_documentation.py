from nicegui import ui

from . import doc


@doc.demo(ui.leaflet)
def main_demo() -> None:
    m = ui.leaflet(center=(51.505, -0.09))
    ui.label().bind_text_from(m, 'center', lambda center: f'中心: {center[0]:.3f}, {center[1]:.3f}')
    ui.label().bind_text_from(m, 'zoom', lambda zoom: f'缩放: {zoom}')

    with ui.grid(columns=2):
        ui.button('伦敦', on_click=lambda: m.set_center((51.505, -0.090)))
        ui.button('柏林', on_click=lambda: m.set_center((52.520, 13.405)))
        ui.button(icon='zoom_in', on_click=lambda: m.set_zoom(m.zoom + 1))
        ui.button(icon='zoom_out', on_click=lambda: m.set_zoom(m.zoom - 1))


@doc.demo('更改地图样式', '''
    默认地图样式是OpenStreetMap。
    您可以在 <https://leaflet-extras.github.io/leaflet-providers/preview/> 找到更多地图样式。
    每次调用 `tile_layer` 都会堆叠在之前的基础上。
    因此，如果您想更改地图样式，必须先删除默认的。

    *2.12.0版本更新：支持WMTS和WMS地图服务。*
''')
def map_style() -> None:
    ui.label('网络地图切片服务')
    map1 = ui.leaflet(center=(51.505, -0.090), zoom=3)
    map1.clear_layers()
    map1.tile_layer(
        url_template=r'https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png',
        options={
            'maxZoom': 17,
            'attribution':
                'Map data: &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, <a href="https://viewfinderpanoramas.org/">SRTM</a> | '
                'Map style: &copy; <a href="https://opentopomap.org">OpenTopoMap</a> (<a href="https://creativecommons.org/licenses/by-sa/3.0/">CC-BY-SA</a>)'
        },
    )

    ui.label('网络地图服务')
    map2 = ui.leaflet(center=(51.505, -0.090), zoom=3)
    map2.clear_layers()
    map2.wms_layer(
        url_template='http://ows.mundialis.de/services/service?',
        options={
            'layers': 'TOPO-WMS,OSM-Overlay-WMS'
        },
    )


@doc.demo('点击添加标记', '''
    您可以使用 `marker` 向地图添加标记。
    `center` 参数是纬度和经度的元组。
    此演示通过点击地图来添加标记。
    请注意，"map-click" 事件指的是地图对象的点击事件，
    而 "click" 事件指的是容器div的点击事件。
''')
def markers() -> None:
    from nicegui import events

    m = ui.leaflet(center=(51.505, -0.09))

    def handle_click(e: events.GenericEventArguments):
        lat = e.args['latlng']['lat']
        lng = e.args['latlng']['lng']
        m.marker(latlng=(lat, lng))
    m.on('map-click', handle_click)


@doc.demo('Move Markers', '''
    You can move markers with the `move` method.
''')
def move_markers() -> None:
    m = ui.leaflet(center=(51.505, -0.09))
    marker = m.marker(latlng=m.center)
    ui.button('移动标记', on_click=lambda: marker.move(51.51, -0.09))


@doc.demo('Image Overlays', '''
    Leaflet supports [image overlays](https://leafletjs.com/reference.html#imageoverlay).
    You can add an image overlay with the `image_overlay` method.

    *Added in version 2.17.0*
''')
def overlay_image():
    m = ui.leaflet(center=(40.74, -74.18), zoom=11)
    m.image_overlay(
        url='https://maps.lib.utexas.edu/maps/historical/newark_nj_1922.jpg',
        bounds=[[40.712216, -74.22655], [40.773941, -74.12544]],
        options={'opacity': 0.8},
    )


@doc.demo('Video Overlays', '''
    Leaflet supports [video overlays](https://leafletjs.com/reference.html#videooverlay).
    You can add a video overlay with the `video_overlay` method.

    *Added in version 2.17.0*
''')
def overlay_video():
    m = ui.leaflet(center=(23.0, -115.0), zoom=3)
    m.video_overlay(
        url='https://www.mapbox.com/bites/00188/patricia_nasa.webm',
        bounds=[[32, -130], [13, -100]],
        options={'opacity': 0.8, 'autoplay': True, 'playsInline': True},
    )


@doc.demo('Vector Layers', '''
    Leaflet supports a set of [vector layers](https://leafletjs.com/reference.html#:~:text=VideoOverlay-,Vector%20Layers,-Path) like circle, polygon etc.
    These can be added with the `generic_layer` method.
    We are happy to review any pull requests to add more specific layers to simplify usage.
''')
def vector_layers() -> None:
    m = ui.leaflet(center=(51.505, -0.09)).classes('h-32')
    m.generic_layer(name='circle', args=[m.center, {'color': 'red', 'radius': 300}])


@doc.demo('Disable Pan and Zoom', '''
    There are [several options to configure the map in Leaflet](https://leafletjs.com/reference.html#map).
    This demo disables the pan and zoom controls.
''')
def disable_pan_zoom() -> None:
    options = {
        'zoomControl': False,
        'scrollWheelZoom': False,
        'doubleClickZoom': False,
        'boxZoom': False,
        'keyboard': False,
        'dragging': False,
    }
    ui.leaflet(center=(51.505, -0.09), options=options)


@doc.demo('Draw on Map', '''
    You can enable a toolbar to draw on the map.
    The `draw_control` can be used to configure the toolbar.
    This demo adds markers and polygons by clicking on the map.
    By setting "edit" and "remove" to `True` (the default), you can enable editing and deleting drawn shapes.
''')
def draw_on_map() -> None:
    from nicegui import events

    def handle_draw(e: events.GenericEventArguments):
        layer_type = e.args['layerType']
        coords = e.args['layer'].get('_latlng') or e.args['layer'].get('_latlngs')
        ui.notify(f'在 {coords} 绘制了 {layer_type}')

    draw_control = {
        'draw': {
            'polygon': True,
            'marker': True,
            'circle': True,
            'rectangle': True,
            'polyline': True,
            'circlemarker': True,
        },
        'edit': {
            'edit': True,
            'remove': True,
        },
    }
    m = ui.leaflet(center=(51.505, -0.09), draw_control=draw_control)
    m.classes('h-96')
    m.on('draw:created', handle_draw)
    m.on('draw:edited', lambda: ui.notify('编辑完成'))
    m.on('draw:deleted', lambda: ui.notify('删除完成'))


@doc.demo('Draw with Custom Options', '''
    You can draw shapes with custom options like stroke color and weight.
    To hide the default rendering of drawn items, set `hide_drawn_items` to `True`.
''')
def draw_custom_options():
    from nicegui import events

    def handle_draw(e: events.GenericEventArguments):
        options = {'color': 'red', 'weight': 1}
        m.generic_layer(name='polygon', args=[e.args['layer']['_latlngs'], options])

    draw_control = {
        'draw': {
            'polygon': True,
            'marker': False,
            'circle': False,
            'rectangle': False,
            'polyline': False,
            'circlemarker': False,
        },
        'edit': {
            'edit': False,
            'remove': False,
        },
    }
    m = ui.leaflet(center=(51.5, 0), draw_control=draw_control, hide_drawn_items=True)
    m.on('draw:created', handle_draw)


@doc.demo('Run Map Methods', '''
    You can run methods of the Leaflet map object with `run_map_method`.
    This demo shows how to fit the map to the whole world.
''')
def run_map_methods() -> None:
    m = ui.leaflet(center=(51.505, -0.09)).classes('h-32')
    ui.button('适合世界', on_click=lambda: m.run_map_method('fitWorld'))


@doc.demo('Run Layer Methods', '''
    You can run methods of the Leaflet layer objects with `run_layer_method`.
    This demo shows how to change the opacity of a marker or change its icon.
''')
def run_layer_methods() -> None:
    m = ui.leaflet(center=(51.505, -0.09)).classes('h-32')
    marker = m.marker(latlng=m.center)
    ui.button('隐藏', on_click=lambda: marker.run_method('setOpacity', 0.3))
    ui.button('显示', on_click=lambda: marker.run_method('setOpacity', 1.0))

    icon = 'L.icon({iconUrl: "https://leafletjs.com/examples/custom-icons/leaf-green.png"})'
    ui.button('更改图标', on_click=lambda: marker.run_method(':setIcon', icon))


@doc.demo('等待初始化', '''
    您可以使用 `initialized` 方法等待地图初始化。
    当您想在地图创建后立即运行适合地图边界的方法时，这是必要的。
''')
async def wait_for_init() -> None:
    # @ui.page('/')
    async def page():
        m = ui.leaflet(zoom=5)
        central_park = m.generic_layer(name='polygon', args=[[
            (40.767809, -73.981249),
            (40.800273, -73.958291),
            (40.797011, -73.949683),
            (40.764704, -73.973741),
        ]])
        await m.initialized()
        bounds = await central_park.run_method('getBounds')
        m.run_map_method('fitBounds', [[bounds['_southWest'], bounds['_northEast']]])
    ui.timer(0, page, once=True)  # HIDE


@doc.demo('Leaflet Plugins', '''
    You can add plugins to the map by passing the URLs of JS and CSS files to the `additional_resources` parameter.
    This demo shows how to add the [Leaflet.RotatedMarker](https://github.com/bbecquet/Leaflet.RotatedMarker) plugin.
    It allows you to rotate markers by a given `rotationAngle`.

    *Added in version 2.11.0*
''')
def leaflet_plugins() -> None:
    m = ui.leaflet((51.51, -0.09), additional_resources=[
        'https://unpkg.com/leaflet-rotatedmarker@0.2.0/leaflet.rotatedMarker.js',
    ])
    m.marker(latlng=(51.51, -0.091), options={'rotationAngle': -30})
    m.marker(latlng=(51.51, -0.090), options={'rotationAngle': 30})


doc.reference(ui.leaflet)
