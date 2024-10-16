'''
Name: Arshia Goraya and Gio Rafael Dela Cruz
Course Code: ICS4U1-01
Date: Thursday, January 20, 2023
Program Name: CPT - Super Red Bros
'''
#Import tkinter, PIL, ghost class, player class, spikeball class, door class, fall class, pygame
from tkinter import Tk, Canvas, Toplevel, messagebox, Radiobutton, Label, font
from tkinter import *
from PIL import ImageTk, Image
from player import Player, Direction
from ghost import Ghost
from door import Door
from spikeball import Spikeball
import pygame
from pygame import mixer
from fall import Fall

#initalize pygame mixer and set the sound effects
pygame.mixer.init()
pygame.mixer.music.load("sounds/background.wav")
pygame.mixer.music.set_volume(0.1)
dying = mixer.Sound('sounds/dying.wav')
dying.set_volume(0.1)
won = mixer.Sound('sounds/passedsound.wav')
won.set_volume(0.1)

#function that times how long the user takes to complete the level
def timer():
    global seconds, min, canvas, timerid, outputtime, dead, win
    timerid = root.after(1000, timer)
    #if the player dies or wins the timer stops and the replay function is called
    if dead == True:
        root.unbind('<KeyPress>')
        root.after_cancel(timerid)
        root.after(2000, die)
    elif win == True:
        root.after_cancel(timerid)
        root.after(2000, winner)
    else:
        seconds += 1
        if seconds == 60:
            min += 1
            seconds = 0
            canvas.itemconfig(outputtime, text=f'TIME: {min}min {seconds}sec')
        if min == 0:
            canvas.itemconfig(outputtime, text=f'TIME: {seconds}')
        else:
            canvas.itemconfig(outputtime, text=f'TIME: {min}min {seconds}sec')

#replay function if the player dies
def die():
    global howlose, selection, gmove, gdown, gup, ghostcallcount, dead, win, timerid, seconds, min, j, ball, dcollisionid, gcollisionid, canvas, p, bgoutput, d, g, b, outputtime, seconddrop, kill, overpic, fdown, thirddrop, fcollisionid, f, firstdrop
    #reverts all variables to what they were initially
    canvas.delete(overpic)
    canvas.delete(bgoutput)
    canvas.delete(outputtime)
    canvas.delete(p)
    canvas.delete(d)
    if fdown != None:
        root.after_cancel(fdown)
    gmove = None
    gdown = None
    gup = None
    ghostcallcount = 0
    timerid = None
    seconds = 0
    min = 0
    j = None
    ball = None
    dcollisionid = None
    gcollisionid = None  
    fcollisionid = None 
    bgoutput = None
    if g != []:
        for x in g:
            canvas.delete(x)
            g.remove(x)
        g = []
    if b != []:
        for x in b:
            canvas.delete(x)
            b.remove(x)
        b = []
    if f != []:
        for x in f:
            canvas.delete(x)
            f.remove(x)
        f = []
    outputtime = None
    firstdrop = None
    seconddrop = None   
    thirddrop = None       
    kill = 0
    root.unbind('<KeyPress>')
    root.geometry(f'1x1+{0-50}+{0-50}')
    #if the player loses because of a ghost the ghost message box appears and asks if you want to replay - if they dont want to replay they will be brought to the level window
    if howlose == 'ghost':
        answer = messagebox.askyesno('Super Red Bros', f'boo hoo you lost!\nWould you like to play again?')
        if answer == True:
            root.bind('<KeyPress>', onkeypress)
            dead = False
            win = False
            if selection == 'L1':
                L1()
            elif selection == 'L2':
                L2()
            elif selection == 'L3':
                L3()
        else:
            dead = False 
            win = False
            level_window()
    #if the player loses because of a spike ball or hole the message box appears and asks if you want to replay - if they dont want to replay they will be brought to the level window
    elif howlose == 'spikeball':
        answer = messagebox.askyesno('Super Red Bros', f'You lost!\nWould you like to play again?')
        if answer == True:
            root.bind('<KeyPress>', onkeypress)
            dead = False 
            win = False
            if selection == 'L1':
                L1()
            elif selection == 'L2':
                L2()
            elif selection == 'L3':
                L3()
        else:
            dead = False 
            win = False
            level_window()

