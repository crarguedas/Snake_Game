from tkinter import *
import random   

#v 2.0
#Some constants
GAME_WIDTH = 700
GAME_HEIGHT = 700
SPEED = 100
SPACE_SIZE = 25
BODY_PARTS = 3
SNAKE_COLOR = "#cffc03" 
FOOD_COLOR = "#fc0303"
BACKGROUND_COLOR = "#030000"
GAME_STATE = 'ACTIVE'

#A few variables
food_shape = ''
color = ''
new_speed = 0

class Snake:
    '''creates snake object'''
    def __init__(self):
        
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.square = []

        for i in range(0,BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake" )
            self.square.append(square)
class Food:
    '''creates food object with random shape and colors'''
    '''#03fc84: green, #0328fc: blue ,#96030a: red'''
    '''1: oval, 2:rectangle'''
    color = ''   
    def __init__(self):
        global food_shape
        global color
        food_shape = random.randint(1,2)
        
        c = {'C1': '#03fc84', 'C2': '#0328fc',
            'C3': '#f5f0f0', 'C4':'#96030a', 'C5': '#eb7005',
            'C6':'#ed91bc','C7': '#eded0c', 'C8':'#a8a8a7'}
         
        num = random.randint(1,6)
        key = 'C' + str(num)

        color =(c[key])

        if food_shape == 1:

            x = random.randint(0, (GAME_WIDTH /  SPACE_SIZE) -1) * SPACE_SIZE
            y = random.randint(0, (GAME_HEIGHT / SPACE_SIZE) -1) * SPACE_SIZE
            
            self.coordinates = [x,y]

            canvas.create_oval(x , y, x + SPACE_SIZE, y + SPACE_SIZE, fill=color, tag="food")
            
        else:
            x = random.randint(0, (GAME_WIDTH /  SPACE_SIZE) -1) * SPACE_SIZE
            y = random.randint(0, (GAME_HEIGHT / SPACE_SIZE) -1) * SPACE_SIZE

            self.coordinates = [x,y]
            canvas.create_rectangle(x , y, x + SPACE_SIZE, y + SPACE_SIZE, fill=color, tag="food")
def next_turn(snake, food):
    '''Determines actions after the snake catches the food'''
    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
         x += SPACE_SIZE

    snake.coordinates.insert(0,(x, y))

    squares = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill= SNAKE_COLOR)
    
    snake.square.insert(0, squares)


    if x == food.coordinates[0] and y == food.coordinates[1]:

        speed_calc()
        score = score_mult()

        canvas.delete("food")

        food = Food()
        
    else:
         del snake.coordinates[-1]

         canvas.delete(snake.square[-1])

         del snake.square[-1]

    if check_collisions(snake):
        global GAME_STATE
        GAME_STATE = 'INACTIVE'
        prompt()

    else:
        
        window.after((SPEED), next_turn, snake, food)
        
def change_direction(new_direction):
    '''Controls snake direction during game'''
    global direction

    if new_direction == 'left':
        if direction != 'right':
            direction = new_direction

    elif new_direction == 'right':
        if direction != 'left':
            direction = new_direction

    elif new_direction == 'up':
        if direction != 'down':
            direction = new_direction

    elif new_direction == 'down':
        if direction != 'up':
            direction = new_direction

def change_game(state):
    '''Conditional used for the Game over prompt'''
    global GAME_STATE
    
    if GAME_STATE == "INACTIVE":
        if state == 'r':
            global SPEED
            global score
            SPEED = 100
            GAME_STATE = 'Active'
            score = 0
            label.config(text="Score: {}".format(score))
            label1.config(text="Speed: {}".format(new_speed))
            restart() 
        elif state == 'q':
            canvas.delete("max_speed","max_score","prompt")
            global window
            window.quit()
        
def score_mult():
    '''Generates food points based on color and shape'''
    global color
    global score
    '''#03fc84: green, #0328fc: blue ,#96030a: red'''
    '''1: oval, 2:rectangle'''
    
    if food_shape == 1:
        if color == '#96030a':
            score += 30
        elif color == '#03fc84':
            score += 25         
        elif color == '#0328fc':
            score += 20                   
        else:
            score += 1 
    
    elif food_shape == 2:
        if color == '#96030a':
            score += 15
        elif color == '#03fc84':
            score += 10
        elif color == '#0328fc':
            score += 5
        else:
            score += 1    
    label.config(text="Score: {}".format(score))

def speed_calc():
    '''Increases the speed of the snake while on the game, this needs further development'''
    global SPEED
    global new_speed
    '''SPEED is the internal snake speed which is set as a game constant with a value of 100'''
    SPEED -= 2
    '''New speed is the speed players see on the screen, increases by two each time food is caught b the snake'''
    new_speed = (SPEED - 100) * (-1)
   
    label1.config(text="Speed: {}".format(new_speed))
def prompt():
    '''Game over prompt'''
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2,
                        font=('consolas', 15,), text="Thanks for playing. Press r to start a new game or q to exit",fill="orange", tag="prompt")
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2.5,
                        font=('consolas', 15,), text="Your max Score: {}".format(score),fill="orange", tag="max_score")
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/3,
                        font=('consolas', 15,), text="Max speed reached: {}".format(new_speed),fill="orange", tag="max_speed")
    window.bind('<r>', lambda event: change_game('r'))
    window.bind('<q>', lambda event: change_game('q'))  
    window.bind('<R>', lambda event: change_game('r'))
    window.bind('<Q>', lambda event: change_game('q'))  
    
def check_collisions(snake):
    '''Check if the snake collides against window frame or against itself'''
    x, y = snake.coordinates[0]

    if x < 0 or x >= GAME_WIDTH:
        return True
    elif y < 0 or y >= GAME_HEIGHT:
        
        return True
    
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part [1]:
           
            return True
    
    return False

def restart():
    '''Restarts the game'''
    canvas.delete(ALL)
    snake = Snake()
    food = Food()
    global direction
    global new_speed
    direction = 'down'
    change_direction('down')  
    window.after((new_speed), next_turn, snake, food)
    new_speed = 1
    label.config(text="Score: {}".format(score))
    label1.config(text="Speed: {}".format(new_speed))
    
window = Tk()
window.title(r"Snake game v2.0")

icon = PhotoImage(file='logo.png')
window.iconphoto(True,icon)

window.resizable(False,False)

score = 0
SPEED = 100
direction = 'down'
new_speed = 1

label = Label(window, text="Score: {}".format(score), font=('Consolas', 15))
label.pack()
label1 = Label(window, text="Speed : {}".format(new_speed), font=('Consolas', 10))
label1.pack()

canvas = Canvas(window, bg= BACKGROUND_COLOR, height= GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

window.update()

window_width = window.winfo_width()
window_height = window.winfo_height()

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width/2) - (window_width/2))
y = int((screen_height/2) - (screen_height/2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))

window.bind('<a>', lambda event: change_direction('left'))
window.bind('<d>', lambda event: change_direction('right'))
window.bind('<w>', lambda event: change_direction('up'))
window.bind('<s>', lambda event: change_direction('down'))

window.bind('<A>', lambda event: change_direction('left'))
window.bind('<D>', lambda event: change_direction('right'))
window.bind('<W>', lambda event: change_direction('up'))
window.bind('<S>', lambda event: change_direction('down'))

snake = Snake()
food = Food()

next_turn(snake, food)

window.mainloop()