import pygame, copy
from random import randint

class Settings:
    def __init__(self):#initialize settings

        self.window_width = 900 #width of window
        self.window_height = 600 #height of window
        self.top_margin_height = 50 #Size of y margin
        self.bottom_margin_height = 25
        self.margin_width = 20 #Size of x margin
        self.gap_size = 2 #Space between rectangles
        self.game_running = True

        self.default_font_size = self.top_margin_height * 3/5

        self.x_num_rect = 15 #x and y number of squares in board
        self.y_num_rect = 15

        self.board_width = self.window_width - 2 * self.margin_width #pixel width of board
        self.board_height = self.window_height - (self.top_margin_height + self.bottom_margin_height)#pixel height of board

        self.box_width = (self.board_width - self.gap_size * (self.x_num_rect - 1))/self.x_num_rect #box height
        self.box_height = (self.board_height - self.gap_size * (self.y_num_rect - 1))/self.y_num_rect #box width

        self.player1_move = 5 #Infected plaer number of moves per turn
        self.player2_move = 7 #Uninfected player number of moves per turn

        self.white = (255, 255, 255) #colors used
        self.gray = (199, 199, 199) #May need to change
        self.blue = (64, 133, 198)
        self.red = (240, 79, 69)
        self.dark_blue = (20, 54, 86)

        #game colors
        self.bg_color = self.gray
        self.empty_color = self.dark_blue
        self.infected_color = self.red
        self.uninfected_color = self.blue

    def left_top_coords_of_box(self, boxx,boxy):
        '''converts board coordinates to pixel coordinates'''
        left = (boxx - 1) * (self.box_width + self.gap_size) + self.margin_width #formula for finding left of box
        top = (boxy - 1) * (self.box_height + self.gap_size) + self.top_margin_height #formula for finding top of box
        return left, top

    def get_box_at_pixel(self, x, y):
        for boxx in range (self.x_num_rect + 1):
            for boxy in range (self.y_num_rect + 1):
                left, top = self.left_top_coords_of_box(boxx, boxy)
                box_rect = pygame.Rect(left, top, self.box_width, self.box_height) #runs through all rectanglas
                if box_rect.collidepoint(x,y): #tests if box is in box_rect
                    return (boxx, boxy)#coord of box
        return (None, None) #returns none,none if no 

    def draw_board(self, board, screen): 
        '''resets screen with new board'''

        screen.fill(self.bg_color)
        for boxx in range (self.x_num_rect):
            for boxy in range (self.y_num_rect):
                left, top = self.left_top_coords_of_box(boxx + 1, boxy + 1) #I don't know why this works but it works
                if board[boxy][boxx] == 0:
                    pygame.draw.rect(screen, self.empty_color,(left, top, self.box_width, self.box_height)) #draws empty boxes
                elif board[boxy][boxx] == 1:
                    pygame.draw.rect(screen, self.infected_color,(left, top, self.box_width, self.box_height)) #draws infected boxes
                elif board[boxy][boxx] == 2:
                    pygame.draw.rect(screen, self.uninfected_color,(left, top, self.box_width, self.box_height)) 


