from abc import ABC, abstractmethod
from enum import Enum
import pygame
from typing import Callable, Optional, Any
from enum import Enum
import math
import random
import sys
import pygame

pygame.font.init()
pygame.display.init()

#%% constants.py

# Beam Width List Constants
BEAM_WIDTH_LIST = [1, 3, 5, 10, 50, 999999]

# Generate Maze List Constants
GENERATE_MAZE_TYPE = [
    # "Recursive Division",
    # "Prim's Algorithm",
    "Randomised DFS",
    "Basic Random Maze",
    # "Basic Weight Maze",
]

# List Cell Weights Constants
CELL_WEIGHTS = [1, 2, 3, 4, 5, 6, 7, 8]
CELL_WEIGHTS_AND_PATH = ("1", "2", "3", "4", "5", "6", "7", "8", "V", "*")

# Search Algorithms Constants
SEARCH_ALGORITHMS = [
    "Local Beam Search",
    "Breadth First Search",
    # "Hill Climbing Search",
    # "Greedy Best First Search",
    # "Depth First Search",
    # "Dijkstra's Algorithm",
    # "A* Algorithm",
]

# Colors
BLACK = (0, 0, 0)
DARK = (11, 53, 71)
GREEN = (26, 188, 157)
GREEN_2 = (104, 224, 185)
BLUE = (100, 206, 228)
WHITE = (255, 255, 255)
YELLOW = (255, 254, 106)
GRAY = (166, 222, 255)
DARK_BLUE = (52, 73, 94)
BLUE_2 = (81, 145, 228)
DARK_BLUE_2 = (44, 67, 208)
PURPLE = (17, 104, 217)

# Window Dimensions
WINDOW_INFO = pygame.display.Info()
SCREEN_WIDTH, SCREEN_HEIGHT = WINDOW_INFO.current_w, WINDOW_INFO.current_h
WIDTH = 1280 if SCREEN_WIDTH >= 1280 else SCREEN_WIDTH - 150
HEIGHT = 900 if SCREEN_HEIGHT >= 900 else SCREEN_HEIGHT - 150
HEADER_HEIGHT = 200

# Maze
CELL_SIZE = 40
if len(sys.argv) > 1:
    arg = sys.argv[1]

    try:
        assert arg.startswith("--cell-size:") == True

        size = arg.split(":")[1]
        size = int(size)

        if size < 10:
            size = 10
        elif size > 90:
            size = 90

        CELL_SIZE = size
    except:
        print("\nInvalid command line arguments")
        print("USAGE: python3 run.pyw [ --cell-size:<int> ]")
        exit(1)

REMAINDER_W = WIDTH % CELL_SIZE
if REMAINDER_W == 0:
    REMAINDER_W = CELL_SIZE

REMAINDER_H = (HEIGHT - HEADER_HEIGHT) % CELL_SIZE
if REMAINDER_H == 0:
    REMAINDER_H = CELL_SIZE

MAZE_WIDTH = WIDTH - REMAINDER_W
MAZE_HEIGHT = HEIGHT - HEADER_HEIGHT - REMAINDER_H

# Framerate
FPS = 60
CLOCK = pygame.time.Clock()

# Images and fonts
WEIGHT = pygame.image.load("assets/images/weight.png")
START = pygame.image.load("assets/images/triangle.png")
GOAL = pygame.image.load("assets/images/circle.png")
FONT_14 = pygame.font.Font("assets/fonts/Montserrat-Regular.ttf", 14)
FONT_18 = pygame.font.Font("assets/fonts/Montserrat-Regular.ttf", 18)

# Animations
MIN_SIZE = 0.3 * CELL_SIZE
MAX_SIZE = 1.2 * CELL_SIZE


#%% widgets.py
class Widget(ABC):
    x: int
    y: int
    width: int
    height: int
    screen: pygame.surface.Surface
    rect: pygame.rect.Rect
    text: str

    @abstractmethod
    def draw(self) -> None:
        pass

    @abstractmethod
    def set_surface(self, surf: pygame.surface.Surface) -> None:
        pass


