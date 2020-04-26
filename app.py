"""
Primary module for Alien Invaders

This module contains the main controller class for the Alien Invaders application. There
is no need for any additional classes in this module.  If you need more classes, 99% of
the time they belong in either the wave module or the models module. If you are unsure
about where a new class should go, post a question on Piazza.

Adam Nnoli aon2
12-2-2018
"""
from consts import *
from game2d import *
from wave import *


# PRIMARY RULE: Invaders can only access attributes in wave.py via getters/setters
# Invaders is NOT allowed to access anything in models.py

class Invaders(GameApp):
    """
    The primary controller class for the Alien Invaders application

    This class extends GameApp and implements the various methods necessary for processing
    the player inputs and starting/running a game.

        Method start begins the application.

        Method update either changes the state or updates the Play object

        Method draw displays the Play object and any other elements on screen

    Because of some of the weird ways that Kivy works, you SHOULD NOT create an
    initializer __init__ for this class.  Any initialization should be done in
    the start method instead.  This is only for this class.  All other classes
    behave normally.

    Most of the work handling the game is actually provided in the class Wave.
    Wave should be modeled after subcontrollers.py from lecture, and will have
    its own update and draw method.

    The primary purpose of this class is to manage the game state: which is when the
    game started, paused, completed, etc. It keeps track of that in an attribute
    called _state.

    INSTANCE ATTRIBUTES:
        view:   the game view, used in drawing (see examples from class)
                [instance of GView; it is inherited from GameApp]
        input:  the user input, used to control the ship and change state
                [instance of GInput; it is inherited from GameApp]
        _state: the current state of the game represented as a value from consts.py
                [one of STATE_INACTIVE, STATE_NEWWAVE, STATE_ACTIVE, STATE_PAUSED, STATE_CONTINUE, STATE_COMPLETE]
        _wave:  the subcontroller for a single wave, which manages the ships and aliens
                [Wave]
        _text:  the currently active message
                [GLabel, or None if there is no message to display]

    STATE SPECIFIC INVARIANTS:
        Attribute _text is only None if _state is STATE_ACTIVE.

    For a complete description of how the states work, see the specification for the
    method update.

    You may have more attributes if you wish (you might want an attribute to store
    any score across multiple waves). If you add new attributes, they need to be
    documented here.

    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY

    _round: the wave number the player is one
            [an int >= 1]
    _previouslives: the number of lives the player had remaning in the last round
            [an int >= 0]
    _alienspeed: The number of seconds between alien steps
            [a float 0 < speed <= 1]
    _gamescore: The score that the player has achieved in the game
            [GLabel Object]
    _scorekeeper: The score that the player has acheived in the game
            [an int >= 0]
    """

    # THREE MAIN GAMEAPP METHODS
    def start(self):
        """
        Initializes the application.

        This method is distinct from the built-in initializer __init__ (which you
        should not override or change). This method is called once the game is running.
        You should use it to initialize any game specific attributes.

        This method should make sure that all of the attributes satisfy the given
        invariants. When done, it sets the _state to STATE_INACTIVE and create a message
        (in attribute _text) saying that the user should press to play a game.
        """
        #Create Game Attributes
        self._state = STATE_INACTIVE
        self._round = 1
        self._scorekeeper = 0
        self._lastroundscore = 0
        self._gamescore = GLabel(text="Score: " + str(self._scorekeeper))
        self._gamescore.linecolor = "white"
        self._gamescore.x = GAME_WIDTH/8
        self._gamescore.y = GAME_HEIGHT-(ALIEN_CEILING/2)
        self._gamescore.font_name = 'RetroGame.ttf'
        self._gamescore.font_size = 25
        self._background = GRectangle(width=GAME_WIDTH, height=GAME_HEIGHT, fillcolor = "black", x = GAME_WIDTH/2, y = GAME_HEIGHT/2)
        #Show starting message
        if self._state == STATE_INACTIVE:
            self._show_welcome_message()
        else:
            self._text = None

    def update(self,dt):
        """
        Animates a single frame in the game.

        It is the method that does most of the work. It is NOT in charge of playing the
        game.  That is the purpose of the class Wave. The primary purpose of this
        game is to determine the current state, and -- if the game is active -- pass
        the input to the Wave object _wave to play the game.

        As part of the assignment, you are allowed to add your own states. However, at
        a minimum you must support the following states: STATE_INACTIVE, STATE_NEWWAVE,
        STATE_ACTIVE, STATE_PAUSED, STATE_CONTINUE, and STATE_COMPLETE.  Each one of these
        does its own thing and might even needs its own helper.  We describe these below.

        STATE_INACTIVE: This is the state when the application first opens.  It is a
        paused state, waiting for the player to start the game.  It displays a simple
        message on the screen. The application remains in this state so long as the
        player never presses a key.  In addition, this is the state the application
        returns to when the game is over (all lives are lost or all aliens are dead).

        STATE_NEWWAVE: This is the state creates a new wave and shows it on the screen.
        The application switches to this state if the state was STATE_INACTIVE in the
        previous frame, and the player pressed a key. This state only lasts one animation
        frame before switching to STATE_ACTIVE.

        STATE_ACTIVE: This is a session of normal gameplay.  The player can move the
        ship and fire laser bolts.  All of this should be handled inside of class Wave
        (NOT in this class).  Hence the Wave class should have an update() method, just
        like the subcontroller example in lecture.

        STATE_PAUSED: Like STATE_INACTIVE, this is a paused state. However, the game is
        still visible on the screen.

        STATE_CONTINUE: This state restores the ship after it was destroyed. The
        application switches to this state if the state was STATE_PAUSED in the
        previous frame, and the player pressed a key. This state only lasts one animation
        frame before switching to STATE_ACTIVE.

        STATE_COMPLETE: The wave is over, and is either won or lost.

        You are allowed to add more states if you wish. Should you do so, you should
        describe them here.

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        # Determine the current state
        if self._state == STATE_INACTIVE:
            #Dismiss the Screen and begn game when user is ready
            self._dismiss_screen()
        if self._state == STATE_NEWWAVE:
            #Start the Game
            self._start_game()
        if self._state == STATE_ACTIVE:
            #Update the Score
            self._update_score()
            #Check if the user wants to pause the game
            curr_keys = self.input.keys
            if "spacebar" in curr_keys:
                self._state = STATE_PAUSED
            #Check if the player needs a new ship, beat the round, or lost the game
            ship = self._wave.getShip()
            if ship is None:
                if self._wave.lives_left() == True:
                    #Create a new ship
                    self._state = STATE_PAUSED
                if not (self._wave.lives_left() == True):
                    #Game Over
                    self._handle_loss()
            if not ship is None:
                if not self._wave.lives_left() == True:
                    #Wave Complete
                    self._handle_win()
            #Let Wave Update handle game objects
            self._wave.update(self.input, dt)
            #Keep track of lives
            self._lives_helper()
        if self._state == STATE_PAUSED:
            #Deal with STATE_PAUSED
            self._handle_pause()

    def draw(self):
        """
        Draws the game objects to the view.

        Every single thing you want to draw in this game is a GObject.  To draw a GObject
        g, simply use the method g.draw(self.view).  It is that easy!

        Many of the GObjects (such as the ships, aliens, and bolts) are attributes in
        Wave. In order to draw them, you either need to add getters for these attributes
        or you need to add a draw method to class Wave.  We suggest the latter.  See
        the example subcontroller.py from class.
        """
        self._background.draw(self.view)
        if self._state == STATE_ACTIVE or self._state == STATE_PAUSED:
            #Show only if Game is Active or Paused
            self._wave.draw(self.view)
            self._gamescore.draw(self.view)
        if not self._text is None:
            #Show if text is there
            self._text.draw(self.view)


    #First Game Beginning Helper Methods
    def _show_welcome_message(self):
        """
        Returns: GLabel Object

        This method creates a GLabel object for the welcome message
        and assigns it to the attribute _text
        """
        #Create A Glabel object for the message
        welcome_message = GLabel(text="Press S to Start \n or Space for \n Intructions")
        welcome_message.x = (GAME_WIDTH/2.0)
        welcome_message.y = (GAME_HEIGHT/2.0)
        welcome_message.font_size = 50
        welcome_message.font_name = 'RetroGame.ttf'
        welcome_message.linecolor = "white"
        #Assign the GLabel Object to the _text attribute
        self._text = welcome_message

    def _displayInstructions(self):
        """
        Creates a shows a message with the instructions on how to play the game.
        """
        #Write the Message
        text = "INSTRUCTIONS \n Goal: Survive for as long as and\n get as many points as"+\
        "possible\n\nCONTROLS\n Up: Fire a Laser Bolt\nLeft: Move Left\nRight: Move Right" + \
        "\n Space: Pause Game\n \nIf you get hit by an alien laser bolt,\n" +\
        "you will lose a life. \nYou will gain a life \nfor every round you survive\n"+\
        "The aliens will speed up\n each time you kill one\n and after every round" +\
        "\nYou will lose the game if\nyou lose all your lives.\n\nPress S to Begin"
        #Create A Glabel object for the message
        intstruction_message = GLabel(text=text)
        intstruction_message.x = (GAME_WIDTH/2.0)
        intstruction_message.y = (GAME_HEIGHT/2.0)
        intstruction_message.font_size = 24
        intstruction_message.font_name = 'RetroGame.ttf'
        intstruction_message.linecolor = "white"
        #Assign the GLabel Object to the _text attribute
        self._text = intstruction_message

    def _dismiss_screen(self):
        """
        Dismisses the Welcome Screen when given an input

        This method determines if the key, 'S', has been pressed down,
        and if so dismisses the welcome screen and changes the state
        of the game to STATE_NEWWAVE
        """
        #Determine What the player wants to do
        curr_keys = self.input.keys
        if 's' in curr_keys: #Start Game
            self._state = STATE_NEWWAVE
            self._text = None
        if "spacebar" in curr_keys: #Show Instructions
            self._displayInstructions()


    #STATE_PAUSED Helpers
    def _handle_pause(self):
        """
        Handles the game when _state is STATE_PAUSED and the player is
        between lives.

        This method deals with the necessary actions when the game is
        paused; display the appropriate message, and starts a new life and sets
        the state back to STATE_ACTIVE when given the appropriate input.
        """
        self._display_pause_message()
        curr_keys = self.input.keys
        if "s" in curr_keys and self._wave.getShip() is None:
            self._wave.new_life()
            self._text = None
            self._state = STATE_ACTIVE
        if "s" in curr_keys and not self._wave.getShip() is None:
            self._text = None
            self._state = STATE_ACTIVE

    def _display_pause_message(self):
        """
        This method creates a GLabel object for the Paused message
        and assigns it to the attribute _text
        """
        #Create A Pause Message to and show remaining lives
        lives = self._wave.getLives()
        lives = str(lives)
        pause_message = GLabel(text="Press 'S' to Continue\n" + lives +\
         " Lives Remaining")
        pause_message.x = (GAME_WIDTH/2.0)
        pause_message.y = (GAME_HEIGHT/2.0)
        pause_message.width = GAME_WIDTH
        pause_message.font_size = 45
        pause_message.font_name = 'RetroGame.ttf'
        pause_message.linecolor = "yellow"
        #Assign message to _text attrbute
        self._text = pause_message



    #STATE_ACTIVE HELPERS
    def _update_score(self):
        """
        Updates the score of the game
        """
        roundScore = self._wave.getRoundScore()
        self._scorekeeper = self._lastroundscore + roundScore
        self._gamescore.text = "Score: " + str(self._scorekeeper)


    #START NEW ROUND HELPERS
    def _handle_win(self):
        """
        This method begins a new round for the Player.

        This method creates a GLabel object to tell the player what round
        they made it to and adds a life for them. It then sents the state to
        STATE_INACTIVE so the player can begin the round when they are ready.
        """
        #Change the Round
        self._round += 1
        #Get speed and score before the new wave is created and they are cleared
        self._alienspeed = self._wave.getAlienSpeed()
        self._lastroundscore += self._wave.getRoundScore() + ROUND_POINTS
        #Create a Display a Next Round Message
        win_message = GLabel(text="Round " +str(self._round) + "\n Press S to Begin")
        win_message.x = (GAME_WIDTH/2.0)
        win_message.y = (GAME_HEIGHT/2.0)
        win_message.font_size = 60
        win_message.font_name = 'RetroGame.ttf'
        self._text = win_message
        #Change State to so update can handle creating the new round
        self._state = STATE_INACTIVE

    def _lives_helper(self):
        """
        Helper method to help keep track of lives between rounds.

        This helper method stores the lives the player has remaining in
        the attribute _previouslives so that it can be accessed later to
        know how many lives the player had left in the previous round
        """
        a = self._wave.getLives()
        if a != -1:
            self._previouslives = a

    def _start_game(self):
        """
        Begins the Game

        This method changes the state of the game from STATE_NEWWAVE to
        STATE_ACTIVE. It creates a new Wave object and assigns it to
        the attribute _wave.
        """
        #Create New Wave
        self._wave = Wave()
        if self._round > 1:
            #Change Lives to reflect actually amount
            lives = self._previouslives + 1
            self._wave.setLives(lives)
            #Speed up the game
            for x in range(self._round):
                self._alienspeed *= A_SPEED_FAC
            self._wave.setAlienSpeed(self._alienspeed)
            #Begin the Wave
        self._state = STATE_ACTIVE


    #Game Over (STATE_COMPLETE) Helpers
    def _handle_loss(self):
        """
        This method creates a GLabel object for the Loss message in
        between lives and assigns it to the attribute _text
        """
        #Create A Game Over Message
        loss_message = GLabel(text="Game Over")
        loss_message.x = (GAME_WIDTH/2.0)
        loss_message.y = (GAME_HEIGHT/2.0)
        loss_message.font_size = 60
        loss_message.font_name = 'RetroGame.ttf'
        loss_message.linecolor = "white"
        self._text = loss_message
        #Change State to Complete
        self._state = STATE_COMPLETE
