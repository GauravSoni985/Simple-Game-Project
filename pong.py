import turtle    # library for graphics 

# Set up the window
win = turtle.Screen() 
win.title("Pong Game") 
win.bgcolor("black") 
win.setup(width=800, height=600)  # window screen size
win.tracer(0) # tracker(0) turn off the screen updates 

# Score
score_a = 0 # score track krne k liye
score_b = 0
win_score = 5   # set winning score

# Left Paddle
paddle_a = turtle.Turtle() # turtle.turtle 1 movable object create krta h 
paddle_a.speed(0)
paddle_a.shape("square")
paddle_a.color("white")
paddle_a.shapesize(stretch_wid=5, stretch_len=1)
paddle_a.penup() # no drawing line when moving 
paddle_a.goto(-350, 0) # left side paddle position

# Right Paddle
paddle_b = turtle.Turtle()
paddle_b.speed(0)
paddle_b.shape("square")
paddle_b.color("white")
paddle_b.shapesize(stretch_wid=5, stretch_len=1)
paddle_b.penup()
paddle_b.goto(350, 0)  # right side coordinates

# Ball
ball = turtle.Turtle()
ball.speed(0)
ball.shape("circle")
ball.color("white")
ball.penup() # no drawing line when moving
ball.goto(0, 0) # at begining at the center
ball.dx = 0.175 # ball movement in x direction
ball.dy = -0.175 # ball movement in y direction

# Score Display
pen = turtle.Turtle()  # pen 1 text object create krta h
pen.speed(0)
pen.color("white")
pen.penup() 
pen.hideturtle()
pen.goto(0, 260)
pen.write("Player A: 0  Player B: 0", align="center", font=("Courier", 24, "normal"))

# Paddle movement
def paddle_a_up():
    y = paddle_a.ycor() # current y coordinate of paddle a
    if y < 250:
        paddle_a.sety(y + 20)  # 1 step m 20 px hi move krega 

def paddle_a_down():
    y = paddle_a.ycor()
    if y > -240:
        paddle_a.sety(y - 20)

def paddle_b_up():
    y = paddle_b.ycor()
    if y < 250:
        paddle_b.sety(y + 20)

def paddle_b_down():
    y = paddle_b.ycor()
    if y > -240:
        paddle_b.sety(y - 20)

# Keyboard bindings
win.listen()
win.onkeypress(paddle_a_up, "w")
win.onkeypress(paddle_a_down, "s")
win.onkeypress(paddle_b_up, "Up")
win.onkeypress(paddle_b_down, "Down")

# Game loop
while True:
    win.update()

    # Move ball
    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)

    # Border bounce
    if ball.ycor() > 290:  # border touch krne pr bounce krna h
        ball.sety(290)
        ball.dy *= -1

    if ball.ycor() < -290:
        ball.sety(-290)
        ball.dy *= -1

    # when ball crosses right edge -> player A scores
    if ball.xcor() > 390:
        ball.goto(0, 0)
        ball.dx *= -1
        score_a += 1
        pen.clear()
        pen.write(f"Player A: {score_a}  Player B: {score_b}",
                  align="center", font=("Courier", 24, "normal"))

        if score_a == win_score:
            pen.clear()
            pen.goto(0, 0)
            pen.write("PLAYER A WINS!", align="center", font=("Courier", 32, "bold"))
            break

    # when ball crosses left edge -> player B scores
    if ball.xcor() < -390:
        ball.goto(0, 0)
        ball.dx *= -1
        score_b += 1
        pen.clear()
        pen.write(f"Player A: {score_a}  Player B: {score_b}",
                  align="center", font=("Courier", 24, "normal"))

        if score_b == win_score:
            pen.clear()
            pen.goto(0, 0)
            pen.write("PLAYER B WINS!", align="center", font=("Courier", 32, "bold"))
            break

    # Paddle collision
    if (340 < ball.xcor() < 350 and
        paddle_b.ycor() - 50 < ball.ycor() < paddle_b.ycor() + 50):
        ball.setx(340)
        ball.dx *= -1

    if (-350 < ball.xcor() < -340 and
        paddle_a.ycor() - 50 < ball.ycor() < paddle_a.ycor() + 50):
        ball.setx(-340)
        ball.dx *= -1

# Keep the window open so the winner message remains visible
win.mainloop()
