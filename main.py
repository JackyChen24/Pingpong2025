from tkinter import *
import time
import random
#from pynput import keyword
#from pynput.keyboard import key

class GUI:
    """GUI class handles a lot of the other classes"""\

    CANVAS_LENGTH = 600
    CANVAS_WIDTH = 1200
    def __init__(self):

        self.window = Tk() # toolkit
        self.canvas = Canvas(self.window, width=f"{self.CANVAS_WIDTH}", height="600",
                        background="blanchedalmond")
        self.canvas.pack()

        self._paddle_1 = Paddle("blue", self.canvas, 1, self.window)
        self._paddle_2 = Paddle("red", self.canvas, 2, self.window)
        self._score_one = 0
        self._score_two = 0
        self.bob = False
        self._ball = Ball(self.canvas, "white", self._paddle_1, self._paddle_2, self)
        self.input_list  = set()

        self.after_call = None
        self.move()
        start_button = Button(self.window, text="start", command=self.start_movement)
        start_button.pack()

        self.window.bind("<KeyPress>", self.event)
        self.window.bind("<KeyRelease>", self.event_released)


        self.window.mainloop()


    def score(self,player,ball):
        if player == 0:
            self._score_one += 1
        else:
            self._score_two +=1
        self.canvas.moveto(ball, GUI.CANVAS_LENGTH/2, 450)



    def event(self, event):
        key_pressed = event
        self.input_list.add(key_pressed.keysym)
        #player one

        print(self.input_list)

    def event_released(self, event):
        key_pressed = event
        self.input_list.remove(key_pressed.keysym)
        #player one
        if key_pressed.keysym == "w":
            self._paddle_1.up()
        if key_pressed.keysym == "s":
            self._paddle_1.down()
        #player two
        if key_pressed.keysym == "Up":
            self._paddle_2.up()
        if key_pressed.keysym == "Down":
            self._paddle_2.down()
        print(self.input_list)


    def move(self):
        for word in self.input_list:
            if word == "w":
                self._paddle_1.up()
            if word == "s":
                self._paddle_1.down()
            # player two
            if word.keysym == "Up":
                self._paddle_2.up()
            if word.keysym == "Down":
                self._paddle_2.down()
        #Using after call constantly updates the movement of all objects
        #Does not directly manipulate the object
        if self.bob:
            self._ball.move_ball()
            self._paddle_2.move()
            self._paddle_1.move()


        self.after_call = self.window.after(16, self.move)

    def stop_movement(self):
        self.bob = False

    def start_movement(self):
        self.bob = True

    def collsion(self):
        #Detects the collision between the paddle and the ball and
        #reflects the ball correctly
        pass






class Paddle:
    """Paddle class"""
    def __init__(self, color, canvas, index, window):
        self.colour = color
        self.paddle_index = index
        self.canvas = canvas
        self.vel_y = 0
        #self.up = window.bind("<KeyPress>", PaddleController())
        if index == 1:
            self.paddle_id = self.canvas.create_rectangle(50, 250, 75, 100, fill = self.colour) # DOO THIS
        else:
            self.paddle_id = self.canvas.create_rectangle(1150, 250, 1175, 100, fill=self.colour)

    def up(self):
        self.vel_y = -20


    def down(self):
        self.vel_y = 20



    def move(self):
        if self.canvas.coords(self.paddle_id)[3] > 600 or self.canvas.coords(self.paddle_id)[1] < 0:
            self.vel_y = 0
        self.canvas.move(self.paddle_id, 0, self.vel_y)
        self.vel_y = 0

    # collides with ball
class Ball:
    """Ball class"""
    def __init__(self, canvas, color, paddle1, paddle2, GUI):
        self.vel_X = 5
        self.vel_y = 5
        self.paddles = [paddle1,paddle2]
        self.hit_count = 0
        self.canvas = canvas
        self.ball_id = canvas.create_oval(0,0,15,15, fill = color)
        self.canvas.move(self.ball_id, GUI.CANVAS_WIDTH/2, GUI.CANVAS_LENGTH/2)
        self.GUI = GUI


    def collision(self):
        if self.hit_count < 4:
            self.hit_count += 1


    def score(self, index):
        self.GUI.score(index, self.ball_id)
        self.GUI.stop_movement()
        self.hit_count = 0


    def move_ball(self):
        if self.canvas.coords(self.ball_id)[2] > GUI.CANVAS_WIDTH:
            self.score(0)
        if self.canvas.coords(self.ball_id)[0] < 0:
            self.score(1)


        if self.canvas.coords(self.ball_id)[3] > 600 or self.canvas.coords(self.ball_id)[1] < 0:
            self.vel_y = -self.vel_y
            self.collision()
        for paddle in self.paddles:
            x1, y1, x2, y2 = self.canvas.coords(paddle.paddle_id)
            if self.canvas.find_overlapping(x1, y1, x2, y2):
                if len(self.canvas.find_overlapping(x1, y1, x2, y2)) >= 2:
                    self.vel_X = -self.vel_X



        self.canvas.move(self.ball_id, self.vel_X * self.hit_count, self.vel_y)

GUI()