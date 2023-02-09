"""
This program shows how to:
  * Have one or more instruction screens
  * Show a 'Game over' text and halt the game
  * Allow the user to restart the game

Make a separate class for each view (screen) in your game.
The class will inherit from arcade.View. The structure will
look like an arcade.Window as each view will need to have its own draw,
update and window event methods. To switch a view, simply create a view
with `view = MyView()` and then use the view.show() method.

This example shows how you can set data from one View on another View to pass data
around (see: time_taken), or you can store data on the Window object to share data between
all Views (see: total_score).

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.view_instructions_and_game_over.py

Modified by David F. Barrero
This file includes code from the following sources:
https://api.arcade.academy/en/latest/examples/view_instructions_and_game_over.html#view-instructions-and-game-over


"""

import arcade
import random
import os


file_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(file_path)


WIDTH = 1500
HEIGHT = 720
SPRITE_SCALING = 1

class MenuView(arcade.View):
    def on_show(self):
        arcade.set_background_color(arcade.color.REDWOOD)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Simulador de Hacienda.", WIDTH / 2, HEIGHT / 2,
                         arcade.color.DUTCH_WHITE, font_size=160, anchor_x="center", font_name="Kenney Pixel")
        arcade.draw_text("Click to play", WIDTH / 2, HEIGHT / 2 - 75,
                         arcade.color.COOL_BLACK, font_size=80, anchor_x="center", font_name="Kenney Pixel")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        instructions_view = InstructionView()
        self.window.show_view(instructions_view)


class InstructionView(arcade.View):
    def on_show(self):
        arcade.set_background_color(arcade.color.PURPLE_NAVY)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Guía rápida", WIDTH / 2, HEIGHT / 2,
                         arcade.color.BLACK, font_size=50, anchor_x="center", font_name="Kenney Pixel")
        arcade.draw_text("Desplaza el cursor para mover a la agencia tributaria .Recolecta todo el dinero que puedas.", WIDTH / 2, HEIGHT / 2 - 75,
                         arcade.color.GRAY, font_size=20, anchor_x="center", font_name="Kenney Pixel")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view = GameView()
        self.window.show_view(game_view)


class GameView(arcade.View):
    def __init__(self):
        super().__init__()

        self.time_taken = 0

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.cash_list = arcade.SpriteList()

        # Set up the player
        self.score = 0
        self.player_sprite = arcade.Sprite("Agencia_Tributaria.svg.png",
                                           SPRITE_SCALING)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 50
        self.player_list.append(self.player_sprite)

        for i in range(10):

            # Create the coin instance
            coin = arcade.Sprite("12-Moneda-de-1-euro.png", SPRITE_SCALING / 20)
            cash = arcade.Sprite("07-Billete-500-euros.png", SPRITE_SCALING/30)
            # Position the coin
            coin.center_x = random.randrange(WIDTH)
            coin.center_y = random.randrange(HEIGHT)
            cash.center_x = random.randrange(WIDTH)
            cash.center_y = random.randrange(HEIGHT)

            # Add the coin to the lists
            self.coin_list.append(coin)
            self.cash_list.append(cash)

    def on_show(self):
        arcade.set_background_color(arcade.color.BABY_BLUE)

        # Don't show the mouse cursor
        self.window.set_mouse_visible(False)

    def on_draw(self):
        arcade.start_render()
        # Draw all the sprites.
        self.player_list.draw()
        self.coin_list.draw()
        self.cash_list.draw()
        # Put the text on the screen.
        output = f"Score: {self.score}"
        arcade.draw_text(output, 10, 30, arcade.color.WHITE, 14)
        output_total = f"Total Score: {self.window.total_score}"
        arcade.draw_text(output_total, 10, 10, arcade.color.WHITE, 14)

    def on_update(self, delta_time):
        self.time_taken += delta_time

        # Call update on all sprites (The sprites don't do much in this
        # example though.)
        self.coin_list.update()
        self.cash_list.update()
        self.player_list.update()

        # Generate a list of all sprites that collided with the player.
        hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.coin_list)
        hit_list2 = arcade.check_for_collision_with_list(self.player_sprite, self.cash_list)
        # Loop through each colliding sprite, remove it, and add to the
        # score.
        for coin in hit_list:
            coin.kill()
            self.score += 1
            self.window.total_score += 1
        for cash in hit_list2:
            cash.kill()
            self.score += 500
            self.window.total_score += 500
        # If we've collected all the games, then move to a "GAME_OVER"
        # state.
        if len(self.coin_list) == 0 and len(self.cash_list) == 0:
            game_over_view = GameOverView()
            game_over_view.time_taken = self.time_taken
            self.window.set_mouse_visible(True)
            self.window.show_view(game_over_view)

    def on_mouse_motion(self, x, y, _dx, _dy):
        """
        Called whenever the mouse moves.
        """
        self.player_sprite.center_x = x
        self.player_sprite.center_y = y


class GameOverView(arcade.View):
    def __init__(self):
        super().__init__()
        self.time_taken = 0

    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        arcade.start_render()
        """
        Draw "Game over" across the screen.
        """
        arcade.draw_text("GG", 240, 400, arcade.color.WHITE, 54, anchor_x="left", anchor_y="center", font_name="Kenney Pixel")
        arcade.draw_text("¿Quieres volver a intentarlo?", 310, 300, arcade.color.WHITE, 24, anchor_x="left", anchor_y="center", font_name="Kenney Pixel")

        time_taken_formatted = f"{round(self.time_taken, 2)} segundos"
        arcade.draw_text(f"Tiempo de dinero: {time_taken_formatted}",
                         WIDTH / 2,
                         200,
                         arcade.color.GRAY,
                         font_size=15,
                         anchor_x="center")

        output_total = f"Total Score: {self.window.total_score}"
        arcade.draw_text(output_total, 10, 10, arcade.color.WHITE, 14)

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view = GameView()
        self.window.show_view(game_view)


def main():
    window = arcade.Window(WIDTH, HEIGHT, "Different Views Example")
    window.total_score = 0
    menu_view = MenuView()
    window.show_view(menu_view)
    arcade.run()


if __name__ == "__main__":
    main()