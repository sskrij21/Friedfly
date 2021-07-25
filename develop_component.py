import pyxel


class App:

    def __init__(self):
        self.mouse_pressed = False
        self.circ_x = 80
        self.circ_y = 80
        pyxel.init(160, 160, caption="Fried fly")
        pyxel.run(self.update, self.draw)

    def update(self):
        # quit a game when Q is pressed
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        # display the cursor
        pyxel.mouse(True)
        # check if a mouse is pressed
        self.mouse_pressed = pyxel.btn(pyxel.MOUSE_LEFT_BUTTON)
        if self.mouse_pressed:
            self.circ_x = pyxel.mouse_x
            self.circ_y = pyxel.mouse_y

    def draw(self):
        # fill the screen with a black
        pyxel.cls(pyxel.COLOR_BLACK)
        # draw circle when mouse left button is pressed
        if self.mouse_pressed:
            pyxel.circ(self.circ_x, self.circ_y, 30, pyxel.COLOR_RED)


App()
