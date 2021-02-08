from abc import ABCMeta, abstractmethod
from contextlib import redirect_stdout
from io import StringIO

with redirect_stdout(StringIO()):
    # Pygame logs a message upon being imported, but we want to keep the console clean in this project.
    import pygame
from pygame import Surface
from pygame.time import Clock


def scale(surface: Surface) -> Surface:
    from pygame.transform import scale2x
    return scale2x(scale2x(surface))


class Screen(metaclass=ABCMeta):
    color: int

    @abstractmethod
    def activate(self):
        pass

    @abstractmethod
    def run_one_frame(self):
        pass


class FakeScreen(Screen):

    def __init__(self):
        self._active = False

    def activate(self):
        if self._active:
            raise Exception("Screen is already active!")
        self._active = True

    def run_one_frame(self):
        if not self._active:
            raise Exception("Screen has not been activated yet!")


class PygameScreen(Screen):
    def __init__(self):
        self.color = 0
        self._scaling = 4
        self._caption = "DEMO"
        self._surface = None
        self._clock = None
        self._screen = None
        self._active = False

    def activate(self):
        if self._active:
            raise Exception("Screen is already active!")
        resolution = (128, 128)
        size = (resolution[0] * self._scaling, resolution[1] * self._scaling)
        self._surface = Surface(resolution)
        self._clock = Clock()
        self._screen = pygame.display.set_mode(size)
        pygame.display.set_caption(self._caption)
        self._active = True

    def run_one_frame(self):
        if not self._active:
            raise Exception("Screen has not been activated yet!")
        self._clock.tick(30)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.display.quit()
        self._surface.fill((self.color, self.color, self.color))
        self._screen.blit(scale(self._surface), (0, 0))
        pygame.display.update()
        pygame.display.set_caption(f"{self._caption} ({round(self._clock.get_fps(), 1)})")
