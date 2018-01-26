import pygame

class Ui(object):
    def get_screen(width, height):
        return (pygame.display.set_mode((width, height)))

    def initialise_pygame(target):
        pygame.init()
        pygame.key.set_repeat(250,25)
        target.default_font =  pygame.font.Font(
            pygame.font.get_default_font(), 12)
        pygame.event.set_blocked(pygame.MOUSEMOTION)

    def set_timer(timeout):
        pygame.time.set_timer(pygame.USEREVENT+1, timeout)

    def draw(screen, color, x_pos, y_pos, cell_size):
        pygame.draw.rect(
            screen,
            color,
            pygame.Rect(
                (x_pos) *
                  cell_size,
                (y_pos) *
                  cell_size, 
                cell_size,
                cell_size),0)

    def update():
        pygame.display.update()

    def get_clock():
        return pygame.time.Clock()

    def draw_line(screen, rlim, height):
        pygame.draw.line(screen,
            (255,255,255),
            (rlim+1, 0),
            (rlim+1, height-1))

    def get_events():
        return pygame.event.get()

