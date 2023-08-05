from .utils import ABCSafeMember

import abc


class RGBColor:
    __slots__ = ()
    BLACK = (0, 0, 0)
    AZURE = (0, 127, 255)
    WHITE = (255, 255, 255)
    BLUE = (0, 0, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    PURPLE = (255, 0, 255)
    YELLOW = (255, 255, 0)


class GameView(ABCSafeMember):
    """RGB"""
    __slots__ = ('_window',)

    HEIGHT = 600
    WIDTH = 400

    BACKGROUND_COLOR = (255, 200, 150)
    FORE_COLOR = (0, 0, 255)  # blue
    VIEW_CONTROLLER: object = None

    def __init__(self, window):
        assert self.VIEW_CONTROLLER is not None, NotImplementedError("please assign an object for VIEW_CONTROLLER")
        self._window = window

    @abc.abstractmethod
    def update(self):
        ...

    @abc.abstractmethod
    def clear_canvas(self):
        ...

    @abc.abstractmethod
    def destroy_view(self):
        ...


class KeyboardController(ABCSafeMember):
    __slots__ = ()
    KEYBOARD_CONTROLLER: object = None

    def __init__(self):
        assert self.KEYBOARD_CONTROLLER is not None, NotImplementedError('KEYBOARD_CONTROLLER is None')

    @abc.abstractmethod
    def get_event(self):
        ...
