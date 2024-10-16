from PIL import ImageTk, Image
from tkinter import Tk
from enum import Enum 

class Direction(Enum):
    EAST = 0
    WEST = 1

class Player:
    def __init__(self, canvas):
        """ Creates a player object in the canvas

        Args:
            canvas (canvas): Canvas
        """        
        self.__canvas = canvas
        self.__eastfiles, self.__westfiles = [], []
        self.__eastimages, self.__westimages = [], []
        self.__jumpingeastfiles, self.__jumpingwestfiles = [], []
        self.__jumpingeastimages, self.__jumpingwestimages = [], []
        self.__xpos = 0
        self.__ypos = 0
        self.__pilImageeast = Image.open('images/player/east/Dead (10).png')
        self.__imgdeadeast = ImageTk.PhotoImage(self.__pilImageeast)
        self.__pilImagewest = Image.open('images/player/west/Dead (10).png')
        self.__imgdeadwest = ImageTk.PhotoImage(self.__pilImagewest)

        # Cycles through all the images for running animations depending on the direction
        for index in range(8):
            self.__eastfiles.append(Image.open(f'images/player/east/Run ({index + 1}).png'))
            self.__westfiles.append(Image.open(f'images/player/west/Run ({index + 1}).png'))
            self.__eastimages.append(ImageTk.PhotoImage(self.__eastfiles[index]))
            self.__westimages.append(ImageTk.PhotoImage(self.__westfiles[index]))
        
        # Cycles through all the images for jump animations depending on the direction
        for index in range(12):
            self.__jumpingeastfiles.append(Image.open(f'images/player/east/Jump ({index + 1}).png'))
            self.__jumpingwestfiles.append(Image.open(f'images/player/west/Jump ({index + 1}).png'))
            self.__jumpingeastimages.append(ImageTk.PhotoImage(self.__jumpingeastfiles[index]))
            self.__jumpingwestimages.append(ImageTk.PhotoImage(self.__jumpingwestfiles[index]))
        
        self.__direction = Direction.EAST
        self.__walkindex = 0
        self.__jumpindex = 0
        self.__width = self.__eastimages[self.__walkindex].width()
        self.__height = self.__eastimages[self.__walkindex].height()
        self.__currentimage = self.__canvas.create_image(self.__xpos, self.__ypos, image=self.__eastimages[self.__walkindex], anchor='c')
        self.__jump = False
        self.__j = None

    def jump(self):
        """ Depending what direction the player jumps, it cycles through the images and add or minus a xpos or ypos
        """        
        self.__j = self.__canvas.after(100, self.jump)
        self.__jump = True
        if self.__direction == Direction.EAST:
            if self.__jumpindex > 0 and self.__jumpindex <= 3:
                self.__xpos += 7
                self.__canvas.coords(self.__currentimage, self.__xpos, self.__ypos)
                self.__canvas.itemconfig(self.__currentimage, image=self.__jumpingeastimages[self.__jumpindex - 1])
            elif self.__jumpindex == 4:
                self.__ypos -= 10
                self.__canvas.coords(self.__currentimage, self.__xpos, self.__ypos)
                self.__canvas.itemconfig(self.__currentimage, image=self.__jumpingeastimages[self.__jumpindex - 1])
            elif self.__jumpindex >= 5 and self.__jumpindex <= 8:
                self.__xpos += 7
                self.__ypos -= 10
                self.__canvas.coords(self.__currentimage, self.__xpos, self.__ypos)
                self.__canvas.itemconfig(self.__currentimage, image=self.__jumpingeastimages[self.__jumpindex - 1])
            elif self.__jumpindex >= 9 and self.__jumpindex <= 11:
                self.__xpos += 7
                self.__ypos += 10
                self.__canvas.coords(self.__currentimage, self.__xpos, self.__ypos)
                self.__canvas.itemconfig(self.__currentimage, image=self.__jumpingeastimages[self.__jumpindex - 1])
            elif self.__jumpindex == 12:
                self.__ypos += 20
                self.__canvas.coords(self.__currentimage, self.__xpos, self.__ypos)
                self.__canvas.itemconfig(self.__currentimage, image=self.__jumpingeastimages[self.__jumpindex - 1])
        
        elif self.__direction == Direction.WEST:
            if self.__jumpindex > 0 and self.__jumpindex <= 3:
                self.__xpos -= 7
                self.__canvas.coords(self.__currentimage, self.__xpos, self.__ypos)
                self.__canvas.itemconfig(self.__currentimage, image=self.__jumpingwestimages[self.__jumpindex - 1])
            elif self.__jumpindex == 4:
                self.__ypos -= 10
                self.__canvas.coords(self.__currentimage, self.__xpos, self.__ypos)
                self.__canvas.itemconfig(self.__currentimage, image=self.__jumpingwestimages[self.__jumpindex - 1])
            elif self.__jumpindex >= 5 and self.__jumpindex <= 8:
                self.__xpos -= 7
                self.__ypos -= 10
                self.__canvas.coords(self.__currentimage, self.__xpos, self.__ypos)
                self.__canvas.itemconfig(self.__currentimage, image=self.__jumpingwestimages[self.__jumpindex - 1])
            elif self.__jumpindex >= 9 and self.__jumpindex <= 11:
                self.__xpos -= 7
                self.__ypos += 10
                self.__canvas.coords(self.__currentimage, self.__xpos, self.__ypos)
                self.__canvas.itemconfig(self.__currentimage, image=self.__jumpingwestimages[self.__jumpindex - 1])
            elif self.__jumpindex == 12:
                self.__ypos += 20
                self.__canvas.coords(self.__currentimage, self.__xpos, self.__ypos)
                self.__canvas.itemconfig(self.__currentimage, image=self.__jumpingwestimages[self.__jumpindex - 1])
        self.__jumpindex += 1
        if self.__jumpindex > 12:
            self.__jumpindex = 0
            if self.__direction == Direction.EAST:
                self.__canvas.itemconfig(self.__currentimage, image=self.__jumpingeastimages[0])
            else:
                self.__canvas.itemconfig(self.__currentimage, image=self.__jumpingwestimages[0])
            self.__canvas.after_cancel(self.__j)
            self.__jump = False

    def breakjump(self):
        """ When the animation of jumping occurs
        """        
        self.__jump = True
        self.__canvas.after_cancel(self.__j)

    def getjump(self):
        """ Returns the jump animation

        Returns:
            jump: defaults to false
        """        
        return self.__jump

    def move(self, dir, xpixels=0, ypixels=0):   
        """ Moving the object to wherever the user wants

        Args:
            dir (direction): Gets the direction of the player
            xpixels (int, optional): how many x pixels you want it to move. Defaults to 0.
            ypixels (int, optional): how many y pixels you want it to move. Defaults to 0.
        """        
        self.__direction = dir
        if self.__walkindex >= len(self.__eastimages):
            self.__walkindex = 0
        self.__ypos += ypixels
        if self.__direction == Direction.EAST:
            self.__xpos += xpixels
            self.__canvas.itemconfig(self.__currentimage, image=self.__eastimages[self.__walkindex])
        elif self.__direction == Direction.WEST:
            self.__xpos -= xpixels
            self.__canvas.itemconfig(self.__currentimage, image=self.__westimages[self.__walkindex])
        self.__canvas.coords(self.__currentimage, self.__xpos, self.__ypos)
        self.__walkindex += 1

    def die(self):
        """ Setting the dead image when it dies depending on the direction
        """        
        if self.__direction == Direction.EAST:
            self.__canvas.itemconfig(self.__currentimage, image=self.__imgdeadeast)
        else:
            self.__canvas.itemconfig(self.__currentimage, image=self.__imgdeadwest)
        self.__canvas.coords(self.__currentimage, self.__xpos, self.__ypos)

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

    def setLocation(self, x, y):
        """ Setting location depending on the x pos and y pos

        Args:
            x (int): sets the x postion
            y (int): sets the y postion
        """        
        self.setX(x)
        self.setY(y)
        self.__canvas.coords(self.__currentimage, self.__xpos, self.__ypos)

    def setX(self, x):
        """ Sets the x position of the object

        Args:
            x (int): x postion of the object
        """
        self.__xpos = x
        self.__canvas.coords(self.__currentimage, self.__xpos, self.__ypos)
    
    def setY(self, y):
        """ Sets the y position of the object

        Args:
            y (int): y postion of the object
        """
        self.__ypos = y
        self.__canvas.coords(self.__currentimage, self.__xpos, self.__ypos)
    
    def getDirection(self):
        """ returns the direction of the object

        Returns:
            direction: gets the direction of the object
        """        
        return self.__direction
    
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
    width = property(getWidth)
    height = property(getHeight)
    x = property(getX, setX)
    y = property(getY, setY)
    right = property(getRight)
    left = property(getLeft)
    bottom = property(getBottom)
    top = property(getTop)