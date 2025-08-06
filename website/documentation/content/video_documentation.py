from nicegui import ui

from . import doc


@doc.demo(ui.video)
def main_demo() -> None:
    v = ui.video('https://test-videos.co.uk/vids/bigbuckbunny/mp4/h264/360/Big_Buck_Bunny_360_10s_1MB.mp4')
    v.on('ended', lambda _: ui.notify('视频播放完成'))


@doc.demo('控制视频元素', '''
    本演示展示如何通过编程方式播放、暂停和跳转视频。
''')
def control_demo() -> None:
    v = ui.video('https://test-videos.co.uk/vids/bigbuckbunny/mp4/h264/360/Big_Buck_Bunny_360_10s_1MB.mp4')
    ui.button('播放', on_click=v.play)
    ui.button('暂停', on_click=v.pause)
    ui.button('跳转到0:05', on_click=lambda: v.seek(5))


doc.reference(ui.video)
