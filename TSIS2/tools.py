import pygame
from collections import deque
from datetime import datetime
from math import sqrt

WIDTH = 900
HEIGHT = 650
TOOLBAR_HEIGHT = 95
CANVAS_HEIGHT = HEIGHT - TOOLBAR_HEIGHT
CLEAR_BUTTON_RECT = pygame.Rect(WIDTH - 180, 12, 95, 32)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (230, 230, 230)
DARK_GRAY = (50, 50, 50)

BRUSH_SIZES = {
    1: 2,
    2: 5,
    3: 10,
}

COLORS = {
    "black": (0, 0, 0),
    "red": (220, 30, 30),
    "green": (30, 170, 70),
    "blue": (30, 90, 220),
    "yellow": (240, 210, 40),
    "purple": (150, 70, 200),
    "white": (255, 255, 255),
}

TOOLS = {
    "pencil": "Pencil",
    "line": "Line",
    "rectangle": "Rectangle",
    "circle": "Circle",
    "square": "Square",
    "right_triangle": "Right triangle",
    "equilateral_triangle": "Equilateral triangle",
    "rhombus": "Rhombus",
    "eraser": "Eraser",
    "picker": "Color picker",
    "fill": "Flood fill",
    "text": "Text",
}

PREVIEW_TOOLS = {
    "line",
    "rectangle",
    "circle",
    "square",
    "right_triangle",
    "equilateral_triangle",
    "rhombus",
}


def inside_canvas(screen_pos):
    x, y = screen_pos
    return 0 <= x < WIDTH and TOOLBAR_HEIGHT <= y < HEIGHT


def screen_to_canvas(screen_pos):
    x, y = screen_pos
    return x, y - TOOLBAR_HEIGHT


def clamp_canvas_pos(canvas_pos):
    x, y = canvas_pos
    x = max(0, min(WIDTH - 1, x))
    y = max(0, min(CANVAS_HEIGHT - 1, y))
    return x, y


def normalize_rect(start, end):
    x1, y1 = start
    x2, y2 = end

    left = min(x1, x2)
    top = min(y1, y2)
    width = abs(x2 - x1)
    height = abs(y2 - y1)

    return pygame.Rect(left, top, width, height)


def sign(value):
    if value < 0:
        return -1
    return 1


