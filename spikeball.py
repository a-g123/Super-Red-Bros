from PIL import Image, ImageTk

class Spikeball:
    def __init__(self, canvas,  x=0, y=0):
        """ Creates a spikeball object in the canvas where it has a x position and y position and an angle

        Args:
            canvas (canvas): Canvas
            x (int, optional): x position. Defaults to 0.
            y (int, optional): y position. Defaults to 0.
        """        
        self.__pilImage = Image.open('images/Spike_Ball.png')
        self.__imgball = ImageTk.PhotoImage(self.__pilImage)
        self.__canvas = canvas
        self.__xpos = x
        self.__ypos = y
        self.__width = self.__imgball.width()
        self.__height = self.__imgball.height()
        self.__currentimage = self.__canvas.create_image(self.__xpos, self.__ypos, image=self.__imgball, anchor='c')
        self.__update()
    
    def move(self, xpixels=0, ypixels=0):   
        """ Moning the object 

        Args:
            xpixels (int, optional): how many x pixels you want it to move. Defaults to 0.
            ypixels (int, optional): how many y pixels you want it to move. Defaults to 0.
        """        
        self.__ypos += ypixels
        self.__xpos += xpixels
        self.__canvas.coords(self.__currentimage, self.__xpos, self.__ypos)

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
        """ Returns the height of the object

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
    
    def __update(self):
        """ updating the coordinates
        """
        self.__canvas.coords(self.__currentimage, self.__xpos, self.__ypos)
        
    def getRight(self):
        """ Returns the right side of the object

        Returns:
            int: right side
        """
        return self.__xpos + (self.__width / 2)
    
    def getLeft(self):
        """ Returns the left side of the object

        Returns:
            int: left side
        """
        return self.__xpos - (self.__width / 2)

    def getBottom(self):
        """ Returns the bottom side of the object

        Returns:
            int: bottom side
        """
        return self.__ypos + (self.__height / 2)

    def getTop(self):
        """ Returns the top side of the object

        Returns:
            int: top side
        """
        return self.__ypos - (self.__height / 2)
    
    # Properties of the object
    right = property(getRight)
    left = property(getLeft)
    bottom = property(getBottom)
    top = property(getTop)