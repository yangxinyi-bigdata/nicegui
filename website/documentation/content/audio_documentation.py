from nicegui import ui

from . import doc


@doc.demo(ui.audio)
def main_demo() -> None:
    a = ui.audio('https://cdn.pixabay.com/download/audio/2022/02/22/audio_d1718ab41b.mp3')
    a.on('ended', lambda _: ui.notify('Audio playback completed'))

    ui.button(on_click=lambda: a.props('muted'), icon='volume_off').props('outline')
    ui.button(on_click=lambda: a.props(remove='muted'), icon='volume_up').props('outline')


@doc.demo('控制音频元素', '''
    本演示展示如何通过编程方式播放、暂停和跳转音频。
''')
def control_demo() -> None:
    a = ui.audio('https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3')
    ui.button('播放', on_click=a.play)
    ui.button('暂停', on_click=a.pause)
    ui.button('跳转到0:30', on_click=lambda: a.seek(30))


@doc.demo('事件订阅', '''
    本演示展示如何订阅一些[可用事件](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/audio#events)。
''')
def event_demo() -> None:
    a = ui.audio('https://cdn.pixabay.com/download/audio/2022/02/22/audio_d1718ab41b.mp3')
    a.on('play', lambda _: ui.notify('开始播放'))
    a.on('pause', lambda _: ui.notify('已暂停'))
    a.on('ended', lambda _: ui.notify('播放完成'))


doc.reference(ui.audio)
