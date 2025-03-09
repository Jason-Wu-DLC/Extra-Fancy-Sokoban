import tkinter as tk
from tkinter import messagebox, filedialog
from typing import Callable
from model import SokobanModel, Tile, Entity
from a2_support import *
from a3_support import *


class FancyGameView(AbstractGrid):
    """
    A grid-based graphic depiction of the game perspective.

    The FancyGameView displays the game map,
    including tiles, entities, and the player.
    """

    def __init__(self, master, dimensions, size, **kwargs):
        """
        Create a grid with the FancyGameView's initial dimensions and size.
        """
        super().__init__(master, dimensions, size)
        self._get_image_cache = {}

    def display(self, maze: Grid, entities: Entities, player_position: Position):
        """
        The game view is initially cleared of all previous graphics.

        Then, a picture is created and displayed on the FancyGameView
        instance for each tile and creature.

        A FLOOR tile is presumed to be underneath
        and is rendered first when an entity occupies a spot;

        The entity picture is then rendered on top.

        Parameters:
            maze (Grid): A list of Tile objects representing the game's maze layout.

            entities (Entities): A dictionary mapping Position objects to Entity objects.

            Represents the positions and types of entities in the game.

            player_position (Position): The current position of the player in the maze.
        """
        # Clear previous stats data
        self.clear()

        # Render the maze tiles
        for row, row_maze in enumerate(maze):
            for col_idx, tile_type in enumerate(row_maze):
                tile = maze[row][col_idx]
                tile_type = tile.get_type()
                position_x, position_y = self.get_midpoint((row, col_idx))

                # Check the type of the tile and render the appropriate image
                if tile_type == WALL:
                    image = get_image("images/W.png",
                                      self.get_cell_size(),
                                      self._get_image_cache)
                    self.create_image(position_x, position_y, image=image)

                elif tile_type == GOAL:
                    image = get_image("images/G.png",
                                      self.get_cell_size(),
                                      self._get_image_cache)
                    self.create_image(position_x, position_y, image=image)

                elif tile_type == FLOOR:
                    image = get_image("images/Floor.png",
                                      self.get_cell_size(),
                                      self._get_image_cache)
                    self.create_image(position_x, position_y, image=image)

        # Render the game entities
        for position, game_entity in entities.items():
            position_x, position_y = self.get_midpoint(position)
            entity_type = game_entity.get_type()

            COIN = '$'

            # Check the type of the entity and render the appropriate image
            if entity_type == CRATE:
                entity_strength = game_entity.get_strength()
                image = get_image("images/C.png",
                                  self.get_cell_size(),
                                  self._get_image_cache)
                self.create_image(position_x, position_y, image=image)
                self.create_text(position_x - 3,
                                 position_y - 10,
                                 text=str(entity_strength),
                                 font=CRATE_FONT)

            elif entity_type == COIN:
                image = get_image("images/$.png",
                                  self.get_cell_size(),
                                  self._get_image_cache)
                self.create_image(position_x, position_y, image=image)

            elif entity_type == STRENGTH_POTION:
                image = get_image("images/S.png",
                                  self.get_cell_size(),
                                  self._get_image_cache)
                self.create_image(position_x, position_y, image=image)

            elif entity_type == MOVE_POTION:
                image = get_image("images/M.png",
                                  self.get_cell_size(),
                                  self._get_image_cache)
                self.create_image(position_x, position_y, image=image)

            elif entity_type == FANCY_POTION:
                image = get_image("images/F.png",
                                  self.get_cell_size(),
                                  self._get_image_cache)
                self.create_image(position_x, position_y, image=image)

        # Render the player's position
        player_center_x, player_center_y = self.get_midpoint(player_position)
        player_image = get_image("images/P.png",
                                 self.get_cell_size(),
                                 self._get_image_cache)
        self.create_image(player_center_x, player_center_y, image=player_image)


