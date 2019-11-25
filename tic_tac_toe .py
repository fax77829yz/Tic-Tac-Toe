import random
import time
import pygame
import sys,os

WHITE = (255,255,255)
BLACK = (0,0,0)
GRAY = (105, 105, 105)
DIMGRAY = (54, 54, 54)

def who_goes_first():
    # Randomly choose which player goes first.
    if random.randint(0, 1) == 0:
        return 'player'
    else:
        return 'computer'


def is_winner(bd, lt):
    # Given a board and a player's letter, this function returns True if
    #  that player has won.
    # We use "bd" instead of "board" and "lt" instead of "letter" so we
    # don't have to type as much.
    return ((bd[7] == lt and bd[8] == lt and bd[9] == lt) or 
            (bd[4] == lt and bd[5] == lt and bd[6] == lt) or 
            (bd[1] == lt and bd[2] == lt and bd[3] == lt) or 
            (bd[7] == lt and bd[4] == lt and bd[1] == lt) or 
            (bd[8] == lt and bd[5] == lt and bd[2] == lt) or 
            (bd[9] == lt and bd[6] == lt and bd[3] == lt) or 
            (bd[7] == lt and bd[5] == lt and bd[3] == lt) or 
            (bd[9] == lt and bd[5] == lt and bd[1] == lt)) 

def is_space_free(board, move):
    return board[move] == ' '

def is_board_full(board):
    # Return True if every space on the board has been taken. Otherwise,
    # return False.
    for i in range(1, 10):
        if is_space_free(board, i):
            return False
    return True

def get_player_move(board):
    # Let the player enter their move.
    move = ' '
    while move not in ['1', '2', '3', '4', '5', '6', '7', '8', '9'] or \
    not is_space_free(board, int(move)):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                pos = pygame.mouse.get_pos()
                if ( 20 < pos[0] and pos[0] < 170 ) :
                    if ( 90 < pos[1] and pos[1] < 240 ) :
                        move = '7'
                    elif ( 270 < pos[1] and pos[1] < 420 ) :
                        move = '4'
                    elif ( 450 < pos[1] and pos[1] < 600 ) :
                        move = '1'
                elif ( 200 < pos[0] and pos[0] < 350 ) :
                    if ( 90 < pos[1] and pos[1] < 240 ) :
                        move = '8'
                    elif ( 270 < pos[1] and pos[1] < 420 ) :
                        move = '5'
                    elif ( 450 < pos[1] and pos[1] < 600 ) :
                        move = '2'
                elif ( 380 < pos[0] and pos[0] < 530 ) :
                    if ( 90 < pos[1] and pos[1] < 240 ) :
                        move = '9'
                    elif ( 270 < pos[1] and pos[1] < 420 ) :
                        move = '6'
                    elif ( 450 < pos[1] and pos[1] < 600 ) :
                        move = '3'
    return int(move)

def make_move(board, letter, move):
    board[move] = letter

def random_choose(board):
    """Returns a valid move from the passed list on the passed board.
    Returns None if there is no valid move."""
    print('computer is thinking...')
    time.sleep(0.5)
    
    possible_moves = []
    # TODO: check valid locations and randomly pick one.
    for i in range(1,10) :
        if is_space_free(board, i) :
            possible_moves.append(i)

    return possible_moves[random.randint(0,len(possible_moves)-1)]

def find_winning_move(board, computer_letter):
    """For every possible move, check if it can win with that move."""
    for i in range(len(board)):
        boardcopy = board.copy()
        if is_space_free(boardcopy, i):
            make_move(boardcopy, computer_letter, i)
            if is_winner(boardcopy, computer_letter):
                return i
    return None

def block_player_move(board, player_letter):
    """try to block a player's move"""
    return find_winning_move(board, player_letter)

def choose_corner(board):
    """choose a corner move if possible"""
    if is_space_free(board, 1) : return 1
    elif is_space_free(board, 3) : return 3
    elif is_space_free(board, 7) : return 7
    elif is_space_free(board, 9) : return 9
    return None

def choose_center(board):
    """choose the center if possible"""
    if is_space_free(board, 5) : return 5
    return None
    
def choose_side(board):
    """choose side positions if possible"""
    if is_space_free(board, 2) : return 2
    elif is_space_free(board, 4) : return 4
    elif is_space_free(board, 6) : return 6
    elif is_space_free(board, 8) : return 8
    return None

