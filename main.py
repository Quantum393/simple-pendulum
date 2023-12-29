import pygame
import math

COLOUR_BG = (15, 15, 15)



FPS = 60
clock = pygame.time.Clock()


def draw(origin, screen, pos):
    line_width = 20
    pendulum = pygame.draw.circle(screen, (70, 70, 255),
                                  (int(pos[0]), int(pos[1])), 20)
    centre = pygame.draw.circle(screen, (255, 255, 255),
                                (int(origin[0]), int(origin[1])), 7)
    line_width = 5

    # Draw the thicker line
    for i in range(-line_width // 2, line_width // 2 + 1):
        pygame.draw.line(screen, (200, 200, 200),
                         (int(origin[0]), int(origin[1] + i)),
                         (int(pos[0]), int(pos[1] + i)))

    pygame.display.flip()


def update_position(start_time, line_length, origin, screen, max_amplitude):
    # The maths here is presuming that the pendulum is a simple harmonic oscillator

    offset = 0
    gravity = 9.81

    dt = (
        pygame.time.get_ticks() - start_time
    ) / 100  # Delta time (change in time) in seconds (when divided by 1000)
    period = 2 * math.pi * math.sqrt(line_length / gravity)
    # calculate the current amplitude as the initial amplitude * the damping factor e^(-damping * t)
    damping = 0.05
    initial_amplitude = max_amplitude
    current_amplitude = initial_amplitude * math.exp(-damping * dt)

    theta = current_amplitude * math.cos(2 * math.pi / period * dt + offset)
    x = line_length * math.sin(theta)
    y = line_length * math.cos(theta)
    pos = (origin[0] + x, origin[1] + y)
    draw(origin, screen, pos)
    pygame.display.update()


def main():
    pygame.init()
    length = 1200
    width = 800
    screen = pygame.display.set_mode((length, width))
    running = True
    origin = (length / 2, (width / 2)-350)
    pos = (900, 400)
    line_length = math.sqrt((pos[1] - origin[1])**2 + (pos[0] - origin[0])**2)
    max_amplitude = math.radians(math.degrees(math.asin((pos[0] - origin[0]) / line_length)))
    start_time = 0

    while running:
        screen.fill(COLOUR_BG)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()
            start_time = pygame.time.get_ticks()
            x_length = pos[1] - origin[1]
            y_length = pos[0] - origin[0]
            line_length = math.sqrt(x_length**2 + y_length**2)
            max_amplitude = math.radians(math.degrees(math.asin(y_length / line_length)))

        update_position(start_time, line_length, origin, screen, max_amplitude)
        clock.tick(FPS)

    pygame.quit()

if __name__ == '__main__':
    main()
