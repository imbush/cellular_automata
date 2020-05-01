#Turn based surround game
#created by Inle Bush

import pygame, sys, copy, time
from pygame.locals import *
from random import randint
from definitions import *


def main():
    pygame.init()

    while True:
        settings = Settings() #initializes settings

        #Initializes variables
        mousex = 0
        mousey = 0 
        game_running = True

        screen = pygame.display.set_mode((settings.window_width, settings.window_height))
        pygame.display.set_caption("Infected Escape")
        
        game_board = game_array(settings.x_num_rect, settings.y_num_rect) #make initial game board

        game_ai = ai(settings.y_num_rect, settings.x_num_rect, settings.player1_move, 0, "medium")#initiaizes game ai
        player = 1
        move_count = 1

        display_board = game_board.return_board()
        settings.draw_board(display_board, screen)
        pygame.display.flip()

        #creates moves left and score objects with text class
        moves_left_text = text("Moves Left:  " + str(settings.player1_move), settings.default_font_size, settings.red, screen)
        score_text = text("Infected Player Score:  0", settings.default_font_size, settings.dark_blue, screen)

        #calls text rectangle to test whether they collide
        moves_left_text_rectangle = moves_left_text.left_return_rectangle(settings.margin_width, settings.top_margin_height / 2)
        score_text_rectangle = score_text.right_return_rectangle(settings.window_width - settings.margin_width, settings.top_margin_height / 2)
        
        #While the two score board rectangles collide, resize
        if pygame.Rect.colliderect(moves_left_text_rectangle, score_text_rectangle):
            while pygame.Rect.colliderect(moves_left_text_rectangle, score_text_rectangle):
                # reduces size to fit
                moves_left_text.text_size -= 1
                score_text.text_size -= 1

                # resets variables
                moves_left_text_rectangle = moves_left_text.left_return_rectangle(settings.margin_width, settings.top_margin_height / 2)
                score_text_rectangle = score_text.right_return_rectangle(settings.window_width - settings.margin_width, settings.top_margin_height / 2)
        
            
            # decreases both text sizes by the ratio of the side margins to the game board (intended to add a little gap)
            moves_left_text.text_size -= round(moves_left_text.text_size * (2 * settings.margin_width)/settings.window_width)
            score_text.text_size -= round(score_text.text_size * (2 * settings.margin_width)/settings.window_width)

        

        #Main Loop
        while game_running:
            mouse_clicked =  False

            #sets score for score counter
            score = game_board.count_score(1)
                
            #determines which player's move it is 
            if (move_count - 1) % (settings.player1_move + settings.player2_move) <= (settings.player1_move-1):
                player = 1
                moves_left_text.color = settings.red
            else:
                player = 2
                moves_left_text.color = settings.blue

            #determines the moves left for each player
            if player == 1:
                moves_left = settings.player1_move - (move_count - 1)%(settings.player1_move + settings.player2_move)
            else:
                moves_left = (settings.player1_move + settings.player2_move) - (move_count - 1) % (settings.player1_move + settings.player2_move)
            
            if player != game_ai.ai_player: #Only looks for mouse clicks when it is the players turn
                #runs through events
                for event in pygame.event.get(): 
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                    elif event.type == MOUSEBUTTONUP:
                        mousex, mousey = event.pos
                        mouse_clicked = True

                if mouse_clicked:
                    boxx, boxy = settings.get_box_at_pixel(mousex, mousey)
                    if boxx != None and boxy != None: #checks if click was in a rectangle
                        if game_board.check_move_valid(player, boxx, boxy, move_count,settings.player1_move):
                            game_board.change_rect_status(player, boxx, boxy)
                            move_count += 1 #increases move counts
                            
                            game_running, score = game_board.running_check()#checks game running

            else:
                time.sleep(0.2) #waits while ai makes move
                game_ai.make_move(game_board, move_count) #ai makes move
                move_count += 1 #increases move count
                game_running, score = game_board.running_check()#checks game running

            #switches player at end of turn

            if player == 1: 
                player = 2
            else:
                player = 1


            display_board = game_board.return_board()
            settings.draw_board(display_board, screen)

            moves_left_text.characters = "Moves Left:  " + str(moves_left)
            score_text.characters = "Infected Player Score:  " + str(score)

            #displays score text in the center of the top margin and in the 
            score_text.right_display_rectangle(settings.window_width - settings.margin_width, settings.top_margin_height/2)

            #displays moves left test in the center of the top margin and in the left fifth of 
            moves_left_text.left_display_rectangle(settings.margin_width, settings.top_margin_height / 2)

            pygame.display.flip() 

        print("game has ended. The infected player expanded to ", score, " squares.")

        #creates restart button
        restart_game = text("Restart Game", score_text.text_size, settings.dark_blue, screen)
        
        #creates display
        display_board = game_board.return_board()
        settings.draw_board(display_board, screen)

        #creates text boxes at top
        score_text.right_display_rectangle(settings.window_width - settings.margin_width, settings.top_margin_height/2)
        restart_game.left_display_rectangle(settings.margin_width, settings.top_margin_height / 2)
        pygame.display.flip() 

        restart_game_rectangle = restart_game.left_return_rectangle(settings.margin_width, settings.top_margin_height / 2)

        while not game_running: #Lets window run until player closes
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == MOUSEBUTTONUP:
                    mousex, mousey = event.pos
                    mouse_clicked = True
            if restart_game_rectangle.collidepoint(mousex, mousey):
                game_running = True

if __name__ == "__main__":
    main()