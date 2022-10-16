import pygame, sys
from pygame import *

pygame.init()
screen = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()

white = (255, 255, 255)
black = (0, 0, 0)

class appearing_text(object):

    def __init__(self, lines):

        self.all_lines = []

        for line_count in range(len(lines)):
            text_surf = self.write(lines[line_count], black, white)
            width = text_surf.get_width()
            height = text_surf.get_height()

            text_co_ords = []

            text_array = pygame.surfarray.array3d(text_surf)

            for x in range(width):
                for y in range(height):
                    if text_array[x][y][0] == 0 and text_array[x][y][1] == 0 and text_array[x][y][2] == 0:
                        text_co_ords.append((x, y))

            self.all_lines.append(text_co_ords)

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise SystemExit

        start_x = 20
        start_y = 20

        for line in self.all_lines:
            for co_ords in line:
                x = co_ords[0]
                y = co_ords[1]
                pygame.draw.line(screen, (255, 255, 255), (start_x + x, start_y + y), (start_x + x + 1, start_y + y))
                pygame.display.flip()

            start_y += 20

    def write(self, msg, fg_col=white, bg_col=black, size=20):
        print(msg)
        myfont = pygame.font.SysFont("verdana", 20)
        text_surf = myfont.render(msg, False, black, white)
        text_surf = text_surf.convert()
        return text_surf


if __name__ == "__main__":
    at = appearing_text(
        ["This is the text that appears on your screen, and I hope you like it", "This is some more text to appear"])
    at.update()
    sys.exit()