#replay function if the user wins
def winner():
    global howlose, selection, gmove, gdown, gup, ghostcallcount, dead, win, timerid, seconds, min, j, ball, dcollisionid, gcollisionid, canvas, p, bgoutput, d, g, b, outputtime, seconddrop, kill, winpic, fcollisionid, thirddrop, f, firstdrop
    #reverts all variables to what they were initially
    canvas.delete(winpic)
    canvas.delete(bgoutput)
    canvas.delete(outputtime)
    canvas.delete(p)
    canvas.delete(d)
    gmove = None
    gdown = None
    gup = None
    ghostcallcount = 0
    timerid = None
    j = None
    ball = None
    dcollisionid = None
    gcollisionid = None  
    fcollisionid = None 
    bgoutput = None
    if g != []:
        for x in g:
            canvas.delete(x)
            g.remove(x)
        g = []
    if b != []:
        for x in b:
            canvas.delete(x)
            b.remove(x)
        b = []
    if f != []:
        for x in f:
            canvas.delete(x)
            f.remove(x)
        f = []
    outputtime = None
    firstdrop = None
    seconddrop = None   
    thirddrop = None      
    kill = 0
    root.unbind('<KeyPress>')
    root.geometry(f'1x1+{0-50}+{0-50}')
    #if the user was on level 1 or level 2 they will be asked if they want to move onto the next level - if they dont want to they will be brought to the level window
    if selection == 'L1' or selection == 'L2':
        answer = messagebox.askyesno('Super Red Bros', f'Congratulations on winning the level in {min} minutes and {seconds} seconds!\nWould you like to move on to the next level?')
        min = 0
        seconds = 0
        if answer == True:
            dead = False 
            win = False
            root.bind('<KeyPress>', onkeypress)
            if selection == 'L1':
                L2()
                selection = 'L2'
            elif selection == 'L2':
                L3()
                selection = 'L3'
        if answer == False:
            dead = False 
            win = False
            level_window()
    #if the user was on level 3 they are told all levels are done they can either replay certain levels or exit the game
    else:
        answer = messagebox.askyesno('Super Red Bros', f'Congratulations on beating the heardest level in {min} minutes and {seconds} seconds!\nYou have completed all the current levels, would you like to select another level?')
        min = 0
        seconds = 0
        if answer == True:
            level_window()
        if answer == False:
            close_option()

#variable to ensure the space bar is only pressed once 
counter = 0
def onkeypress(event):
    global counter, startjump
    if counter == 0:
        if event.char == ' ':
            close_splashscreen()
    elif counter > 0:
        #moves the player right
        if event.keysym == 'Right' or event.keysym == 'd':
            p.move(Direction.EAST, 3)
            rightKey()
        #moves the player left
        elif event.keysym == 'Left' or event.keysym == 'a':
            p.move(Direction.WEST, 3)
            leftKey()
        #makes the player jump
        elif event.keysym == 'Up' or event.keysym == 'w':
            root.unbind('<KeyPress>')
            startjump = True
            p.jump()
            jumpcheck()
    counter += 1

#variable to ensure the right side bounds and makes the background move at certain points - also keeps objects in current place - does not allow them to move
def rightKey():
    global canvas, p, bgoutput, g, b, f
    if p.getX() > 600 and p.getX() < 700:
        canvas.move(bgoutput, -1, 0)
        d.setX(d.getX() - 3)
        for x in g:
            x.setX(x.getX() - 1)
        if len(b) > 0:
            for x in b:
                x.setX(x.getX() - 1)
        if len(f) > 0:
            for x in f:
                x.setX(x.getX() - 1)
    elif p.getX() > 100 and p.getX() < 200:
        canvas.move(bgoutput, -1, 0)
        d.setX(d.getX() - 3)
        for x in g:
            x.setX(x.getX() - 1)
        if len(b) > 0:
            for x in b:
                x.setX(x.getX() - 1)
        if len(f) > 0:
            for x in f:
                x.setX(x.getX() - 1)
    # the player is not allowed to leave the screen -- if they do they will be relocated to the right
    if p.x + p.width / 2 >= 795:
        p.setX(canvas.winfo_width() - (p.width/2))
    canvas.focus_set()

