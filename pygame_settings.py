import pygame

'''Contains settings and functions for pygame representations'''

class Settings:
    def __init__(self, x_num_rect, y_num_rect):#initialize settings

        self.window_width = 1200
        self.window_height = 650
        self.top_margin_height = 5
        self.bottom_margin_height = 5
        self.margin_width = 5 #Size of x margin
        self.gap_size = 1 #Space between rectangles
        self.game_running = True

        self.default_font_size = self.top_margin_height * 3/5

        self.x_num_rect = x_num_rect #x and y number of squares in board
        self.y_num_rect = y_num_rect

        self.board_width = self.window_width - 2 * self.margin_width #pixel width of board
        self.board_height = self.window_height - (self.top_margin_height + self.bottom_margin_height)#pixel height of board

        self.box_width = (self.board_width - self.gap_size * (self.x_num_rect - 1))/self.x_num_rect #box height
        self.box_height = (self.board_height - self.gap_size * (self.y_num_rect - 1))/self.y_num_rect #box width

        self.white = (230, 230, 230) #colors used
        self.gray = (80, 80, 80) #May need to change
        self.black = (0, 0, 0)

        #game colors
        self.bg_color = self.gray
        self.off_color = self.white
        self.on_color = self.black

    def left_top_coords_of_box(self, boxx,boxy):
        '''converts board coordinates to pixel coordinates'''
        left = (boxx - 1) * (self.box_width + self.gap_size) + self.margin_width #formula for finding left of box
        top = (boxy - 1) * (self.box_height + self.gap_size) + self.top_margin_height #formula for finding top of box
        return left, top

    def draw_board(self, board, screen): 
        '''resets screen with new board'''

        screen.fill(self.bg_color)
        for boxx in range (self.x_num_rect):
            for boxy in range (self.y_num_rect):
                left, top = self.left_top_coords_of_box(boxx + 1, boxy + 1) 

                if board[boxy][boxx] == 0:#draws off boxes
                    pygame.draw.rect(screen, self.off_color,(left, top, self.box_width, self.box_height)) 
                elif board[boxy][boxx] == 1:#draws on boxes
                    pygame.draw.rect(screen, self.on_color,(left, top, self.box_width, self.box_height)) 