class Button(Widget):
    """Model a button (Can be used for creating labels)"""

    def __init__(
            self,
            text: str,
            x: float | str,
            y: float | str,
            padding: int = 5,
            font_size: int = 18,
            bold: bool = False,
            outline: bool = False,
            foreground_color: pygame.Color = pygame.Color(0, 0, 0),
            background_color: pygame.Color = pygame.Color(255, 255, 255),
            surface: pygame.surface.Surface | None = None,
    ) -> None:
        if surface:
            self.screen = surface
        self.text = text
        self.padding = padding
        self.outline = outline
        self.foreground_color = foreground_color
        self.background_color = background_color

        # Render text
        if bold:
            font = pygame.font.Font(
                "assets/fonts/Montserrat-Bold.ttf", font_size)
        else:
            font = pygame.font.Font(
                "assets/fonts/Montserrat-Regular.ttf", font_size)

        self.text_surf = font.render(
            self.text, True, foreground_color
        )

        # Get Rect object out of the text surface
        self.text_rect = self.text_surf.get_rect()

        # Translate params: x and y if they are strings
        self.width = self.text_rect.width + padding * 2
        self.height = self.text_rect.height + padding * 2

        if x == "center":
            x = (WIDTH - self.width) / 2

        if y == "center":
            y = (HEIGHT - self.height) / 2

        # Create the actual button
        self.rect = pygame.Rect(
            float(x),
            float(y),
            self.text_rect.width + padding * 2,
            self.text_rect.height + padding * 2
        )

        self.text_rect.topleft = self.rect.x + padding, self.rect.y + padding

    def set_surface(self, surf: pygame.surface.Surface) -> None:
        self.screen = surf

    def draw(self):
        """Draw the button (or label)

        Args:
            surf (pygame.surface.Surface): Window surface

        Returns:
            bool: Whether this button was clicked
        """

        # Whether button is clicked or not
        action = False

        # Get mouse position
        pos = pygame.mouse.get_pos()

        # Check mouseover and clicked conditions
        action = self.rect.collidepoint(pos) \
            and pygame.mouse.get_pressed()[0]

        # Draw button
        pygame.draw.rect(self.screen, self.background_color, self.rect)

        if self.outline:
            pygame.draw.rect(self.screen, BLACK,
                             self.rect, width=self.outline)

        text_x, text_y = self.rect.x + self.padding, self.rect.y + self.padding
        self.screen.blit(self.text_surf, (text_x, text_y))

        return action

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}{tuple(vars(self).values())!r}"


class Label(Button):
    def draw(self) -> None:
        """Draw label

        Args:
            surf (pygame.surface.Surface): Destination surface
        """
        # Draw label rectangle
        pygame.draw.rect(self.screen, self.background_color, self.rect)

        # Draw outline
        if self.outline:
            pygame.draw.rect(self.screen, BLACK,
                             self.rect, width=self.outline)

        # Render text
        text_x, text_y = self.rect.x + self.padding, self.rect.y + self.padding
        self.screen.blit(self.text_surf, (text_x, text_y))


class Menu(Widget):
    def __init__(
        self,
        surface: pygame.surface.Surface,
        button: Button,
        children: list[Widget]
    ) -> None:
        self.screen = surface
        self.button = button
        self.children = children
        self.clicked = False
        self.selected: Widget | None = None

        self.height = sum(child.rect.height for child in children)
        self.width = max(child.rect.width for child in children)

        self.x = self.button.rect.x - 10
        self.y = self.button.rect.y

        if self.width < self.button.width:
            self.width = self.button.width + 40
            self.x = self.button.rect.x

        children[0].rect.x = self.x
        children[0].rect.top = self.button.rect.bottom

        for i in range(1, len(children)):
            child = children[i]
            prev = children[i - 1]
            child.rect.x = self.x
            child.rect.top = prev.rect.bottom

        self.rect = self.button.rect
        self.popup_rect = pygame.Rect(self.x - 20,
                                self.button.rect.bottom,
                                self.width + 40,
                                self.height + 20)
        

    def set_surface(self, surf: pygame.surface.Surface) -> None:
        self.screen = surf
        self.button.set_surface(surf)

    def draw(self) -> bool:
        """Draw the menu

        Args:
            surf (pygame.surface.Surface): Window surface

        Returns:
            bool: Whether any button in this menu is clicked
        """

        clicked = self.button.draw()
        self.selected = None

        if clicked:
            self.clicked = True

        if not self.clicked:
            return False

        # Whether button is clicked or not
        action = False

        pygame.draw.rect(
            self.screen,
            DARK_BLUE,
            self.popup_rect,
            border_radius=10
        )

        # Handle selection
        for child in self.children:
            if child.draw():
                self.selected = child
                self.clicked = False
                action = True

        return action


class Orientation(Enum):
    HORIZONTAL = "X"
    VERTICAL = "Y"


class Alignment(Enum):
    CENTER = "C"
    LEFT = "L"
    RIGHT = "R"
    TOP = "T"
    BOTTOM = "B"
    NONE = "N"