#variable to ensure the left side bounds and makes the background move at certain points
def leftKey():
    global canvas, p, bgoutput, g, b
    if p.getX() > 600 and p.getX() < 700:
        canvas.move(bgoutput, 1, 0)
        d.setX(d.getX() + 3)
        for x in g:
            x.setX(x.getX() + 1)
        if len(b) > 0:
            for x in b:
                x.setX(x.getX() + 1)
        if len(f) > 0:
            for x in f:
                x.setX(x.getX() + 1)
    elif p.getX() > 100 and p.getX() < 200:
        canvas.move(bgoutput, 1, 0)
        d.setX(d.getX() + 3)
        for x in g:
            x.setX(x.getX() + 1)
        if len(b) > 0:
            for x in b:
                x.setX(x.getX() + 1)
        if len(f) > 0:
            for x in f:
                x.setX(x.getX() + 1)
    # the player is not allowed to leave the screen -- if they do they will be relocated to the left
    if p.x - (p.width / 2) <= 5:
        p.setX(p.width / 2)
    canvas.focus_set()

#variable that checks for jumping 
j = None
def jumpcheck():
    global startjump
    #checks to see when jump has stopped
    j = root.after(1, jumpcheck)
    #once jump has stoped - timer stopped and keys rebinded
    if p.getjump() == False:
        #if the player dies while jumping they complete their jump then fall and die
        if dead != True:
            root.bind('<KeyPress>', onkeypress)
            root.after_cancel(j)
            j = None
        else:
            p.die()
    # if the jump just begins a key is called based on direction
    if startjump == True:
        if p.getDirection() == Direction.EAST:
            rightKey()
        elif p.getDirection() == Direction.WEST:
            leftKey()
    startjump = False
    #ensures the boundaries are maintained and the user cannot pass the screen
    if p.x - (p.width / 2) <= 5:
        p.setX(p.width / 2)
    if p.x + p.width / 2 >= 795:
        p.setX(canvas.winfo_width() - (p.width/2))

#the user must select a level at the start of the game - once they click ready the game screen shows up and the game begins
selection = 'L1'
def ready():
    global selection, dead, win
    close_levelwindow()
    if selection == 'L1':
        L1()
    elif selection == 'L2':
        L2()
    else:
        L3()
    root.bind('<KeyPress>', onkeypress)
    dead = False
    win = False

#function checks the users level selection 
def select_level():
    global selection
    if radioVariable.get() == 0:
        selection = 'L1'
    elif radioVariable.get() == 1:
        selection = 'L2'
    elif radioVariable.get() == 2:
        selection = 'L3'

#function opens a level window
def level_window():
    selection_window.geometry(f'{selection_window.winfo_width()}x{selection_window.winfo_height()}+{root.winfo_screenwidth() // 2 - selection_window.winfo_width() // 2}+{root.winfo_screenheight() // 2 - selection_window.winfo_height() // 2}')
    selection_window.deiconify()

#function closes the level window
def close_levelwindow():
    selection_window.withdraw()

#fucntion closes the start splash screen
def close_splashscreen():
    root.deiconify()
    splash_screen.withdraw()
    #asks the user if they want to read the instructions before playing - if they dont the screen automatically goes to the level window
    answer = messagebox.askyesno('Super Red Bros', 'Hello! We are excited to have you!\nWould you like to read the instructions before playing?')
    if answer == True:
        messagebox.showinfo('Super Red Bros', 'Game: Super Red Bros\n\nObjective: Complete all the levels while avoiding obstacles. The goal is to get to the door and pass the levels.\n*there are three levels*\n\nKeys of Use:\nspace: starts the game\nleft key and a key: moves the player left\nright key and d key: moves the player right\nup key and w key: makes the player jump\n\nObstacles:\nspikeball: at random points in the games a spikeball will fall directly above the player - user objective to avoid them by moving left or right\nghost: ghosts move up and down - user objective to avoid them\nholes: the map in level 2 and 3 has holes - user objective to jump over them')
    level_window()

