# Tank Wars Code Challenge

Welcome to the Tank Wars Game project! This game is an exciting, fast-paced battle where players maneuver up to four tanks in a strategic environment, aiming to outwit and outlast their opponents. The game is developed in Python, utilizing the Pygame library for rendering and game logic.

## Getting Started
- Clone repository
- Install python version 3
  - Make sure to let installer indlude pip and add python to PATH
- pip install pygame
- Run "python tankwars_game_server.py"

# Objectives
Your team must build a Tank Operator BOT that can play the Tank Wars Game - and win glory for you!

For the Tank wars code challenge, you will have to implement the "my_tank_operator.py" file.

You can play Tank Wars in two ways:
- Locally, to test your tank operator bot as you develop it, or against others (or human players) for fun.
- On the game server - where the finals will take place.

### To start the game locally:
- Edit **server_settings.py** : Optionally change server settings such as which bots to play against.
> python tankwars_game_server.py

### To connect to a game server on LAN:
- Add ip of server and port to **client_settings.py** (and specify which operator to use)
> python tankwars_game_client.py

### To develop your tank operator
- In **my_tank_operator.py** file: Implement the *get_tank_action* function: A function that is called in real time with the current game state - and returns the actions your tank bot will take. You will have to implement logic that continuously evaluates the other tanks positions etc. and shots being fired, and decide what to do. Also implement the *get_operator_name* function: give your operator bot a name.
- What you need to know:
  - Look in the **tank_operator.py** - this has all the classes you need to know for the game interface GameState->(your code in get_tank_action)->OperatorActions
  - The GameState objects have 2D vectors called Vec. The Vec class is implemented in **src/vec.py**. It has a lot of nice vector functionality - check it out.
  - You shouldn't need to look in any other game files.

## Enjoy!


