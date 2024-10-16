from player import Direction
from PIL import Image, ImageTk

class Door:
    def __init__(self, canvas,  x=0, y=0):
        """ Creates a Door object in the canvas where it has a x position and y position

        Args:
            canvas (canvas): Canvas
            x (int, optional): x position. Defaults to 0.
            y (int, optional): y position. Defaults to 0.
        """        
        self.__pilImage = Image.open('images/door.png')
        self.__imgdoor = ImageTk.PhotoImage(self.__pilImage)
        self.__pilImage2 = Image.open('images/open_door.png')
        self.__imgopendoor = ImageTk.PhotoImage(self.__pilImage2)
        self.__canvas = canvas
        self.__xpos = x
        self.__ypos = y
        self.__width = self.__imgdoor.width()
        self.__height = self.__imgdoor.height()
        self.__currentimage = self.__canvas.create_image(self.__xpos, self.__ypos, image=self.__imgdoor, anchor='c')
        self.__update()
    
    def open(self):
        """ changing the current image to a diffirent images for opening the door
        """        
        self.__currentimage = self.__canvas.create_image(self.__xpos, self.__ypos, image=self.__imgopendoor, anchor='c')
        self.__update()

    def setLocation(self, x, y):
        """ Setting location depending on the x pos and y pos

        Args:
            x (int): sets the x postion
            y (int): sets the y postion
        """          
        self.setX(x)
        self.setY(y)
        self.__update()
                
    def getWidth(self):
        """ Returns the width of the object

        Args:
            width (width): A width representing the width of the object
        """
        return self.__width
    
    def getHeight(self):
        """ Returns the height of the card

        Args:
            height (height): A height representing the height of the object
        """
        return self.__height
    
    def getX(self):
        """ Returns the x pos

        Returns:
            int: x position of the object
        """
        return self.__xpos
    
    def getY(self):
        """ Returns the y pos

        Returns:
            int: y position of the object
        """
        return self.__ypos
                
    def setX(self, x):
        """ Sets the x position of the object

        Args:
            x (int): x postion of the object
        """
        self.__xpos = x
        self.__update()
    
    def setY(self, y):
        """ Sets the y position of the object

        Args:
            y (int): y postion of the object
        """
        self.__ypos = y
        self.__update()
    
    def getRight(self):
        """ Returns the right side of the object

        Returns:
            int: right side
        """
        return self.__xpos + self.__width
    
    def getBottom(self):
        """ Returns the bottom side of the object

        Returns:
            int: bottom side
        """
        return self.__ypos + self.__height
    
    def getTop(self):
        """ Returns the top side of the object

        Returns:
            int: top side
        """
        return self.__ypos - self.__height
    
    def getLeft(self):
        """ Returns the left side of the object

        Returns:
            int: left side
        """
        return self.__xpos - self.__width
    
    def getBounds(self):
        """ getting the bounds of the object

        Returns:
            int: Bounds of the object
        """        
        x1 = self.__canvas.bbox(self.__currentimage)[0] # Left side
        y1 = self.__canvas.bbox(self.__currentimage)[1] # Top side
        x2 = self.__canvas.bbox(self.__currentimage)[2] # Right side
        y2 = self.__canvas.bbox(self.__currentimage)[3] # Bottom side
        bounds = [x1, y1, x2, y2]
        return bounds
    
    def __update(self):
        """ updating the coordinates
        """
        self.__canvas.coords(self.__currentimage, self.__xpos, self.__ypos)
    
    # Properties of the object
    width = property(getWidth)
    height = property(getHeight)