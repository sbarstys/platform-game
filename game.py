import pygame
import math
from elements import *

#Game class for handling gameplay, movements, and setup/display
class Game:
    #Game constants
    BACKGROUND_COLOR = (125, 249, 255)
    SCREEN_WIDTH =  800
    SCREEN_HEIGHT = 700
    KEY_UP_THRESH = 6
    FPS = 60
    INITIAL_VELOCITY = 11 
    RL_VEL = 8
    GRAVITY = 1
    SPRITE_INDICATOR = 5
    SURFACE_INDICATOR = 6
    WHITE = (255, 255, 255)
    WINNER_LOSER_FONT = 'arial'
    FONT_SIZE = 100
    ENEMY_INDICATOR = 11
    GROUND_TYPE = 'Ground'
    CHARACTER_TYPE = 'Character'
    LOSE_PLACEMENT = ()
    WIN_PLACEMENT = ()
    WIN_PHRASE = 'YOU WIN'
    LOSE_PHRASE = 'YOU LOSE'
    WIN_TEXT_X = 185
    WIN_TEXT_Y = 10
    LOSE_TEXT_X = 155
    LOSE_TEXT_Y = 10

    def make_game_lists(self, text_file):
        game_list = []
        file_input = []
        first_line = ''
        second_line = ''
        with open(text_file) as in_file:
            first_line = in_file.readline()
            first_line = first_line.split(' ')
            file_input = in_file.readlines()

        if(len(first_line) == Game.SPRITE_INDICATOR):
            game_list.append(Character(first_line))
            second_line = file_input.pop(0)
            second_line = second_line.split(' ')
            game_list.append(Character(second_line))
        elif(len(first_line) == Game.SURFACE_INDICATOR):
            game_list.append(Ground(first_line))

        for data in file_input:
            if(len(first_line) == Game.SPRITE_INDICATOR):    
                input_list = data.split(' ')
                game_list.append(Enemy(input_list))
            elif(len(first_line) == Game.SURFACE_INDICATOR):
                input_list = data.split(' ')
                game_list.append(Shelf(input_list))
        
        return game_list

    def make_sub_lists(self, input_list):
        counter = 0
        return_list = []
        stopping_point = 0
        if input_list[0].get_type() == Game.GROUND_TYPE:
            stopping_point = 1
        elif input_list[0].get_type() == Game.CHARACTER_TYPE:
            stopping_point = 2
        for item in input_list:
            if counter >= stopping_point:
                return_list.append(item)
            counter += 1
        return return_list


    #Constructor for Game object. surface_file and sprite_file are the data used  
    def __init__(self, surface_file, sprite_file):
        self.surface_file = surface_file
        self.sprite_file = sprite_file
        self.display = pygame.display.set_mode((Game.SCREEN_WIDTH, Game.SCREEN_HEIGHT))
        self.sky_color = Game.BACKGROUND_COLOR
        self.ground = self.make_game_lists(self.surface_file)[0]
        self.shelf_list = self.make_sub_lists(self.make_game_lists(self.surface_file))
        self.player = self.make_game_lists(self.sprite_file)[0]
        self.coin = self.make_game_lists(self.sprite_file)[1]
        self.enemy_list = self.make_sub_lists(self.make_game_lists(self.sprite_file))
        self.lose_by_enemy = self.check_enemy_collision()
        self.win_by_coin = self.check_coin_collision()        
        self.sprite_group = pygame.sprite.Group()
        self.sprite_group.add(self.player)
        self.sprite_group.add(self.coin)
        for enemy in self.enemy_list:
            self.sprite_group.add(enemy)


    def shelf_horiz_range(self, *args):
        if len(args) == 0:
            in_left = self.player.rect.x >= self.player.prev_x_y_range[0] and self.player.rect.x <= self.player.prev_x_y_range[1]
            in_right = self.player.rect.x + self.player.width <= self.player.prev_x_y_range[1] and self.player.rect.x + self.player.width >= self.player.prev_x_y_range[0]
            return in_left or in_right
        else:
            in_left = self.player.rect.x >= args[0].rect.x and self.player.rect.x <= args[0].rect.x + args[0].rect.width
            in_right = self.player.rect.x + self.player.width <= args[0].rect.x + args[0].rect.width and self.player.rect.x + self.player.width >= args[0].rect.x
            return in_left or in_right

    #Checks for collisions with the characters and shelves (platforms) in the list
    def check_collision(self):
        for shelf in self.shelf_list:
            if self.player.rect.colliderect(shelf):
                return shelf

    #Determines whether the player sprite is above the visible windows
    def hit_ceiling(self):
        return self.player.rect.y < 0
    

    def check_contact(self):
        if self.player.rect.y >= self.ground.col_thresh and self.player.current_vel < 0:
            self.player.rect.y = self.player.vert_spawn
            return True
        #This will see if we are colliding with the same surface
        if self.player.rect.y == self.player.prev_shelf_y and self.shelf_horiz_range():
            return True
        #This will check for new collisions
        contact_shelf = None
        if self.player.current_vel != 0:
            contact_shelf = self.check_collision()
        if self.hit_ceiling():
            self.player.rect.y = 0
            self.current_vel = 0
        if contact_shelf != None:
            hit_head = self.player.rect.y > contact_shelf.rect.y
            if self.player.current_vel < 0 and self.shelf_horiz_range(contact_shelf) and not hit_head:
                self.player.rect.y = contact_shelf.sprite_on_surf
                self.player.prev_shelf_y = contact_shelf.sprite_on_surf
                self.player.prev_x_y_range = (contact_shelf.rect.x, contact_shelf.rect.x + contact_shelf.width)
                return True
            elif self.player.current_vel > 0 and self.shelf_horiz_range(contact_shelf):
                self.player.rect.y = contact_shelf.rect.y + contact_shelf.rect.height
                self.current_vel = 0
        return False

    #Applies gravitational acceleration to the player sprite
    def apply_gravity(self):
        self.player.rect.y -= self.player.current_vel
        self.player.current_vel -= Game.GRAVITY 

    #If t
    def handle_pos(self):
        if not self.check_contact():
            self.apply_gravity()
        else:
            self.current_vel = 0
            self.up_counter = 0

    
    def move_left(self):
        self.player.rect.x -= Game.RL_VEL
    
    def move_right(self):
        self.player.rect.x += Game.RL_VEL

    def jump(self):
        self.up_counter += 1
        self.player.current_vel = Game.INITIAL_VELOCITY
        self.player.rect.y -= Game.INITIAL_VELOCITY
    
    #Moves enemies according to their predefined positions and speeds
    def move_enemies(self):
        for enemy in self.enemy_list:
            if (enemy.rect.x <= enemy.horiz_range[0] or enemy.rect.x >= enemy.horiz_range[1]) and enemy.speed != 0:
                enemy.horiz_vel *= -1
                if enemy.rect.x < enemy.horiz_range[0]:
                    enemy.rect.x = enemy.horiz_range[0]
                if enemy.rect.x > enemy.horiz_range[1]:
                    enemy.rect.x = enemy.horiz_range[1] 
            if (enemy.rect.y <= enemy.vert_range[0] or enemy.rect.y >= enemy.vert_range[1]) and enemy.speed != 0:
                enemy.vert_vel *= -1
                if enemy.rect.y < enemy.vert_range[0]:
                    enemy.rect.y = enemy.vert_range[0]
                if enemy.rect.y > enemy.vert_range[1]:
                    enemy.rect.y = enemy.vert_range[1] 
            enemy.rect.x += enemy.horiz_vel
            enemy.rect.y += enemy.vert_vel
            enemy.speed = math.sqrt((enemy.horiz_vel ** 2) + (enemy.vert_vel ** 2))

    #Handles the user keyboard input
    def handle_key_mov(self, key_pressed):
        if key_pressed[pygame.K_RIGHT] and self.player.rect.x + self.player.width < Game.SCREEN_WIDTH:
            self.move_right()
        if key_pressed[pygame.K_LEFT] and self.player.rect.x > 0:
            self.move_left()
        if key_pressed[pygame.K_UP] and self.up_counter < Game.KEY_UP_THRESH:
            self.jump()


    def check_enemy_collision(self):
        for enemy in self.enemy_list:
            if self.player.rect.colliderect(enemy.rect):
                self.lose_by_enemy = True
                return

    #Determines if the player sprite collides with the coin which would mean the player wins
    def check_coin_collision(self):
        self.win_by_coin = self.player.rect.colliderect(self.coin)

    #Displays the text 'You Win' or 'You Lose' depending on the outcome of the game
    def draw_winner_loser(self):
        end_font = pygame.font.SysFont(Game.WINNER_LOSER_FONT, Game.FONT_SIZE)
        if self.win_by_coin:
            rendering = end_font.render(Game.WIN_PHRASE, 1, Game.WHITE)
            self.display.blit(rendering, (Game.WIN_TEXT_X, Game.WIN_TEXT_Y))
        elif self.lose_by_enemy:
            rendering = end_font.render(Game.LOSE_PHRASE, 1, Game.WHITE)
            self.display.blit(rendering, (Game.LOSE_TEXT_X, Game.LOSE_TEXT_Y))

    #Draws the window to screen. Includes sky background, sprites, and platforms
    def draw_window(self):
        self.display.fill(self.sky_color)
        pygame.draw.rect(self.display, (0, 0, 0), self.ground)
        self.display.blit(self.ground.ground_img, (0, self.ground.rect.y))
        for shelf in self.shelf_list:
            pygame.draw.rect(self.display, (0, 0, 0), shelf)
            self.display.blit(shelf.shelf_img, (shelf.rect.x, shelf.rect.y))        
        self.sprite_group.draw(self.display)
        self.draw_winner_loser()