class TableCell:
    def __init__(
        self,
        child: Widget,
        color: tuple[int, int, int] = WHITE,
        align: Alignment = Alignment.NONE
    ) -> None:
        self.child = child
        self.color = color
        self.alignment = align
        self.rect = pygame.Rect(child.rect)

    def draw(self, surf: pygame.surface.Surface) -> None:
        pygame.draw.rect(surf, self.color, self.rect)
        self.child.draw()


class Table(Widget):
    def __init__(
        self,
        x: int,
        y: int,
        rows: int,
        columns: int,
        children: list[list[TableCell]],
        color: tuple[int, int, int] = WHITE,
        padding: int = 0,
        surface: pygame.surface.Surface | None = None,
    ) -> None:
        self.x, self.y = 0, 0
        self.padding = padding

        if surface:
            self.screen = surface
            self.x = x
            self.y = y

        self.rows = rows
        self.columns = columns
        self.children = children

        max_col_widths = [max(child.rect.width for child in col)
                          for col in zip(*self.children)]

        idx = 0
        for col in zip(*self.children):
            for child in col:
                child.rect.width = max_col_widths[idx]

            idx += 1

        self.width = self.padding * 2
        self.height = self.padding * 2
        self.width += sum(max_col_widths)

        for row in self.children:
            self.height += max([child.rect.height for child in row])

        y = self.padding
        for row in range(self.rows):
            x = self.padding
            for col in range(self.columns):
                child = children[row][col]
                child.rect.x = x
                child.rect.y = y

                match child.alignment:
                    case Alignment.CENTER:
                        child.child.rect.center = child.rect.center
                    case Alignment.RIGHT:
                        child.child.rect.center = child.rect.center
                        child.child.rect.right = child.rect.right
                    case _:
                        child.child.rect.center = child.rect.center
                        child.child.rect.left = child.rect.left

                x += children[row][col].rect.width

            y += max(children[row][i].rect.height for i in range(self.columns))

        self.surface = pygame.Surface((self.width, self.height))
        self.surface.fill(color)
        self.rect = pygame.Rect(x, y, self.width, self.height)

        for row in self.children:
            for child in row:
                child.child.set_surface(self.surface)

    def set_surface(self, surf: pygame.surface.Surface) -> None:
        self.screen = surf

    def draw(self):
        for row in self.children:
            for child in row:
                child.draw(self.surface)
        self.screen.blit(self.surface, self.rect)


class Popup(Widget):
    def __init__(
        self,
        surface: pygame.surface.Surface,
        x: int,
        y: int,
        children: list[Widget],
        padding: int,
        color: tuple[int, int, int] = WHITE,
        width: int | None = None,
        height: int | None = None,
        orientation: Orientation = Orientation.HORIZONTAL,
        x_align: Alignment = Alignment.NONE,
        y_align: Alignment = Alignment.NONE,
    ) -> None:
        self.screen = surface
        self.children = children
        self.x = x
        self.y = y
        self.width = width if width else 0
        self.height = height if height else 0

        if orientation == Orientation.HORIZONTAL:
            content_width = sum(child.rect.width for child in children)
            content_height = max(child.rect.height for child in children)
        else:
            content_width = max(child.rect.width for child in children)
            content_height = sum(child.rect.height for child in children)

        if self.width == 0:
            self.width = content_width

        if self.height == 0:
            self.height = content_height

        if padding:
            self.width += padding * 2
            self.height += padding * 2

        self.padding = padding
        self.surface = pygame.Surface((self.width, self.height))
        self.surface.fill(color)
        self.rect = pygame.Rect(x - padding, y - padding,
                                self.width, self.height)

        for child in children:
            child.set_surface(self.surface)

        if orientation == Orientation.HORIZONTAL:
            match x_align:
                case Alignment.CENTER:
                    children[0].rect.left = (
                        self.width - content_width) // 2
                case Alignment.RIGHT:
                    children[0].rect.left = (
                        self.width - self.padding - content_width)
                case _:
                    children[0].rect.left = self.padding

            match y_align:
                case Alignment.CENTER:
                    children[0].rect.centery = (self.height) // 2
                case Alignment.BOTTOM:
                    children[0].rect.top = (
                        self.height - self.padding - content_height
                    )
                case _:
                    children[0].rect.top = self.padding

            for i in range(1, len(children)):
                child = children[i]
                prev = children[i - 1]
                child.rect.x = prev.rect.right
                child.rect.y = self.padding

                if y_align == Alignment.CENTER:
                    child.rect.centery = prev.rect.centery
                elif y_align != Alignment.NONE:
                    child.rect.top = prev.rect.top
        else:
            match x_align:
                case Alignment.CENTER:
                    children[0].rect.centerx = self.width // 2
                case Alignment.RIGHT:
                    children[0].rect.left = (
                        self.width - self.padding - content_width)
                case _:
                    children[0].rect.left = self.padding

            match y_align:
                case Alignment.CENTER:
                    children[0].rect.top = (
                        self.height - content_height) // 2
                case Alignment.BOTTOM:
                    children[0].rect.top = (
                        self.height - self.padding - content_height
                    )
                case _:
                    children[0].rect.top = self.padding

            for i in range(1, len(children)):
                child = children[i]
                prev = children[i - 1]
                child.rect.y = prev.rect.bottom
                child.rect.x = self.padding

                if x_align == Alignment.CENTER:
                    child.rect.centerx = prev.rect.centerx
                elif x_align != Alignment.NONE:
                    child.rect.left = prev.rect.left

        self.close_btn = Button(
            surface=self.surface,
            text="   X   ",
            x=0,
            y=0,
            background_color=pygame.Color(*DARK_BLUE),
            foreground_color=pygame.Color(*WHITE),
            font_size=20, outline=False
        )
        self.close_btn.rect.right = self.rect.right
        self.close_btn.rect.top = self.rect.top

    def set_surface(self, surf: pygame.surface.Surface) -> None:
        self.screen = surf
        self.close_btn.set_surface(surf)

    def update_center(self, center: tuple[int, int]):
        self.rect.center = center
        self.close_btn.rect.right = self.rect.right
        self.close_btn.rect.top = self.rect.top

    def draw(self) -> bool:
        for child in self.children:
            child.draw()

        self.screen.blit(self.surface, self.rect)
        return self.close_btn.draw()


