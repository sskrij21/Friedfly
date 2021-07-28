import pyxel


class App:

    def __init__(self):
        self.mouse_pressed = False
        self.drawing_anime = False
        self.frame_anime_init = 0
        self.circ_x = 80
        self.circ_y = 80
        pyxel.init(160, 160, caption="Fried fly")
        pyxel.load('friedfly.pyxres')
        pyxel.run(self.update, self.draw)

    def update(self):
        # quit a game when Q is pressed
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        # display the cursor
        pyxel.mouse(True)
        # check if a mouse is pressed
        self.mouse_pressed = pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON)
        self.circ_x = pyxel.mouse_x
        self.circ_y = pyxel.mouse_y
        if self.mouse_pressed and not self.drawing_anime:
            self.drawing_anime = True
            self.frame_anime_init = pyxel.frame_count

    def draw(self):
        # fill the screen with a black
        pyxel.cls(pyxel.COLOR_BLACK)
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


App()