def draw_dot(surface, pos, color, width):
    radius = max(1, width // 2)
    pygame.draw.circle(surface, color, pos, radius)


def draw_line_between(surface, start, end, color, width):
    pygame.draw.line(surface, color, start, end, width)
    draw_dot(surface, start, color, width)
    draw_dot(surface, end, color, width)


def draw_rectangle(surface, start, end, color, width):
    rect = normalize_rect(start, end)

    if rect.width == 0 or rect.height == 0:
        draw_line_between(surface, start, end, color, width)
    else:
        pygame.draw.rect(surface, color, rect, width)


def draw_square(surface, start, end, color, width):
    x1, y1 = start
    x2, y2 = end

    dx = x2 - x1
    dy = y2 - y1

    side = min(abs(dx), abs(dy))

    if side == 0:
        draw_dot(surface, start, color, width)
        return

    new_end = (x1 + sign(dx) * side, y1 + sign(dy) * side)
    draw_rectangle(surface, start, new_end, color, width)


def draw_circle(surface, start, end, color, width):
    x1, y1 = start
    x2, y2 = end

    radius = int(((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5)

    if radius == 0:
        draw_dot(surface, start, color, width)
    else:
        pygame.draw.circle(surface, color, start, radius, width)


def draw_right_triangle(surface, start, end, color, width):
    x1, y1 = start
    x2, y2 = end

    points = [
        (x1, y1),
        (x1, y2),
        (x2, y2),
    ]

    pygame.draw.polygon(surface, color, points, width)


def draw_equilateral_triangle(surface, start, end, color, width):
    x1, y1 = start
    x2, y2 = end

    side = abs(x2 - x1)

    if side == 0:
        side = abs(y2 - y1)
        x2 = x1 + side

    if side == 0:
        draw_dot(surface, start, color, width)
        return

    direction = 1 if y2 >= y1 else -1
    height = int(sqrt(3) / 2 * side)

    points = [
        (x1, y1),
        (x2, y1),
        ((x1 + x2) // 2, y1 + direction * height),
    ]

    pygame.draw.polygon(surface, color, points, width)


def draw_rhombus(surface, start, end, color, width):
    x1, y1 = start
    x2, y2 = end

    left = min(x1, x2)
    right = max(x1, x2)
    top = min(y1, y2)
    bottom = max(y1, y2)

    mid_x = (left + right) // 2
    mid_y = (top + bottom) // 2

    points = [
        (mid_x, top),
        (right, mid_y),
        (mid_x, bottom),
        (left, mid_y),
    ]

    pygame.draw.polygon(surface, color, points, width)


def draw_shape(surface, tool, start, end, color, width):
    if tool == "line":
        draw_line_between(surface, start, end, color, width)
    elif tool == "rectangle":
        draw_rectangle(surface, start, end, color, width)
    elif tool == "circle":
        draw_circle(surface, start, end, color, width)
    elif tool == "square":
        draw_square(surface, start, end, color, width)
    elif tool == "right_triangle":
        draw_right_triangle(surface, start, end, color, width)
    elif tool == "equilateral_triangle":
        draw_equilateral_triangle(surface, start, end, color, width)
    elif tool == "rhombus":
        draw_rhombus(surface, start, end, color, width)


def flood_fill(surface, start_pos, new_color):
    width, height = surface.get_size()
    x, y = start_pos

    if not (0 <= x < width and 0 <= y < height):
        return

    target_color = surface.get_at((x, y))
    fill_color = pygame.Color(*new_color)

    if target_color == fill_color:
        return

    pixels = deque([(x, y)])

    surface.lock()

    while pixels:
        px, py = pixels.pop()

        if px < 0 or px >= width or py < 0 or py >= height:
            continue

        if surface.get_at((px, py)) != target_color:
            continue

        surface.set_at((px, py), fill_color)

        pixels.append((px + 1, py))
        pixels.append((px - 1, py))
        pixels.append((px, py + 1))
        pixels.append((px, py - 1))

    surface.unlock()


def save_canvas(surface):
    filename = "canvas_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".png"
    pygame.image.save(surface, filename)
    return filename


def draw_text_to_canvas(surface, pos, text, font, color):
    if text == "":
        return

    rendered_text = font.render(text, True, color)
    surface.blit(rendered_text, pos)


def draw_text_preview(screen, pos, text, font, color):
    x, y = pos
    screen_pos = (x, y + TOOLBAR_HEIGHT)

    if text != "":
        rendered_text = font.render(text, True, color)
        screen.blit(rendered_text, screen_pos)

    cursor_x = screen_pos[0]

    if text != "":
        cursor_x += font.size(text)[0]

    pygame.draw.line(
        screen,
        color,
        (cursor_x, screen_pos[1]),
        (cursor_x, screen_pos[1] + font.get_height()),
        2,
    )


def draw_toolbar(screen, active_tool, current_color, brush_size, message, font, small_font):
    pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, TOOLBAR_HEIGHT))
    pygame.draw.line(screen, DARK_GRAY, (0, TOOLBAR_HEIGHT - 1), (WIDTH, TOOLBAR_HEIGHT - 1), 2)

    title = f"Tool: {TOOLS[active_tool]} | Brush: {brush_size}px | Color: {current_color}"
    screen.blit(font.render(title, True, BLACK), (10, 8))

    line1 = "Tools: P pencil, L line, R rectangle, C circle, S square, T right triangle, E equilateral, H rhombus"
    line2 = "Other: D eraser, I picker, F fill, N text | Brush: 1=2px, 2=5px, 3=10px | Ctrl+S save"
    line3 = "Colors: 4 black, 5 red, 6 green, 7 blue, 8 yellow, 9 purple, 0 white"

    screen.blit(small_font.render(line1, True, BLACK), (10, 35))
    screen.blit(small_font.render(line2, True, BLACK), (10, 55))
    screen.blit(small_font.render(line3, True, BLACK), (10, 75))

    pygame.draw.rect(screen, current_color, (WIDTH - 60, 15, 35, 35))
    pygame.draw.rect(screen, BLACK, (WIDTH - 60, 15, 35, 35), 2)



    pygame.draw.rect(screen, WHITE, CLEAR_BUTTON_RECT)
    pygame.draw.rect(screen, BLACK, CLEAR_BUTTON_RECT, 2)

    clear_text = small_font.render("CLEAR", True, BLACK)
    clear_x = CLEAR_BUTTON_RECT.centerx - clear_text.get_width() // 2
    clear_y = CLEAR_BUTTON_RECT.centery - clear_text.get_height() // 2
    screen.blit(clear_text, (clear_x, clear_y))


    if message:
        message_surface = small_font.render(message, True, BLACK)
        screen.blit(message_surface, (WIDTH - message_surface.get_width() - 20, 60))