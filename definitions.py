import numpy as np, pygame
from pygame_settings import Settings

def binary_one_dimension(input_row, rule: int):
    '''Returns the next iteration of input_row. Rules according to wolfram code'''

    rule = "00000000" + bin(rule)[2:] #Converts rule to a string of 1s and 0s , takes away the 0b at the beginning and adds buffer 0s
    
    new_row = np.copy(input_row)

    for index in range(1, input_row.size - 1):
        num = ""
        for x in [-1,0,1]: #looks at neighbors above and constructs a binary number corresponding to case
            num += str(input_row[index + x])
        num = int(num,base = 2) #converts num to decimal

        new_row[index] = rule[-(num+1)] #Sets to the rule from the right
    return new_row

if __name__ == "__main__":
    width = 63
    height = (width+1)//2
    buffer = height -1 #A height-1 buffer is required to simulate an infinite grid.
    rule = int(input("\nWhich wolfram code would you like to see?\n(Please input an integer between 0 and 255): ").strip())
    
    #initializes first row and array
    first_row = np.zeros((width + 2*buffer), dtype=int) 
    first_row[int((width + 1)/2)-1 + buffer] = 1 # sets center of first row to 1
    arr = np.zeros((height, width + 2*buffer), dtype=int)
    arr[0] = first_row

    for index in range(1, height):
        arr[index] = binary_one_dimension(arr[index-1], rule)

    arr = arr[:,buffer: width + buffer] #removes the buffer regions from array

    #Draws arr with pygame
    settings = Settings(width, height) #initializes settings

    pygame.init()
    screen = pygame.display.set_mode((settings.window_width, settings.window_height))
    pygame.display.set_caption("Maze")

    settings.draw_board(arr, screen)
    pygame.display.flip()

    running = True
    while running: #waits for exit
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                pygame.quit()
                running = False