class FancyStatsView(AbstractGrid):
    """AbstractGrid should be the ancestor of FancyStatsView.

    A 3x3 grid view to show player statistics.

    This class is a grid-formatted detailed representation of a player's statistics.

    'Player Stats' is displayed in the top row,
    the titles of each stat are shown in the second row,

    and the values of those stats are shown in the third row.

"""

    def __init__(self, master: tk.Frame):
        """
        Initializes the FancyStatsView grid with the required number of rows and columns
        """

        super().__init__(master, (3, 3),
                         (MAZE_SIZE + SHOP_WIDTH, STATS_HEIGHT))

    def draw_stats(self, moves_remaining: int, strength: int, money: int):
        """

        Draws the FancyStatsView using the provided statistics.

        This method clears the current data in the FancyStatsView
        and displays new statistics in the form of steps
        remaining, power, and money.

        Parameters:
            moves_remaining (int): The number of moves the player has left.
            strength (int): The strength of the player.
            money (int): The amount of money the player has.
        """
        # Clear previous stats data
        self.clear()

        # Annotate the title for the stats view
        self.annotate_position((0, 1), "Player Stats", TITLE_FONT)

        # Annotate labels for each stat category
        self.annotate_position((1, 0), "Moves remaining:")
        self.annotate_position((1, 1), "Strength:")
        self.annotate_position((1, 2), "Money:")

        # Show the current value of each stat
        self.annotate_position((2, 0), f"{moves_remaining}", TITLE_FONT)
        self.annotate_position((2, 1), f"{strength}", TITLE_FONT)
        self.annotate_position((2, 2), f"${money}", TITLE_FONT)


class Shop(tk.Frame):
    """
    A Shop frame displaying relevant information
    and buttons for buyable items in the game.

    The Shop should contain a title at the top
    and a frame for each buyable item (each potion).

    Each item’s frame should contain the following widgets,
    packed left to right.
    """

    def __init__(self, master: tk.Frame):
        """
        Set up a new buyable item in the shop with its label and buy button.
        """
        super().__init__(master)

        # sets up the shop title label.
        self.title_label = tk.Label(self, text="Shop", font=TITLE_FONT)
        # sets up the shop frame
        self.title_label.pack(pady=10)

    def create_buyable_item(self, item: str, amount: int, callback):
        """
        Creates a new frame within the shop frame.

        Creates a label and button within that child frame.

        The button be bound to the provided callback.

        Parameters:
            item (str): The name of the item.
            amount (str): The price of the item.
            callback: Executed when the "Buy" button is clicked.
        """

        # Sets up the item frame
        item_frame = tk.Frame(self)
        item_frame.pack(pady=5)

        # Display item name & price
        frame_label = tk.Label(item_frame, text=f"{item}: ${amount}")
        frame_label.pack(side=tk.LEFT, padx=10)

        # Buy button with given callback
        buy_button = tk.Button(item_frame, text="Buy", command=callback)
        buy_button.pack(side=tk.LEFT)


class FancySokobanView:
    """
    The FancySokobanView class provides a wrapper
    around the smaller GUI components which has just built.
    """
    def clear_all(self):
        """
        Clear all FancySokobanView instance
        """
        self.gameview.clear()
        self.stats.clear()

    def __init__(self, master: tk.Tk, dimensions, size):
        """
        Creating the title banner, setting the title on the window,
        and instantiating and packing the three widgets
        """
        # Initialize image cache and banner image
        self._image_cache = {}
        self.image = get_image(
            "images/banner.png",
            size=(MAZE_SIZE + SHOP_WIDTH, BANNER_HEIGHT)
        )

        # Set the frame of banner
        self.framebanner = tk.Frame(master)
        self.framebanner.config(width=MAZE_SIZE + SHOP_WIDTH, height=BANNER_HEIGHT)
        self.framebanner.pack(side=tk.TOP)
        self.framebanner.pack_propagate(False)
        label = tk.Label(self.framebanner, image=self.image)
        label.pack()

        # Main container to hold other views
        self.frameall = tk.Frame(master)
        self.frameall.pack()

        # Set the frame of stats
        self.framestats = tk.Frame(master)
        self.framestats.config(width=MAZE_SIZE, height=STATS_HEIGHT)
        self.framestats.pack(side=tk.BOTTOM)
        self.stats = FancyStatsView(self.framestats)
        self.stats.pack()

        # Set the frame's view of maze
        self.framemaze = tk.Frame(self.frameall)
        self.framemaze.config(width=MAZE_SIZE, height=MAZE_SIZE)
        self.framemaze.pack(side=tk.LEFT)
        self.framemaze.pack_propagate(False)
        self.gameview = FancyGameView(self.framemaze, dimensions, size)
        self.gameview.pack()

        # Set the frame's view of shop
        self.frameshop = tk.Frame(self.frameall)
        self.frameshop.config(width=SHOP_WIDTH, height=MAZE_SIZE)
        self.frameshop.pack_propagate(False)
        self.frameshop.pack(side=tk.RIGHT)
        self.shop = Shop(self.frameshop)
        self.shop.pack()

    def display_game(self, maze: Grid, entities: Entities,
                     player_position: Position):
        """
        First Clears and redraws the game view
        """
        self.gameview.clear()
        self.gameview.display(maze, entities, player_position)

    def display_stats(self, moves: int, strength: int, money: int):
        """
        First Clears and redraws the stats view.
        """
        self.stats.clear()
        self.stats.draw_stats(moves, strength, money)

    def create_shop_items(self, shop_items: dict[str, int],
                          button_callback: Callable[[str], None] | None = None):
        """
        Creates all the buyable items in the shop. Shop items maps item id’s
        (result of calling get type on the item entity) to price.

        For each of these items,
        the callback given to create buyable item in Shop should be a function
        which requires no positional arguments
        and calls button callback with the item id as an argument.

        Parameters:
            shop_items (dict[str, int]):
            A Dictionary of buyable items their prices in the shop.

            button_callback: Callable (str):
            A callback function that's invoked when a shop item button is clicked.
        """
        # Render Iterating over shop
        for key, value in shop_items.items():
            item_name = None

            # Check display name for each item ID
            if key == STRENGTH_POTION:
                item_name = "Strength Potion"
            elif key == MOVE_POTION:
                item_name = "Move Potion"
            elif key == FANCY_POTION:
                item_name = "Fancy Potion"

            # Create the buyable item in the shop
            self.shop.create_buyable_item(item_name, value,
                                          lambda current_key=key:
                                          button_callback(current_key))