def get_computer_move(board, computer_letter, player_letter):
    move = find_winning_move(board, computer_letter)
    if move != None: return move
    move = block_player_move(board, player_letter)
    if move != None: return move
    move = choose_corner(board)
    if move != None: return move
    move = choose_center(board)
    if move != None: return move
    return choose_side(board)

def display_message(msg):
    textSurfaceObj = fontObj.render(msg, True, (255,255,255), GRAY)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (x_range//2, upper_size//2)
    base_surf.blit(textSurfaceObj, textRectObj)
        
def draw_board(bd):
    x = border
    base_surf.fill(GRAY)
    pygame.draw.rect(base_surf, DIMGRAY, (0,upper_size,border,y_range-upper_size))
    while x < x_range :
        y = upper_size
        while y < y_range :
            pygame.draw.rect(base_surf, DIMGRAY, (x,y,size,size))
            y += size + line_width
        
        if x + size + line_width > x_range :
            pygame.draw.rect(base_surf, DIMGRAY, (x+size,upper_size,border,y_range-upper_size))
        x += size + line_width
    
    for i in range(1,10) :
        if bd[i] is 'X':
            base_surf.blit(pygame.transform.scale(X_img, (150, 150)),(cal_pos('x', i),(cal_pos('y', i))))
        elif bd[i] is 'O':
            base_surf.blit(pygame.transform.scale(O_img, (150, 150)),(cal_pos('x', i),(cal_pos('y', i))))

def cal_pos(d, num) :
    if d is 'x' :
        if num%3 is 1 : return 20
        elif num%3 is 2 : return 200
        else : return 380
    elif d is 'y' :
        if num <= 3: return 450
        elif num >= 7: return 90
        else : return 270

def tic_tac_toe() :
    is_playing = True
    board = [' '] * 10 
    turn = who_goes_first()
    while is_playing:  
        draw_board(board)      
        display_message('it\'s '+turn+'\'s turn.') 
        pygame.display.update()   
        if turn == 'player':
            move = get_player_move(board)
            make_move(board, player_letter, move)

            if is_winner(board, player_letter):
                draw_board(board)
                display_message('win')
                is_playing = False
                
            elif is_board_full(board):
                draw_board(board)
                display_message('draw')
                break
            
            else:
                turn = 'computer'
        else:
            time.sleep(1)
            # move = random_choose(board)
            move = get_computer_move(board, computer_letter, player_letter)
            make_move(board, computer_letter, move)
            
            if is_winner(board, computer_letter):
                draw_board(board)
                display_message('lose')
                is_playing = False
                
            elif is_board_full(board):
                draw_board(board)
                display_message('draw')
                break
            
            else:
                turn = 'player'

def draw_start_screen():
    base_surf.fill(DIMGRAY)
    display_message('Tic-Tac-Toe')
    textSurfaceObj = fontObj.render('Choose your symbol!', True, (255,255,255), DIMGRAY)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (x_range//2, upper_size+10)
    base_surf.blit(textSurfaceObj, textRectObj)
    nameSurfaceObj = s_fontObj.render('10527214 Heng-Chia Kuo', True, BLACK, DIMGRAY)
    nameRectObj = nameSurfaceObj.get_rect()
    nameRectObj.midbottom = (x_range//2, y_range)
    base_surf.blit(nameSurfaceObj, nameRectObj)
    return base_surf.blit(pygame.transform.scale(X_img, (200, 200)),(50,(y_range-upper_size)//2)), \
    base_surf.blit(pygame.transform.scale(O_img, (200, 200)),(300,(y_range-upper_size)//2))

pygame.init()
x_range, y_range = 550,600
size = 150
line_width = 30
border = (int(x_range-150*3-line_width*2)/2)
upper_size = y_range - x_range + border*2
fontObj = pygame.font.Font('freesansbold.ttf', 40)
s_fontObj = pygame.font.Font('freesansbold.ttf', 20)
X_img = pygame.image.load(os.path.dirname(__file__) + '/image/x.png') 
O_img = pygame.image.load(os.path.dirname(__file__) + '/image/o.png') 

is_running = True

while is_running:
    base_surf = pygame.display.set_mode((x_range,y_range))
    x_btn, o_btn = draw_start_screen()
    pygame.display.update()
    for e in pygame.event.get() :
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1: 
            choose = False
            pos = pygame.mouse.get_pos()
            if x_btn.collidepoint(pos):
                player_letter, computer_letter = 'X','O'
                choose = True
            elif o_btn.collidepoint(pos):
                player_letter, computer_letter = 'O','X'
                choose = True

            if choose: 
                tic_tac_toe()
                pygame.display.update()
                time.sleep(3)
                
                
    