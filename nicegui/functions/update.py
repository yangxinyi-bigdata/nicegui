from ..element import Element


def update(*elements: Element) -> None:
    """更新给定的元素。"""
    for element in elements:
        element.update()
