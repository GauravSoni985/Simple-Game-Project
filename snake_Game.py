from tkinter import *
import random

# Game Constants
SPACE_SIZE = 25
BODY_PARTS = 3
SNAKE_COLOR = "#D1A40E"
FOOD_COLOR = "#1A3AA0"
BACKGROUND_COLOR = "#000000"
START_SPEED = 120

# Global Game Variables
score = 0
high_score = 0
speed = START_SPEED
direction = 'down'
snake = None
food = None
running = True

# --- Create Window Fullscreen ---
window = Tk()
window.title("Snake Game - Full Screen")
window.attributes('-fullscreen', True)
window.configure(bg='black')

# Get Screen Size
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

# Score Label Frame
top_frame = Frame(window, bg='black')
top_frame.pack(side=TOP, fill=X)

score_label = Label(top_frame, text="Score: 0  |  High Score: 0", font=('consolas', 24), bg='black', fg='white')
score_label.pack(side=LEFT, padx=20, pady=10)

# New Game Button
new_game_btn = Button(top_frame, text="New Game", font=("consolas", 18), command=lambda: new_game(), bg="green", fg="white")
new_game_btn.pack(side=RIGHT, padx=20)

# Game Canvas
canvas = Canvas(window, bg=BACKGROUND_COLOR, width=screen_width, height=screen_height - 60)
canvas.pack()

# Snake Class
class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(BODY_PARTS):
            self.coordinates.append([SPACE_SIZE * 5, SPACE_SIZE * 5])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE,
                                             fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)

# Food Class
class Food:
    def __init__(self):
        x = random.randint(0, (screen_width // SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, ((screen_height - 60) // SPACE_SIZE) - 1) * SPACE_SIZE
        self.coordinates = [x, y]
        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")

# Update Score
def update_score():
    score_label.config(text=f"Score: {score}  |  High Score: {high_score}")

# Move Snake
def next_turn():
    global score, speed, snake, food, running, high_score

    if not running:
        return

    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, [x, y])
    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)
    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        score += 10
        if score > high_score:
            high_score = score
        update_score()
        speed = max(50, speed - 2)
        canvas.delete("food")
        food.__init__()
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_collisions():
        return game_over()
    window.after(speed, next_turn)

# Collision Check
def check_collisions():
    x, y = snake.coordinates[0]

    if x < 0 or x >= screen_width or y < 0 or y >= (screen_height - 60):
        return True

    for body in snake.coordinates[1:]:
        if x == body[0] and y == body[1]:
            return True

    return False

# Change Direction
def change_direction(new_dir):
    global direction
    opposites = {"up": "down", "down": "up", "left": "right", "right": "left"}
    if new_dir != opposites.get(direction):
        direction = new_dir

# Game Over Screen
def game_over():
    global running
    running = False
    canvas.create_text(screen_width // 2, (screen_height - 60) // 2,
                       font=('consolas', 60), text="GAME OVER", fill="red", tag="text")
    canvas.create_text(screen_width // 2, (screen_height - 60) // 2 + 60,
                       font=('consolas', 30), text="Press 'New Game' to Restart", fill="white", tag="text")

# Start New Game
def new_game():
    global score, speed, direction, snake, food, running
    canvas.delete("all")
    score = 0
    speed = START_SPEED
    direction = 'down'
    update_score()
    running = True
    snake = Snake()
    food = Food()
    next_turn()

# Bind Controls
window.bind("<Left>", lambda e: change_direction("left"))
window.bind("<Right>", lambda e: change_direction("right"))
window.bind("<Up>", lambda e: change_direction("up"))
window.bind("<Down>", lambda e: change_direction("down"))
window.bind("<Escape>", lambda e: window.attributes("-fullscreen", False))

# WASD support
window.bind("a", lambda e: change_direction("left"))
window.bind("d", lambda e: change_direction("right"))
window.bind("w", lambda e: change_direction("up"))
window.bind("s", lambda e: change_direction("down"))

# Start Game
new_game()
window.mainloop()