class game_array:
    def __init__(self, array_x_length, array_y_length):
        board_setup = []

        self.array_x_length = array_x_length
        self.array_y_length = array_y_length

        #board
        outer_row = [3 for x in range(array_x_length + 2)]
        middle_row = [3,3]

        for _ in range(0,array_x_length):#creates inner row
            middle_row.insert(1,0)

        board_setup.append(outer_row)
        for _ in range(0,array_y_length):
            board_setup.append(list(middle_row))
        board_setup.append(outer_row)

        self.board = copy.deepcopy(board_setup)
        self.board_setup = board_setup

    def change_rect_status(self, status, boxx, boxy): 
        '''changes the value in an entry in self.board'''

        self.board[boxy][boxx] = status

    def return_board(self): 
        '''returns board without the frame of 3s'''

        new_board = []
        for row_check in range(1, self.array_y_length + 1):
            new_row = list.copy(self.board[row_check])
            del new_row[0]
            del new_row[self.array_x_length]
            new_board.append(new_row)

        return new_board

    def check_move_valid(self, player, valid_boxx, valid_boxy, move_count, player1_move): 
        '''validates a move'''
    
        if self.board[valid_boxy][valid_boxx] == 0:
            if self.board[valid_boxy-1][valid_boxx] == player: #checks box below
                return True
            elif self.board[valid_boxy][valid_boxx-1] == player: #checks box to the left
                return True
            elif self.board[valid_boxy+1][valid_boxx] == player: #checks box above
                return True
            elif self.board[valid_boxy][valid_boxx+1] == player: #checks box to the right
                return True
            elif move_count == 1 or move_count == player1_move + 1: #validates inf's first move or noninf's first move
                return True
        return False

    def check_game_running(self): 
        '''Sees if game is running, returns 0 if running,
        returns 1 = player 1 cannot expand, returns 2 = player 2 cannot expand'''

        inf_surrounded = True #default sets game ended
        noninf_surrounded = True #default sets game ended
        noninf_first_move = True #default sets no noninf on the board

        for row_check in range(1, self.array_y_length + 1): #Checks playable rows
            for column_check in range(1, self.array_x_length + 1): #checks playable columns

                entry = self.board[row_check][column_check] #stores current entry as a variable
                
                if entry == 1: #tests entry value
                    if self.board[row_check-1][column_check] == 0: #checks adjacent entries
                        inf_surrounded = False

                    elif self.board[row_check+1][column_check] == 0:
                        inf_surrounded = False
                                        
                    elif self.board[row_check][column_check-1] == 0:
                        inf_surrounded = False
                                    
                    elif self.board[row_check][column_check+1] == 0:
                        inf_surrounded = False

                elif entry == 2: #tests entry value

                    noninf_first_move = False# if there are 2's on the screen, it is not 2's first move

                    if self.board[row_check-1][column_check] == 0: #checks adjacent entries
                        noninf_surrounded = False

                    elif self.board[row_check+1][column_check] == 0:
                        noninf_surrounded = False                                            
                    
                    elif self.board[row_check][column_check-1] == 0:
                        noninf_surrounded = False
                                        
                    elif self.board[row_check][column_check+1] == 0:
                        noninf_surrounded = False

        if noninf_first_move: #if it is player 2's first move, game continues
            return 0

        elif inf_surrounded: # if inf surrounded return 1, ends game
            return 1

        elif noninf_surrounded: # if noninfected surrounded return 2, ends game
            return 2

        else: 
            return 0 #else, continue game
    def fill_all(self, player):
        '''Used at the end of the game if the noninfected player becomes surrounded to convert all remaining 0s to 1s'''
        for row_check in range(1, self.array_y_length + 1): #Checks playable rows
            for column_check in range(1, self.array_x_length + 1): #checks playable columns
                if self.board[row_check][column_check] == 0:
                    self.board[row_check][column_check] = player #if 0 converts to 1

    def count_score(self, player): 
        '''counts score'''
        score = 0
        for row_check in range(1, self.array_y_length + 1): #checks all rows
            for column_check in range(1, self.array_x_length + 1): #checks all columns
                if self.board[row_check][column_check] == player:
                    score +=  1
        return score

    def valid_move_array(self, player, move_count, player1_move):
        '''returns array with valid moves marked 1'''
        move_array = copy.deepcopy(self.board_setup)#creates an empty array

        for y_rect in range(1, self.array_y_length + 1): #checks all rows
            for x_rect in range(1, self.array_x_length + 1): #checks all columns
                if self.check_move_valid(player, x_rect, y_rect, move_count, player1_move):
                    move_array[y_rect][x_rect] = 1

        return move_array

    def running_check(self):
        '''Checks whether game is running'''
        running_value = self.check_game_running()
        
        #if 2 or 1 can't expand, convert the rest of the board to 1 or 2
        if running_value == 2: 
            self.fill_all(1)
        elif running_value == 1:
            self.fill_all(2)

        #recounts score and returns false if game is not running
        score = self.count_score(1)
        if running_value != 0:
            return False, score
        return True, score




class text: #used for all text boxes
    def __init__(self, characters, text_size, color, screen, font = "freesansbold.ttf"):
        '''initializes object in text class'''
        self.characters = characters
        self.text_size = round(text_size)
        self.color = color
        self.screen = screen
        self.font = font

    def right_display_rectangle(self, x_right, y_cent):
        '''creates and displays text on screen'''
        
        font = pygame.font.Font(self.font, self.text_size) #creates a font object
        
        text_object = font.render(self.characters, True, self.color) #creates a text surface object

        rectangle = text_object.get_rect()

        #sets coordinates of rectangle based off of left side and height center
        rectangle.right = x_right
        rectangle.centery = y_cent

        self.screen.blit(text_object, rectangle)

    def left_display_rectangle(self, x_left, y_cent):
        '''creates and displays text on screen'''
        
        font = pygame.font.Font(self.font, self.text_size) #creates a font object
        
        text_object = font.render(self.characters, True, self.color) #creates a text surface object

        rectangle = text_object.get_rect()

        #sets coordinates of rectangle based off of left side and height center
        rectangle.left = x_left
        rectangle.centery = y_cent

        self.screen.blit(text_object, rectangle)


    def right_return_rectangle(self,x_right,y_cent):
        '''returns rectangle based on right,center coordinates'''
        font = pygame.font.Font(self.font, self.text_size) #creates a font object
        
        text_object = font.render(self.characters, True, self.color) #creates a text surface object

        rectangle = text_object.get_rect()

        #sets coordinates of rectangle based off of left side and height center
        rectangle.right = x_right
        rectangle.centery = y_cent

        return rectangle

    def left_return_rectangle(self,x_left,y_cent):
        '''returns rectangle based on left,center coordinates'''
        font = pygame.font.Font(self.font, self.text_size) #creates a font object
        
        text_object = font.render(self.characters, True, self.color) #creates a text surface object

        rectangle = text_object.get_rect()

        #sets coordinates of rectangle based off of left side and height center
        rectangle.left = x_left
        rectangle.centery = y_cent

        return rectangle

    
        

