import random
from collections import namedtuple
from enum import Enum

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
SPEED = 20
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = 0xFFE5B4
BLUE1 = 0x4169e1
BLUE2 = 0x4299f6

class SnakeGame:
    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h

        self.display = pg.display.set_mode((self.w, self.h))
        pg.display.set_caption("Snake")
        self.clock = pg.time.Clock()
        

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

    
    def _place_food(self):
        x = random.randint(0, (self.w-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        y = random.randint(0, (self.h-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        self.food = Point(x,y)
        if self.food in self.snake:
            self._place_food()



    def play_step(self):
        #collect the user input and key pressed
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                    self.direction = Direction.LEFT
            
                elif event.key == pg.K_RIGHT:
                    self.direction = Direction.RIGHT
            
                elif event.key == pg.K_UP:
                    self.direction = Direction.UP
            
                elif event.key == pg.K_DOWN:
                    self.direction = Direction.DOWN

        self._move(self.direction)
        self.snake.insert(0, self.head)

        game_over = False
        if self._is_collision():
            game_over = True
            return game_over, self.score

        if self.head == self.food:
            self.score += 1
            self._place_food()
        
        else:
            self.snake.pop()


        self._update_ui()
        self.clock.tick(SPEED)


        
        return game_over, self.score

    def _is_collision(self):
        if self.head.x > self.w - BLOCK_SIZE or self.head.x < 0 or self.head.y > self.h - BLOCK_SIZE or self.head.y < 0:
            return True
        if self.head in self.snake[1:]:
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

    def _move(self, direction):
        x = self.head.x
        y = self.head.y
        if direction== Direction.RIGHT:
            x += BLOCK_SIZE
        elif direction== Direction.LEFT:
            x -= BLOCK_SIZE
        elif direction== Direction.UP:
            y -= BLOCK_SIZE
        elif direction== Direction.DOWN:
            y += BLOCK_SIZE
            y -= BLOCK_SIZE

        self.head = Point(x, y)

    

if __name__ == "__main__":
    game = SnakeGame()

    while True:
        game_over, score = game.play_step()

        if game_over == True:
            break
        
    print("Final score: "+ str(score))

    pg.quit()
#just having fun