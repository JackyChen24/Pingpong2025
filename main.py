from tkinter import *
import time
import random
#from pynput import keyword
#from pynput.keyboard import key

class GUI:
    """GUI class handles a lot of the other classes"""\

    CANVAS_LENGTH = 900
    CANVAS_WIDTH = 1200
    def __init__(self):

        self.window = Tk() # toolkit
        self.canvas = Canvas(self.window, width=f"{self.CANVAS_WIDTH}", height="600",
                        background="blanchedalmond")
        self.canvas.pack()

        self.paddle_1 = Paddle("blue", self.canvas, 1, self.window)
        self.paddle_2 = Paddle("red", self.canvas, 2, self.window)
        self.ball = Ball(self.canvas, "white", self.paddle_1, self.paddle_2)

        self.after_call = None
        start_button = Button(self.window, text="start", command=self.move)
        start_button.pack()

        self.window.bind("<KeyPress>", self.bob)


        self.window.mainloop()


    def bob(self, event):
        self.paddle_1.Up()
        print(event)


    def move(self):
        #Using after call constantly updates the movement of all objects
        #Does not directly manipulate the object
        self.ball.move_ball()
        self.paddle_2.move()
        self.paddle_1.move()

        self.after_call = self.window.after(16, self.move)


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

    def Up(self):
        print("Up")
        self.vel_y = -5



    def move(self):
        if self.canvas.coords(self.paddle_id)[3] > 600 or self.canvas.coords(self.paddle_id)[1] < 0:
            self.vel_y = 0
        self.canvas.move(self.paddle_id, 0, self.vel_y)
        self.vel_y = 0

    # collides with ball
class Ball:
    """Ball class"""
    def __init__(self, canvas, color, paddle1, paddle2):
        self.vel_X = 5
        self.vel_y = 5
        self.paddles = [paddle1,paddle2]
        self.hit_count = 0
        self.canvas = canvas
        self.ball_id = canvas.create_oval(0,0,15,15, fill = color)
        self.canvas.move(self.ball_id, GUI.CANVAS_WIDTH/2, GUI.CANVAS_LENGTH/2)


    def collision(self):
        if self.hit_count < 4:
            self.hit_count += 1

    def move_ball(self):
        if self.canvas.coords(self.ball_id)[2] > GUI.CANVAS_WIDTH or self.canvas.coords(self.ball_id)[0] < 0:
            self.collision()
            self.vel_X = -self.vel_X
        if self.canvas.coords(self.ball_id)[3] > 600 or self.canvas.coords(self.ball_id)[1] < 0:
            self.vel_y = -self.vel_y
            self.collision()
        for paddle in self.paddles:
            x1, y1, x2, y2 = self.canvas.coords(paddle.paddle_id)
            if self.canvas.find_overlapping(x1, y1, x2, y2):
                print(self.canvas.find_overlapping(x1, y1, x2, y2))
                if len(self.canvas.find_overlapping(x1, y1, x2, y2)) >= 2:
                    self.vel_X = -self.vel_X



        self.canvas.move(self.ball_id, self.vel_X * self.hit_count, self.vel_y)
        print(self.vel_X)

GUI()