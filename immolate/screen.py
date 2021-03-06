from abc import ABCMeta, abstractmethod
from contextlib import redirect_stdout
from io import StringIO
from typing import List, Tuple

from pygame.font import Font

from immolate.memory import Memory

with redirect_stdout(StringIO()):
    # Pygame logs a message upon being imported, but we want to keep the console clean in this project.
    import pygame
from pygame import Surface
from pygame.time import Clock


class MemoryAddresses:
    SPRITE_POSITIONS = [(200, 201), (202, 203), (204, 205), (206, 207), (208, 209)]
    BACKGROUND_COLOR = (210, 211, 212)
    KEYS_STATUS = {
        pygame.K_LEFT: 213,
        pygame.K_UP: 214,
        pygame.K_DOWN: 215,
        pygame.K_RIGHT: 216,
    }


def scale(surface: Surface) -> Surface:
    from pygame.transform import scale2x
    return scale2x(scale2x(surface))


class Screen(metaclass=ABCMeta):

    @abstractmethod
    def activate(self):
        pass

    @abstractmethod
    def run_one_frame(self):
        pass


class FakeScreen(Screen):

    def __init__(self, memory: Memory):
        self._active = False
        self.memory = memory

    def activate(self):
        if self._active:
            raise Exception("Screen is already active!")
        self._active = True

    def run_one_frame(self):
        if not self._active:
            raise Exception("Screen has not been activated yet!")


class PygameScreen(Screen):
    def __init__(self, memory: Memory, caption: str):
        self._scaling = 4
        self._caption = caption
        self._surface = None
        self._clock = None
        self._screen = None
        self._active = False
        self._sprites: List[Surface] = []
        for sprite in memory.sprites:
            surface = Surface((16, 16))
            for y in range(16):
                for x in range(16):
                    intensity = sprite[x + y * 16]
                    surface.set_at((x, y), (intensity, intensity, intensity))
            self._sprites.append(surface)
        self._memory = memory
        self._status_area_width = 200
        self._font = None

    def activate(self):
        if self._active:
            raise Exception("Screen is already active!")
        resolution = (128, 128)
        size = (resolution[0] * self._scaling, resolution[1] * self._scaling)
        self._surface = Surface(resolution)
        self._clock = Clock()
        self._screen = pygame.display.set_mode((size[0] + self._status_area_width, size[1]))
        pygame.display.set_caption(self._caption)
        self._active = True
        pygame.font.init()
        self._font = Font("Courier New Bold.ttf", 12)

    def run_one_frame(self):
        if not self._active:
            raise Exception("Screen has not been activated yet!")
        self._clock.tick(30)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.display.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key in MemoryAddresses.KEYS_STATUS:
                    address = MemoryAddresses.KEYS_STATUS[event.key]
                    self._memory[address] = 1
            elif event.type == pygame.KEYUP:
                if event.key in MemoryAddresses.KEYS_STATUS:
                    address = MemoryAddresses.KEYS_STATUS[event.key]
                    self._memory[address] = 0
        (addr_r, addr_g, addr_b) = MemoryAddresses.BACKGROUND_COLOR
        background_color = (self._memory[addr_r], self._memory[addr_g], self._memory[addr_b])
        self._screen.fill((0, 0, 0))
        self._surface.fill(background_color)

        for i, sprite in enumerate(self._sprites):
            (addr_x, addr_y) = MemoryAddresses.SPRITE_POSITIONS[i]
            sprite_position = (self._memory[addr_x], self._memory[addr_y])
            self._surface.blit(sprite, sprite_position)
        self._screen.blit(scale(self._surface), (0, 0))
        self._render_debug_info()
        pygame.display.update()
        pygame.display.set_caption(f"{self._caption} ({round(self._clock.get_fps(), 1)})")

    def _render_debug_info(self):
        margin = 10
        y = margin + 20
        color = (255, 255, 255)

        def render_text(text, position: Tuple[int, int]):
            self._screen.blit(self._font.render(str(text), True, color), position)

        x = self._screen.get_width() - self._status_area_width + margin
        render_text("0-31", (x, margin))
        for i in range(32):
            render_text(self._memory[i], (x, y + i * 15))

        x += 60
        render_text("200-255", (x, margin))
        for i in range(32):
            render_text(self._memory[200 + i], (x, y + i * 15))

        x += 30
        for i in range(23):
            render_text(self._memory[232 + i], (x, y + i * 15))