#function for if user tries to close game
def close_option():
    #music stops
    pygame.mixer.music.pause()
    #message prompt asking if user wants to exit
    answer = messagebox.askyesno("Super Red Bros", "Are you sure you want to exit?")
    #if user says yes, exit game, if not, continue the game and the music will recontinue
    if answer == True:
        messagebox.showinfo("Super Red Bros", "Thank you for playing Super Red Bros!")
        exit()
    else:
        pygame.mixer.music.unpause()

#function moves ghost up and down when the ghost reachs a certain point
def move_ghost():
    global g, gmove, gdown, gup, ghostcallcount
    gmove = root.after(1, move_ghost)
    if ghostcallcount == 0:
        gdown = root.after(100, g_down)
        gup = root.after(100, g_up)
        gcollide()
    #if the ghost reaches a point less than 30 it will start moving down
    if len(g) > 0:
        if g[0].getY() <= 30:
            root.after_cancel(gup)
            g[0].move(0, 2)
            gdown = root.after(100, g_down)
        #if the ghost reaches a point greater than 130 it will start moving up 
        elif g[0].getY() >= 130:
            root.after_cancel(gdown)
            g[0].move(0, -2)
            gup = root.after(100, g_up)
    ghostcallcount += 1

#function moves the ghost down
def g_down():
    global gdown, g, dead, win
    if dead != True or win != True:
        for x in g:
            x.move(0, 2)
        gdown = root.after(100, g_down)
    else:
        root.after_cancel(gdown)

#function moves the ghost up
def g_up():
    global gup, g, dead, win
    if dead == False or win == False:
        for x in g:
            x.move(0, -2)
        gup = root.after(100, g_up)
    else:
        root.after_cancel(gup)

#function that is called when the spikeball is about to drop to get the x position of the player to make sure the ball goes over the player
def dropspike():
    global b, p
    if len(b) > 0:
        b[0].setLocation(p.getX(), -5)
        movespikeball()

#function that moves the spikeball down and checks when it reaches a certain point to remove the spike ball from the list
def movespikeball():
    global b, ball, balltimerid
    if b[0].getY() >= 130:
        root.after(300, removespikeball)
    else:
        b[0].move(0, 5)
        ball = root.after(50, movespikeball)
        bcollide()
    if len(b) == 0:
        root.after_cancel(ball)
        root.after_cancel(balltimerid)
        balltimerid = None
        ball = None
    
#function removes the spikeball from the list
def removespikeball():
    global b, ball
    for x in b:
        if x.getY() >= 130:
            b.remove(x)

#function that checks for collision with the door
def dcollide():
    global dcollisionid, d, p, win, j, winpic, gcollisionid, gmove, gup, gdown, fcollisionid, fdown, firstdrop, seconddrop, thirddrop
    dcollisionid = root.after(1, dcollide)
    #checks for left and right collision
    if p.right >= d.getLeft() and p.left <= d.getRight():
        #checks for top and bottom collision
        if p.bottom >= d.getTop() and p.top <= d.getBottom():
            #once collision is confirmed the timers stop, music stops, movement stops and the player has won the level, the player is removed from the screen
            root.after_cancel(dcollisionid)
            p.setLocation(-3000,-3000)
            root.unbind('<KeyPress>')
            win = True
            d.open()
            pygame.mixer.music.stop()
            won.play()
            winpic = canvas.create_image(400, 84, image=imgpassed, anchor='c')
            canvas.focus_set()
            root.after_cancel(gmove)
            root.after_cancel(gup)
            root.after_cancel(gdown)
            root.after_cancel(gcollisionid)
            if balltimerid != None:
                root.after_cancel(balltimerid)
            if ball != None:
                root.after_cancel(balltimerid)
            if fcollisionid != None:
                root.after_cancel(fcollisionid)
            if fdown != None:
                root.after_cancel(fdown)
                fdown = None
            if firstdrop != None:
                root.after_cancel(firstdrop)
            if seconddrop != None:
                root.after_cancel(seconddrop)
            if thirddrop != None:
                root.after_cancel(thirddrop)

