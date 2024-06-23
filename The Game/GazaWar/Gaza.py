import turtle
import winsound  # We Can also use lib playSound or PyGame
import math
import random 
# import serial       ## The Arduino_Lib
from threading import Thread
from time import sleep

# Set up the screen
wn = turtle.Screen()
wn.bgcolor("#100004")
wn.title("Gaza War")
wn.bgpic("back.gif")

# Register the shape
turtle.register_shape("tank.gif")
turtle.register_shape("solider.gif")

# Draw border
border_pen = turtle.Turtle()
border_pen.speed(0)
border_pen.color("#DBF9DB")
border_pen.penup()
border_pen.setposition(-300,-300)
border_pen.pendown()
border_pen.pensize(5)
for side in range(4):
    border_pen.fd(600)
    border_pen.lt(90)
border_pen.hideturtle()

# Set the score to 0
score = 0

# Draw the pen
score_pen = turtle.Turtle()
score_pen.speed(0)
score_pen.color("#DBF9DB")
score_pen.penup()
score_pen.setposition(-20, 270)
scorestring = "Score: %s" %score
score_pen.write(scorestring, False, align="left", font=("Times New Roman", 16, "normal"))
score_pen.hideturtle()

# Create the player turtle
player = turtle.Turtle()
player.shape("solider.gif")
player.penup()
player.speed(0)
player.setposition(0,-250)
player.setheading(90)

playerspeed = 15

# Choose a number of enemies
number_of_enemies = 8
# Creat an empty list of enemies
enemies = []

# Add enemies to the list
for i in range(number_of_enemies):
    # create the enemy
    enemies.append(turtle.Turtle())

for enemy in enemies:
    enemy.shape("tank.gif")
    enemy.penup()
    enemy.speed(0)
    x = random.randint(-200, 200)
    y =  random.randint(100, 250)
    enemy.setposition(x, y)

enemyspeed = 5

# Creat the player's bullet
bullet = turtle.Turtle()
bullet.color("red")
bullet.shape("triangle")
bullet.penup()
bullet.speed(0)
bullet.setheading(90)
bullet.shapesize(1,1)
bullet.hideturtle()

bulletspeed = 40

bulletstate = "ready"


# Move the player left and rightMove

    
def move_left():
    x = player.xcor()
    x -= playerspeed
    if x < -280: x = -280
    player.setx(x)

def move_right():
    x = player.xcor()
    x += playerspeed
    if x > 280: x = 280
    player.setx(x)

def fire_bullet():
    global bulletstate
    if bulletstate == "ready":
        bulletstate = "fire"
        # Move the bullet to the just above the player
        winsound.PlaySound("explosion-e+b", winsound.SND_ASYNC)
        x = player.xcor()
        y = player.ycor() + 10
        bullet.setposition(x,y)
        bullet.showturtle()

# For collision between enemy and bullet
def isCollision_enemy_bullet(t1, t2):
    distance = math.sqrt(math.pow(t1.xcor()-t2.xcor(),2)+math.pow(t1.ycor()-t2.ycor(),2))
    if distance < 30: return True
    else: return False

# For collision between enemy and player
def isCollision_enemy_player(t1, t2):
    distance = math.sqrt(math.pow(t1.xcor()-t2.xcor(),2)+math.pow(t1.ycor()-t2.ycor(),2))
    if distance < 25: return True
    else: return False

# Create keyboard bindings
turtle.listen()
turtle.onkey(move_left, "Left")
turtle.onkey(move_right, "Right")
turtle.onkey(fire_bullet, "space")

# ardiunoData = serial.Serial('com3', 9600)
# global key
# key = ''
# def control(txt):
#     if chr(txt[0]) == '0': fire_bullet()
#     elif chr(txt[0]) == '#': move_left()
#     elif chr(txt[0]) == '*': move_right()

# def read_serial():
#     global key
#     while True:
#         txt = ardiunoData.readline()
#         key = txt

# var = Thread(target=read_serial)

# var.daemon = True
# var.start()

# Main game loop
Game_Over = False
missed_enemies = 0
while True:
    # if key:
    #     control(key)
    #     key = ''
    for enemy in enemies:
        # Move the enemy left and right
        x = enemy.xcor()
        x += enemyspeed
        enemy.setx(x)

        # Move the enemy back and down
        if enemy.xcor() > 270:
            # Move all enemies down
            for e in enemies:
                y = e.ycor()
                y -= 40
                e.sety(y)
                if e.ycor() < -285 and Game_Over == False:
                    e.hideturtle()
                    missed_enemies += 1
                    if missed_enemies == 2: Game_Over = True
                    x = random.randint(-200, 200)
                    y = random.randint(100, 250)
                    e.setposition(x, y)
                    e.showturtle()
            # Change enemy direction
            enemyspeed *= -1

        if enemy.xcor() < -270:
            # Move all enemies down
            for e in enemies:
                y = e.ycor()
                y -= 40
                e.sety(y)
                if e.ycor() < -285 and Game_Over == False:
                    e.hideturtle()
                    missed_enemies += 1
                    if missed_enemies == 2:
                        Game_Over = True
                    x = random.randint(-200, 200)
                    y = random.randint(100, 250)
                    e.setposition(x, y)
                    e.showturtle()
            # Change enemy direction
            enemyspeed *= -1

        # check for a collision between the bullet and the enemy
        if isCollision_enemy_bullet(bullet, enemy):
            winsound.PlaySound("firing.wav", winsound.SND_ASYNC) 
            bullet.hideturtle()
            bulletstate = "ready"
            bullet.setposition(0, -400)
            
            # Reset the enemy
            x = random.randint(-200, 200)
            y = random.randint(100, 250)
            enemy.setposition(x, y)
            enemyspeed += 0.5

            # update the score
            score += 10
            scorestring = "Score: %s" %score
            score_pen.clear()
            score_pen.write(scorestring, False, align="left", font=("Arial", 14, "normal"))
        if isCollision_enemy_player(player, enemy):
            winsound.PlaySound("explosion-e+p.wav", winsound.SND_ASYNC) 
            Game_Over = True
        if Game_Over == True:
            player.hideturtle()
            bullet.hideturtle()
            for e in enemies:
                e.hideturtle()
            wn.bgpic("last.png")
            break

    # Move the bullet
    if bulletstate == "fire":
        y = bullet.ycor()
        y += bulletspeed
        bullet.sety(y)

    # Check to see if the bullet has gone to the top
    if bullet.ycor() > 275:
        bullet.hideturtle()
        bulletstate = "ready"