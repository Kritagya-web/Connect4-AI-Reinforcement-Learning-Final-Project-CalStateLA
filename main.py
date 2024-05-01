import numpy as np
import pygame
from pygame import mixer
import  pymunk
import sys
import random
from Board import Board
from button import Button
from assets import (black_coin, disc_drop_1, disc_drop_2, event_sound,
                    red_coin, yellow_coin, winning_sound)
pygame.init()
RADIUS = 49
inf = float('inf')

BG = pygame.image.load("assets/Background.jpg")
pygame.mixer.init()
win_sound = pygame.mixer.Sound("./sounds/cheering-crowd.wav")
def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)

def isValidInput(col,board):
    if col >=0 and col <= 6:
        if board[0][col] == 0:
            return True
        else:
            return False
    else:
        return False

def AI(board,difficulty):
    boards,inputs = board.generateChildren(2)
    scores = []
    for b in boards:
        scores.append(minimax(0,b,False,-inf,inf,difficulty))
    board.playerInput(2,inputs[scores.index(max(scores))])
    print(inputs[scores.index(max(scores))])
    return (inputs[scores.index(max(scores))]*100 + 50,50)

def minimax(depth,board,isMaximizing,alpha,beta,h):

    if depth == h:
        return board.getScore(2,1)

    if isMaximizing:
        p = 2
    else:
        p = 1
    boardss, inputss = board.generateChildren(p)
    if isMaximizing:
        maxEval = -inf
        for b in boardss:
            eval = (minimax(depth + 1, b, False,alpha,beta, h))
            maxEval = max(maxEval,eval)
            alpha = max(alpha,eval)
            if beta <= alpha:
                break
        return maxEval
    else:
        minEval = inf
        for b in boardss:
            eval = (minimax(depth + 1, b, True,alpha,beta, h))
            minEval = min(minEval,eval)
            beta = min(beta,eval)
            if beta <= alpha:
                break
        return minEval

def minimaxb(depth,board,isMaximizing,h):
    if depth == h:
        return board.getScore(2, 1)

    if isMaximizing:
        p = 2
    else:
        p = 1
    boardss, inputss = board.generateChildren(p)
    scoress = []
    if isMaximizing:
        for b in boardss:
            scoress.append(minimaxb(depth + 1, b, False, h))
        return max(scoress)
    else:
        for b in boardss:
            scoress.append(minimaxb(depth + 1, b, True, h))
        return min(scoress)

board = Board(np.zeros((6,7)))


def createPiece(space,pos,colour):
    body = pymunk.Body(0.01,10,body_type=pymunk.Body.DYNAMIC)
    body.position = pos
    shape = pymunk.Circle(body,RADIUS)
    space.add(body,shape)
    return shape , colour

def removePieces(space,pieces):
    for piece in pieces:
        space.remove(piece[0])


def drawPieces(pieces):
    for p in pieces:
        x = int(p[0].body.position.x)
        y = int(p[0].body.position.y)
        pygame.draw.circle(window,p[1],(x,y),p[0].radius)


def createFloor(space):
    body = pymunk.Body(body_type= pymunk.Body.STATIC)
    body.position = (350,750)
    shape = pymunk.Poly.create_box(body,size = (700,10))
    space.add(body,shape)
    return shape


def createWall(space,pos):
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.position = (n*100,450)
        shape = pymunk.Poly.create_box(body, (1, 600))
        space.add(body,shape)
        return shape


window = pygame.display.set_mode((700,750))
space = pymunk.Space()
space.gravity = (0,500)
f=createFloor(space)


boardImg = pygame.image.load("board.png").convert_alpha()

for n in range(8):
 createWall(space,(n*100,450))

clock = pygame.time.Clock()
ai = False

