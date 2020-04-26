"""
Subcontroller module for Alien Invaders

This module contains the subcontroller to manage a single level or wave in the Alien
Invaders game.  Instances of Wave represent a single wave.  Whenever you move to a
new level, you are expected to make a new instance of the class.

The subcontroller Wave manages the ship, the aliens and any laser bolts on screen.
These are model objects.  Their classes are defined in models.py.

Most of your work on this assignment will be in either this module or models.py.
Whether a helper method belongs in this module or models.py is often a complicated
issue.  If you do not know, ask on Piazza and we will answer.

Adam Nnoli aon2
12-2-2018
"""
from game2d import *
from consts import *
from models import *
import random
from Sounds import *

# PRIMARY RULE: Wave can only access attributes in models.py via getters/setters
# Wave is NOT allowed to access anything in app.py (Subcontrollers are not permitted
# to access anything in their parent. To see why, take CS 3152)


class Wave(object):
    """
    This class controls a single level or wave of Alien Invaders.

    This subcontroller has a reference to the ship, aliens, and any laser bolts on screen.
    It animates the laser bolts, removing any aliens as necessary. It also marches the
    aliens back and forth across the screen until they are all destroyed or they reach
    the defense line (at which point the player loses). When the wave is complete, you
    should create a NEW instance of Wave (in Invaders) if you want to make a new wave of
    aliens.

    If you want to pause the game, tell this controller to draw, but do not update.  See
    subcontrollers.py from Lecture 24 for an example.  This class will be similar to
    than one in how it interacts with the main class Invaders.

    #UPDATE ME LATER
    INSTANCE ATTRIBUTES:
        _ship:   the player ship to control [Ship]
        _aliens: the 2d list of aliens in the wave [rectangular 2d list of Alien or None]
        _bolts:  the laser bolts currently on screen [list of Bolt, possibly empty]
        _dline:  the defensive line being protected [GPath]
        _lives:  the number of lives left  [int >= 0]
        _time:   The amount of time since the last Alien "step" [number >= 0]


    As you can see, all of these attributes are hidden.  You may find that you want to
    access an attribute in class Invaders. It is okay if you do, but you MAY NOT ACCESS
    THE ATTRIBUTES DIRECTLY. You must use a getter and/or setter for any attribute that
    you need to access in Invaders.  Only add the getters and setters that you need for
    Invaders. You can keep everything else hidden.

    You may change any of the attributes above as you see fit. For example, may want to
    keep track of the score.  You also might want some label objects to display the score
    and number of lives. If you make changes, please list the changes with the invariants.

    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY

    _adirect: the direction that the aliens are moving [string "right" or "left"]
    _afirerate: the number of steps the aliens will take before firing [random integer between 1 and BOLT_RATE]
    _asteps: the number of steps the aliens have taken since last firing [int >= 0]
    _soundshipbolt: the sound made when a bolt is fired from the ship [Sound Object]
    _soundalienbolt: the sound made when a bolt is fired by an alien [Sound Object]
    _soundshipdie: the sound made when the ship is destroyed [Sound Object]
    _soundaliendie: the sound made when an alien is destroyed [Sound Object]
    _lostlives: the number of lives the player lost in the current round[int >= 0]
    _alienspeed: the number of seconds (0 < float <= 1) between alien steps
    _roundscore: the score that the player has achieved in the current round[int >= 0]
    """

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getShip(self):
        """
        Returns: The Ship object of the game
        """
        return self._ship

    def getLives(self):
        """
        Returns: The number of lives remaining
        """
        return self._lives

    def setLives(self, lives):
        """
        Sets the number of lives the player has.

        Parameter: lives
        Precondtion: Must be an int
        """
        self._lives = lives

    def getAlienSpeed(self):
        """
        Returns: The number of seconds between alien steps
        """
        return self._alienspeed

    def setAlienSpeed(self, speed):
        """
        Sets the number of seconds between alien steps to the speed given

        Parameter: Speed
        Precondtion: Must be an float
        """
        #To speed up aliens, factor should be < 1
        #To slow down aliens, factor should be > 1
        self._alienspeed = speed

    def getRoundScore(self):
        """
        Returns: the score that the player has achieved in the current round
        """
        return self._roundscore

    # INITIALIZER (standard form) TO CREATE SHIP AND ALIENS
    def __init__(self):
        """
        Initializes the Wave.

        This method uses helper methods to create the aliens, ship. and defense
        line. It also creates the other attributes necessary for the game.
        """
        self._create_aliens()
        self._create_ship()
        self._create_dline()
        self._adirect = "right"
        self._time = 0
        self._bolts = []
        self._alienspeed = ALIEN_SPEED
        self._afirerate = random.randint(1,BOLT_RATE)
        self._asteps = 0
        self._lives = SHIP_LIVES
        self._lostlives = 0
        self._soundshipbolt = Sound("pew1.wav")
        self._soundalienbolt = Sound("pew2.wav")
        self._soundshipdie = Sound("blast3.wav")
        self._soundaliendie = Sound("blast1.wav")
        self._roundscore = 0

    # UPDATE METHOD TO MOVE THE SHIP, ALIENS, AND LASER BOLTS
    def update(self,input,dt):
        """
        Updates the positions and existence of the game objects.

        This method uses helper methods to update the position of the
        aliens, ship, and bolts and determine if different objects need to
        be removed from the game.
        """
        self._update_ship(input)
        self._update_aliens(dt)
        self._update_bolts(input,dt)
        self._update_score()

    # DRAW METHOD TO DRAW THE SHIP, ALIENS, DEFENSIVE LINE AND BOLTS
    def draw(self,view):
        """
        Draws the Aliens, Ship, Defense Line, and Bolts to the approviate view

        This method calls the draw method for each object in the game
        """
        #Draw ALiens
        for row in self._aliens:
            for alien in row:
                if not alien is None:
                    alien.draw(view)
        #Draw Defense Line
        self._dline.draw(view)
        #Draw Ship
        if not self._ship is None:
           self._ship.draw(view)
         #Draw Bolts
        for bolt in self._bolts:
            bolt.draw(view)

    #Helper Methods for multiple lives
    def lives_left(self):
        """
        Returns True if the player has any lives remaining; False otherwise
        """
        if self._lives >= 0:
            return True
        if self._lives < 0:
            return False

    def new_life(self):
        """
        Creates a new ship object to begin a new life for the player
        """
        self._create_ship()

    #Methods to Crete Game Objects
    def _create_aliens(self):
        """
        Creates the aliens for the game.

        This method creates a 2D list of alien objects and gives it to
        the attribute _aliens.
        """
        result = [] #will hold the nested list
        alien_y = GAME_HEIGHT-ALIEN_CEILING-(ALIEN_ROWS)*(ALIEN_HEIGHT+ALIEN_V_SEP)
        alien_y += ALIEN_HEIGHT/2 #Find the vertical height for the alien row
        c = 0
        if ALIEN_ROWS % 2 == 0: #even number of rows
            for x in range(int(ALIEN_ROWS/2)):
                alien_source = ALIEN_IMAGES[c%(len(ALIEN_IMAGES))] #Find the correct image for the aliens
                for k in range(2): #Create 2 Rows with the image
                    e = self._create_alien_row(alien_source,alien_y) # Create Row
                    alien_y += (ALIEN_V_SEP + ALIEN_HEIGHT) #Move down after each row
                    result.append(e)
                c += 1
        if ALIEN_ROWS % 2 == 1: #odd number of rows
            for x in range(int(ALIEN_ROWS/2.0 -.5)):
                alien_source = ALIEN_IMAGES[c%(len(ALIEN_IMAGES))] #Find the correct image
                for k in range(2): #Create 2 Rows with the image
                    e = self._create_alien_row(alien_source,alien_y) # Create Row
                    alien_y += (ALIEN_V_SEP + ALIEN_HEIGHT) #Move down after each row
                    result.append(e)
                c += 1
            alien_source = ALIEN_IMAGES[c%(len(ALIEN_IMAGES))]
            e = self._create_alien_row(alien_source,alien_y) #Make last row
            result.append(e)
        self._aliens = result

    def _create_alien_row(self,image,y):
        """
        Creates 1 row of aliens.

        This method creates 1 row of aliens using the image provided
        starting at the y coordinate provided.

        Parameter: image, the image of the aliens in the row
        Precondition: String representing an image file

        Parameter: y, the height of the alien row
        Precondition: Must be a number, float or int
            (DEFENSE_LINE < y < GAME_HEIGHT - ALIEN_CEILING)
        """
        alien_x = ALIEN_H_SEP + (ALIEN_WIDTH/2)
        row = []
        for i in range(ALIENS_IN_ROW):# Make Each Alien in the row
            alien= Alien(x=alien_x, y=y, width=ALIEN_WIDTH,
                            height=ALIEN_HEIGHT, source=image)
            alien_x += (ALIEN_WIDTH + ALIEN_H_SEP) # Move over for each alien
            row.append(alien)
        return row

    def _create_ship(self):
        """
        Creates the Ship for the Game

        This method initializes a new Ship object
        and assigns it to the attribute _ship
        """
        #Find Ship Coordinates
        x = GAME_WIDTH/2
        y = SHIP_BOTTOM + (SHIP_HEIGHT/2)
        # Create Ship Object
        result = Ship(x, y, SHIP_WIDTH, SHIP_HEIGHT, 'ship.png')
        self._ship = result

    def _create_dline(self):
        """
        Creates the Defense Line for the Game

        This method initializes a new GPath object
        and assigns it to the attribute _dline
        """
        #Find Endpoints
        points = [0,DEFENSE_LINE, GAME_WIDTH, DEFENSE_LINE]
        #Create GPath Object
        self._dline = GPath(points=points, linewidth = 1,linecolor = "black")

    def _create_bolt(self, x, y, BOLT_VELOCITY):
        """
        Returns: A Bolt object

        This method creates a single Bolt object for the game

        Parameter: x, the x coordinate of the center of the bolt
        Precondition: Must be a number, float or int
            (0 < x < GAME_WIDTH)

        Parameter: y, the height of the alien row
        Precondition: Must be a number, float or int
            (0 < y < GAME_HEIGHT - ALIEN_CEILING)

        Parameter: BOLT_VELOCITY,
        Precondition: A float #Use positive or negative velocity to
            determine if the bolt was shot by the ship or an alien
        """
        #Create Bolt object
        bolt = Bolt(x,y,BOLT_WIDTH, BOLT_HEIGHT,BOLT_VELOCITY)
        return bolt

    #Methods to Update Game Objects

    #Update Ship Object
    def _update_ship(self, input):
        """
        Updates the Ship's Position and life.

        This method moves the ship left or right depending on user input, and
        calls a helper method to determine if the ship has been hit by a bolt
        and needs to be destroyed.
        """
        #Check what keys the user is inputing
        curr_keys = input.keys
        if not self._ship is None:
            #Move ship left or right as necessary
            if "left" in curr_keys:
                self._ship.x -= SHIP_MOVEMENT
            if "right" in curr_keys:
                self._ship.x += SHIP_MOVEMENT
            #Check if ship went off-screen and move it back
            if self._ship.x + SHIP_WIDTH > GAME_WIDTH:
                self._ship.x -= GAME_WIDTH
            if self._ship.x - SHIP_WIDTH < 0:
                self._ship.x += GAME_WIDTH
            #Call helper to see if ship was hit
            self._kill_ship()

    #Update Alien Objects
    def _update_aliens(self,dt):
        """
        Updates the position of the aliens and removes the aliens that have died.

        This method checks if enough time has passed and if so calls a helper
        method to move the aliens. This method also calls a helper method to
        check if any aliens have been hit by bolts and if so removes them.
        This method also checks if all of the aliens have been destroyed and the
        win condition has been met.
        """
        #Call helper to see if all aliens have been destroyed
        self._check_win()

        #Check to see if the aliens should be moved
        if self._time >= self._alienspeed:
            self._move_aliens() #Call helper to move them if necessary
            self._time = 0 #reset time
        else:
            self._time += dt #add time if alins have not moved

        #Call helper to check if any aliens have been killed
        self._kill_aliens()

    def _move_aliens(self):
        """
        Moves the aliens to their correct position

        This method checks to see if the aliens need to be moved down, left,
        or right, and then calls the appropriate helper function.
        """
        self._asteps += 1 #Keep track of number of steps taken to see when to fire
        alien_xs = []
        #Check if aliens should move down and change direction
        for row in self._aliens:
            for alien in row:
                if not alien is None:
                    alien_xs.append(alien.x)
        if len(alien_xs) == 0:
            self._check_win()
        else:
            furthest_left = max(alien_xs)
            furthest_right = min(alien_xs)
            #Move down and march left
            if furthest_left > GAME_WIDTH - ALIEN_H_SEP and self._adirect == "right":
                self._move_aliens_down()
                self._adirect = "left"
            #Move down and march right
            if furthest_right < ALIEN_H_SEP and self._adirect == "left":
                self._move_aliens_down()
                self._adirect = "right"
            #Call helpers to move left or right
            if self._adirect == "left":
                self._move_aliens_left()
            if self._adirect ==  "right":
                self._move_aliens_right()

    def _move_aliens_right(self):
        """
        Moves the aliens right ALIEN_H_WALK
        """
        for row in self._aliens:
            for alien in row:
                if not alien is None:
                    alien.x += ALIEN_H_WALK

    def _move_aliens_left(self):
        """
        Moves the aliens left ALIEN_H_WALK
        """
        for row in self._aliens:
            for alien in row:
                if not alien is None:
                    alien.x -= ALIEN_H_WALK

    def _move_aliens_down(self):
        """
        Moves the aliens down ALIEN_V_WALK
        """
        for row in self._aliens:
            for alien in row:
                if not alien is None:
                    alien.y -= ALIEN_V_WALK
                    #Check if Aliens passed the Defense line
                    if alien.y < DEFENSE_LINE:
                        self._lives = -1
                        self._ship = None
                        #Set lives to -1 and ship to None so Invaders update
                        #takes care of ending the round in the next frame

    #Update Bolt Objects
    def _update_bolts(self,input, dt):
        """
        Creates and Moves Bolts
        """
        #Create Ship Bolts
        curr_keys = input.keys
        if "up" in curr_keys and (not self._ship is None) and (not self._isPlayerBolt()):
            x = self._ship.x
            y = self._ship.y + (SHIP_HEIGHT/2)
            bolt = self._create_bolt(x, y, BOLT_SPEED)
            self._bolts.append(bolt)
            self._soundshipbolt.play(loop=False)
        
        #Create Alien Bolts
        if self._asteps == self._afirerate: #Check if aliens have taken enough steps
            self._fire_alien_bolt()
            self._asteps = 0

        #Move Bolts
        for bolt in self._bolts:
            bolt.y += bolt.getVelocity()
            if bolt.y > GAME_HEIGHT or bolt.y < 0:
                self._bolts.remove(bolt)
                #Get rid of bolts that have gone off-screen

    def _fire_alien_bolt(self):
        """
        Fires a Bolt from a single Alien
        """
        #Choose an alien to fire from
        b = []
        while len(b) == 0:
            a = random.randint(0,ALIENS_IN_ROW-1) #Choose random column
            for row in self._aliens:
                c = row[a] #Gather all aliens in the column
                if not c is None:
                    b.append(c)
        #Find the alien at the lowest height the column
        d = []
        for alien in b:
            e = alien.y
            d.append(e)
        f = d.index(min(d))
        g = b[f]
        #Create the Bolt for the alien
        a = self._create_bolt(g.x, g.y - (ALIEN_HEIGHT/2), -1 * BOLT_SPEED)
        #Make Bolt Velocity negative to show alien bolt
        self._soundalienbolt.play(loop=False) #Play the alien bolt sound
        self._bolts.append(a)

    def _isPlayerBolt(self):
        """
        Returns: True if a bolt made by the player is currently on the screen
        """
        for bolt in self._bolts:
            if bolt.getVelocity() > 0: #Pos velocity means fired by ship
                return True
        return False

    #Update Score
    def _update_score(self):
        """
        Updates the score for the round, ALIEN_POINTS per each alien killed
        """
        self._roundscore = 0 #Reset Score to only add when alien killed
        for row in self._aliens:
            for alien in row:
                if alien is None: #For each alien killed add points
                    self._roundscore += ALIEN_POINTS

    #Methods to Handle Collisions
    def _kill_aliens(self):
        """
        Checks if any aliens have collided with a bolt and if so kills them,
        plays the appropriate sound, and removes the bolt.
        """
        for bolt in self._bolts:
            #Only Check Ship Bolts
            if bolt.getVelocity() > 0:
                for row in self._aliens:
                    for alien in row:
                        if not alien is None:
                            if alien.collides(bolt):
                                #Kill Alien, Play Sound, Remove Bolt, Change Speed
                                row[row.index(alien)] = None
                                self._soundaliendie.play(loop=False)
                                self._bolts.remove(bolt)
                                self.setAlienSpeed(self._alienspeed * A_SPEED_FAC)

    def _kill_ship(self):
        """
        Checks to see if the ship has been destroyed.

        This method checks to see if a bolt fired from an alien has hit the
        ship and if so destroys the ship and changes the amount of lives the
        player has left and has lost to the correct number.
        """
        for bolt in self._bolts:
            #Only Check ALien Bolts
            if bolt.getVelocity() < 0 and not self._ship is None and self._ship.collides(bolt):
                    #Kill Ship, Play Sund, Remove Bolt, Change Lives
                    self._ship = None
                    self._soundshipdie.play(loop=False)
                    self._bolts.remove(bolt)
                    self._lives -= 1
                    self._lostlives += 1

    #Method to See if the round has been completed
    def _check_win(self):
        """
        Checks to see if the player has completed the round

        This method checks to see if all the aliens are None, have been
        destroyed, and if so sets the number of lives for the player to -1
        to trigger the update method in Invaders to create a new round.
        """
        dead_aliens = 0
        for row in self._aliens:
            for alien in row:
                if alien is None: #if the alien is None add to a
                    dead_aliens += 1
        #Check if all of the aliens in the wave are dead
        if dead_aliens == ALIEN_ROWS*ALIENS_IN_ROW:
            self._lives = -1
            self._bolts.clear()
