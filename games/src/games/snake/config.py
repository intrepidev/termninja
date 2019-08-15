from src.core import cursor

WELCOME_MESSAGE = fr"""{cursor.CLEAR}
{cursor.GREEN}
                /^\/^ \
              _|__|  O| \
      \/     /~     \_/  \
      \____|__________/   \
              \_______      \
                      `\     \                  \
                        |     |                   \
                      /      /                     \
                      /     /                       \ \
                    /      /                         \  \
                  /     /                            \   \
                /     /             _----_            \   \
                /     /           _-~      ~-_         |   |
              (      (        _-~    _--_    ~-_     _/   |
                \      ~-____-~    _-~    ~-_    ~-_-~    /
                  ~-_           _-~          ~-_       _-~
                    ~--______-~                ~-___-~
{cursor.RESET}

{cursor.YELLOW}Make sure to run this game "real-time" (-i)
See website for details{cursor.RESET}

{cursor.BLUE}Press enter when ready....{cursor.RESET}

"""

DESCRIPTION = "An all ascii take on the classic game of snake."


HEIGHT = 15
WIDTH = 25
DELAY = 0.18
PADDING = 3

SNAKE_HEAD = "\U0001F534"  # red circle
SNAKE_BODY = "\U0001F535"  # blue circle
FOODS = [
    "\U0001F401",  # mouse
    "\U0001F414",  # chicken
    "\U0001F400",  # rat
    "\U0001F41B",  # bug
    "\U0001F41D",  # honeybee
    "\U0001F9A0"  # microbe
]
TREES = [
    "\U0001F332",  # evergreen
    "\U0001F333",  # deciduous
    "\U0001F334",  # palm
    "\U0001F335"   # cactus
]

TOP_LINE = f"{' ' * PADDING}{'{0}' * (WIDTH + 2)}\n"
MIDDLE_LINE = f"{' ' * PADDING}{'{0}'}{WIDTH * '  '}{'{0}'}\n"
EMPTY_BOARD = (
    f"{TOP_LINE}"
    f"{MIDDLE_LINE * HEIGHT}"
    f"{TOP_LINE}"
)

GAME_OVER = cursor.red('\n\nGAME OVER\n\n')

SCORE_MESSAGE = "\U0001F480"