def gameVsAi(difficulty):
    # Boolean variable to track if the win sound has been played
    win_sound_played = False
    pieces = []
    p1W = False
    aiW = False
    board = Board(np.zeros((6, 7)))
    turn = 0
    colour = "red"
    gameOver = False
    while True:

            window.fill("Black")
            drawPieces(pieces)
            window.blit(boardImg, (0, 145))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    mixer.music.load(event_sound)
                    mixer.music.play(0)
                    sys.exit()
                elif event.type == pygame.KEYDOWN and gameOver:
                    if event.key == pygame.K_RETURN:
                        removePieces(space,pieces)

                        MainMenu()
                elif event.type == pygame.MOUSEBUTTONDOWN and not gameOver:
                    if turn % 2 == 0:
                        colour = "red"
                        pos = pygame.mouse.get_pos()
                        newPos = pos
                        if pos[0] % 100 == 0:
                            randomArr = [-1, 1]
                            newPos = (pos[0] + random.choice(randomArr), pos[1])
                        mixer.music.load(disc_drop_2)
                        mixer.music.play(0)
                        pieces.append(createPiece(space, newPos, colour))
                        board.playerInput(1, int(newPos[0] / 100))
                        colour = "yellow"

                    else:
                        colour = "yellow"
                        newPos = AI(board,difficulty)
                        mixer.music.load(disc_drop_1)
                        mixer.music.play(0)
                        pieces.append(createPiece(space, newPos, colour))
                        board.print()

                        colour = "red"

                    turn += 1

            DRAW_TEXT = get_font(50).render("Draw", True, "blue")
            DRAW_TEXT_RECT = DRAW_TEXT.get_rect(center=(360, 50))
            if board.checkWin(1):
                p1W = True
                gameOver = True
                if not win_sound_played:
                    win_sound.play(maxtime=30000)  # Play for 30,000 milliseconds (30 seconds)
                    win_sound_played = True

            elif board.checkWin(2):
                aiW = True
                gameOver = True
                if not win_sound_played:
                    win_sound.play(maxtime=30000)  # Play for 30,000 milliseconds (30 seconds)
                    win_sound_played = True

            elif turn > 42 and not gameOver:
                gameOver = True
                mixer.music.load(event_sound)
                mixer.music.play(0)
                window.blit(DRAW_TEXT,DRAW_TEXT_RECT)
                window.blit(GO_BACK_TEXT, GO_BACK_TEXT_RECT)

            GO_BACK_TEXT = get_font(25).render("Press Enter to go back", True, "white")
            GO_BACK_TEXT_RECT = GO_BACK_TEXT.get_rect(center=(360, 120))

            P1_TEXT = get_font(50).render("You Won!!", True, "red")
            P1_RECT = P1_TEXT.get_rect(center=(360, 50))
            if p1W == True:

                window.blit(P1_TEXT, P1_RECT)
                window.blit(GO_BACK_TEXT,GO_BACK_TEXT_RECT)


            P2_TEXT = get_font(50).render("Ai Won !!", True, "yellow")
            P2_RECT = P2_TEXT.get_rect(center=(360, 50))
            if aiW == True:
                window.blit(P2_TEXT, P2_RECT)
                window.blit(GO_BACK_TEXT,GO_BACK_TEXT_RECT)
            if pygame.mouse.get_pos()[1]<= 100 and turn%2 == 0 and not gameOver:
                pygame.draw.circle(window,colour,pygame.mouse.get_pos(),RADIUS)
            elif turn % 2 == 0 and not gameOver :
                pygame.draw.circle(surface=window,color=colour,center=(pygame.mouse.get_pos()[0],100),radius=RADIUS)




            pygame.display.update()
            space.step(1 / 50)
            clock.tick(60)

def gameVsP2():
    pieces = []
    p1W = False
    p2W = False
    win_sound_played = False
    board = Board(np.zeros((6,7)))
    turn = 0
    colour = "red"
    gameOver = False
    while True:
        window.fill("Black")
        drawPieces(pieces)
        window.blit(boardImg, (0, 145))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN and gameOver:
                if event.key == pygame.K_RETURN:
                    removePieces(space,pieces)
                    MainMenu()
            elif event.type == pygame.MOUSEBUTTONDOWN and not gameOver:
                if turn % 2 == 0:
                    colour = "red"
                    pos = pygame.mouse.get_pos()
                    newPos = pos
                    if pos[0] % 100 == 0:
                        randomArr = [-1, 1]
                        newPos = (pos[0] + random.choice(randomArr), pos[1])
                    mixer.music.load(disc_drop_2)
                    mixer.music.play(0)
                    pieces.append(createPiece(space, newPos, colour))
                    board.playerInput(1, int(newPos[0] / 100))
                    colour = "yellow"
                elif not gameOver:
                    colour = "yellow"
                    pos = pygame.mouse.get_pos()
                    newPos = pos
                    if pos[0] % 100 == 0:
                        randomArr = [-1, 1]
                        newPos = (pos[0] + random.choice(randomArr), pos[1])
                    mixer.music.load(disc_drop_1)
                    mixer.music.play(0)
                    pieces.append(createPiece(space, newPos, colour))
                    board.playerInput(2, int(newPos[0] / 100))
                    colour = "red"

                turn += 1
        DRAW_TEXT = get_font(50).render("DRAW", True, "blue")
        DRAW_TEXT_RECT = DRAW_TEXT.get_rect(center=(360, 50))
        if board.checkWin(1):
            p1W = True
            gameOver = True
            if not win_sound_played:
                win_sound.play(maxtime=30000)  # Play for 30,000 milliseconds (30 seconds)
                win_sound_played = True


        elif board.checkWin(2):
            p2W = True
            gameOver = True
            if not win_sound_played:
                win_sound.play(maxtime=30000)  # Play for 30,000 milliseconds (30 seconds)
                win_sound_played = True

        elif turn > 42 and not gameOver:
            gameOver = True
            mixer.music.load(event_sound)
            mixer.music.play(0)
            window.blit(DRAW_TEXT, DRAW_TEXT_RECT)
            window.blit(GO_BACK_TEXT, GO_BACK_TEXT_RECT)

        GO_BACK_TEXT = get_font(25).render("press Enter to go back", True, "white")
        GO_BACK_TEXT_RECT = GO_BACK_TEXT.get_rect(center=(360, 120))

        P1_TEXT = get_font(50).render("Player 1 Won!!", True, "red")
        P1_RECT = P1_TEXT.get_rect(center=(360, 50))

        if p1W == True:
            window.blit(P1_TEXT, P1_RECT)
            window.blit(GO_BACK_TEXT,GO_BACK_TEXT_RECT)
        P2_TEXT = get_font(50).render("Player 2 Won!!", True, "yellow")
        P2_RECT = P2_TEXT.get_rect(center=(360, 50))
        if p2W == True:
            window.blit(P2_TEXT, P2_RECT)
            window.blit(GO_BACK_TEXT, GO_BACK_TEXT_RECT)

        if pygame.mouse.get_pos()[1] <= 100 and not gameOver:
            pygame.draw.circle(window, colour, pygame.mouse.get_pos(), RADIUS)
        elif not gameOver:
            pygame.draw.circle(surface=window, color=colour, center=(pygame.mouse.get_pos()[0], 100), radius=RADIUS)



        pygame.display.update()
        space.step(1 / 50)
        clock.tick(60)

