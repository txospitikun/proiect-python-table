import pygame


class GUI:
    def __init__(self, width, height, caption, background_color = (223, 212, 252)):
        self.width = width
        self.height = height
        self.clock = pygame.time.Clock()
        self.running = True
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.background_color = background_color
        pygame.display.set_caption(caption)
        self.screen.fill(self.background_color)
        pygame.display.flip()

    def gui_loop(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            self.clock.tick(60)
            pygame.display.update()

game_gui = GUI(1000, 800, "Table")
game_gui.gui_loop()
