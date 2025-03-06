from tkinter import *


class Gui:
    """gui class handles a lot of the other classes."""
    PLAYER1_ID = 1
    PLAYER2_ID = 2
    CANVAS_LENGTH = 600
    CANVAS_WIDTH = 1200

    def __init__(self):


        self.window = Tk()  # toolkit
        self.canvas =\
            Canvas(self.window, width=f"{self.CANVAS_WIDTH}", height="600",
                        background="blanchedalmond")
        self.canvas.pack()

        self._paddle_1 = (
            Paddle("blue", self.canvas, self.PLAYER1_ID, self.window))
        self._paddle_2 = (
            Paddle("red", self.canvas, self.PLAYER2_ID, self.window))
        self._score_one = 0
        self._score_two = 0
        self.is_moving = False
        self._ball = Ball(self.canvas, "white", self._paddle_1, self._paddle_2, self)
        self.input_list  = set()
        self.labels = []
        self.labels.append(TextDisplay(self._score_one, self.window, 0, self))
        self.labels.append(TextDisplay(self._score_two, self.window, 1, self))

        self.player_one_up = "w"
        self.player_one_down = "s"


        self.player_two_up = "up"
        self.player_two_down = "down"

        self.after_call = None
        self.update_step()
        start_button = Button(self.window, text="start", command=self.start_movement)
        start_button.pack()

        for i in self.labels:
            i.score_label.pack()
        self.window.bind("<KeyPress>", self.event)
        self.window.bind("<KeyRelease>", self.event_released)


        self.window.mainloop()


    def score(self,player,ball):
        if player == Gui.PLAYER2_ID:
            self._score_one += 1
        else:
            self._score_two +=1
        self.canvas.moveto(ball, 600, 450)
        for i in self.labels:
            i.update()
            print("update")
        print(f"(player one score {self._score_one} player two score {self._score_two})")


    def get_score(self, index):
        if index == Gui.PLAYER1_ID:
            return self._score_one
        else:
            return self._score_two


    def event(self, event):
        key_pressed = event
        self.input_list.add(key_pressed.keysym.lower())

    def event_released(self, event):
        key_pressed = event
        self.input_list.remove(key_pressed.keysym.lower())


    def update_step(self):
        for word in self.input_list:
            if word == self.player_one_up:
                self._paddle_1.up()
            if word == self.player_one_down:
                self._paddle_1.down()
            # player two
            if word == self.player_two_up:
                self._paddle_2.up()
            if word == self.player_two_down:
                self._paddle_2.down()
        #Using after call constantly updates the movement of all objects
        #Does not directly manipulate the object
        if self.is_moving:
            self._ball.move_ball()
            self._paddle_2.move()
            self._paddle_1.move()

        self.after_call = self.window.after(16, self.update_step)

    def stop_movement(self):
        self.is_moving = False

    def start_movement(self):
        self.is_moving = True

    def collsion(self):
        #Detects the collision between the paddle and the ball and
        #reflects the ball correctly
        pass



class TextDisplay:
    def __init__(self, text, window, index, gui):
        self.text = text

        self.index = index
        self.window = window
        self.gui = gui

        self.score_label = Label(self.window,
                                  text=self.text,
                                  anchor=CENTER,
                                  )


    def update(self):
        self.score_label.config(text=self.gui.get_score(self.index))
        pass



class Paddle:
    """Paddle class/Constructor"""
    def __init__(self, color, canvas, index, window):
        self.colour = color
        self.paddle_index = index
        self.canvas = canvas
        self.vel_y = 0
        self.movement_speed = 20
        #self.up = window.bind("<KeyPress>", PaddleController())
        if index == 1:
            self.paddle_id = self.canvas.create_rectangle(50, 250, 55, 100, fill = self.colour) # DOO THIS
        else:
            self.paddle_id = self.canvas.create_rectangle(1150, 250, 1155, 100, fill=self.colour)

    def up(self):
        self.vel_y = -self.movement_speed


    def down(self):
        self.vel_y = self.movement_speed



    def move(self):
        if self.canvas.coords(self.paddle_id)[3] > 600:
            if self.vel_y == self.movement_speed:
                self.vel_y = 0
        if self.canvas.coords(self.paddle_id)[1] < 0:
            if self.vel_y == -self.movement_speed:
                self.vel_y = 0

        self.canvas.move(self.paddle_id, 0, self.vel_y)
        self.vel_y = 0

    # collides with ball
class Ball:
    """Ball class/ Constructor"""
    def __init__(self, canvas, color, paddle1, paddle2, gui):
        self.vel_X = 5
        self.vel_y = 5
        self.paddles = [paddle1,paddle2]
        self.hit_count = 0
        self.canvas = canvas
        self.ball_id = canvas.create_oval(0,0,15,15, fill = color)
        self.canvas.move(self.ball_id, gui.CANVAS_WIDTH/2, gui.CANVAS_LENGTH/2)
        self.gui = gui


    def collision(self):
        if self.hit_count < 4:
            self.hit_count += 1


    def score(self, index):
        self.gui.score(index, self.ball_id)
        self.gui.stop_movement()
        self.hit_count = 0



    def move_ball(self):
        if self.canvas.coords(self.ball_id)[2] > Gui.CANVAS_WIDTH:
            self.score(Gui.PLAYER1_ID)
        if self.canvas.coords(self.ball_id)[0] < 0:
            self.score(Gui.PLAYER2_ID)


        if self.canvas.coords(self.ball_id)[3] > 600 or self.canvas.coords(self.ball_id)[1] < 0:
            self.vel_y = -self.vel_y
            self.collision()
        for paddle in self.paddles:
            x1, y1, x2, y2 = self.canvas.coords(paddle.paddle_id)
            if self.canvas.find_overlapping(x1, y1, x2, y2):
                if len(self.canvas.find_overlapping(x1, y1, x2, y2)) >= 2:
                    self.vel_X = -self.vel_X



        self.canvas.move(self.ball_id, self.vel_X * self.hit_count, self.vel_y)

Gui()