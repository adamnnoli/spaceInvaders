"""
Models module for Alien Invaders

This module contains the model classes for the Alien Invaders game. Anything that you
interact with on the screen is model: the ship, the laser bolts, and the aliens.

Just because something is a model does not mean there has to be a special class for
it.  Unless you need something special for your extra gameplay features, Ship and Aliens
could just be an instance of GImage that you move across the screen. You only need a new
class when you add extra features to an object. So technically Bolt, which has a velocity,
is really the only model that needs to have its own class.

With that said, we have included the subclasses for Ship and Aliens.  That is because
there are a lot of constants in consts.py for initializing the objects, and you might
want to add a custom initializer.  With that said, feel free to keep the pass underneath
the class definitions if you do not want to do that.

You are free to add even more models to this module.  You may wish to do this when you
add new features to your game, such as power-ups.  If you are unsure about whether to
make a new class or not, please ask on Piazza.

Adam Nnoli aon2
12-3-2018
"""
from consts import BOLT_HEIGHT, BOLT_WIDTH
from game2d import GImage, GRectangle

# PRIMARY RULE: Models are not allowed to access anything in any module other than
# consts.py.  If you need extra information from Gameplay, then it should be
# a parameter in your method, and Wave should pass it as a argument when it
# calls the method.


class Ship(GImage):
    """
    A class to represent the game ship.

    At the very least, you want a __init__ method to initialize the ships dimensions.
    These dimensions are all specified in consts.py.

    You should probably add a method for moving the ship.  While moving a ship just means
    changing the x attribute (which you can do directly), you want to prevent the player
    from moving the ship offscreen.  This is an ideal thing to do in a method.

    You also MIGHT want to add code to detect a collision with a bolt. We do not require
    this.  You could put this method in Wave if you wanted to.  But the advantage of
    putting it here is that Ships and Aliens collide with different bolts.  Ships
    collide with Alien bolts, not Ship bolts.  And Aliens collide with Ship bolts, not
    Alien bolts. An easy way to keep this straight is for this class to have its own
    collision method.

    However, there is no need for any more attributes other than those inherited by
    GImage. You would only add attributes if you needed them for extra gameplay
    features (like animation). If you add attributes, list them below.

    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    """

    # INITIALIZER TO CREATE A NEW SHIP
    def __init__(self, x, y, width, height, source):
        """
        Create a Ship Object

        This method create a ship object by calling the intializer for a
        GImage Object.

        Parameter: x, x-coordinate of ship center
        Precondition: Must be a number, int or float (center of Game View)

        Parameter: y, y-coordinate of ship center
        Precondition: Must be a number, int or float (SHIP_BOTTOM + height/2)

        Parameter: width, horizontal length of the ship
        Precondition: Must be a number, int or float (SHIP_WIDTH)

        Parameter: height, vertical length of the ship
        Precondition: Must be a number, int or float (SHIP_HEIGHT)

        Parameter: source, image of the ship
        Precondition: string corresponding to a valid image(.png)
        """
        # Call the GImage Initializer
        super().__init__(x=x, y=y, width=width, height=height, source=source)

    # HELPER METHOD TO CHECK FOR COLLISIONS
    def collides(self, bolt):
        """
        Returns: True if the bolt was fired by an alien and collides with the player

        Parameter bolt: The laser bolt to check
        Precondition: bolt is of class Bolt
        """
        left_edge = bolt.x - (BOLT_WIDTH/2)
        right_edge = bolt.x + (BOLT_WIDTH/2)
        top_edge = bolt.y + (BOLT_HEIGHT/2)
        bottom_edge = bolt.y - (BOLT_HEIGHT/2)
        top_left = super().contains((left_edge, top_edge))
        bot_left = super().contains((left_edge, bottom_edge))
        top_right = super().contains((right_edge, top_edge))
        bot_right = super().contains((right_edge, bottom_edge))
        return top_left or bot_left or top_right or bot_right


