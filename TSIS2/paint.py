import pygame

from tools import (
    BLACK,
    BRUSH_SIZES,
    CANVAS_HEIGHT,
    CLEAR_BUTTON_RECT,
    COLORS,
    HEIGHT,
    PREVIEW_TOOLS,
    TOOLBAR_HEIGHT,
    WHITE,
    WIDTH,
    clamp_canvas_pos,
    draw_dot,
    draw_line_between,
    draw_shape,
    draw_text_preview,
    draw_text_to_canvas,
    draw_toolbar,
    flood_fill,
    inside_canvas,
    save_canvas,
    screen_to_canvas,
)


def main():
    pygame.init()
    pygame.font.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Paint Practice")
    clock = pygame.time.Clock()

    canvas = pygame.Surface((WIDTH, CANVAS_HEIGHT))
    canvas.fill(WHITE)

    toolbar_font = pygame.font.SysFont("arial", 24)
    small_font = pygame.font.SysFont("arial", 18)
    text_font = pygame.font.SysFont("arial", 36)

    active_tool = "pencil"
    current_color = BLACK
    brush_size = BRUSH_SIZES[2]

    mouse_is_down = False
    last_pos = None

    dragging_shape = False
    shape_start = None
    shape_end = None

    text_active = False
    text_pos = None
    text_buffer = ""

    saved_message = ""
    saved_message_until = 0

    running = True

    while running:
        pressed = pygame.key.get_pressed()

        ctrl_held = pressed[pygame.K_LCTRL] or pressed[pygame.K_RCTRL]
        alt_held = pressed[pygame.K_LALT] or pressed[pygame.K_RALT]

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:

                if text_active:
                    if event.key == pygame.K_RETURN:
                        draw_text_to_canvas(canvas, text_pos, text_buffer, text_font, current_color)
                        text_active = False
                        text_buffer = ""

                    elif event.key == pygame.K_ESCAPE:
                        text_active = False
                        text_buffer = ""

                    elif event.key == pygame.K_BACKSPACE:
                        text_buffer = text_buffer[:-1]

                    elif event.unicode and not ctrl_held:
                        text_buffer += event.unicode

                    continue

                if event.key == pygame.K_w and ctrl_held:
                    running = False

                elif event.key == pygame.K_F4 and alt_held:
                    running = False

                elif event.key == pygame.K_ESCAPE:
                    running = False

                elif event.key == pygame.K_s and ctrl_held:
                    filename = save_canvas(canvas)
                    saved_message = f"Saved: {filename}"
                    saved_message_until = pygame.time.get_ticks() + 3000

                elif event.key == pygame.K_1:
                    brush_size = BRUSH_SIZES[1]

                elif event.key == pygame.K_2:
                    brush_size = BRUSH_SIZES[2]

                elif event.key == pygame.K_3:
                    brush_size = BRUSH_SIZES[3]

                elif event.key == pygame.K_4:
                    current_color = COLORS["black"]

                elif event.key == pygame.K_5:
                    current_color = COLORS["red"]

                elif event.key == pygame.K_6:
                    current_color = COLORS["green"]

                elif event.key == pygame.K_7:
                    current_color = COLORS["blue"]

                elif event.key == pygame.K_8:
                    current_color = COLORS["yellow"]

                elif event.key == pygame.K_9:
                    current_color = COLORS["purple"]

                elif event.key == pygame.K_0:
                    current_color = COLORS["white"]

                elif event.key == pygame.K_p:
                    active_tool = "pencil"

                elif event.key == pygame.K_l:
                    active_tool = "line"

                elif event.key == pygame.K_r:
                    active_tool = "rectangle"

                elif event.key == pygame.K_c:
                    active_tool = "circle"

                elif event.key == pygame.K_s:
                    active_tool = "square"

                elif event.key == pygame.K_t:
                    active_tool = "right_triangle"

                elif event.key == pygame.K_e:
                    active_tool = "equilateral_triangle"

                elif event.key == pygame.K_h:
                    active_tool = "rhombus"

                elif event.key == pygame.K_d:
                    active_tool = "eraser"

                elif event.key == pygame.K_i:
                    active_tool = "picker"

                elif event.key == pygame.K_f:
                    active_tool = "fill"

                elif event.key == pygame.K_n:
                    active_tool = "text"

            elif event.type == pygame.MOUSEBUTTONDOWN:

                if event.button == 1 and CLEAR_BUTTON_RECT.collidepoint(event.pos):
                    canvas.fill(WHITE)
                    saved_message = "Canvas cleared"
                    saved_message_until = pygame.time.get_ticks() + 2000
                    continue

                if event.button == 1 and inside_canvas(event.pos):
                    canvas_pos = screen_to_canvas(event.pos)
                    canvas_pos = clamp_canvas_pos(canvas_pos)

                    if active_tool == "picker":
                        picked = canvas.get_at(canvas_pos)
                        current_color = (picked.r, picked.g, picked.b)

                    elif active_tool == "fill":
                        flood_fill(canvas, canvas_pos, current_color)

                    elif active_tool == "text":
                        text_active = True
                        text_pos = canvas_pos
                        text_buffer = ""

                    elif active_tool in ("pencil", "eraser"):
                        mouse_is_down = True
                        last_pos = canvas_pos

                        if active_tool == "eraser":
                            draw_color = WHITE
                        else:
                            draw_color = current_color

                        draw_dot(canvas, last_pos, draw_color, brush_size)

                    elif active_tool in PREVIEW_TOOLS:
                        dragging_shape = True
                        shape_start = canvas_pos
                        shape_end = canvas_pos

            elif event.type == pygame.MOUSEMOTION:

                if inside_canvas(event.pos):
                    canvas_pos = screen_to_canvas(event.pos)
                    canvas_pos = clamp_canvas_pos(canvas_pos)

                    if mouse_is_down and last_pos is not None:

                        if active_tool == "eraser":
                            draw_color = WHITE
                        else:
                            draw_color = current_color

                        draw_line_between(canvas, last_pos, canvas_pos, draw_color, brush_size)
                        last_pos = canvas_pos

                    if dragging_shape:
                        shape_end = canvas_pos

            elif event.type == pygame.MOUSEBUTTONUP:

                if event.button == 1:
                    mouse_is_down = False
                    last_pos = None

                    if dragging_shape and shape_start is not None:
                        canvas_pos = screen_to_canvas(event.pos)
                        canvas_pos = clamp_canvas_pos(canvas_pos)

                        shape_end = canvas_pos

                        draw_shape(
                            canvas,
                            active_tool,
                            shape_start,
                            shape_end,
                            current_color,
                            brush_size,
                        )

                    dragging_shape = False
                    shape_start = None
                    shape_end = None

        if pygame.time.get_ticks() > saved_message_until:
            saved_message = ""

        screen.fill(WHITE)

        draw_toolbar(
            screen,
            active_tool,
            current_color,
            brush_size,
            saved_message,
            toolbar_font,
            small_font,
        )

        if dragging_shape and shape_start is not None and shape_end is not None:
            preview_canvas = canvas.copy()

            draw_shape(
                preview_canvas,
                active_tool,
                shape_start,
                shape_end,
                current_color,
                brush_size,
            )

            screen.blit(preview_canvas, (0, TOOLBAR_HEIGHT))

        else:
            screen.blit(canvas, (0, TOOLBAR_HEIGHT))

        if text_active and text_pos is not None:
            draw_text_preview(screen, text_pos, text_buffer, text_font, current_color)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()