import pygame
import random
from enum import Enum
from collections import namedtuple

pygame.init()
font = pygame.font.Font('OrelegaOne-Regular.ttf', 25)

BLOCKSIZE = 20
SNAKE_PADDING = 3

Point = namedtuple('Point', ['x', 'y'])

class Color:
    WHITE = (255, 255, 255)
    RED = (200, 0, 0)
    BLUE1 = (0, 0, 255)
    BLUE2 = (0, 100, 255)
    BLACK = (0, 0, 0)
    GREY = (24, 24, 24)
    LIME = (0, 255, 0)

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

class SnakeGame:
    def __init__(self, w=640, h=480) -> None:
        self.w = w
        self.h = h

        self.obstaculos = [Point(5, 5), Point(6, 4), Point(6, 5)]

        # Iniciar tela
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Jogo da cobrinha')
        self.clock = pygame.time.Clock()

        # Iniciar estado do jogo
        self.direction = Direction.RIGHT
        self.speed = 8
        self.head = Point(self.w/2, self.h/2)
        self.snake = [self.head, Point(self.head.x-BLOCKSIZE, self.head.y), Point(self.head.x-(2*BLOCKSIZE), self.head.y)]

        self.score = 0
        self.food = None
        self._place_food()
    
    def play_step(self):
        # 1 - Receber o input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if self.direction != Direction.DOWN:
                        self.direction = Direction.UP
                elif event.key == pygame.K_DOWN:
                    if self.direction != Direction.UP:
                        self.direction = Direction.DOWN
                elif event.key == pygame.K_LEFT:
                    if self.direction != Direction.RIGHT:
                        self.direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT:
                    if self.direction != Direction.LEFT:
                        self.direction = Direction.RIGHT

        # 2 - Mover
        self._move(self.direction)
        self.snake.insert(0, self.head)

        # 3 - Checar se o jogo acabou
        game_over = False
        if self._is_colision():
            game_over = True
            return game_over, self.score

        # 4 - Checar se comeu
        if self.head == self.food:
            self.score += 1
            self.speed += 1
            self._place_food()
        else:
            self.snake.pop()

        # 5 - Atualizar UI e clock
        self._update_ui()
        self.clock.tick(self.speed)

        # 6 - Retornar game over e score
        return game_over, self.score

    def _place_food(self):
        x = random.randint(0, (self.w-BLOCKSIZE) // BLOCKSIZE) * BLOCKSIZE
        y = random.randint(0, (self.h-BLOCKSIZE) // BLOCKSIZE) * BLOCKSIZE

        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()     

    def _move(self, direction):
        x = self.head.x
        y = self.head.y

        if direction == Direction.RIGHT:
            x += BLOCKSIZE
        elif direction == Direction.LEFT:
            x -= BLOCKSIZE
        elif direction == Direction.UP:
            y -= BLOCKSIZE
        elif direction == Direction.DOWN:
            y += BLOCKSIZE
        
        if x > self.w - BLOCKSIZE:
            x = 0
        elif x < 0:
            x = self.w - BLOCKSIZE

        if y > self.h - BLOCKSIZE:
            y = 0
        elif y < 0:
            y = self.h - BLOCKSIZE
        
        self.head = Point(x, y)

    def _is_colision(self):
        if self.head in self.snake[1:]:
            return True
        
        return False

    def _update_ui(self):
        self.display.fill(Color.BLACK)

        for x in range(0, self.w, BLOCKSIZE):
            for y in range(0, self.h, BLOCKSIZE):
                rect = pygame.Rect(x, y, BLOCKSIZE, BLOCKSIZE)
                pygame.draw.rect(self.display, Color.GREY, rect, 1)
        
        for obs in self.obstaculos:
            pygame.draw.rect(self.display, Color.LIME, pygame.Rect(obs.x*BLOCKSIZE, obs.y*BLOCKSIZE, BLOCKSIZE, BLOCKSIZE))

        for unit in self.snake:
            pygame.draw.rect(self.display, Color.BLUE1, pygame.Rect(unit.x, unit.y, BLOCKSIZE, BLOCKSIZE))
            pygame.draw.rect(self.display, Color.BLUE2, pygame.Rect(unit.x+SNAKE_PADDING, unit.y+SNAKE_PADDING, BLOCKSIZE-(2*SNAKE_PADDING), BLOCKSIZE-(2*SNAKE_PADDING)))

        pygame.draw.rect(self.display, Color.RED, pygame.Rect(self.food.x, self.food.y, BLOCKSIZE, BLOCKSIZE))

        score_text = font.render('Pontos: ' + str(self.score), True, Color.WHITE)
        self.display.blit(score_text, [5, 3])
        pygame.display.flip()


if __name__ == '__main__':
    game = SnakeGame(720, 720)

    while True:
        game_over, score = game.play_step()

        # Se o jogo acabar, sai do loop
        if game_over:
            break
    
    print('Pontuação final:', score)

    pygame.quit()