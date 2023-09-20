import random
from collections import namedtuple
from enum import Enum
import numpy as np
import pygame as pg

pg.init()
font = pg.font.Font('arial.ttf', 25)

#reset
#reward
#play(action) -> direction
#game_iteration
#is_collision


class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4


Point = namedtuple("Point", "x, y")

BLOCK_SIZE = 20
SPEED = 100
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = 0xFFE5B4
BLUE1 = 0x4169e1
BLUE2 = 0x4299f6

class SnakeGameAI:
    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h

        self.display = pg.display.set_mode((self.w, self.h))
        pg.display.set_caption("Snake")
        self.clock = pg.time.Clock()
        self.reset()
        

    def reset(self):
        self.direction = Direction.RIGHT

        self.head = Point(self.w / 2, self.h / 2)
        self.snake = [
            self.head,
            Point(self.head.x - BLOCK_SIZE, self.head.y),
            Point(self.head.x - (2 * BLOCK_SIZE), self.head.y),
        ]

        self.score = 0
        self.food = None
        self._place_food()
        self.frame_iteration = 0

    
    def _place_food(self):
        x = random.randint(0, (self.w-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        y = random.randint(0, (self.h-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        self.food = Point(x,y)
        if self.food in self.snake:
            self._place_food()



    def play_step(self, action):
        self.frame_iteration += 1
        #collect the user input and key pressed
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            

        self._move(action)
        self.snake.insert(0, self.head)

        reward = 0
        game_over = False
        if self.is_collision() or self.frame_iteration > 100*len(self.snake):
            game_over = True
            reward = -10
            return reward, game_over, self.score

        if self.head == self.food:
            self.score += 1
            reward = 10
            self._place_food()
        
        else:
            self.snake.pop()


        self._update_ui()
        self.clock.tick(SPEED)

        return reward, game_over, self.score

    def is_collision(self, pt = None):
        if pt is None:
            pt=self.head
        if pt.x > self.w - BLOCK_SIZE or pt.x < 0 or pt.y > self.h - BLOCK_SIZE or pt.y < 0:
            return True
        if pt in self.snake[1:]:
            return True
        
        return False

    def _update_ui(self):
        self.display.fill(BLACK)
        for pt in self.snake:
            pg.draw.rect(self.display, BLUE1, pg.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pg.draw.rect(self.display, BLUE2, pg.Rect(pt.x+4, pt.y+4, 12, 12))
        
        pg.draw.rect(self.display, RED, pg.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))

        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0,0])
        pg.display.flip()

    def _move(self, action):
        # [straght, right, left]

        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clock_wise.index(self.direction)

        if np.array_equal(action, [1,0,0]):
            new_direction = clock_wise[idx] #no change
        elif np.array_equal(action, [0,1,0]):
            next_idx = (idx+1) %4
            new_direction = clock_wise[next_idx] #right turn
        else: #[0,0,1]
            next_idx = (idx - 1) %4
            new_direction = clock_wise[next_idx]
        
        self.direction = new_direction

        x = self.head.x
        y = self.head.y
        if self.direction== Direction.RIGHT:
            x += BLOCK_SIZE
        elif self.direction== Direction.LEFT:
            x -= BLOCK_SIZE
        elif self.direction== Direction.UP:
            y -= BLOCK_SIZE
        elif self.direction== Direction.DOWN:
            y += BLOCK_SIZE

        self.head = Point(x, y)

