import pyxel
import math
import random


def dist(p, q):
    return math.sqrt(sum((px - qx) ** 2.0 for px, qx in zip(p, q)))


class App:

    def __init__(self):
        # Player
        self.mouse_pressed = False
        # Player
        self.drawing_anime = False
        # Player
        self.frame_anime_init = 0
        # General
        self.game_score = 0
        # Player
        self.circ_x = 80
        self.circ_y = 80
        # Enemy
        self.pos_ene_x = random.randint(0, 160)
        self.pos_ene_y = 0
        self.speed = 1
        self.vel_ene_x = 0
        self.vel_ene_y = 0
        # Sweet
        self.pos_sweet_x = 80-16/2
        self.pos_sweet_y = 160-16
        # General
        pyxel.init(160, 160, caption="Fried fly")
        pyxel.load('friedfly.pyxres')
        pyxel.run(self.update, self.draw)

    def update(self):
        # General
        # quit a game when Q is pressed
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        # display the cursor
        pyxel.mouse(True)
        # check if a mouse is pressed
        # General
        self.mouse_pressed = pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON)
        self.update_player()
        self.update_enemy()
        self.update_score()

    def update_player(self):
        self.circ_x = pyxel.mouse_x
        self.circ_y = pyxel.mouse_y
        if self.mouse_pressed and not self.drawing_anime:
            self.drawing_anime = True
            self.frame_anime_init = pyxel.frame_count

    def update_enemy(self):
        vec_x = self.pos_sweet_x - self.pos_ene_x
        vec_y = self.pos_sweet_y - self.pos_ene_y
        abs_vec = math.sqrt(vec_x*vec_x+vec_y*vec_y)
        self.pos_ene_x += self.speed * vec_x / abs_vec
        self.pos_ene_y += self.speed * vec_y / abs_vec

    def update_score(self):
        if self.mouse_pressed and dist([self.circ_x, self.circ_y], [80, 80]) <= 5:
            self.game_score += 100

    def draw(self):
        # fill the screen with a black
        # General
        pyxel.cls(pyxel.COLOR_BLACK)
        self.draw_sweet()
        self.draw_enemy()
        self.draw_player()
        self.draw_score()

    def draw_player(self):
        if self.drawing_anime:
            # Count how many frames were passed from the begining
            current_frame = pyxel.frame_count - self.frame_anime_init
            # First four frames
            if current_frame//4 == 0:
                pyxel.blt(self.circ_x, self.circ_y, 0, 16, 0, 16, 32, pyxel.COLOR_BROWN)
            # Next four frames
            if current_frame//4 == 1:
                pyxel.blt(self.circ_x, self.circ_y, 0, 32, 0, 16, 32, pyxel.COLOR_BROWN)
            # if the animation lasts more than eight frames, kill it.
            if current_frame >= 8:
                self.drawing_anime = False
        else:
            # nominal state (without a click)
            pyxel.blt(self.circ_x, self.circ_y, 0, 0, 0, 16, 32, pyxel.COLOR_BROWN)

    def draw_sweet(self):
        pyxel.blt(self.pos_sweet_x, self.pos_sweet_y, 0, 0, 48, 16, 16, pyxel.COLOR_GREEN)

    def draw_enemy(self):
        if pyxel.frame_count % 4 < 2:
            pyxel.blt(self.pos_ene_x, self.pos_ene_y, 0, 16, 32, 16, 16, pyxel.COLOR_BROWN)
        if pyxel.frame_count % 4 >= 2:
            pyxel.blt(self.pos_ene_x, self.pos_ene_y, 0, 32, 32, 16, 16, pyxel.COLOR_BROWN)

    def draw_score(self):
        # Score
        pyxel.blt(80, 80, 0, 0, 32, 16, 16, pyxel.COLOR_BROWN)
        pyxel.circ(80, 80, 5, pyxel.COLOR_BROWN)
        pyxel.text(110, 5, 'SCORE: {}'.format(self.game_score), pyxel.COLOR_GREEN)
        pyxel.text(109, 5, 'SCORE: {}'.format(self.game_score), pyxel.COLOR_RED)


App()
