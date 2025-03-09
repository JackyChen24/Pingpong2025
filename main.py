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

        Instance Attributes:
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
    """Display the score labels."""

    def __init__(self, score, window, player_index, gui):
        """Initialize the text display for score.

        Parameter:
            score (str): The score number.
            window (Tk): The window it will be displayed on.
            player_index (int): The player's identification number.
            gui (Gui): The main game GUI instance.
        """
        self._score = score
        self._player_id = player_index
        self._window = window
        self._gui = gui

        self.score_label = Label(self._window,
                                 text=f"Player "
                                      f"{self._player_id}: "
                                      f"{self._score}",
                                 anchor=CENTER)

    def update(self):
        """Update the score label."""
        self.score_label.config(text=f"Player "
                                     f"{self._player_id}: "
                                     f"{self._gui.get_score(self._player_id)}")


class Paddle:
    """Construct a paddle object for Pong game."""

    def __init__(self, color, canvas, index):
        """Initialize paddle with color, canvas, and player index.

        Parameter:
            color (str): The color of the paddle.
            canvas (Canvas): The canvas where the paddle is drawn.
            index (int): Player identification number.

        Instance Attribute:
            vel_y (int): The vertical velocity of the paddle,
            initially set to 0.
            movement_speed (int): The speed the paddle moves.
        """
        self._colour = color
        self._paddle_index = index
        self._canvas = canvas
        self._vel_y = 0
        self._movement_speed = 20
        if index == 1:
            #  Player 1's paddle spawns on the left.
            self._paddle_id = self._canvas.create_rectangle(50,
                                                            250,
                                                            55,
                                                            100,
                                                            fill=self._colour)
        else:
            #  If not player 1, paddle spawn on the right.
            self._paddle_id = self._canvas.create_rectangle(1150,
                                                            250,
                                                            1155,
                                                            100,
                                                            fill=self._colour)

    def get_paddle_id(self):
        """Return _paddle_id."""
        return self._paddle_id

    def up(self):
        """Make the paddle go up."""
        self._vel_y = -self._movement_speed

    def down(self):
        """Make the paddle go down."""
        self._vel_y = self._movement_speed

    def move(self):
        """Move the paddle.

        Prevents paddle from moving out of canvas boundaries.
        """
        if self._canvas.coords(self._paddle_id)[3] > 600:
            #  If the paddle hits the top boundary of canvas.
            if self._vel_y == self._movement_speed:
                self._vel_y = 0
        if self._canvas.coords(self._paddle_id)[1] < 0:
            #  If the paddle hits the bottom boundary of canvas.
            if self._vel_y == -self._movement_speed:
                self._vel_y = 0

        self._canvas.move(self._paddle_id, 0, self._vel_y)
        self._vel_y = 0
    # collides with ball


class Ball:
    """Construct ball object for Pong game."""

    def __init__(self, canvas, color, paddle1, paddle2, gui):
        """Initialize ball object.

        Parameter:
            canvas (Canvas): The game canvas where the ball is drawn.
            color (str): The color of ball.
            paddle1 (Paddle): The paddle of player 1.
            paddle2 (Paddle): The paddle of player 2.
            gui (Gui): The main GUI instance.

        Instance Attribute:
        _vel_x (int): The horizontal velocity of ball.
        _vel_y (int): The vertical velocity of ball.
        _hit_count (int): The amount of times the ball has rebounded.
        """
        self._vel_x = 5
        self._vel_y = 5
        self._paddles = [paddle1, paddle2]
        self._hit_count = 0
        self._canvas = canvas
        self._gui = gui
        self._ball_id = canvas.create_oval(0,
                                           0,
                                           15,
                                           15,
                                           fill=color)
        self._canvas.move(self._ball_id,
                          gui.CANVAS_WIDTH / 2,
                          gui.CANVAS_LENGTH / 2)

    def collision(self):
        """Increases _hit_count (int) when collision occur.

        When _hit_count reaches 4,
        _hit_count stops increasing.
        """
        if self._hit_count < 4:
            self._hit_count += 1

    def score(self, index):
        """Update score when ball goes out of bounds.

        Once it goes out of bounds,
        call score function to update score,
        stops the ball from moving,
        and resets the hit count of the ball.

        Parameter:
            index (int): The player's identification number.
        """
        self._gui.score(index, self._ball_id)
        self._gui.stop_movement()
        self._hit_count = 0

    def move_ball(self):
        """Handle movement of ball across canvas and collision."""
        if self._canvas.coords(self._ball_id)[2] > Gui.CANVAS_WIDTH:
            #  If the ball hits the right boundary.
            self.score(Gui.PLAYER1_ID)
        if self._canvas.coords(self._ball_id)[0] < 0:
            # If the ball hits the left boundary.
            self.score(Gui.PLAYER2_ID)

        if (self._canvas.coords(self._ball_id)[3] > 600 or
                self._canvas.coords(self._ball_id)[1] < 0):
            self._vel_y = -self._vel_y
            self.collision()
        for paddle in self._paddles:
            x1, y1, x2, y2 = self._canvas.coords(paddle.get_paddle_id())
            if self._canvas.find_overlapping(x1, y1, x2, y2):
                if len(self._canvas.find_overlapping(x1, y1, x2, y2)) >= 2:
                    self._vel_x = -self._vel_x

        self._canvas.move(self._ball_id,
                          self._vel_x * self._hit_count,
                          #  x velocity increases everytime hit count goes up.
                          self._vel_y)


Gui()
