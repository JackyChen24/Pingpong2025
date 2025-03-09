"""A pong game made using Tkinter."""
from tkinter import *


class Gui:
    """Handles the graphical interface and game logic for a Pong game.

    Attributes:
        PLAYER1_ID (int): Identifier for player 1.
        PLAYER2_ID (int): Identifier for player 2.
        CANVAS_LENGTH (int): Height of the game canvas.
        CANVAS_WIDTH (int): Width of the game canvas.
    """

    PLAYER1_ID = 1
    PLAYER2_ID = 2
    CANVAS_LENGTH = 600
    CANVAS_WIDTH = 1200

    def __init__(self):
        """Initialize the GUI for the Pong game.

        Attributes:
            _player_one_up (str): Keybind for player 1's paddle to move up.
            _player_one_down (str): Keybind for player 1's paddle to move down.
            _player_two_up (str): Keybind for player 2's paddle to move up.
            _player_two_down (str): Keybind for player 2's paddle to move down.
            _score_one (int): The score of player 1, initially set to 0.
            _score_two (int): The score of player 2, initially set to 0.
            _input_list (set): Tracks currently pressed keys.
            _labels (list): Stores score labels.
            _window (Tk): The main Tkinter window.
            _canvas (Canvas): The game canvas where paddles and ball drawn.
            _paddle_1 (Paddle): Paddle object for player 1.
            _paddle_2 (Paddle): Paddle object for player 2.
            _ball (Ball): The ball object.
            _is_moving (bool): Indication whether the ball is moving.
        """
        self._player_one_up = "w"
        self._player_one_down = "s"
        self._player_two_up = "up"
        self._player_two_down = "down"

        self._score_one = 0
        self._score_two = 0

        self._input_list = set()
        self._labels = []
        self._window = Tk()
        self._is_moving = False
        self._after_call = None

        self._window.bind("<KeyPress>", self.event)
        self._window.bind("<KeyRelease>", self.event_released)

        self._canvas = Canvas(self._window,
                              width=f"{self.CANVAS_WIDTH}",
                              height="600",
                              background="blanchedalmond")

        self._paddle_1 = (Paddle("blue",
                                 self._canvas,
                                 self.PLAYER1_ID))
        self._paddle_2 = (Paddle("red",
                                 self._canvas,
                                 self.PLAYER2_ID))

        self._ball = Ball(self._canvas,
                          "white",
                          self._paddle_1,
                          self._paddle_2,
                          self)

        start_button = Button(self._window,
                              text="start",
                              command=self.start_movement)

        self._canvas.pack()

        self._labels.append(TextDisplay(self._score_one,
                                        self._window,
                                        Gui.PLAYER1_ID,
                                        self))
        self._labels.append(TextDisplay(self._score_two,
                                        self._window,
                                        Gui.PLAYER2_ID,
                                        self))

        self.update_step()
        start_button.pack()

        for label in self._labels:
            label.score_label.pack()

        self._window.mainloop()

    def score(self, player, ball):
        """Configure score of players and resets ball position.

        Parameter:
            player (int): The player's identification number.
            ball (Ball): The ball.
        """
        if player == Gui.PLAYER1_ID:
            self._score_one += 1
        else:
            self._score_two += 1
        self._canvas.moveto(ball, 600, 450)
        for label in self._labels:
            label.update()

    def get_score(self, index):
        """Return score of player.

        Parameter:
            index (int): The player's identification number.
        """
        if index == Gui.PLAYER1_ID:
            return self._score_one
        else:
            return self._score_two

    def event(self, event):
        """Add the current pressed key to _input_list.

        Parameter:
            event (str): Key pressed.
        """
        key_pressed = event
        self._input_list.add(key_pressed.keysym.lower())

    def event_released(self, event):
        """Remove the current released key from _input_list.

        Parameter:
           event (str): Key released.
        """
        key_pressed = event
        self._input_list.remove(key_pressed.keysym.lower())

    def update_step(self):
        """Update the game state.

        When game is active,
        updates the position of player's paddle according to _input_list,
        and continuously updates the movement of the ball.
        """
        for word in self._input_list:
            #  Player one
            if word == self._player_one_up:
                self._paddle_1.up()
            if word == self._player_one_down:
                self._paddle_1.down()
            #  Player two
            if word == self._player_two_up:
                self._paddle_2.up()
            if word == self._player_two_down:
                self._paddle_2.down()
        #  Using after call constantly updates the movement of all objects
        #  Does not directly manipulate the object
        if self._is_moving:
            self._ball.move_ball()
            self._paddle_2.move()
            self._paddle_1.move()

        self._after_call = self._window.after(16, self.update_step)

    def stop_movement(self):
        """Set the movement of ball to not moving (False)."""
        self._is_moving = False

    def start_movement(self):
        """Set the movement of the ball to moving (True)."""
        self._is_moving = True


class TextDisplay:
    def __init__(self, text, window, index, gui):
        self.text = text

        self.index = index
        self.window = window
        self.gui = gui

        self.score_label = Label(self.window,
                                 text=f"Player {self.index}: {self.text}",
                                 anchor=CENTER)

    def update(self):
        self.score_label.config(text=f"Player {self.index}: "
                                     f"{self.gui.get_score(self.index)}")
        pass


class Paddle:
    """Paddle class/Constructor"""

    def __init__(self, color, canvas, index):
        self.colour = color
        self.paddle_index = index
        self.canvas = canvas
        self.vel_y = 0
        self.movement_speed = 20
        if index == 1:
            self.paddle_id = self.canvas.create_rectangle(50,
                                                          250,
                                                          55,
                                                          100,
                                                          fill=self.colour)
        else:
            self.paddle_id = self.canvas.create_rectangle(1150,
                                                          250,
                                                          1155,
                                                          100,
                                                          fill=self.colour)

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
        self.paddles = [paddle1, paddle2]
        self.hit_count = 0
        self.canvas = canvas
        self.ball_id = canvas.create_oval(0,
                                          0,
                                          15,
                                          15,
                                          fill=color)
        self.canvas.move(self.ball_id,
                         gui.CANVAS_WIDTH/2,
                         gui.CANVAS_LENGTH/2)
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

        if (self.canvas.coords(self.ball_id)[3] > 600 or
                self.canvas.coords(self.ball_id)[1] < 0):
            self.vel_y = -self.vel_y
            self.collision()
        for paddle in self.paddles:
            x1, y1, x2, y2 = self.canvas.coords(paddle.paddle_id)
            if self.canvas.find_overlapping(x1, y1, x2, y2):
                if len(self.canvas.find_overlapping(x1, y1, x2, y2)) >= 2:
                    self.vel_X = -self.vel_X

        self.canvas.move(self.ball_id, self.vel_X * self.hit_count, self.vel_y)


Gui()
