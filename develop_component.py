import pyxel
import math

def dist(p,q):
    return math.sqrt(sum((px - qx) ** 2.0 for px, qx in zip(p, q)))
class App:

    def __init__(self):
        ## Player
        self.mouse_pressed = False
        ## Player
        self.drawing_anime = False
        ## Player
        self.frame_anime_init = 0
        ## General
        self.game_score = 0
        ## Player
        self.circ_x = 80
        self.circ_y = 80
        ## General
        pyxel.init(160, 160, caption="Fried fly")
        pyxel.load('friedfly.pyxres')
        pyxel.run(self.update, self.draw)

    def update(self):
        ## General
        # quit a game when Q is pressed
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        # display the cursor
        pyxel.mouse(True)
        # check if a mouse is pressed
        ## General
        self.mouse_pressed = pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON)
        self.update_player()
        self.update_score()

    def update_player(self):
        self.circ_x = pyxel.mouse_x
        self.circ_y = pyxel.mouse_y
        if self.mouse_pressed and not self.drawing_anime:
            self.drawing_anime = True
            self.frame_anime_init = pyxel.frame_count

    def update_score(self):
        if self.mouse_pressed and dist([self.circ_x,self.circ_y],[80,80]) <= 5: self.game_score += 100

    def draw(self):
        # fill the screen with a black
        ## General
        pyxel.cls(pyxel.COLOR_BLACK)
        self.draw_score()
        self.draw_player()


    def draw_player(self):
        if self.drawing_anime:
            # Count how many frames were passed from the begining
            current_frame = pyxel.frame_count - self.frame_anime_init
            # First four frames
            if current_frame//4 == 0: pyxel.blt(self.circ_x, self.circ_y, 0, 16, 0, 16, 32, pyxel.COLOR_BROWN)
            # Next four frames
            if current_frame//4 == 1: pyxel.blt(self.circ_x, self.circ_y, 0, 32, 0, 16, 32, pyxel.COLOR_BROWN)
            # if the animation lasts more than eight frames, kill it.
            if current_frame >= 8:
                self.drawing_anime = False
        else:
            # nominal state (without a click)
            pyxel.blt(self.circ_x, self.circ_y, 0, 0, 0, 16, 32, pyxel.COLOR_BROWN)

    def draw_score(self):
        ## Score
        pyxel.blt(80, 80, 0, 0, 32, 16, 16, pyxel.COLOR_BROWN)
        pyxel.circ(80, 80, 5, pyxel.COLOR_BROWN)
        pyxel.text(110, 5, 'SCORE: {}'.format(self.game_score), pyxel.COLOR_GREEN)
        pyxel.text(109, 5, 'SCORE: {}'.format(self.game_score), pyxel.COLOR_RED)

App()