#variable that states how the player died so the correct message box appears 
howlose = None
#variables to check for ball collision
def bcollide():
    global b, balltimerid, ball, seconddrop, thirddrop, gdown, gup, dead, dcollisionid, j, howlose, overpic, fcollisionid, gcollisionid, fdown
    balltimerid = root.after(100, bcollide)
    #goes through every ball
    for x in b:
        #checks for left and right collision
        if p.right >= x.left + 3 and p.left <= x.right - 3:
            #checks for top and bottom collision
            if p.bottom >= x.top and p.top <= x.bottom - 12:
                #once collision is confirmed the timers stop, music stops, movement stops and the player is dead
                p.die()
                dead = True
                pygame.mixer.music.stop()
                dying.play()
                overpic = canvas.create_image(400, 84, image=imgOver, anchor='c')
                canvas.focus_set()
                root.unbind('<KeyPress>')
                root.after_cancel(balltimerid)
                root.after_cancel(ball)
                if firstdrop != None:
                    root.after_cancel(firstdrop)
                if seconddrop != None:
                    root.after_cancel(seconddrop)
                if thirddrop != None:
                    root.after_cancel(thirddrop)
                root.after_cancel(gmove)
                root.after_cancel(gup)
                root.after_cancel(gdown)
                root.after_cancel(dcollisionid)
                root.after_cancel(gcollisionid)
                if fcollisionid != None:
                    root.after_cancel(fcollisionid)
                if fdown != None:
                    root.after_cancel(fdown)
                    fdown = None
                howlose = 'spikeball'
                for x in b:
                    x.setLocation(p.x, p.y - 15)
                
#variable to check for ghost collsion                
def gcollide():
    global gcollisionid, gup, gdown, gmove, dead, dcollisionid, j, howlose, overpic, kill, balltimerid, b, fcollisionid, fdown
    gcollisionid = root.after(100, gcollide)
    #goes through every ghost
    for x in g:
        #goes through every ball
        if p.right >= x.left + 8 and p.left <= x.right - 8:
            #checks for top and bottom collision
            if p.bottom >= x.top and p.top <= x.bottom - 13:
                #ensures the player only dies once
                if kill == 0:
                    #once collision is confirmed the timers stop, music stops, movement stops and the player is dead
                    p.die()
                    pygame.mixer.music.stop()
                    dying.play()
                    overpic = canvas.create_image(400, 84, image=imgOver, anchor='c')
                    canvas.focus_set()
                    if j != None:
                        root.after_cancel(j)
                        p.breakjump()
                        root.bind('<KeyPress>', onkeypress)
                    root.unbind('<KeyPress>')
                    root.after_cancel(gcollisionid)
                    if fcollisionid != None:
                        root.after_cancel(fcollisionid)
                    if balltimerid != None:
                        root.after_cancel(balltimerid)
                    if ball != None:
                        root.after_cancel(ball)
                    dead = True
                    root.after_cancel(gmove)
                    root.after_cancel(gdown)
                    root.after_cancel(gup)
                    root.after_cancel(dcollisionid)
                    if firstdrop != None:
                        root.after_cancel(firstdrop)
                    if seconddrop != None:
                        root.after_cancel(seconddrop)
                    if thirddrop != None:
                        root.after_cancel(thirddrop)
                    howlose = 'ghost'
                    if fdown != None:
                        root.after_cancel(fdown)
                        fdown = None
                kill += 1
                break

