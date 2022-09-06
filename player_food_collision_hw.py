# You need three files for this assignment:  testing.py, vector.py, (on Slack #general), 
# and box_player_food_collision_hw.py (this file)

#========================================================================================
# NOTES about your submission
#========================================================================================
# Your SUBMISSION should include a GIF animation of your file, embedded into Canvas, AND
# Include just this one Python file, FILLED IN at all spots marked TODO
# DO NOT MAKE ANY OTHER MODIFICATIONS TO THIS FILE
# DO NOT INCLUDE vector.py or testing.py in your submission
# DO NOT MODIFY vector.py or testing.py when doing this assignmennt
#========================================================================================

# # ONLY CHANGE THE PARTS OF THE BOX CLASS MARKED TODO:

import pygame as pg
import sys, time
from vector import Vector
from random import randint


MOVESPEED = 4
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)
CYAN = (0, 255, 255)
DARK_GREY = (60, 60, 60)

COLORS = [RED, GREEN, BLUE, YELLOW, PURPLE, CYAN]

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800


class Box:    # base object for creating rectangles at posn, with width, height, clr, and vel
    boxes_created = 0
    def __init__(self, screen, left, top, width, height, vel, clr):
        self.screen = screen
        self.posn = Vector(left, top)
        self.width, self.height = width, height
        self.vel = vel * MOVESPEED
        self.vel = vel
        self.clr = clr
        self.rect = pg.Rect(left, top, width, height)
        Box.boxes_created += 1
        print(f'Created Box #{Box.boxes_created}: {self}')
    @classmethod      # this function allows multiple constructors in Python
    def create_random(cls, screen, clr=None, width=None, height=None):
        if width == None: 
            width = randint(10, 50)
        if height == None:
            height = randint(10, 50)
        left = randint(0, WINDOW_WIDTH - width)
        top = randint(0, WINDOW_HEIGHT - height)
        vx = randint(-5, 5) 
        vy = randint(-5, 5)
        if vy == 0:
            vy += 1
        if vx == 0:
            vx -= 1
        if clr == None:
            clr = COLORS[randint(0, 5)]
        return Box(screen=screen, left=left, top=top, width=width, height=height, 
                     vel=Vector(x=vx, y=vy), clr=clr)
    def __repr__(self):
        return f'Box(posn={self.posn},vel={self.vel},width={self.width},height={self.height},clr={self.clr})'
    def update(self):
        self.posn += self.vel
        x, y = self.posn.x, self.posn.y
        if x <= 0 or x + self.width >= WINDOW_WIDTH: 
            self.vel.x *= -1
        if y <= 0 or y + self.height >= WINDOW_HEIGHT: 
            self.vel.y *= -1
        self.rect = pg.Rect(self.posn.x, self.posn.y, self.width, self.height)
        self.draw()
    def draw(self):
        s = self.posn
        wh = (self.width, self.height)
        pg.draw.rect(self.screen, self.clr, pg.Rect(s.x, s.y, wh[0], wh[1]))
    

class Food:    # this class has-a Box object in it, and makes Food objects that the Player eats
    FOODSIZE = 20
    def __init__(self, screen, clr=GREEN):
        self.box = Box.create_random(screen=screen, width=Food.FOODSIZE, height=Food.FOODSIZE, clr=clr)
    def __repr__(self):
        return f'Food/{self.box.__repr__()}'
    def collide(self, player):  
        return self.box.rect.colliderect(player)
        #TODO: fill in code to say if a collision occurred between the player and the Food object
    def update(self):  
        self.box.update()
        # TODO: fill in code for updating the Food object
    def draw(self):
        self.box.draw()
        # TODO: fill in code for drawing the Food object


class Foods:      # this class has a list of Food objects in it, which the Player eats
    def __init__(self, screen, nfoods=20):
        self.screen = screen
        self.nfoods = nfoods
        self.foods = []
        self.create_foods()
    def create_foods(self):
        self.foods.clear()
        # TODO: fill in code for creating the Food objects and adding them to self.foods
        for i in range(0, self.nfoods):
            objFood = Food(screen = self.screen)
            self.foods.append(objFood)
    def add_food(self, screen, left, top):
        print(f'in add_food, left={left} and top={top}')
        food = Food(screen=screen)
        food.box = Box(screen=screen, left=left, top=top, width=food.box.width, height=food.box.width,
                      vel=food.box.vel, clr=food.box.clr)
        self.foods.append(food)
    def check_collision(self, player):
        for self.food in self.foods[:]:
            if player.collide(self.food):
                self.foods.remove(self.food)
        # TODO: fill in code for going through all the foods in self.foods
        # calling food.check_collision(player)
        # and if there is a collision, remove the food from self.foods (see Textbook ch. 19)
    def update(self):
        for food in self.foods:
            food.update()   # update the posn of the food object using its vel
            food.draw()     # draw the food object in its new location


class Player(Box):   # this class inherits from Box, and allows the Player to move and eat Food
    PLAYERSIZE = 40
    def __init__(self, screen, clr=RED): 
        size = Player.PLAYERSIZE
        rect = screen.get_rect().centery
        left = screen.get_rect().centerx - size / 2
        top = screen.get_rect().bottom - size
        super().__init__(screen=screen, left=left, top=top, width=size, height=size, 
                         vel=Vector(), clr=clr)
    def __repr__(self): return f'Player/{super().__repr__()}'
    def update(self, foods): 
        foods.check_collision(player=self)
        super().update()


class Game:   # this class controls the initialization and play of the game
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), 0, 32)
        pg.display.set_caption('Animation')   
        self.foods = Foods(screen=self.screen, nfoods=40)   
        self.player = Player(screen=self.screen)
        # self.foods = [Food(screen=self.screen) for _ in range(103)]
        # self.boxes = [Box.create_random(screen=self.screen) for _ in range(103)]
    def play(self):
        keys = [pg.K_LEFT, pg.K_RIGHT, pg.K_UP, pg.K_DOWN]      # up, down, left, right arrows
        movement = {pg.K_LEFT: Vector(-1, 0),   # dictionary to map keys to Vector velocities
                    pg.K_RIGHT: Vector(1, 0),
                    pg.K_UP: Vector(0, -1),
                    pg.K_DOWN: Vector(0, 1)
                    }
        finished = False
        while not finished:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    finished = True
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_x:   # teleport the Player to a random location if 'x' is pressed
                        self.player.posn = Vector(randint(0, WINDOW_WIDTH - self.player.width), 
                                                  randint(0, WINDOW_HEIGHT - self.player.height))
                    elif event.key in keys:   # changes Player vector if arrow keys pressed
                        self.player.vel += MOVESPEED * movement[event.key]
                elif event.type == pg.KEYUP and event.key == pg.K_ESCAPE:  # stop moving Player
                    self.player.vel = Vector()
                elif event.type == pg.MOUSEBUTTONUP:   # makes a new Food object if mouse is clicked
                    self.foods.add_food(self.screen, event.pos[0], event.pos[1])
                    # TODO: fill in code for adding the Food object at event.pos
 
            self.screen.fill(DARK_GREY)     # fill the screen with dark grey
            self.player.update(self.foods)  # update and draw the Player
            self.foods.update()   # update and draw all the Food objects
 
            pg.display.update()   # off-screen bitmap is bit-blitted (bit block transfer) to on-screen
            time.sleep(0.02)
        pg.quit()
        sys.exit()

def main():
    # Vector.run_tests()
    g = Game()
    g.play()            

if __name__ == '__main__':
    main()