class ExtraFancySokoban:
    """
    ExtraFancySokoban is the controller class for the overall game.

    The controller is responsible for creating
    and maintaining instances of the model
    and view classes, event handling,
    and facilitating communication between the model and view classes.
    """

    def __init__(self, root: tk.Tk, maze_file: str):
        """
        Sets up the ExtraFancySokoban instance.

        This includes creating instances of SokobanModel and SokobanView,
        creating the shop items,
        binding keypress events to the relevant handler.

        Redrawing the display to show the initial game state.
        """
        # Initialize the Sokoban model with the maze file
        self.model = SokobanModel(maze_file)

        # Store the root
        self.root = root

        # Initialize the game view with the dimensions and size
        self.gameview = (FancySokobanView
                         (self.root, self.model.get_dimensions(),
                          (MAZE_SIZE, MAZE_SIZE)))

        # Redraw to refresh the view to show the initial game state
        self.redraw()

        # Bind the keypress to the handler function
        self.root.bind("<Key>", self.handle_keypress)

        # Create the game file menu
        self.create_game_file_menu(root)

        # Create shop items in the view
        self.gameview.create_shop_items(
            self.model.get_shop_items(),
            lambda item_id: self.perform_action(item_id)
        )

    def redraw(self):
        """
        Redraws the game view and stats view based on the current model state.
        """
        # Redraws the game view
        self.gameview.display_game(
            self.model.get_maze(),
            self.model.get_entities(),
            self.model.get_player_position()
        )

        # Redraws the game stats
        self.gameview.display_stats(
            self.model.get_player_moves_remaining(),
            self.model.get_player_strength(),
            self.model.get_player_money())

    def chosen(self, message: str):
        """
        Prompts the user with a message
        and chosen whether to restart the game or close the application.

        Parameters:
            message (str): Message ask yes or no
        """
        # Set a messagebox for user to choose restart the game or not
        endresponse = messagebox.askyesno(title="", message=message)

        # if user click yes restart the game.
        if endresponse:
            self.player_position = (0, 0)
            self.moves_remaining = 10
            self.model.reset()
            self.gameview.clear_all()
            self.redraw()

        else:
            self.gameview.clear_all()
            self.model.reset()
            self.root.destroy()


    def handle_keypress(self, event: tk.Event):
        """
        An event handler to be called when a keypress event occurs.

        Tell the model to attempt the move as per the key pressed,
        and then redraw the view.

        If the game has been won or lost after the move,
        this method should cause a messagebox to display.

        Informing the user of the outcome and asking if they would like to play again.

        Parameters:
            event (tk.Event): The captured keypress event.
        """
        # Capture the input key character
        self.char = event.char

        # Process the move if key (w, s, a, d) is pressed
        if self.char in ('w', 's', 'a', 'd'):
            self.model.attempt_move(self.char)

            # Check the game state post-move
            if self.model.has_won():
                self.chosen("You won! Play again?")
                return
            elif (self.model.get_player_moves_remaining() == 0
                  and not self.model.has_won()):
                self.chosen("You lose! Play again?")
                return

            # Update the game view by redraw
            self.redraw()

    def perform_action(self, item_id: str):
        """
        Perform the corresponding operation based on the given project ID.

        If the item ID corresponds to a strength potion,
        the potion's effects will be applied to the player.

        Otherwise, it attempts to purchase the item with the specified ID
        and then redraws the game view.

        Parameters:
        item_id (str): The ID of the item determines the action to be performed
      """

        if item_id == "STRENGTH_POTION":
            self.model.get_player().apply_effect(STRENGTH_POTION.EFFECT)
            return self.model.get_player_strength()

        self.model.attempt_purchase(item_id)
        self.redraw()

    def create_game_file_menu(self, master: tk.Tk):
        """
        Creat a game file menu for save and load game.

        Parameters:
        master (tk.Tk): The root window of menu.
        """
        # Initialize a new game menu bar
        menubar = tk.Menu(self.root)

        # Attach the menu bar to the window
        self.root.config(menu=menubar)

        # Create a 'File' dropdown menu
        filemenu = tk.Menu(menubar)
        menubar.add_cascade(label="File", menu=filemenu)

        # Add "Save" and "Load" option to the dropdown menu
        filemenu.add_command(label="Save", command=self.save_game_state)
        filemenu.add_command(label="Load", command=self.load_game_state)

    def save_game_state(self):
        """
        Save the current game state to a file.

        Save player attributes: strength and remaining moves
        """
        # Open file dialog to select save location and ask enter a file name
        filepath = filedialog.asksaveasfilename()

        with open(filepath, 'w') as file:
            # Save player stats
            strength = self.model.get_player_strength()
            moves_remaining = self.model.get_player_moves_remaining()
            file.write(f"{strength} {moves_remaining}\n")

            # Loop through the maze to save its current state
            for i, row in enumerate(self.model.get_maze()):
                for j, col in enumerate(row):
                    # First save player's position
                    if (i, j) == self.model.get_player_position():
                        file.write(PLAYER)
                    # Second save walls positions
                    elif col.get_type() == WALL:
                        file.write(WALL)
                    # Third save entity positions and types
                    else:
                        entity = self.model.get_entities().get((i, j))
                        if entity:
                            if entity.get_type() == CRATE:
                                entity_strength = entity.get_strength()
                                file.write(str(entity_strength))
                            elif entity.get_type() == FANCY_POTION:
                                file.write(FANCY_POTION)
                            elif entity.get_type() == MOVE_POTION:
                                file.write(MOVE_POTION)
                            elif entity.get_type() == STRENGTH_POTION:
                                file.write(STRENGTH_POTION)
                        else:
                            file.write(' ')  # Empty space
                file.write('\n')

    def load_game_state(self):
        """
        Load the game state from a saved file.
        """
        # Open file dialog to select file
        filepath = filedialog.askopenfilename()

        with open(filepath, 'r') as file:
            lines = file.readlines()
            # Extract player stats from the first line
            player_stats = [int(item) for item in lines[0].strip().split(' ')]

            # Adjust loaded player's strength and moves as loaded from the file
            self.model.player_strength = player_stats[0]
            self.model.player_moves_remaining = player_stats[1]

            for i, line in enumerate(lines[1:]):
                row_maze = []
                entities = {}

                # Loop through each character in the current line
                for j, char in enumerate(line.strip()):
                    # If the character represents a PLAYER
                    if char == PLAYER:
                        player_position = (i, j + 1)
                        # Set the player's position in the model
                        self.model._player_position = player_position
                    # If the character represents a WALL
                    elif char == WALL:
                        # Add wall to the row
                        row_maze.append(WALL)
                    else:
                        # Handle entity creation and placement
                        entity = None

                        # Identify the type of entity based on the character
                        if char == CRATE:
                            entity = CRATE()
                        elif char == FANCY_POTION:
                            entity = FANCY_POTION()
                        elif char == MOVE_POTION:
                            entity = MOVE_POTION()
                        elif char == STRENGTH_POTION:
                            entity = STRENGTH_POTION()

                        # Add it to our entities dictionary If their identified an entity
                        if entity:
                            entities[(i, j)] = entity  # Store entity position

                # Add the row to the maze data
                row_maze.append(row_maze)

            # Update the maze and entities based on the loaded data
            self.model.maze = row_maze
            self.model.get_entities()

        # Redraw to continue game
        self.redraw()


def play_game(root: tk.Tk, maze_file: str):
    """
    Play the game using the given maze file and root window.
    """
    # Set root's title
    root.title("Extra Fancy Sokoban")

    # Initialize the game with the provided maze file
    instance = ExtraFancySokoban(root, maze_file)

    # Keep the root window open and listening for events
    root.mainloop()


def main():
    """ The main function. """
    # Create the main application window
    root = tk.Tk()

    # Load the maze file for the game play
    load_maze_file = "maze_files/coin_maze.txt"

    # Start the game
    play_game(root, load_maze_file)


if __name__ == "__main__":
    main()