fcollisionid = None
#variable to check for hole collsion
def fcollide():
    global gcollisionid, gup, gdown, gmove, dead, dcollisionid, j, howlose, overpic, kill, balltimerid, b, fcollisionid, fdown, firstdrop, seconddrop, thirddrop
    fcollisionid = root.after(1, fcollide)
    #goes through every ghost
    for x in f:
        #checks for top and bottom collision
        if p.right >= x.left + 45 and p.left <= x.right - 10:
            #checks for top and bottom collision
            if p.bottom >= x.top + 10 and p.top <= x.bottom:
                #once collision is confirmed the timers stop, music stops, movement stops and the player is dead
                pygame.mixer.music.stop()
                dying.play()
                overpic = canvas.create_image(400, 84, image=imgOver, anchor='c')
                canvas.focus_set()
                dead = True
                root.unbind('<KeyPress>')
                root.after_cancel(fcollisionid)
                if balltimerid != None:
                    root.after_cancel(balltimerid)
                if ball != None:
                    root.after_cancel(ball)
                if firstdrop != None:
                    root.after_cancel(firstdrop)
                if seconddrop != None:
                    root.after_cancel(seconddrop)
                if thirddrop != None:
                    root.after_cancel(thirddrop)
                root.after_cancel(gmove)
                root.after_cancel(gup)
                root.after_cancel(gdown)
                root.after_cancel(dcollisionid)
                howlose = 'spikeball'
                #calls the function to make the player move down
                fall()

fdown = None
#function that make the player move down when they land in a hole
def fall():
    global fdown
    fdown = root.after(100, fall)
    p.setY(p.getY() + 2)
    if p.getY() == 180:
        root.after_cancel(fdown)
        fdown = None

