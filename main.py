from tkinter import *
import random

class GUI:
    """GUI class handles a lot of the other classes"""

    CANVAS_WIDTH = 1200
    def __init__(self):

        self.window = Tk() # toolkit
        self.canvas = Canvas(self.window, width=f"{self.CANVAS_WIDTH}", height="600",
                        background="blanchedalmond")
        self.paddle_1 = Paddle("blue")
        self.paddle_2 = Paddle("red")
        self.ball = Ball(self)

        pass


    def move(self):
        #Using after call constantly updates the movement of all objects
        #Does not directly manipulate the object
        pass

    def collsion(self):
        #Detects the collision between the paddle and the ball and
        #reflects the ball correctly
        pass



class Paddle:
    """Paddle class"""
    def __init__(self, color):
        self.colour = color
        pass

    def collision(self):
        pass

    def move(self, y):
        #Update movement
        pass

    # collides with ball
class Ball:
    """Ball class"""
    def __init__(self, canvas, ):
        self.vel_X = 1
        self.vel_y = 1
        self.Canvas = canvas
        self.ball
        pass

    def collision(self):
        pass

    def move_ball(self):

        pass

GUI()