#%% animations.py

class Animation(Enum):
    WALL_ANIMATION = "WALL_ANIMATION"
    WEIGHT_ANIMATION = "WEIGHT_ANIMATION"
    PATH_ANIMATION = "PATH_ANIMATION"


AnimationCallback = Callable[[], None]


class AnimatingNode:
    def __init__(
        self,
        rect: pygame.Rect,
        value: str,
        ticks: int,
        center: tuple[int, int],
        color: tuple[int, int, int],
        after_animation: Optional[AnimationCallback] = None,
        colors: list[tuple[int, int, int]] = [],
        animation: Animation = Animation.WALL_ANIMATION,
        duration: int = 300,
    ) -> None:
        self.rect = rect
        self.value = value
        self.ticks = ticks
        self.center = center
        self.color = color
        self.colors = colors
        self.animation = animation
        self.duration = duration
        self.after_animation = after_animation
        self.progress = 0
        self.start = self.ticks
        self.time_updated = False

    def __repr__(self) -> str:
        return f"AnimatingNode{tuple(vars(self).values())}"

    def __str__(self) -> str:
        return f"AnimatingNode: Value: {self.value}, " \
            + f"Progress: {self.progress}/{self.duration}"


class Animator:

    def __init__(self, surface: pygame.surface.Surface, maze) -> None:
        from maze import Maze

        self.surface = surface
        self.maze: Maze = maze

        self.animating = False
        self.nodes_to_animate: dict[tuple[int, int], list[AnimatingNode]] = {}
        self.need_update = False

    def add_nodes_to_animate(
        self,
        nodes: list[AnimatingNode],
        delay: int = 0,
        gap: int = 3
    ) -> None:
        """Add nodes for animation

        Args:
            nodes (list[AnimatingNode]): List of nodes
            delay (bool, optional): Whether to wait for previous nodes to animate. Defaults to False.
        """

        # Update first node's ticks and add it to the list
        if len(self.nodes_to_animate):
            last_node = list(self.nodes_to_animate.values())[-1][0]
            nodes[0].ticks = last_node.ticks + delay

        self.nodes_to_animate[nodes[0].center] = self.nodes_to_animate.get(
            nodes[0].center,
            []
        )
        self.nodes_to_animate[nodes[0].center].append(nodes[0])

        # Rest of the nodes
        for i in range(1, len(nodes)):
            nodes[i].ticks = nodes[i - 1].ticks + gap
            self.nodes_to_animate[nodes[i].center] = self.nodes_to_animate.get(
                nodes[i].center,
                []
            )
            self.nodes_to_animate[nodes[i].center].append(nodes[i])

        self.need_update = True

    def animate_nodes(self):
        """Animate nodes in the nodes_to_animate list
        """
        # Update starting time for animating nodes
        if self.need_update:
            for center in self.nodes_to_animate:
                for node in self.nodes_to_animate[center]:
                    if not node.time_updated:
                        node.ticks += (pygame.time.get_ticks() - node.start)
                        node.time_updated = True

            self.need_update = False

        # Animate every node
        for center in list(self.nodes_to_animate.keys()):
            for i in range(len(self.nodes_to_animate[center]) - 1, -1, -1):
                node = self.nodes_to_animate[center][i]
                node.progress += pygame.time.get_ticks() - node.ticks
                node.ticks = pygame.time.get_ticks()

                if node.progress > 0:
                    self.nodes_to_animate[center][:i] = []
                    break
            else:
                continue

            # Call respective functions
            if node.animation == Animation.WALL_ANIMATION:
                self._wall_animation(node)
            elif node.animation == Animation.PATH_ANIMATION:
                self._path_animation(node)
            else:
                self._weight_animation(node)

            # Handle node images
            row, col = self.maze.get_cell_pos(node.center)
            if (row, col) == self.maze.start:
                image_rect = START.get_rect(center=node.center)
                self.surface.blit(START, image_rect)

            elif (row, col) == self.maze.goal:
                image_rect = GOAL.get_rect(center=node.center)
                self.surface.blit(GOAL, image_rect)

            elif (cost := self.maze.maze[row][col].cost) >= 1:
                image_rect = WEIGHT.get_rect(center=node.center)
                self.surface.blit(WEIGHT, image_rect)

                text = FONT_14.render(
                    str(cost), True, GRAY
                )
                text_rect = text.get_rect()
                text_rect.center = image_rect.center
                self.surface.blit(text, text_rect)

            # Update maze node and remove current animating node
            if node.progress >= node.duration:
                pos = self.maze.get_cell_pos(node.center)
                self.maze.set_cell(pos, node.value)

                self.nodes_to_animate[center].remove(node)
                if not self.nodes_to_animate[center]:
                    self.nodes_to_animate.pop(center)

                if node.after_animation:
                    node.after_animation()

    def _wall_animation(self, node: AnimatingNode) -> None:
        """Handle wall animation

        Args:
            node (AnimatingNode): Wall node
        """

        # Calculate size as per ease-out func
        if node.progress < node.duration / 2:
            size = self._ease_out_sine(
                node.progress, MIN_SIZE, MAX_SIZE - MIN_SIZE, node.duration / 2
            )
        else:
            size = self._ease_out_sine(
                node.progress - node.duration / 2,
                MAX_SIZE, CELL_SIZE - MAX_SIZE, node.duration / 2
            )

        # Update size
        node.rect.width = node.rect.height = int(size)
        node.rect.center = node.center

        # Draw
        pygame.draw.rect(self.surface, node.color, node.rect)

    def _weight_animation(self, node: AnimatingNode) -> None:
        """Handle weighted node animation

        Args:
            node (AnimatingNode): Weighted node
        """

        # Calculate size as per ease-out func
        if node.progress < node.duration / 2:
            size = self._ease_out_sine(
                node.progress, MIN_SIZE, MAX_SIZE - MIN_SIZE, node.duration / 2
            )

        else:
            size = self._ease_out_sine(
                node.progress - node.duration / 2,
                MAX_SIZE, CELL_SIZE - MAX_SIZE, node.duration / 2
            )

        # Update size
        node.rect.width = node.rect.height = int(size)
        node.rect.center = node.center

        # Draw
        pygame.draw.rect(self.surface, GRAY, node.rect)
        pygame.draw.rect(self.surface, DARK, node.rect, width=8)

    def _path_animation(self, node: AnimatingNode) -> None:
        """Animate solution path

        Args:
            node (AnimatingNode): Node in solution path
        """
        border_radius = 0
        if node.progress < 0.02 * node.duration:
            size = node.rect.width
        elif node.progress < 0.75 * node.duration:
            duration = 0.75 * node.duration
            size = self._ease_out_sine(
                node.progress, MIN_SIZE, MAX_SIZE - MIN_SIZE, duration
            )

            border_radius = int(0.40 * size)
            if size > CELL_SIZE:
                border_radius = int(0.12 * size)

        else:
            duration = 0.25 * node.duration
            progress = node.progress - 0.75 * node.duration
            size = self._ease_out_sine(
                progress,
                MAX_SIZE, CELL_SIZE - MAX_SIZE, duration
            )
            border_radius = 0

        if node.progress < 0.02 * node.duration:
            color = node.colors[0]
        elif node.progress < 0.50 * node.duration:
            progress = node.progress
            duration = 0.50 * node.duration
            r, g, b = node.colors[1]
            r2, g2, b2 = node.colors[2]

            r = self._ease_out_sine(
                progress, r, r2 - r, duration
            )
            g = self._ease_out_sine(
                progress, g, g2 - g, duration
            )
            b = self._ease_out_sine(
                progress, b, b2 - b, duration
            )
            color = (round(r), round(g), round(b))
        elif node.progress < 0.75 * node.duration:
            progress = node.progress - 0.50 * node.duration
            duration = 0.25 * node.duration
            r, g, b = node.colors[2]
            r2, g2, b2 = node.colors[3]

            r = self._ease_out_sine(
                progress, r, r2 - r, duration
            )
            g = self._ease_out_sine(
                progress, g, g2 - g, duration
            )
            b = self._ease_out_sine(
                progress, b, b2 - b, duration
            )
            color = (round(r), round(g), round(b))
        else:
            progress = node.progress - 0.75 * node.duration
            duration = 0.25 * node.duration
            r, g, b = node.colors[3]
            r2, g2, b2 = node.colors[-1]

            r = self._ease_out_sine(
                progress, r, r2 - r, duration
            )
            g = self._ease_out_sine(
                progress, g, g2 - g, duration
            )
            b = self._ease_out_sine(
                progress, b, b2 - b, duration
            )
            color = (round(r), round(g), round(b))

        # Update size
        node.rect.width = node.rect.height = int(size)
        node.rect.center = node.center

        # Draw
        pygame.draw.rect(self.surface, color, node.rect,
                         border_radius=border_radius)

        if node.progress > 0.50 * node.duration:
            pygame.draw.rect(
                self.surface,
                GREEN if node.progress < 0.75 * node.duration else GRAY,
                node.rect,
                border_radius=border_radius,
                width=1
            )

    def _ease_out_sine(
        self,
        time: float,
        starting_value: float,
        change_in_value: float,
        duration: float
    ) -> float:
        """Calculate current size

        Args:
            time (float): The current time of the animation.
            starting_value (float): The starting value of the animation.
            change (float): The change in value of the animation.
            duration (float): The total duration of the animation in milliseconds.

        Returns:
            float: Current value
        """
        return change_in_value * math.sin(time / duration * (math.pi / 2)) \
            + starting_value

    def __repr__(self) -> str:
        return f"Animator{tuple(vars(self).values())}"


