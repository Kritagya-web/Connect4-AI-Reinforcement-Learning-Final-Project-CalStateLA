![logooo](https://user-images.githubusercontent.com/102327565/191298260-2b52c59b-e5f4-49a1-bcdd-dad0bcac1b17.png)


<hr>



My first pygame project, a connect4 game where  you can either play against a friend or an AI with several 
difficulties to choose from.
<br>

## Libraries needed:
  * Pygame.
  * Pymunk.
  * Numpy.

## Game Features:
  * Play against an AI or a friend on the same computer.
    - May work on an online multiplayer feature.
  * Physics of both the pieces and board was implemnted using the Pymunk Library.
  
![gameModes](https://user-images.githubusercontent.com/102327565/191301924-1130bbcc-8f02-4d1f-8d0b-cc280817d29a.png)
 
https://user-images.githubusercontent.com/102327565/191302924-cd188326-8dee-4e1b-bd60-1a6bfbba0c78.mp4



## The AI:
  * Currently there are 5 difficulties to choose from.
    - Even easy difficulty is not that easy.
  * All difficulties use the Minimax algorithm in order for the AI to choose the best move.
  * Difficulties differ in how may moves the AI will foresee from the current Connect4 board.
  * Alpha-Beta pruning was also used to eliminate Unreasonable paths for the AI to look into, thus reducing its computation time by a huge factor.
  * Still the Very hard and Impossible difficulties take the AI a couple of seconds, as a matter of fact I am working on more optimizations for the minimax algorithm.
 
![difficulties](https://user-images.githubusercontent.com/102327565/191300734-68613dad-99c2-4b36-a49f-9f4fcae3a0e5.png)

![AiWon](https://user-images.githubusercontent.com/102327565/191300814-7b16b4f3-2c32-4fe9-807e-305595c87cd0.png)


# Tasks 
- [ ] Add more optimizations to the Minimax algorithm.
- [ ] Online multiplayer.
- [ ] Add more gameplay options [Choose colour of piece etc.. ].


