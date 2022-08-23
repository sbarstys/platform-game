import pygame
import os

#Relevant strings and constants for indexing into data input lists
X_INDEX = 0
Y_INDEX = 1
WIDTH_INDEX = 2
HEIGHT_INDEX = 3
SPECIFIC_INDEX = 4
IMAGE_INDEX = 5
IMAGE_INDEX_SPRITE = 4
HORIZ_VEL_INDEX = 4
VERT_VEL_INDEX = 5
HORIZ_LEFT = 6
HORIZ_RIGHT = 7
VERT_TOP = 8
VERT_BOTTOM = 9
STR_INPUT = 10
MEDIA_FOLDER_STR = 'media'
GROUND_TYPE = 'Ground'
CHARACTER_TYPE = 'Character'

#Class used for storing the ground data. Data that is extracted from the files is inputted
#as a list with each location holding a different datapoint.
class Ground:
    def __init__(self, input_list):
        x_loc = float(input_list[X_INDEX])
        y_loc = float(input_list[Y_INDEX])
        width = float(input_list[WIDTH_INDEX])
        height = float(input_list[HEIGHT_INDEX])
        self.col_thresh = float(input_list[SPECIFIC_INDEX])
        img_str = input_list[IMAGE_INDEX].rsplit('\n')[0]
        self.rect = pygame.Rect(x_loc, y_loc, width, height)
        to_transform = pygame.image.load(os.path.join(MEDIA_FOLDER_STR, img_str))
        self.ground_img = pygame.transform.scale(to_transform, (width, height))

    #Returns a string indicating the type of the ground object
    def get_type(self):
        return GROUND_TYPE

#Class used for storing the shelf data. Data that is extracted from the files is inputted
#as a list with each location holding a different datapoint.
class Shelf:
    def __init__(self, input_list):
        x_loc = float(input_list[X_INDEX])
        y_loc = float(input_list[Y_INDEX])
        self.width = float(input_list[WIDTH_INDEX])
        height = float(input_list[HEIGHT_INDEX])
        sprite_on_surf = float(input_list[SPECIFIC_INDEX].rsplit('\n')[0])
        self.rect = pygame.Rect(x_loc, y_loc, self.width, height)
        self.sprite_on_surf = sprite_on_surf
        self.img_str = input_list[IMAGE_INDEX].rsplit('\n')[0]
        to_transform = pygame.image.load(os.path.join(MEDIA_FOLDER_STR, self.img_str))
        self.shelf_img = pygame.transform.scale(to_transform, (self.width, height))


#Class used for storing the character data. Data that is extracted from the files is inputted
#as a list with each location holding a different datapoint.
class Character(pygame.sprite.Sprite):

    def __init__(self, input_list):
        super().__init__()
        self.width = float(input_list[WIDTH_INDEX])
        height = float(input_list[HEIGHT_INDEX])
        self.img_str = input_list[IMAGE_INDEX_SPRITE].rsplit('\n')[0]
        to_scale = pygame.image.load(os.path.join(MEDIA_FOLDER_STR, self.img_str))
        self.image = pygame.transform.scale(to_scale, (self.width, height))
        self.rect = self.image.get_rect()
        self.vert_spawn = float(input_list[Y_INDEX])
        self.rect.x = float(input_list[X_INDEX])
        self.rect.y = float(input_list[Y_INDEX])
        self.current_vel = 0
        self.up_counter = 0
        self.prev_shelf_y = 0
        self.prev_x_y_range = (0,0)

    #Returns a string indicating the type of the character object
    def get_type(self):
        return CHARACTER_TYPE

#Class used for storing the Enemy data. Data that is extracted from the files is inputted
#as a list with each location holding a different datapoint.
class Enemy(pygame.sprite.Sprite):
    #x y width height horiz_velocity, vert_velocity left_most right_most up_most down_most image
    def __init__(self, input_list):
        super().__init__()
        width, height = float(input_list[WIDTH_INDEX]), float(input_list[HEIGHT_INDEX])
        self.img_str = input_list[STR_INPUT].rsplit('\n')[0]
        to_scale = pygame.image.load(os.path.join(MEDIA_FOLDER_STR, self.img_str))
        self.image = pygame.transform.scale(to_scale, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = float(input_list[X_INDEX])
        self.rect.y = float(input_list[Y_INDEX])
        self.horiz_vel = float(input_list[HORIZ_VEL_INDEX])
        self.vert_vel = float(input_list[VERT_VEL_INDEX])
        self.horiz_range = (float(input_list[HORIZ_LEFT]), float(input_list[HORIZ_RIGHT]))
        self.vert_range = (float(input_list[VERT_TOP]), float(input_list[VERT_BOTTOM]))
        self.speed = 0