#%% generate.py



GenerationCallback = Callable[[], None]


class MazeGenerator:

    def __init__(self, animator: Animator) -> None:
        from maze import Maze

        self.animator = animator
        self.maze: Maze = animator.maze

    def _is_valid_cell(self, pos: tuple[int, int]) -> bool:
        """Check if the provided coords are valid

        Args:
            pos (tuple[int, int]): Cell pos

        Returns:
            bool: Whether the cell exists
        """
        rowIdx, colIdx = pos

        return 0 <= rowIdx < self.maze.height \
            and 0 <= colIdx < self.maze.width

    def _get_two_step_neighbors(
        self,
        maze: list[list[Any]],
        cell: tuple[int, int],
        value: str = ""
    ) -> list[tuple[int, int]]:
        """Get neighbors of a cell which are two steps away

        Args:
            cell (tuple[int, int]): Cell pos
            value (str): A string representing the neighbor type. `#` for a wall

        Returns:
            list[tuple[int, int]]: List of neighbors
        """
        neighbors = [(cell[0] + 2, cell[1]),
                     (cell[0] - 2, cell[1]),
                     (cell[0], cell[1] + 2),
                     (cell[0], cell[1] - 2)]

        if value == "#":
            return [neighbor for neighbor in neighbors
                    if self._is_valid_cell(neighbor)
                    and maze[neighbor[0]][neighbor[1]] == "#"]
        elif value != "#":
            return [neighbor for neighbor in neighbors
                    if self._is_valid_cell(neighbor)
                    and maze[neighbor[0]][neighbor[1]] != "#"]

        return [neighbor for neighbor in neighbors
                if self._is_valid_cell(neighbor)]

    def randomised_prims_algorithm(self) -> None:
        """Generate maze by Randomised Prim's algorithm
        """

        # Create a simpler copy of the actual maze
        maze = [["#" for __ in range(self.maze.width)]
                for _ in range(self.maze.height)]

        maze[self.maze.start[0]][self.maze.start[1]] = "1"
        maze[self.maze.goal[0]][self.maze.goal[1]] = "1"

        # Put walls everywhere
        for rowIdx in range(self.maze.height):
            for colIdx in range(self.maze.width):
                self.maze.set_cell((rowIdx, colIdx), "#")

        # Create a list for storing frontier cells
        frontier = self._get_two_step_neighbors(maze, self.maze.start, "#")

        # Visited frontier cells
        visited = set()

        # For animating nodes
        nodes_to_animate = []

        while frontier:
            cell = random.choice(frontier)

            # Skip if already visited
            if cell in visited:
                frontier.remove(cell)
                continue

            # Get neighbors of type "1"
            neighbors = self._get_two_step_neighbors(maze, cell, "1")

            # If neighbors is not empty, break the wall between the neighbor
            # and the frontier cell. Also set neighbor to type "1"
            if neighbors:
                neighbor = random.choice(neighbors)

                wall = ((cell[0] + neighbor[0]) // 2,
                        (cell[1] + neighbor[1]) // 2)

                maze[wall[0]][wall[1]] = "1"
                maze[cell[0]][cell[1]] = "1"

                # For animations
                x, y = self.maze.coords[wall[0]][wall[1]]
                nodes_to_animate.append(
                    AnimatingNode(
                        rect=pygame.Rect(0, 0, MIN_SIZE, MIN_SIZE),
                        center=(x + CELL_SIZE // 2, y + CELL_SIZE // 2),
                        value="1",
                        ticks=pygame.time.get_ticks(),
                        color=BLUE_2
                    )
                )

                x, y = self.maze.coords[cell[0]][cell[1]]
                nodes_to_animate.append(
                    AnimatingNode(
                        rect=pygame.Rect(0, 0, MIN_SIZE, MIN_SIZE),
                        center=(x + CELL_SIZE // 2, y + CELL_SIZE // 2),
                        value="1",
                        ticks=pygame.time.get_ticks(),
                        color=GREEN_2
                    )
                )

                frontier.extend(self._get_two_step_neighbors(maze, cell, "#"))

            # Add current frontier cell to the visited cell
            # and remove it from the frontier
            visited.add(cell)
            frontier.remove(cell)

        # Add nodes for animation
        self.maze.animator.add_nodes_to_animate(nodes_to_animate)

    def randomised_dfs(self) -> None:
        """Generate maze by randomised dfs
        """

        # For animating nodes
        nodes_to_animate = []

        # Draw Walls everywhere except the start and goal pos
        for rowIdx in range(self.maze.height):
            for colIdx in range(self.maze.width):
                self.maze.set_cell((rowIdx, colIdx), "#")

        stack = [self.maze.start]

        visited = set()
        visited.add(self.maze.start)

        while stack:
            # Pop one cell from the stack
            curr = stack.pop()

            # Get unvisited two step neighbors of current cell
            neighbors = self._get_two_step_neighbors(self.maze.maze, curr)
            unvisited_neighbors = [neighbor for neighbor in neighbors
                                   if neighbor not in visited]

            # If the cell has unvisited neighbors, push it to the stack
            # Choose one neighbor and break wall between the neighbor
            # and the current cell. Also set the neighbor to type "1"
            if unvisited_neighbors:
                next = random.choice(unvisited_neighbors)
                stack.append(curr)

                x, y = self.maze.coords[next[0]][next[1]]
                nodes_to_animate.append(
                    AnimatingNode(
                        rect=pygame.Rect(0, 0, MIN_SIZE, MIN_SIZE),
                        center=(x + CELL_SIZE // 2, y + CELL_SIZE // 2),
                        value=str(random.choice(CELL_WEIGHTS)),
                        ticks=pygame.time.get_ticks(),
                        color=BLUE_2
                    )
                )

                rowIdx = (curr[0] + next[0]) // 2
                colIdx = (curr[1] + next[1]) // 2
                x, y = self.maze.coords[rowIdx][colIdx]

                nodes_to_animate.append(
                    AnimatingNode(
                        rect=pygame.Rect(0, 0, MIN_SIZE, MIN_SIZE),
                        center=(x + CELL_SIZE // 2, y + CELL_SIZE // 2),
                        value=str(random.choice(CELL_WEIGHTS)),
                        ticks=pygame.time.get_ticks(),
                        color=GREEN_2,
                    )
                )

                # Add the neighbor to the visited set and push it
                # to the stack
                visited.add(next)
                stack.append(next)

        # Add animating nodes for animation
        self.maze.animator.add_nodes_to_animate(nodes_to_animate)

    def basic_weight_maze(self) -> None:
        """Generate a basic weight maze
        """

        nodes = []
        for rowIdx in range(self.maze.width):
            for colIdx in range(self.maze.height):
                if random.randint(1, 10) < 8:
                    continue

                x, y = self.maze.coords[colIdx][rowIdx]
                nodes.append(
                    AnimatingNode(
                        rect=pygame.Rect(0, 0, MIN_SIZE, MIN_SIZE),
                        center=(x + CELL_SIZE // 2, y + CELL_SIZE // 2),
                        ticks=pygame.time.get_ticks(),
                        value=str(random.choice(CELL_WEIGHTS)),
                        color=WHITE,
                        animation=Animation.WEIGHT_ANIMATION
                    )
                )

        self.maze.animator.add_nodes_to_animate(nodes, gap=2)

    def basic_random_maze(self) -> None:
        """Generate a basic random maze
        """
        nodes = []
        for rowIdx in range(self.maze.width):
            for colIdx in range(self.maze.height):
                if random.randint(1, 10) < 8:
                    continue

                x, y = self.maze.coords[colIdx][rowIdx]
                nodes.append(
                    AnimatingNode(
                        rect=pygame.Rect(0, 0, MIN_SIZE, MIN_SIZE),
                        center=(x + CELL_SIZE // 2, y + CELL_SIZE // 2),
                        ticks=pygame.time.get_ticks(),
                        value="#",
                        color=DARK
                    )
                )

        self.maze.animator.add_nodes_to_animate(nodes, gap=2)

    def recursive_division(
        self,
        x1: int,
        x2: int,
        y1: int,
        y2: int
    ) -> None:
        """Generate maze by recursive division algorithm

        Args:
            x1 (int): Grid row start
            x2 (int): Grid row end
            y1 (int): Grid column start
            y2 (int): Grid column end
        """
        width = x2 - x1
        height = y2 - y1

        # Base case:
        if width < 1 or height < 1:
            return

        # Whether to draw horizontally or vertically
        horizontal = True if height > width else (
            False if width != height else random.choice((True, False)))

        # Arguments for reursive calls
        args_list: list[tuple[int, int, int, int]] = []

        # Divide the maze and add new grids' properties to args_list
        if horizontal:
            y = self._draw_line(x1, x2, y1, y2, horizontal=True)
            args_list.extend([(x1, x2, y1, y - 1), (x1, x2, y + 1, y2)])
        else:
            x = self._draw_line(x1, x2, y1, y2)
            args_list.extend([(x1, x - 1, y1, y2), (x + 1, x2, y1, y2)])

        # Divide the two grids
        for args in args_list:
            self.recursive_division(*args)

    def _draw_line(
        self,
        x1: int,
        x2: int,
        y1: int,
        y2: int,
        horizontal: bool = False
    ) -> int:
        """Draw walls horizontally or vertically

        Args:
            x1 (int): Grid row start
            x2 (int): Grid row end
            y1 (int): Grid column start
            y2 (int): Grid column end
            horizontal (bool, optional): Horizontal or vertical. Defaults to False.

        Returns:
            int: X or Y coordinate of wall line
        """

        # Handle horizontal division
        if horizontal:
            x1, y1 = y1, x1
            x2, y2 = y2, x2

        # Walls at even places
        if x1 % 2 != 0:
            x1 += 1
        wall = random.randrange(x1, x2, 2)

        # Holes at odd places
        if y1 % 2 == 0:
            y1 += 1
        hole = random.randrange(y1, y2, 2)

        # Coordinates
        hole_coords = (hole, wall) if not horizontal else (wall, hole)
        wall_coords = [-1, wall] if not horizontal else [wall, -1]

        # Draw walls
        nodes_to_animate = []
        for i in range(y1, y2 + 1):
            wall_coords[horizontal] = i
            if hole_coords == tuple(wall_coords):
                continue

            # Create a rectangle
            rect = pygame.Rect(0, 0, MIN_SIZE, MIN_SIZE)

            # Set the starting position of the rectangle
            x, y = self.maze.coords[wall_coords[0]][wall_coords[1]]
            rect.center = (x + CELL_SIZE // 2, y + CELL_SIZE // 2)
            nodes_to_animate.append(
                AnimatingNode(
                    center=(x + CELL_SIZE // 2, y + CELL_SIZE // 2),
                    rect=rect,
                    ticks=pygame.time.get_ticks(),
                    value="#",
                    color=DARK
                )
            )
        self.maze.animator.add_nodes_to_animate(nodes_to_animate)

        return wall
