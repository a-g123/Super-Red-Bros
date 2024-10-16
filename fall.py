class Fall():
    def __init__(self, canvas, x=0, y=0):
        """ Creates a canvas rectangle in the canvas where it has a x position and y position

        Args:
            canvas (canvas): Canvas
            x (int, optional): x position. Defaults to 0.
            y (int, optional): y position. Defaults to 0.
        """        
        self.__canvas = canvas
        self.__xpos = x
        self.__ypos = y
        self.__width = 30
        self.__height = 60
        self.__currentimage = self.__canvas.create_rectangle(self.__xpos, self.__ypos, (self.__xpos + 30), (self.__ypos + 60), fill = '#6096ff', outline = '#6096ff')

    def setLocation(self, x, y):  
        """ Setting location depending on the x pos and y pos

        Args:
            x (int): sets the x postion
            y (int): sets the y postion
        """        
        self.__xpos = x
        self.__ypos = y
        self.__update()

    def getWidth(self):
        """ Returns the width of the rectangle

        Args:
            width (width): A width representing the width of the rectangle
        """ 
        return self.__width
    
    def getHeight(self):
        """ Returns the height of the rectangle

        Args:
            height (height): A height representing the height of the rectangle
        """
        return self.__height
    
    def getX(self):
        """ Returns the x pos

        Returns:
            int: x position of the rectangle
        """
        return self.__xpos
    
    def getY(self):
        """ Returns the y pos

        Returns:
            int: y position of the rectangle
        """
        return self.__ypos

    def setX(self, x):
        """ Sets the x position of the rectangle

        Args:
            x (int): x postion of the rectangle
        """ 
        self.__xpos = x
        self.__update()
    
    def setY(self, y):
        """ Sets the y position of the rectangle

        Args:
            y (int): y postion of the rectangle
        """
        self.__ypos = y
        self.__update()
    
    def getRight(self):
        """ Returns the right side of the rectangle

        Returns:
            int: right side
        """
        return self.__xpos + (self.__width / 2)
    
    def getLeft(self):
        """ Returns the left side of the rectangle

        Returns:
            int: left side
        """
        return self.__xpos - (self.__width / 2)

    def getBottom(self):
        """ Returns the bottom side of the rectangle

        Returns:
            int: bottom side
        """
        return self.__ypos + (self.__height / 2)

    def getTop(self):
        """ Returns the top side of the rectangle

        Returns:
            int: top side
        """
        return self.__ypos - (self.__height / 2)

    def __update(self):
        """ updating the current image and the xpos and ypos
        """
        self.__canvas.delete(self.__currentimage)
        self.__currentimage = self.__canvas.create_rectangle(self.__xpos, self.__ypos, (self.__xpos + 30), (self.__ypos + 60), fill = '#6096ff', outline = '#6096ff')

    # Properties of the object
    right = property(getRight)
    left = property(getLeft)
    bottom = property(getBottom)
    top = property(getTop)