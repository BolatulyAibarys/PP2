import pygame

def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Paint")
    clock = pygame.time.Clock()

    radius = 15
    mode = 'blue'
    shape = 'brush'
    points = []

    drawing = False
    start_pos = None

    canvas = pygame.Surface((640, 480))
    canvas.fill((0, 0, 0))

    while True:

        pressed = pygame.key.get_pressed()

        alt_held = pressed[pygame.K_LALT] or pressed[pygame.K_RALT]
        ctrl_held = pressed[pygame.K_LCTRL] or pressed[pygame.K_RCTRL]

        for event in pygame.event.get():

            # determine if X was clicked, or Ctrl+W or Alt+F4 was used
            if event.type == pygame.QUIT:
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and ctrl_held:
                    return
                if event.key == pygame.K_F4 and alt_held:
                    return
                if event.key == pygame.K_ESCAPE:
                    return

                # colors
                if event.key == pygame.K_r:
                    mode = 'red'
                elif event.key == pygame.K_g:
                    mode = 'green'
                elif event.key == pygame.K_b:
                    mode = 'blue'
                elif event.key == pygame.K_y:
                    mode = 'yellow'
                elif event.key == pygame.K_p:
                    mode = 'purple'
                elif event.key == pygame.K_e:
                    mode = 'eraser'

                # shapes
                elif event.key == pygame.K_1:
                    shape = 'brush'
                elif event.key == pygame.K_2:
                    shape = 'rectangle'
                elif event.key == pygame.K_3:
                    shape = 'circle'

                # clear screen
                elif event.key == pygame.K_c:
                    canvas.fill((0, 0, 0))
                    points = []

                # save image
                elif event.key == pygame.K_s:
                    pygame.image.save(canvas, "my_paint.png")

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    drawing = True
                    start_pos = event.pos

                    if shape == 'brush':
                        points = points + [event.pos]
                        points = points[-256:]

                elif event.button == 3:
                    radius = max(1, radius - 1)

                elif event.button == 4:
                    radius = min(200, radius + 1)

                elif event.button == 5:
                    radius = max(1, radius - 1)

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    drawing = False
                    end_pos = event.pos

                    if shape == 'rectangle':
                        x1, y1 = start_pos
                        x2, y2 = end_pos
                        rect = pygame.Rect(min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1))
                        pygame.draw.rect(canvas, get_color(mode), rect, radius)

                    elif shape == 'circle':
                        x1, y1 = start_pos
                        x2, y2 = end_pos
                        circle_radius = int(((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5)
                        pygame.draw.circle(canvas, get_color(mode), start_pos, circle_radius, radius)

            if event.type == pygame.MOUSEMOTION:
                if drawing and shape == 'brush':
                    position = event.pos
                    points = points + [position]
                    points = points[-256:]

                    if len(points) > 1:
                        drawLineBetween(canvas, len(points), points[-2], points[-1], radius, mode)

        screen.blit(canvas, (0, 0))
# small instruction text
        font = pygame.font.SysFont("times new roman", 16)
        text = font.render("R/G/B/Y/P colors | E eraser | 1 brush | 2 rect | 3 circle | C clear | S save", True, (255, 255, 255))
        screen.blit(text, (5, 5))

        pygame.display.flip()
        clock.tick(60)


def get_color(color_mode):
    if color_mode == 'blue':
        return (0, 0, 255)
    elif color_mode == 'red':
        return (255, 0, 0)
    elif color_mode == 'green':
        return (0, 255, 0)
    elif color_mode == 'yellow':
        return (255, 255, 0)
    elif color_mode == 'purple':
        return (150, 0, 200)
    elif color_mode == 'eraser':
        return (0, 0, 0)


def drawLineBetween(screen, index, start, end, width, color_mode):
    color = get_color(color_mode)

    dx = start[0] - end[0]
    dy = start[1] - end[1]
    iterations = max(abs(dx), abs(dy))

    if iterations == 0:
        pygame.draw.circle(screen, color, start, width)
        return

    for i in range(iterations):
        progress = 1.0 * i / iterations
        aprogress = 1 - progress

        x = int(aprogress * start[0] + progress * end[0])
        y = int(aprogress * start[1] + progress * end[1])

        pygame.draw.circle(screen, color, (x, y), width)

main()