#fucntion for level one
def L1():
    global canvas, p, bgoutput, d, root, g, b, outputtime, seconddrop, c, firstdrop
    #setting the screen
    SCREEN_WIDTH, SCREEN_HEIGHT = 800, 168
    backgroundx = (SCREEN_WIDTH - imggamemap1.width) // 2
    backgroundy = (SCREEN_HEIGHT - imggamemap1.height) // 2
    root.geometry(f'{SCREEN_WIDTH}x{SCREEN_HEIGHT}+{(root.winfo_screenwidth() - SCREEN_WIDTH) // 2}+{(root.winfo_screenheight() - SCREEN_HEIGHT) // 2}')
    if c == 0:
        canvas = Canvas(root, width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
        canvas.pack()
        c += 1
    myFont = font.Font(family="Britannic Bold", size=15)
    bgoutput = canvas.create_image(backgroundx, backgroundy, image=map1, anchor='nw')
    outputtime = canvas.create_text(140, (SCREEN_HEIGHT * 0.11), text=f'TIME: {seconds}', font=myFont, fill='white')
    canvas.create_text(50, (SCREEN_HEIGHT * 0.17), text=f'WORLD\n  1-1', font=myFont, fill='white')
    timer()
    canvas.focus_set()

    #initializing the door and setting its x and y position
    d = Door(canvas)
    d.setLocation(940, 120)

    #initializing the player and setting its location
    p = Player(canvas)
    p.setX(p.getRight())
    p.setY(120)
    
    #calling the door collide function
    dcollide()

    #initializing the ghosts, setting its location and calling a function to move them
    g.append(Ghost(canvas))
    g.append(Ghost(canvas))
    g[0].setLocation(150, 30)
    g[1].setLocation(650, 30)
    move_ghost()

    #initializing the ball, setting its initial location and calling a function at the time we want to move them
    b.append(Spikeball(canvas))
    b[0].setLocation(-50, -50)
    b.append(Spikeball(canvas))
    b[1].setLocation(-50, -50)
    firstdrop = root.after(7000, dropspike)
    seconddrop = root.after(10000, dropspike)
    #plays the game music
    pygame.mixer.music.play(-1)

def L2():
    global canvas, p, bgoutput, d, root, g, b, outputtime, seconddrop, thirddrop, c, f, firstdrop
    #setting the screen
    SCREEN_WIDTH, SCREEN_HEIGHT = 800, 168
    backgroundx = (SCREEN_WIDTH - imggamemap1.width) // 2
    backgroundy = (SCREEN_HEIGHT - imggamemap1.height) // 2
    root.geometry(f'{SCREEN_WIDTH}x{SCREEN_HEIGHT}+{(root.winfo_screenwidth() - SCREEN_WIDTH) // 2}+{(root.winfo_screenheight() - SCREEN_HEIGHT) // 2}')
    if c == 0:
        canvas = Canvas(root, width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
        canvas.pack()
        c += 1
    myFont = font.Font(family="Britannic Bold", size=15)
    bgoutput = canvas.create_image(backgroundx, backgroundy, image=map1, anchor='nw')
    outputtime = canvas.create_text(140, (SCREEN_HEIGHT * 0.11), text=f'TIME: {seconds}', font=myFont, fill='white')
    canvas.create_text(50, (SCREEN_HEIGHT * 0.17), text=f'WORLD\n  1-2', font=myFont, fill='white')
    timer()
    canvas.focus_set()

    #initializing the holes and setting their locations
    f.append(Fall(canvas, 60, 145))
    f.append(Fall(canvas, 780, 145))

    #initializing the door and setting its location
    d = Door(canvas)
    d.setLocation(978, 120)

    #initializing the player and setting its location
    p = Player(canvas)
    p.setX(p.getRight())
    p.setY(120)
    
    #calling the door and fall collide functions
    dcollide()
    fcollide()

    #initializing the ghosts, setting its location and calling a function to move them
    g.append(Ghost(canvas))
    g.append(Ghost(canvas))
    g.append(Ghost(canvas))
    g.append(Ghost(canvas))
    g[0].setLocation(150, 30)
    g[1].setLocation(500, 30)
    g[2].setLocation(700, 30)
    g[3].setLocation(250, 30)
    move_ghost()

    #initializing the ball, setting its initial location and calling a function at the time we want to move them
    b.append(Spikeball(canvas))
    b[0].setLocation(-50, -50)
    b.append(Spikeball(canvas))
    b[1].setLocation(-50, -50)
    b.append(Spikeball(canvas))
    b[2].setLocation(-50, -50)
    firstdrop = root.after(10000, dropspike)
    seconddrop = root.after(13000, dropspike)
    thirddrop = root.after(15000, dropspike)
    #plays the game music
    pygame.mixer.music.play(-1)

def L3():
    global canvas, p, bgoutput, d, root, g, b, outputtime, seconddrop, thirddrop, c, firstdrop
    #setting the screen
    SCREEN_WIDTH, SCREEN_HEIGHT = 800, 168
    backgroundx = (SCREEN_WIDTH - imggamemap1.width) // 2
    backgroundy = (SCREEN_HEIGHT - imggamemap1.height) // 2
    root.geometry(f'{SCREEN_WIDTH}x{SCREEN_HEIGHT}+{(root.winfo_screenwidth() - SCREEN_WIDTH) // 2}+{(root.winfo_screenheight() - SCREEN_HEIGHT) // 2}')
    if c == 0:
        canvas = Canvas(root, width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
        canvas.pack()
        c += 1
    myFont = font.Font(family="Britannic Bold", size=15)
    bgoutput = canvas.create_image(backgroundx, backgroundy, image=map1, anchor='nw')
    outputtime = canvas.create_text(140, (SCREEN_HEIGHT * 0.11), text=f'TIME: {seconds}', font=myFont, fill='white')
    canvas.create_text(50, (SCREEN_HEIGHT * 0.17), text=f'WORLD\n  1-3', font=myFont, fill='white')
    timer()
    canvas.focus_set()

    #initializing the holes and setting their locations
    f.append(Fall(canvas, 780, 145))
    f.append(Fall(canvas, 470, 145))
    f.append(Fall(canvas, 400, 145))

    #initializing the door and setting its location
    d = Door(canvas)
    d.setLocation(978, 120)

    #initializing the player and setting its location
    p = Player(canvas)
    p.setX(p.getRight())
    p.setY(120)
    
    #calling the door and fall collide functions
    dcollide()
    fcollide()

    #initializing the ghosts, setting its location and calling a function to move them
    g.append(Ghost(canvas))
    g.append(Ghost(canvas))
    g.append(Ghost(canvas))
    g.append(Ghost(canvas))
    g[0].setLocation(300, 30)
    g[1].setLocation(600, 30)
    g[2].setLocation(700, 30)
    g[3].setLocation(200, 30)
    move_ghost()

    #initializing the ball, setting its initial location and calling a function at the time we want to move them
    b.append(Spikeball(canvas))
    b[0].setLocation(-50, -50)
    b.append(Spikeball(canvas))
    b[1].setLocation(-50, -50)
    b.append(Spikeball(canvas))
    b[2].setLocation(-50, -50)
    firstdrop = root.after(4000, dropspike)
    seconddrop = root.after(6000, dropspike)
    thirddrop = root.after(9000, dropspike)
    #plays the game music
    pygame.mixer.music.play(-1)

#Set values of your tk window, and initalize a tk window
root = Tk()
root.geometry(f'1x1+{0-50}+{0-50}')
#If users click the X button, run the close option function
root.protocol("WM_DELETE_WINDOW", close_option)
root.title('Super Red Bros')

# All the images needed for the game
imggamemap1 = Image.open('images/map1.png')
map1 = ImageTk.PhotoImage(imggamemap1)
imgBackground = Image.open('images/menu.png')
picBackground = ImageTk.PhotoImage(imgBackground)
imgOver = ImageTk.PhotoImage(Image.open('images/game_over.png'))
imgpassed = ImageTk.PhotoImage(Image.open('images/passed.png'))

# Allow keyboard functions
root.bind('<KeyPress>', onkeypress)

#top level variables for the level window
selection_window = Toplevel(padx=10, pady=10, bg='white')
selection_window.title('Select A Level')
selection_window.resizable(False, False)
selection_window.protocol('WM_DELETE_WINDOW', close_option)
selection_window.withdraw()


# Radiobutton for the levels
radioVariable = IntVar()
lblLevel = Label(selection_window, text='Select a Level\nClick the ready button once a selection has been made!', bg='white').grid(row=0, column=1, columnspan=3)
rb1 = Radiobutton(selection_window, text="L1", anchor="c", width=10, pady=2, justify="right",bg='white', variable=radioVariable, value=0, command=select_level).grid(row=1, column=1, columnspan=3)
rb2 = Radiobutton(selection_window, text="L2", anchor="c", width=10, pady=2, justify="right",bg='white', variable=radioVariable, value=1, command=select_level).grid(row=2, column=1, columnspan=3)
rb3 = Radiobutton(selection_window, text="L3", anchor="c", width=10, pady=2, justify="right",bg='white', variable=radioVariable, value=2, command=select_level).grid(row=3, column=1, columnspan=3)
readybtn = Button(selection_window, text='READY', anchor='c', bg='light green', width=15, pady=2, command=ready).grid(row=4, column=1, columnspan=3)
radioVariable.set(0)

# Resize the image for the background
imgSplash = ImageTk.PhotoImage(imgBackground.resize((imgBackground.width // 2, imgBackground.height // 2)))

#Initalize the splash screen, and if user presses certain key (space), close the splash screen
splash_screen = Toplevel()
splash_screen.title('Super Red Bros')
splash_screen.geometry(f'{imgSplash.width()}x{imgSplash.height()}+{(root.winfo_screenwidth() - imgSplash.width()) // 2}+{(root.winfo_screenheight() - imgSplash.height()) // 2}')
splash_screen.resizable(False, False)
splash_screen.bind('<KeyPress>', onkeypress)
splash_screen.protocol('WM_DELETE_WINDOW', close_splashscreen)

#Create a canvas on your splashscreen
canvas_splash = Canvas(splash_screen, width=imgSplash.width(), height=imgSplash.height())
canvas_splash.create_image(0, 0, image=imgSplash, anchor='nw')
canvas_splash.pack()

#variables required for the program
dead = False
win = False
timerid = None
seconds = 0
dead = False
win = False
timerid = None
seconds = 0
min = 0
startjump = False
gmove = None
gdown = None
gup = None
ghostcallcount = 0
ball = None
balltimerid = None
dcollisionid = None
overpic = None
winpic = None
gcollisionid = None                    
kill = 0 
canvas = None
p = None
bgoutput = None
d = None
g = []
b = []
f = []
outputtime = None
firstdrop = None
seconddrop = None
thirddrop = None
c = 0

#hide window
root.withdraw()
#display the window after hiding
splash_screen.deiconify()
#Update your window
root.mainloop()