class Alien(GImage):
    """
    A class to represent a single alien.

    At the very least, you want a __init__ method to initialize the alien dimensions.
    These dimensions are all specified in consts.py.

    You also MIGHT want to add code to detect a collision with a bolt. We do not require
    this.  You could put this method in Wave if you wanted to.  But the advantage of
    putting it here is that Ships and Aliens collide with different bolts.  Ships
    collide with Alien bolts, not Ship bolts.  And Aliens collide with Ship bolts, not
    Alien bolts. An easy way to keep this straight is for this class to have its own
    collision method.

    However, there is no need for any more attributes other than those inherited by
    GImage. You would only add attributes if you needed them for extra gameplay
    features (like giving each alien a score value). If you add attributes, list
    them below.

    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    """

    # INITIALIZER TO CREATE AN ALIEN
    def __init__(self, x, y, width, height, source):
        """
        Creates a single Alien Object

        This method create a single alien object by calling the intializer for a
        GImage Object.

        Parameter: x, x-coordinate of alien center
        Precondition: Must be a number, int or float

        Parameter: y, y-coordinate of alien center
        Precondition: Must be a number, int or float

        Parameter: width, horizontal length of the alien
        Precondition: Must be a number, int or float (ALIEN_WIDTH)

        Parameter: height, vertical length of the alien
        Precondition: Must be a number, int or float (ALIEN_HEIGHT)

        Parameter: source, image of the alien
        Precondition: string corresponding to a valid image(.png)
        """
        # Call GImage Intializer
        super().__init__(x=x, y=y, width=width, height=height, source=source)

    # METHOD TO CHECK FOR COLLISION (IF DESIRED)
    def collides(self, bolt):
        """
        Returns: True if the bolt was fired by the player and collides with this alien

        Parameter bolt: The laser bolt to check
        Precondition: bolt is of class Bolt
        """
        left_edge = bolt.x - (BOLT_WIDTH/2)
        right_edge = bolt.x + (BOLT_WIDTH/2)
        top_edge = bolt.y + (BOLT_HEIGHT/2)
        bottom_edge = bolt.y - (BOLT_HEIGHT/2)
        top_left = super().contains((left_edge, top_edge))
        bot_left = super().contains((left_edge, bottom_edge))
        top_right = super().contains((right_edge, top_edge))
        bot_right = super().contains((right_edge, bottom_edge))
        return top_left or bot_left or top_right or bot_right


class Bolt(GRectangle):
    """
    A class representing a laser bolt.

    Laser bolts are often just thin,white rectangles.  The size of the bolt is
    determined by constants in consts.py. We MUST subclass GRectangle, because we
    need to add an extra attribute for the velocity of the bolt.

    The class Wave will need to look at these attributes, so you will need getters for
    them.  However, it is possible to write this assignment with no setters for the
    velocities.  That is because the velocity is fixed and cannot change once the bolt
    is fired.

    In addition to the getters, you need to write the __init__ method to set the starting
    velocity. This __init__ method will need to call the __init__ from GRectangle as a
    helper.

    You also MIGHT want to create a method to move the bolt.  You move the bolt by adding
    the velocity to the y-position.  However, the getter allows Wave to do this on its
    own, so this method is not required.

    INSTANCE ATTRIBUTES:
        _velocity: The velocity in y direction [int or float]

    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    """

    #Getters and Setters
    def getVelocity(self):
        """
        Returns the velocity of the bolt
        """
        return self._velocity

    # INITIALIZER TO SET THE VELOCITY
    def __init__(self, x, y, BOLT_VELOCITY):
        """
        Creates a single Bolt object

        This method creates a single Bolt object by calling the initializer
        for GRectangle and the setting the bolt velocity.

        Parameter: x, x-coordinate of bolt center
        Precondition: Must be a number, int or float

        Parameter: y, y-coordinate of bolt center
        Precondition: Must be a number, int or float

        Parameter: BOLT_WIDTH, horizontal length of the bolt
        Precondition: Must be a number, int or float (BOLT_WIDTH)

        Parameter: BOLT_HEIGHT, vertical length of the bolt
        Precondition: Must be a number, int or float (BOLT_HEIGHT)

        Parameter: BOLT_VELOCITY, how far the bolt moves each frame
        Precondition: Must be a number, int or float
        """
        # Call GRectangle Initializer
        super().__init__(x=x, y=y, width=BOLT_WIDTH, height=BOLT_HEIGHT, fillcolor="white")

        # Set Velocity
        self._velocity = BOLT_VELOCITY
