import pygame
import random
import numpy as np
from enum import Enum
from collections import namedtuple
from math import dist

pygame.init()
# font = pygame.font.Font('./OrelegaOne-Regular.ttf', 25)
font = pygame.font.SysFont('Arial', 25, bold=True)

BLOCKSIZE = 30
AMBULANCE_PADDING = 3
MINIMUN_DISTANCE = 250

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

class AmbulancIA:
    def __init__(self, w=600, h=600) -> None:
        self.w = w
        self.h = h

        self.walls = self._get_board()
        self.obstacles_points = self._wall_points()

        # Iniciar tela
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('AmbulancIA')
        self.clock = pygame.time.Clock()

        # Iniciar estado do jogo
        self.direction = Direction.RIGHT
        self.speed = 8
        self.head = Point(self.w/2, self.h/2)
        self.ambulance = [self.head, Point(self.head.x-BLOCKSIZE, self.head.y), Point(self.head.x-(2*BLOCKSIZE), self.head.y)]

        self.score = 0
        self.pacient = None
        self.hospital = None
        self.carrying = False
        self._place_pacient()
        self._place_hospital()
    
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
        self.ambulance.insert(0, self.head)

        # 3 - Checar se o jogo acabou
        game_over = False
        if self._has_arrived():
            game_over = True
            return game_over, self.score

        # 4 - Checar se pegou o paciente
        if self.head == self.pacient:
            self.score += 1
            self.speed += 5
            self.carrying = True
            # self._place_pacient()
        else:
            self.ambulance.pop()

        # 5 - Atualizar UI e clock
        self._update_ui()
        self.clock.tick(self.speed)

        # 6 - Retornar game over e score
        return game_over, self.score

    @staticmethod
    def check_distance(origin, destination):
        a = (origin.x, origin.y)
        b = (destination.x, destination.y)
        return dist(a, b)

    def _place_pacient(self):
        x = random.randint(0, (self.w-BLOCKSIZE) // BLOCKSIZE) * BLOCKSIZE
        y = random.randint(0, (self.h-BLOCKSIZE) // BLOCKSIZE) * BLOCKSIZE

        self.pacient = Point(x, y)
        forbidden_places = self._wall_points()

        if self.pacient in forbidden_places:
            self._place_pacient()

    def _place_hospital(self):
        x = random.randint(0, (self.w-BLOCKSIZE) // BLOCKSIZE) * BLOCKSIZE
        y = random.randint(0, (self.h-BLOCKSIZE) // BLOCKSIZE) * BLOCKSIZE

        self.hospital = Point(x, y)
        forbidden_places = self._wall_points()

        if (self.hospital in forbidden_places) or (self.check_distance(self.pacient, self.hospital) < MINIMUN_DISTANCE):
            self._place_hospital()
        
        print(self.check_distance(self.pacient, self.hospital))

    def _move(self, direction):
        obstacle_flag = False
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
            x = self.head.x
        elif x < 0:
            x = self.head.x

        if y > self.h - BLOCKSIZE:
            y = self.head.y
        elif y < 0:
            y = self.head.y

        for obstacle_point in self.obstacles_points:
            if Point(x, y) == obstacle_point:
                obstacle_flag = True

        if not obstacle_flag:
            self.head = Point(x, y)

    def _has_arrived(self):
        if self.carrying and self.head == self.hospital:
            return True
        
        return False

    def _update_ui(self):
        self.display.fill(Color.BLACK)

        # Desenhando o grid
        for x in range(0, self.w, BLOCKSIZE):
            for y in range(0, self.h, BLOCKSIZE):
                rect = pygame.Rect(x, y, BLOCKSIZE, BLOCKSIZE)
                pygame.draw.rect(self.display, Color.GREY, rect, 1)
        
        # Desenhando os obstaculos na tela
        for i in range(self.walls.shape[0]):
            for j in range(self.walls.shape[1]):
                if self.walls[i, j] == 1:
                    pygame.draw.rect(self.display, Color.LIME, pygame.Rect(j*BLOCKSIZE, i*BLOCKSIZE, BLOCKSIZE, BLOCKSIZE))
            
        for unit in self.ambulance:
            if self.carrying:
                pygame.draw.rect(self.display, Color.RED, pygame.Rect(unit.x, unit.y, BLOCKSIZE, BLOCKSIZE))
                pygame.draw.rect(self.display, Color.BLUE2, pygame.Rect(unit.x+AMBULANCE_PADDING, unit.y+AMBULANCE_PADDING, BLOCKSIZE-(2*AMBULANCE_PADDING), BLOCKSIZE-(2*AMBULANCE_PADDING)))
            else:
                pygame.draw.rect(self.display, Color.BLUE1, pygame.Rect(unit.x, unit.y, BLOCKSIZE, BLOCKSIZE))
                pygame.draw.rect(self.display, Color.BLUE2, pygame.Rect(unit.x + AMBULANCE_PADDING, unit.y + AMBULANCE_PADDING, BLOCKSIZE - (2 * AMBULANCE_PADDING), BLOCKSIZE - (2 * AMBULANCE_PADDING)))

        # Desenhar o paciente quando não estiver carregando
        if not self.carrying:
            pygame.draw.rect(self.display, Color.RED, pygame.Rect(self.pacient.x, self.pacient.y, BLOCKSIZE, BLOCKSIZE))
        pygame.draw.rect(self.display, Color.WHITE, pygame.Rect(self.hospital.x, self.hospital.y, BLOCKSIZE, BLOCKSIZE))

        score_text = font.render('Carregando paciente' if self.carrying else 'Buscando paciente', True, Color.WHITE)
        self.display.blit(score_text, [5, 1])
        pygame.display.flip()
    
    def _wall_points(self):
        point_list = list()

        for i in range(self.walls.shape[0]):
            for j in range(self.walls.shape[1]):
                if self.walls[i, j] == 1:
                    point_list.append(Point(j*BLOCKSIZE, i*BLOCKSIZE))
        
        return point_list

    def _get_board(self):
        boards = list()

        boards.append(np.array([
            [1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.,],
            [1., 0., 0., 0., 0., 1., 0., 0., 0., 1., 1., 0., 0., 0., 0., 0., 0., 1., 0., 1.,],
            [1., 1., 1., 1., 0., 1., 1., 1., 0., 1., 1., 0., 1., 0., 0., 1., 0., 1., 0., 1.,],
            [1., 0., 0., 1., 0., 0., 0., 0., 0., 1., 1., 0., 1., 0., 0., 1., 0., 1., 0., 1.,],
            [1., 1., 0., 0., 0., 1., 1., 1., 0., 0., 0., 0., 1., 0., 0., 1., 0., 1., 0., 1.,],
            [1., 0., 0., 1., 0., 1., 0., 1., 0., 1., 0., 0., 1., 0., 1., 1., 1., 1., 0., 1.,],
            [1., 0., 1., 1., 0., 1., 0., 1., 0., 1., 0., 0., 0., 0., 1., 0., 0., 0., 0., 1.,],
            [1., 0., 0., 1., 0., 1., 0., 1., 0., 1., 0., 0., 1., 0., 1., 0., 0., 1., 0., 1.,],
            [1., 0., 0., 1., 0., 1., 0., 0., 0., 1., 0., 0., 1., 0., 0., 0., 0., 1., 0., 1.,],
            [1., 1., 1., 1., 0., 1., 0., 0., 0., 0., 0., 1., 1., 0., 1., 0., 0., 1., 0., 1.,],
            [1., 0., 0., 0., 0., 1., 1., 1., 1., 1., 0., 1., 1., 0., 1., 0., 0., 1., 0., 1.,],
            [1., 0., 1., 1., 0., 0., 0., 0., 0., 1., 0., 1., 1., 0., 1., 1., 1., 1., 0., 1.,],
            [1., 0., 1., 1., 0., 1., 1., 1., 0., 1., 0., 1., 1., 0., 0., 0., 0., 0., 0., 1.,],
            [1., 0., 1., 1., 0., 1., 0., 1., 0., 1., 0., 0., 1., 0., 1., 1., 1., 1., 0., 1.,],
            [1., 0., 1., 1., 0., 1., 0., 1., 0., 1., 0., 0., 1., 0., 1., 0., 0., 1., 0., 1.,],
            [1., 0., 1., 1., 0., 1., 0., 0., 0., 1., 0., 0., 1., 0., 1., 1., 0., 1., 0., 1.,],
            [1., 0., 1., 1., 0., 1., 0., 1., 0., 1., 0., 0., 1., 0., 0., 0., 0., 1., 0., 1.,],
            [1., 0., 1., 1., 0., 1., 0., 1., 0., 1., 0., 0., 1., 1., 1., 1., 1., 1., 0., 1.,],
            [1., 0., 1., 1., 0., 1., 0., 1., 0., 1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 1.,],
            [1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.,]]))
        
        boards.append(boards[0].T)
        
        return boards[random.randint(0, len(boards)-1)]


if __name__ == '__main__':
    game = AmbulancIA()

    while True:
        game_over, score = game.play_step()

        # Se o jogo acabar, sai do loop
        if game_over:
            break
    
    print('Pontuação final:', score)

    pygame.quit()