import pygame
BOX_FONT_SIZE = 120
SCORE_FONT_SIZE = 30
HEIGHT,WIDTH = 600,600
LINE_WIDTH = 5
SPACE = 50

pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
boxFont = pygame.font.SysFont(None,BOX_FONT_SIZE)
scoreFont = pygame.font.SysFont(None,SCORE_FONT_SIZE)

boardChar = [None]*9
white = (255,255,255)
firstPlayer = True
charToPut = 'X'
scoreFirstPlayer = 0
scoreSecondPlayer = 0

def drawBoard():
    """
        This function draws simple board with score of both players
        Length of lines is calculated corresponding to the size of window
        Height and width of window is divided into three parts
        Lines are drawn in the first and the second part
        
    """
    screen.fill((0,0,0))
    pygame.draw.line(screen,white,((WIDTH//3) * 1,SPACE),(WIDTH//3 * 1,WIDTH - SPACE),LINE_WIDTH)
    pygame.draw.line(screen,white,((WIDTH//3) * 2,SPACE),(WIDTH//3 * 2,WIDTH - SPACE),LINE_WIDTH)
    pygame.draw.line(screen,white,(SPACE,(HEIGHT//3) * 1),(HEIGHT - SPACE,HEIGHT//3 * 1),LINE_WIDTH)
    pygame.draw.line(screen,white,(SPACE,(HEIGHT//3) * 2),(HEIGHT - SPACE,HEIGHT//3 * 2),LINE_WIDTH)
    draw_score()
    pygame.display.flip()

def displayChar(text,position):
    """
        Function returns a tuple of surface (with text rendered on it) and rectangle
        where the position of rectangle is calculated according to the
        position where the mouseclick was made
    """
    txt = boxFont.render(text,True,white)
    txtRect = txt.get_rect()
    x,y = position
    coordX,coordY = WIDTH // 3,HEIGHT // 3

    #0
    if (x < coordX and y < coordY): 
        txtRect.centerx = (SPACE+coordX)//2
        txtRect.centery = (SPACE+coordY)//2
    #1
    elif x > coordX and x < coordX*2 and y < coordY: 
        txtRect.centerx = (3*coordX)//2
        txtRect.centery = (SPACE + coordY)//2
    #2
    elif (x > coordX*2 and y < coordY): 
        txtRect.centerx = (2*coordX + WIDTH - SPACE)//2
        txtRect.centery = (SPACE + coordY)//2
    #3
    elif x < coordX and y < coordY*2 and y > coordY: 
        txtRect.centerx = (SPACE + coordX)//2
        txtRect.centery = (3*coordY)//2
    #4
    elif x > coordX and x < coordX*2 and y < coordY*2 and y > coordY: 
        txtRect.centerx = (3*coordX)//2
        txtRect.centery = (3*coordY)//2
    #5
    elif (x > coordX*2 and y > coordY and y < coordY*2): 
        txtRect.centerx = (2*coordX + WIDTH - SPACE)//2
        txtRect.centery = (3*coordX)//2
    #6
    elif (x < coordX and y > coordY*2): 
        txtRect.centerx = (SPACE + coordX)//2
        txtRect.centery = (2*coordY + WIDTH - SPACE)//2
    #7
    elif x > coordX and x < coordX*2 and y > coordY*2: 
        txtRect.centerx = (3*coordX)//2
        txtRect.centery = (2*coordY + WIDTH - SPACE)//2
    #8  
    elif (x > coordX*2 and y > coordY*2): 
        txtRect.centerx = (2*coordX + WIDTH - SPACE)//2
        txtRect.centery = (2*coordY + WIDTH - SPACE)//2
    
    return txt,txtRect

def game_loop():
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                doMove(pos)
        pygame.display.flip()

    pygame.quit()
     

def doMove(pos):
    global boardChar
    global scoreFirstPlayer
    global scoreSecondPlayer
    
    drawBox(pos)
    if check_win_firstPlayer() == 1:
        scoreFirstPlayer+=1
        reset_board()
        drawBoard()
        
    elif check_win_firstPlayer() == 0:
        scoreSecondPlayer += 1
        reset_board()
        drawBoard()
        
    elif check_win_firstPlayer() == -1:
        reset_board()
        drawBoard()
    
def drawBox(position):
    """
        Indexing of board:
        
        0 | 1 | 2
        =========
        3 | 4 | 5
        =========
        6 | 7 | 8

        Function fills the specific box with a character 'X' or 'O' 

    """
    global charToPut
    coordX = WIDTH//3
    coordY = HEIGHT//3
    x,y = position
    draw = False
    
    if x<coordX and y < coordY and isBoxFree(0):
        draw = True
        fillCharBox(0)

    elif x > coordX and x < 2*coordX and y < coordY and isBoxFree(1): 
        draw = True
        fillCharBox(1)

    elif x > coordX*2 and y < coordY and isBoxFree(2):
        draw = True
        fillCharBox(2)

    elif x < coordX and y > coordY and y < coordY*2 and isBoxFree(3):
        draw = True
        fillCharBox(3)

    elif x > coordX and x < 2*coordX and y < 2*coordY and y > coordY and isBoxFree(4):
        draw = True
        fillCharBox(4)

    elif x > 2*coordX and y > coordY and y < 2*coordY and isBoxFree(5):
        draw = True
        fillCharBox(5)

    elif x< coordX and y > coordY*2 and isBoxFree(6):
        draw = True
        fillCharBox(6)

    elif x > coordX and x < coordX*2 and y > coordY*2 and isBoxFree(7):
        draw = True
        fillCharBox(7)
        
    elif x > coordX*2 and y > coordY*2 and isBoxFree(8):
        draw = True
        fillCharBox(8)

    if draw: ## display 'X' or 'O' into corresponding box
        txt,txtrect = displayChar(charToPut,position)
        swap_char()
        swap_player()
        screen.blit(txt,txtrect)
        

def draw_score():
    draw_score_first()
    draw_score_second()

def draw_score_first():
    global scoreFirstPlayer
    score1 = scoreFont.render('Score1: ' + str(scoreFirstPlayer),True,white)
    score1_rect = score1.get_rect()
    score1_rect.centerx = 50
    score1_rect.centery = 10
    screen.blit(score1,score1_rect)

def draw_score_second():
    global scoreSecondPlayer
    score2 = scoreFont.render('Score2: ' + str(scoreSecondPlayer),True,white)
    score2_rect = score2.get_rect()
    score2_rect.centerx = WIDTH - 50
    score2_rect.centery = 10
    screen.blit(score2,score2_rect)
    
def check_win_firstPlayer():
    """Function returns 1 (True) if the first player won,
                        0 (False) if the second player won,
                        -1 in case of draw
    """
    global board
    global firstPlayer
    
    if (boardChar[0] == boardChar[1] == boardChar[2] == 'X' or
        boardChar[3] == boardChar[4] == boardChar[5] == 'X' or
        boardChar[6] == boardChar[7] == boardChar[8] == 'X' or
        boardChar[0] == boardChar[3] == boardChar[6] == 'X' or
        boardChar[1] == boardChar[4] == boardChar[7] == 'X' or
        boardChar[2] == boardChar[5] == boardChar[8] == 'X' or
        boardChar[0] == boardChar[4] == boardChar[8] == 'X' or
        boardChar[2] == boardChar[4] == boardChar[6] == 'X'):
        return not firstPlayer

    if (boardChar[0] == boardChar[1] == boardChar[2] == 'O' or ## horizontal
        boardChar[3] == boardChar[4] == boardChar[5] == 'O' or
        boardChar[6] == boardChar[7] == boardChar[8] == 'O' or
        boardChar[0] == boardChar[3] == boardChar[6] == 'O' or ## vertical
        boardChar[1] == boardChar[4] == boardChar[7] == 'O' or
        boardChar[2] == boardChar[5] == boardChar[8] == 'O' or
        boardChar[0] == boardChar[4] == boardChar[8] == 'O' or ## diagonal
        boardChar[2] == boardChar[4] == boardChar[6] == 'O'):
        return not firstPlayer
    
    if (board_free_places() == 0): # draw
        return -1

def isBoxFree(x):
    global boardChar
    return (boardChar[x] is  None)

def fillCharBox(x):
    global boardChar
    global firstPlayer
    
    if firstPlayer:
        boardChar[x] = 'X'
    else:
        boardChar[x] = 'O'

def swap_char():
    global charToPut
    if charToPut == 'X':
        charToPut = 'O'
    else:
        charToPut = 'X'

def swap_player():
    global firstPlayer
    firstPlayer = not firstPlayer

def board_free_places():
    global boardChar
    return len(boardChar) - boardChar.count('X') - boardChar.count('O')

def reset_board():
    global boardChar
    boardChar = [None] * 9

def main():
    drawBoard()
    game_loop()


if __name__ == "__main__":
    main()
