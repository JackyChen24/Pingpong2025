from tkinter import *
import time
import random

class GUI:
    """GUI class handles a lot of the other classes"""\

    CANVAS_LENGTH = 900
    CANVAS_WIDTH = 1200
    def __init__(self):

        self.window = Tk() # toolkit
        self.canvas = Canvas(self.window, width=f"{self.CANVAS_WIDTH}", height="600",
                        background="blanchedalmond")
        self.canvas.pack()

        self.paddle_1 = Paddle("blue", self.canvas)
        self.paddle_2 = Paddle("red", self.canvas)
        self.ball = Ball(self.canvas, "white")
        self.after_call = None
        start_button = Button(self.window, text="start", command=self.move)
        start_button.pack()

        self.window.mainloop()


    def move(self):
        #Using after call constantly updates the movement of all objects
        #Does not directly manipulate the object
        self.ball.move_ball()

        self.after_call = self.window.after(16, self.move)


        pass

    def collsion(self):
        #Detects the collision between the paddle and the ball and
        #reflects the ball correctly
        pass



class Paddle:
    """Paddle class"""
    def __init__(self, color, canvas):
        self.colour = color
        self.canvas = canvas
        self.paddle_id = self.canvas.create_rectangle() # DOO THIS
        self.vel_y = 0


    def move(self, y):
        self.canvas.move(self.paddle_id, 0, self.vel_y)
        pass

    # collides with ball
class Ball:
    """Ball class"""
    def __init__(self, canvas, color):
        self.vel_X = 5
        self.vel_y = 5
        self.hit_count = 0
        self.canvas = canvas
        self.ball_id = canvas.create_oval(0,0,30,30, fill = color)
        self.canvas.move(self.ball_id, GUI.CANVAS_WIDTH/2, GUI.CANVAS_LENGTH/2)


    def collision(self):
        if self.hit_count < 4:
            self.hit_count += 1

    def move_ball(self):
        print("moving")
        if self.canvas.coords(self.ball_id)[2] > GUI.CANVAS_WIDTH or self.canvas.coords(self.ball_id)[0] < 0:
            self.collision()
            self.vel_X = -self.vel_X
        if self.canvas.coords(self.ball_id)[3] > 600 or self.canvas.coords(self.ball_id)[1] < 0:
            self.vel_y = -self.vel_y
            self.collision()

        self.canvas.move(self.ball_id, self.vel_X * self.hit_count, self.vel_y)

GUI()