def MainMenu():
    while True:
        window.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(60).render("CONNECT 4", True, "white")
        MENU_RECT = MENU_TEXT.get_rect(center=(350, 100))

        INFO_TEXT = get_font(14).render("Play against a friend or AI. Have fun and Enjoy", True, "red")
        INFO_RECT = INFO_TEXT.get_rect(center=(350, 180))

        INFO_TEXT_2 = get_font(14).render("Play against a friend or AI. Have fun and Enjoy", True, "red")
        INFO_RECT_2 = INFO_TEXT.get_rect(center=(350, 180))


        INFO_TEXT_COMMENT = get_font(13).render("Made for AI Final Project By Group 6", True, "green")
        INFO_COMMENT_RECT = INFO_TEXT_COMMENT.get_rect(center=(350, 230))

        CREATED_BY_TEXT = get_font(22).render("Created by KRITAGYA KUMRA", True, "yellow")
        CREATED_BY_RECT = CREATED_BY_TEXT.get_rect(center=(350, 280))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(350, 400),
                             text_input="PLAY", font=get_font(50), base_color="white", hovering_color="green")
        #OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(350, 400),
                                #text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(350, 600),
                             text_input="QUIT", font=get_font(50), base_color="white", hovering_color="green")

        window.blit(MENU_TEXT, MENU_RECT)
        window.blit(CREATED_BY_TEXT, CREATED_BY_RECT)
        window.blit(INFO_TEXT, INFO_RECT)
        window.blit(INFO_TEXT_COMMENT, INFO_COMMENT_RECT)

        for button in [PLAY_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(window)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    playMenu()
                #if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    #options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

def playMenu():
    while True:
        window.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(40).render("Choose game mode", True, "white")
        MENU_RECT = MENU_TEXT.get_rect(center=(350, 100))
        vsPlayer = Button(image=pygame.image.load("assets/Play Rect2.png"), pos=(350, 300),
                             text_input="Player vs Player", font=get_font(30), base_color="white", hovering_color="green")
        vsAi = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(350, 500),
                          text_input="Player vs Ai", font=get_font(30), base_color="white", hovering_color="green")
        window.blit(MENU_TEXT, MENU_RECT)

        for button in [vsPlayer, vsAi]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(window)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if vsPlayer.checkForInput(MENU_MOUSE_POS):
                    gameVsP2()
                # if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                # options()
                if vsAi.checkForInput(MENU_MOUSE_POS):
                    difficultyMenu()
        pygame.display.update()

def difficultyMenu():
    while True:
        window.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()
        MENU_TEXT = get_font(40).render("Choose Difficulty", True, "white")
        MENU_RECT = MENU_TEXT.get_rect(center=(350, 100))
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        Note_TEXT = get_font(10).render("For Very hard and Impossible the AI will need more time to think", True, "white")
        Note_RECT = MENU_TEXT.get_rect(center=(370, 730))
        Easy = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(350, 200),
                             text_input="Easy", font=get_font(30), base_color="white", hovering_color="green")
        Normal = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(350, 300),
                          text_input="Normal", font=get_font(30), base_color="white", hovering_color="green")
        Hard = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(350, 400),
                      text_input="Hard", font=get_font(30), base_color="white", hovering_color="green")
        VeryHard = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(350, 500),
                      text_input="Very Hard", font=get_font(30), base_color="white", hovering_color="green")
        Impossible = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(350, 600),
                      text_input="Impossible", font=get_font(30), base_color="white", hovering_color="green")
        window.blit(MENU_TEXT, MENU_RECT)
        window.blit(Note_TEXT,Note_RECT)

        for button in [Easy,Normal,Hard,VeryHard,Impossible]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(window)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if Easy.checkForInput(MENU_MOUSE_POS):
                    gameVsAi(0)
                elif Normal.checkForInput(MENU_MOUSE_POS):
                    gameVsAi(1)
                elif Hard.checkForInput(MENU_MOUSE_POS):
                    gameVsAi(3)
                elif VeryHard.checkForInput(MENU_MOUSE_POS):
                    gameVsAi(4)
                elif Impossible.checkForInput(MENU_MOUSE_POS):
                    gameVsAi(7)

        pygame.display.update()

MainMenu()