class ai:
    def __init__(self, y_num_rect, x_num_rect, player1_move, ai_player = 0, level = "easy"):
        '''initializes object in ai class'''
        self.ai_player = ai_player #Who the ai is playing (0:none(pvp),1:ai plaing infected player, 2:ai playing noninfected player)
        self.level = level #Level of ai (easy, medium, hard)
        self.y_num_rect = y_num_rect
        self.x_num_rect = x_num_rect
        self.player1_move = player1_move
        
    def player1_easy(self, board, move_count):
        '''Picks a random move from an array of valid moves'''
        if move_count == 1: #If it is the first move, ai takes move in center
            column = round(self.x_num_rect / 2)
            row = round(self.y_num_rect/2)
            return column, row
    
       #initializes move array
        move_array = board.valid_move_array(1, move_count, self.player1_move)
        
        valid_move_number = 0 #Initializes value containing number of valid moves

        for row in move_array:# Sums all valid moves in move_array
            valid_move_number = valid_move_number + row.count(1)
        
        random_index = randint(1,valid_move_number) #gets random move number
        
        current_index = 0 #initializes current index to count valid move positions

        #iterates through valid moves while increasing the corresponding index until the index is equal to the random index
        for row in range(1, self.y_num_rect + 1): 
            for column in range(1, self.x_num_rect + 1):
                if move_array[row][column] == 1: #if move is valid
                    current_index += 1 #increase current number
                    if current_index == random_index: #if this matches with the random number generator
                        return(column, row) #return the row and column of the chosen number 

    def player2_easy(self, board, move_count):
        '''Picks a random move from an array of valid moves'''
        if move_count == self.player1_move + 1: #On the noninfected player's first move, picks a random rectangle adjacent to a infected square
            return self.player1_easy(board, 2) 
       
       #initializes move array
        move_array = board.valid_move_array(2, move_count, self.player1_move)
        
        valid_move_number = 0 #Initializes value containing number of valid moves

        for row in move_array:# Sums all valid moves in move_array
            valid_move_number = valid_move_number + row.count(1)
        
        random_index = randint(1, valid_move_number) #gets random move number
        
        current_index = 0 #initializes current index to count valid move positions

        #iterates through valid moves while increasing the corresponding index until the index is equal to the random index
        for row in range(1, self.y_num_rect + 1): 
            for column in range(1, self.x_num_rect + 1):
                if move_array[row][column] == 1: #if move is valid
                    current_index += 1 #increase current number
                    if current_index == random_index: #if this matches with the random number generator
                        return(column, row) #return the row and column of the chosen number 

    def player1_medium(self):
        '''ranks moves based on their distance from the center and x'''

    def player2_medium(self, board, move_count):
        '''ranks moves based on their distance from the center and the nearest infected square'''
        
        move_array = board.valid_move_array(2, move_count, self.player1_move)

        rank_table = copy.deepcopy(board.board_setup)

        #Changes values of table containing the rankings of moves
        for row in range(1, self.y_num_rect + 1):#iterates through possible boxes
            for column in range(1, self.x_num_rect + 1):
                if move_array[row][column] == 1: #If it is a valid move
                    rank_table[row][column] = (((self.y_num_rect + 1)/2 - row)**2 + ((self.x_num_rect + 1)/2 - column)**2) ** 0.5 #Calculates distance to the center 
                    
                    #finds lowest distance 
                    lowest_dist = 10000 #initializes high lowest distance
                    for board_row in range(1, self.y_num_rect + 1):
                        for board_column in range(1, self.x_num_rect + 1):
                            if board.board[board_row][board_column] == 1:
                                dist_to_infected = ((row - board_row)**2 + ((column - board_column)**2)) ** 0.5
                                lowest_dist = min(lowest_dist, dist_to_infected) #compares current distance and previous distance
                    rank_table[row][column] = rank_table[row][column] + 1000*lowest_dist #adds lowest distance(weighted higher) to rank_table box
        
        #Finds lowest move
        lowest_ranking = 100000 #Initializes high lowest ranking
        for row in range(1, self.y_num_rect + 1):
            for column in range(1, self.x_num_rect + 1):
                if move_array[row][column] == 1:
                    if rank_table[row][column] < lowest_ranking:
                        best_move = (column, row)
                        lowest_ranking = rank_table[row][column]
        return best_move
                    
    def player2_hard(self):
        print("Hello")
    def player2_hard(self):
        print("Yup")
    def make_move(self, board, move_count):
        '''changes board'''
        if self.level == "easy":
            if self.ai_player == 1:
                boxx , boxy = self.player1_easy(board, move_count)
            else:
                boxx, boxy = self.player2_easy(board, move_count)
        elif self.level == "medium":
            if self.ai_player == 1:
                boxx, boxy = self.player1_medium(board, move_count)
            else:
                boxx, boxy = self.player2_medium(board, move_count)

        else: #if ai level = "hard"
            if self.ai_player == 1:
                self.player1_hard(board, move_count)
            else:
                self.player2_hard(board, move_count)
        board.change_rect_status(self.ai_player, boxx, boxy) #change the status of the chosen box in the board