# -*- coding: utf-8 -*-
"""appJar.py: Provides a GUI class, for making simple tkinter GUIs."""
# Nearly everything I learnt came from: http://effbot.org/tkinterbook/
# with help from: http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/index.html
# with snippets from stackexchange.com

from tkinter import *
from tkinter import messagebox
from tkinter import colorchooser
from tkinter import filedialog
from tkinter import scrolledtext
from tkinter import font
import os, sys, re, socket, hashlib, imghdr, time
import __main__ as theMain
from platform import system as platform
import webbrowser
from idlelib.TreeWidget import TreeItem, TreeNode
from xml.dom.minidom import parseString

# import borrowed libraries
from appJar.lib.tooltip import ToolTip
from appJar.lib.tkinter_png import *
from appJar.lib import nanojpeg

# only try to import winsound if we're on windows
if platform() in [ "win32", "Windows"]:
    import winsound

# details
__author__ = "Richard Jarvis"
__copyright__ = "Copyright 2016, Richard Jarvis"
__credits__ = ["Graham Turner", "Sarah Murch"]
__license__ = "GPL"
__version__ = "0.1"
__maintainer__ = "Richard Jarvis"
__email__ = "info@appJar.info"
__status__ = "Development"

#class to allow simple creation of tkinter GUIs
class gui:
    """
        Class to represent the GUI
        - Create one of these
        - add some widgets
        - call the go() function
    """
    built = False

    # used to identify widgets in component configurations
    WINDOW=0
    LABEL=1
    ENTRY=2
    BUTTON=3
    CHECKBOX=4
    SCALE=5
    RADIOBUTTON=6
    LISTBOX=7
    MESSAGE=8
    SPIN=9
    OPTION=10
    TEXTAREA=11
    LINK=12
    METER=13
    IMAGE=14
    PIECHART=15
    RB=60
    CB=40
    LB=70
    LABELFRAME=16
    TABBEDFRAME=17
    PANEDWINDOW=18
    SCROLLPANE=19
    PAGEDWINDOW=20
    TOGGLEFRAME=21

    # positioning
    N = N
    NE = NE
    E = E
    SE = SE
    S = S
    SW = SW
    W = W
    NW = NW
    CENTER = CENTER
    LEFT = LEFT
    RIGHT = RIGHT

    # reliefs
    SUNKEN=SUNKEN
    RAISED=RAISED
    GROOVE=GROOVE
    RIDGE=RIDGE
    FLAT=FLAT

    # containers
    C_ROOT='rootPage'
    C_LABELFRAME='labelFrame'
    C_TOGGLEFRAME="toggleFrame"

    # 2 containers for pagedsWindow
    C_PAGEDWINDOW="pagedWindow"
    C_PAGE="page"
    # 2 containers for tabbedFrame
    C_TABBEDFRAME='tabbedFrame'
    C_TAB='tab'
    # 2 containers for panedWindow
    C_PANEDWINDOW="panedWindow"
    C_PANEDFRAME="panedFrame"

    C_SUBWINDOW="subWindow"
    C_SCROLLPANE="scrollPane"

    # names for each of the widgets defined above
    # used for defining functions
    WIDGETS = { LABEL:"Label", MESSAGE:"Message", BUTTON:"Button", ENTRY:"Entry", CB:"Cb", SCALE:"Scale", RB:"Rb",
              LB:"Lb", SPIN:"SpinBox", OPTION:"OptionBox", TEXTAREA:"TextArea", LINK:"Link", METER:"Meter", IMAGE:"Image",
              RADIOBUTTON:"RadioButton", CHECKBOX:"CheckBox", LISTBOX:"ListBox", PIECHART:"PieChart", #TABBEDFRAME:"TabbedFrame",
              LABELFRAME:"LabelFrame", PANEDWINDOW:"PanedWindow" }

    # music stuff
    BASIC_NOTES = {"A":440, "B":493, "C":261, "D":293, "E":329, "F":349, "G":392 }
    NOTES={'f8': 5587, 'c#6': 1108, 'f4': 349, 'c7': 2093, 'd#2': 77, 'g8': 6271,
         'd4': 293, 'd7': 2349, 'd#7': 2489, 'g#4': 415, 'e7': 2637, 'd9': 9397,
         'b8': 7902, 'a#4': 466, 'b5': 987, 'b2': 123, 'g#9': 13289, 'g9': 12543,
         'f#2': 92, 'c4': 261, 'e1': 41, 'e6': 1318, 'a#8': 7458, 'c5': 523, 'd6': 1174,
         'd3': 146, 'g7': 3135, 'd2': 73, 'd#3': 155, 'g#6': 1661, 'd#4': 311, 'a3': 219,
         'g2': 97, 'c#5': 554, 'd#9': 9956, 'a8': 7040, 'a#5': 932, 'd#5': 622, 'a1': 54,
         'g#8': 6644, 'a2': 109, 'g#5': 830, 'f3': 174, 'a6': 1760, 'e8': 5274, 'c#9': 8869,
         'f5': 698, 'b1': 61, 'c#4': 277, 'f#9': 11839, 'e5': 659, 'f9': 11175, 'f#5': 739,
         'a#1': 58, 'f#8': 5919, 'b7': 3951, 'c#8': 4434, 'g1': 48, 'c#3': 138, 'f#7': 2959,
         'c6': 1046, 'c#2': 69, 'c#7': 2217, 'c3': 130, 'e9': 10548, 'c9': 8372, 'a#6': 1864,
         'a#7': 3729, 'g#2': 103, 'f6': 1396, 'b3': 246, 'g#3': 207, 'b4': 493, 'a7': 3520,
         'd#6': 1244, 'd#8': 4978, 'f2': 87, 'd5': 587, 'f7': 2793, 'f#6': 1479, 'g6': 1567,
         'e3': 164, 'f#3': 184, 'g#1': 51, 'd8': 4698, 'f#4': 369, 'f1': 43, 'c8': 4186, 'g4': 391,
         'g3': 195, 'a4': 440, 'a#3': 233, 'd#1': 38, 'e2': 82, 'e4': 329, 'a5': 880, 'a#2': 116,
         'g5': 783, 'g#7': 3322, 'b6': 1975, 'c2': 65, 'f#1': 46}

    DURATIONS={"BREVE":2000, "SEMIBREVE":1000, "MINIM":500, "CROTCHET":250,  "QUAVER":125,"SEMIQUAVER":63, "DEMISEMIQUAVER":32, "HEMIDEMISEMIQUAVER":16}

#####################################
## CONSTRUCTOR - creates the GUI
#####################################
    def __init__(self, title=None, geom=None, warn=True, debug=False):
        self.WARN = warn
        self.DEBUG = debug

        # a stack to hold containers as being built
        # done here, as initArrays is called elsewhere - to reset the gubbins
        self.containerStack = []

        # first up, set up all the data stores
        self.__initArrays()

        # dynamically create lots of functions for configuring stuff
        self.__buildConfigFuncs()

        # set up some default path locations
        self.lib_file = os.path.abspath(__file__)
        self.exe_file = os.path.basename(theMain.__file__)
        self.exe_loc = os.path.dirname(theMain.__file__)
        # location of appJar
        self.lib_path = os.path.dirname(self.lib_file)
        self.resource_path = os.path.join(self.lib_path, "resources")
        self.icon_path = os.path.join(self.resource_path,"icons")
        self.sound_path = os.path.join(self.resource_path,"sounds")
        self.appJarIcon = os.path.join(self.icon_path,"favicon3.ico")

        # user configurable
        self.userImages = self.exe_loc
        self.userSounds = self.exe_loc

        # create the main window - topLevel
        self.topLevel = Tk()
        self.topLevel.bind('<Configure>', self.__windowEvent)
        # override close button
        self.topLevel.protocol("WM_DELETE_WINDOW", self.stop)
        # temporarily hide it
        self.topLevel.withdraw()
        self.locationSet = False

        # create a frame to store all the widgets
        self.appWindow = Frame(self.topLevel)
        self.appWindow.pack(fill=BOTH, expand=True)

        # set the windows title
        if title is None: title = self.exe_file
        self.setTitle(title)

        # configure the geometry of the window
        self.topLevel.escapeBindId = None # used to exit fullscreen
        self.setGeom(geom)

        # set the resize status - default to True
        self.setResizable(True)

        # set up fonts
        self.buttonFont = font.Font(family="Helvetica", size=12,)
        self.labelFont = font.Font(family="Helvetica", size=12)
        self.entryFont = font.Font(family="Helvetica", size=12)
        self.messageFont = font.Font(family="Helvetica", size=12)
        self.rbFont = font.Font(family="Helvetica", size=12)
        self.cbFont = font.Font(family="Helvetica", size=12)
        self.tbFont = font.Font(family="Helvetica", size=12)
        self.scaleFont = font.Font(family="Helvetica", size=12)
        self.statusFont = font.Font(family="Helvetica", size=12)
        self.spinFont = font.Font(family="Helvetica", size=12)
        self.optionFont = font.Font(family="Helvetica", size=12)
        self.lbFont = font.Font(family="Helvetica", size=12)
        self.taFont = font.Font(family="Helvetica", size=12)
        self.meterFont = font.Font(family="Helvetica", size=12, weight='bold')
        self.linkFont = font.Font(family="Helvetica", size=12, weight='bold', underline=1)
        self.labelFrameFont = font.Font(family="Helvetica", size=12)
        self.toggleFrameFont = font.Font(family="Helvetica", size=12)
        self.tabbedFrameFont = font.Font(family="Helvetica", size=12)
        self.panedWindowFont = font.Font(family="Helvetica", size=12)
        self.scrollPaneFont = font.Font(family="Helvetica", size=12)

        # for simple grids - RETHINK
        self.gdFont = font.Font(family="Helvetica", size=12)
        self.ghFont = font.Font(family="Helvetica", size=14, weight="bold")
        self.ghBg= "gray"
        self.gdBg= self.topLevel.cget("bg")
        self.gdHBg= "red"
        self.gdSBg= "blue"
        self.ghHBg= self.topLevel.cget("bg")
        self.gdC= self.topLevel.cget("bg")
        self.gdHighlight = "red"

#        self.fgColour = self.topLevel.cget("foreground")
#        self.buttonFgColour = self.topLevel.cget("foreground")
#        self.labelFgColour = self.topLevel.cget("foreground")

        # create a menu bar - only shows if populated
        # now created in menu functions, as it generated a blank line...
        self.hasMenu = False
        self.hasStatus = False
        self.hasTb = False

        # won't pack, if don't pack it here
        self.tb = Frame(self.appWindow, bd=1, relief=RAISED)
        self.tb.pack(side=TOP, fill=X)

        # create the main container for this GUI
        container = Frame(self.appWindow)
        #container = Label(self.appWindow) # made as a label, so we can set an image
        container.config(padx=2, pady=2, background=self.topLevel.cget("bg"))
        container.pack(fill=BOTH, expand=True)
        self.__addContainer(self.C_ROOT, container, 0, 1)

        # set up the main container to be able to host an image
        self.__configBg(container)

        # an array to hold any threaded events....
        self.events = []
        self.pollTime = 250
        self.built = True
        self.topLevel.wm_iconbitmap(self.appJarIcon)

    def __configBg(self, container):
        # set up a background image holder
        # alternative to label option above, as label doesn't update widgets properly
        self.bgLabel = Label(container)
        self.bgLabel.config(anchor=CENTER, font=self.labelFont, background=self.__getContainerBg())
        self.bgLabel.place(x=0, y=0, relwidth=1, relheight=1)
        container.image = None

#####################################
## set the arrays we use to store everything
#####################################
    def __initArrays(self):
        # set up a row counter - used to auto add rows
        # breaks once user sets own row

        #set up a minimum label width for label combos
        self.labWidth=1

        # validate function callbacks - used by numeric texts
        # created first time a widget is used
        self.validateNumeric = None
        self.validateSpinBox = None

        # set up flash variable
        self.doFlash = False

        # used to hide/show title bar
        self.hasTitleBar=True
        # records if we're in fullscreen - stops hideTitle from breaking
        self.isFullscreen = False

        # collections of widgets, widget name is key
        self.n_frames=[] # un-named, so no direct access
        self.n_labels = {}
        self.n_buttons = {}
        self.n_entries={}
        self.n_messages={}
        self.n_scales={}
        self.n_cbs={}
        self.n_rbs={}
        self.n_lbs={}
        self.n_tbButts={}
        self.n_spins={}
        self.n_options={}
        self.n_frameLabs={}
        self.n_textAreas={}
        self.n_links={}
        self.n_meters={}
        self.n_subWindows={}
        self.n_labelFrames={}
        self.n_tabbedFrames={}
        self.n_panedWindows={}
        self.n_pagedWindows={}
        self.n_panedFrames={}
        self.n_toggleFrames={}
        self.n_scrollPanes={}
        self.n_trees={}
        self.n_flashLabs = []
        self.n_pieCharts={}
        self.n_separators=[]

        # variables associated with widgets
        self.n_entryVars={}
        self.n_optionVars={}
        self.n_boxVars={}
        self.n_rbVars={}
        self.n_rbVals={}
        self.n_images={}        # image label widgets
        self.n_imageCache={}    # image file objects
        self.n_taHashes={}      # for monitoring textAreas

        # for simple grids
        self.n_grids={}

        # menu stuff
        self.n_menus={}
        self.n_menuVars={}

    # function to generate warning messages
    def warn(self, message):
        if self.WARN: print("Warning -", message)
    # function to turn off warning messages
    def disableWarnings(self): self.WARN=False

    # function to generate warning messages
    def debug(self, message):
        if self.DEBUG: print("Debug -", message)
    # function to turn on debug messages
    def enableDebug(self): self.DEBUG=True

#####################################
## Event Loop - must always be called at end
#####################################
    def go(self):
        """ Most important function! Start the GUI """
        # check the containers have all been stopped
        if len(self.containerStack) > 1:
              self.warn("You didn't stop all containers")
              for i in range(len(self.containerStack)-1, 0, -1):
                    kind = self.containerStack[i]['type']
                    if kind not in [self.C_PANEDFRAME]:
                          self.warn("STOP: "+kind)

        if len(self.n_trees)>0:
            for k in self.n_trees:
                self.n_trees[k].update()
                self.n_trees[k].expand()

        # only add the menu bar at the end...
        if self.hasMenu:
              self.topLevel.config(menu=self.menuBar)

        # pack it all in & make sure it's drawn
        self.appWindow.pack(fill=BOTH)
        self.topLevel.update_idletasks()

        # check geom is set and set a minimum size, also positions the window if necessary
        self.__dimensionWindow()

        # bring to front
        self.topLevel.deiconify()
        self.__bringToFront()

        # start the call back & flash loops
        self.__poll()
        self.__flash()

        # start the main loop
        self.topLevel.mainloop()

    def setStopFunction(self, function):
        """ set a funciton to call when the GUI is quit. Must return True or False """
        if self.containerStack[-1]['type'] == self.C_SUBWINDOW:
            self.containerStack[-1]['container'].stopFunction = function
        else:
            self.containerStack[0]['stopFunction'] = function

    def stop(self, event=None):
        """ Closes the GUI. If a stop function is set, will only close the GUI if True """
        theFunc = self.containerStack[0]['stopFunction']
        if theFunc is None or theFunc():
            # stop any sounds, ignore error when not on Windows
            try: self.stopSound()
            except: pass
            self.topLevel.destroy()

#####################################
## Functions for configuring polling events
#####################################
    #events will fire in order of being added, after sleeping for time
    def setPollTime(self, time):
        """ Set a frequency for executing queued functions """
        self.pollTime = time

    # register events to be called by the sleep timer
    def registerEvent(self, func):
        """ Queue a function, to be executed every poll time """
        self.events.append(func)

    # internal function, called by 'after' function, after sleeping
    def __poll(self):
        # run any registered actions
        for e in self.events:
              # execute the event
              e()
        self.topLevel.after(self.pollTime, self.__poll)

    # not used now, but called every time window is resized
    # may be used in the future...
    def __windowEvent(self, event):
        new_width = self.topLevel.winfo_width()
        new_height = self.topLevel.winfo_height()
        self.debug("Window resized: " + str(new_width)+"x"+str(new_height))

    # will call the specified function when enter key is pressed
    def enableEnter(self, func):
        """ Binds <Return> to the specified function - all widgets """
        self.bindKey("<Return>", func)

    def disableEnter(self):
        """ unbinds <enter> from all widgets """
        self.unbindKey("<Return>")

    def bindKey(self, key, func):
        """ bind the specified key, to the specified function, for all widgets """
        # for now discard the Event...
        myF = self.__makeFunc(func, key, True)
        self.__getTopLevel().bind(key, myF)

    def unbindKey(self, key):
        """ unbinds the specified key from whatever functions it os bound to """
        self.__getTopLevel().unbind(key)

    # helper - will see if the mouse is in the specified widget
    def __isMouseInWidget(self, w):
        l_x = w.winfo_rootx()
        l_y = w.winfo_rooty()

        if l_x <= w.winfo_pointerx() <= l_x+w.winfo_width() and l_y <= w.winfo_pointery() <= l_y+w.winfo_height():
              return True
        else:
              return False

    # function to give a clicked widget the keyboard focus
    def __grabFocus(self, e): e.widget.focus_set()

#####################################
## FUNCTIONS for configuring GUI settings
#####################################
    # set a minimum size
    def __dimensionWindow(self):
        if self.__getTopLevel().geom != "fullscreen":
            # get the apps requested width & height
            r_width=self.__getTopLevel().winfo_reqwidth()
            r_heigth=self.__getTopLevel().winfo_reqheight()

            # if a geom has not ben set
            if self.__getTopLevel().geom is None:
                # determine a minimum geom
                width=self.__getTopLevel().winfo_width()
                height=self.__getTopLevel().winfo_height()

                if r_width>width: width=r_width
                if r_heigth>height: height=r_heigth

                # store it in the app's geom
                self.__getTopLevel().geom = str(width)+"x"+str(height)

            # now split the app's geom
            width = int(self.__getTopLevel().geom.lower().split("x")[0])
            height = int(self.__getTopLevel().geom.lower().split("x")[1])

            # and set it as the minimum size
            self.__getTopLevel().minsize(width, height)

            # warn the user that their geom is not big enough
            if width < r_width or height < r_heigth:
                self.warn("Specified dimensions ("+self.__getTopLevel().geom+"), less than requested dimensions ("+str(r_width)+"x"+str(r_heigth)+")")

            # if the window hasn't been positioned by the user, put it in the middle
            if not self.locationSet:
                x = (self.topLevel.winfo_screenwidth() - width) / 2
                y = (self.topLevel.winfo_screenheight() - height) / 2
                self.setLocation(x,y)

    # called to update screen geometry
    def setGeometry(self, geom, height=None):
        self.setGeom(geom, height)

    def setGeom(self, geom, height=None):
        if height is not None: geom = str(geom)+"x"+str(height)
        container = self.__getTopLevel()
        container.geom = geom
        if container.geom == "fullscreen":
              self.setFullscreen()
        else:
              self.exitFullscreen()
              if container.geom is not None: container.geometry(container.geom)

    # called to set screen position
    def setLocation(self, x, y):
        self.locationSet = True
        self.__getTopLevel().geometry("+%d+%d" % (x, y))

    # called to make sure this window is on top
    def __bringToFront(self):
        if platform() == "Darwin":
              val=os.system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "python3" to true' ''')
#                  val=os.system('''/usr/bin/osascript -e 'tell app "System Events" to tell process "python3" perform action "AXRaise" of window ' ''')
#                  self.topLevel.lift()
#                  self.topLevel.call('wm', 'attributes', '.', '-topmost', True)
#                  self.topLevel.call('wm', 'focusmodel', '.', 'active')
#                  self.topLevel.call('wm', 'deiconify', '.')
#                  self.topLevel.after_idle(self.topLevel.call, 'wm', 'attributes', '.', '-topmost', True)
        else:
              self.topLevel.lift()

    def setFullscreen(self, container=None):
        if not self.isFullscreen:
              self.isFullscreen = True
              if container is None: container = self.__getTopLevel()
              container.attributes('-fullscreen', True)
              container.escapeBindId = container.bind('<Escape>', self.__makeFunc(self.exitFullscreen, container, True), "+")

    # function to turn off fullscreen mode
    def exitFullscreen(self, container=None):
        if self.isFullscreen:
            self.isFullscreen = False
            if container is None: container = self.__getTopLevel()
            container.attributes('-fullscreen', False)
            if container.escapeBindId is not None: container.unbind('<Escape>', container.escapeBindId)
            self.__doTitleBar()

    # sets the padding around the border of the root container
    def setPadding(self, x, y):
        self.containerStack[0]['container'].config(padx=x, pady=y)

    # set the current container's external grid padding
    def setPadX(self, x=0): self.containerStack[-1]['padx'] = x
    def setPadY(self, y=0): self.containerStack[-1]['pady'] = y

    # sets the current containers internal padding
    def setIPadX(self, x=0): self.containerStack[-1]['ipadx'] = x
    def setIPadY(self, y=0): self.containerStack[-1]['ipady'] = y

    # set an override sticky for this container
    def setSticky(self, sticky):
        self.containerStack[-1]['sticky'] = sticky

    # this tells widgets what to do when GUI is resized
    def setExpand(self, exp):
        if exp.lower() == "none": self.containerStack[-1]['expand'] = "NONE"
        elif exp.lower() == "row": self.containerStack[-1]['expand'] = "ROW"
        elif exp.lower() == "column": self.containerStack[-1]['expand'] = "COLUMN"
        else: self.containerStack[-1]['expand'] = "ALL"

    def getFonts(self): return list ( font.families() ). sort()

    def increaseButtonFont(self): self.setButtonFont(self.buttonFont['size'] + 1 )
    def decreaseButtonFont(self): self.setButtonFont(self.buttonFont['size'] - 1 )

    def setButtonFont(self, size, font=None):
        if font == None: font = self.buttonFont['family']
        self.buttonFont.config(family=font, size=size)

    def increaseLabelFont(self): self.setLabelFont(self.labelFont['size'] + 1 )
    def decreaseLabelFont(self): self.setLabelFont(self.labelFont['size'] -1 )

    def setLabelFont(self, size, font=None):
        if font == None: font = self.labelFont['family']
        self.labelFont.config(family=font, size=size)
        self.entryFont.config(family=font, size=size)
        self.rbFont.config(family=font, size=size)
        self.cbFont.config(family=font, size=size)
        self.scaleFont.config(family=font, size=size)
        self.messageFont.config(family=font, size=size)
        self.spinFont.config(family=font, size=size)
        self.optionFont.config(family=font, size=size)
        self.lbFont.config(family=font, size=size)
        self.taFont.config(family=font, size=size)
        self.linkFont.config(family=font, size=size)
        self.meterFont.config(family=font, size=size)
        self.labelFrameFont.config(family=font, size=size)
        self.toggleFrameFont.config(family=font, size=size)
        self.tabbedFrameFont.config(family=font, size=size)
        self.panedWindowFont.config(family=font, size=size)
        self.scrollPaneFont.config(family=font, size=size)

        # for simple grids - RETHINK
        self.lbFont.configure (family=font, size=size)
        self.taFont.configure (family=font, size=size)
        self.gdFont.configure (family=font, size=size)
        self.ghFont.configure (family=font, size=size+2, weight="bold")

    def increaseFont(self):
         self.increaseLabelFont()
         self.increaseButtonFont()

    def decreaseFont(self):
         self.decreaseLabelFont()
         self.decreaseButtonFont()

    def setFont(self, size, font=None):
         self.setLabelFont(size, font)
         self.setButtonFont(size, font)

    # need to set a default colour for container
    # then populate that field
    # then use & update that field accordingly
    # all widgets will then need to use it
    # and here we update all....
    def setFg(self, colour):
        for na in self.n_labels:
              self.n_labels[na].config(foreground=colour)
        for na in self.n_messages:
              self.n_messages[na].config(foreground=colour)

    # self.topLevel = Tk()
    # self.appWindow = Frame, fills all of self.topLevel
    # self.tb = Frame, at top of appWindow
    # self.container = Frame, at bottom of appWindow => C_ROOT container
    # self.bglabel = Label, filling all of container
    def setBg(self, colour):
        if self.containerStack[-1]['type'] == self.C_ROOT:
            self.appWindow.config(background=colour)
            self.bgLabel.config(background=colour)
        elif self.containerStack[-1]['type'] in [self.C_PAGEDWINDOW, self.C_TOGGLEFRAME]:
            self.containerStack[-1]['container'].setBg(colour)

        self.containerStack[-1]['container'].config(background=colour)

        for child in self.containerStack[-1]['container'].winfo_children():
            if not self.__widgetIsContainer(child): self.__setWidgetBg(child, colour)

    def __widgetIsContainer(self, widget):
        try:
            if widget.isContainer: return True
        except: pass
        return False
            
    def setResizable(self, canResize=True):
        self.__getTopLevel().isResizable = canResize
        if self.__getTopLevel().isResizable: self.__getTopLevel().resizable(True, True)
        else: self.__getTopLevel().resizable(False, False)

    def getResizable(self):
        return self.__getTopLevel().isResizable

    def __doTitleBar(self):
        self.__getTopLevel().overrideredirect(not self.hasTitleBar)

    def hideTitleBar(self):
        self.hasTitleBar=False
        self.__doTitleBar()

    def showTitleBar(self):
        self.hasTitleBar=True
        self.__doTitleBar()

    # function to set the window's title
    def setTitle(self, title):
        self.__getTopLevel().title(title)

    # set an icon
    def setIcon(self, image):
        container = self.__getTopLevel()
        if image.endswith('.ico'):
              container.wm_iconbitmap(image)
        else:
              icon = self.__getImage(image)
              container.iconphoto(True, icon)

    def __getTopLevel(self):
        if len(self.containerStack) > 1 and self.containerStack[-1]['type'] == self.C_SUBWINDOW:
            return self.containerStack[-1]['container']
        else:
            return self.topLevel

    # make the window transparent (between 0 & 1)
    def setTransparency(self, percentage):
        if percentage>1: percentage = percentage/100
        self.__getTopLevel().attributes("-alpha", percentage)

##############################
## funcitons to deal with tabbing and right clicking
##############################
    def __focusNextWindow(self,event):
        event.widget.tk_focusNext().focus_set()
        nowFocus = self.topLevel.focus_get()
        if isinstance(nowFocus, Entry): nowFocus.select_range(0,END)
        return("break")

    def __focusLastWindow(self,event):
        event.widget.tk_focusPrev().focus_set()
        nowFocus = self.topLevel.focus_get()
        if isinstance(nowFocus, Entry): nowFocus.select_range(0,END)
        return("break")

    def __rightClick(self,event):
        def rClick_Copy(event, apnd=0):
            #event.widget.event_generate('<Control-c>')
            try:
                text = event.widget.selection_get()
                self.topLevel.clipboard_clear()
                #text = event.widget.get("sel.first", "sel.last")
                self.topLevel.clipboard_append(text)
            except TclError: pass

        def rClick_Cut(event):
            #event.widget.event_generate('<Control-x>')
            try:
                text = event.widget.selection_get()
                self.topLevel.clipboard_clear()
                self.topLevel.clipboard_append(text)
                event.widget.delete("sel.first", "sel.last")
            except TclError: pass

        def rClick_Paste(event):
            #event.widget.event_generate('<Control-v>')
            text = self.topLevel.selection_get(selection='CLIPBOARD')
            event.widget.insert('insert', text)

        event.widget.focus()

        nclst=[
              (' Cut', lambda e=event: rClick_Cut(event)),
              (' Copy', lambda e=event: rClick_Copy(event)),
              (' Paste', lambda e=event: rClick_Paste(event)),
              ]

        rmenu = Menu(None, tearoff=0, takefocus=0)
        for (txt, cmd) in nclst:
            rmenu.add_command(label=txt, command=cmd)

        rmenu.tk_popup(event.x_root+40, event.y_root+10,entry="0")
        event.widget.selection_clear()
        return("break")

#####################################
## FUNCTION to configure widgets
#####################################
    def __getItems(self, kind):
        if kind == self.LABEL: return self.n_labels
        elif kind == self.MESSAGE: return self.n_messages
        elif kind == self.BUTTON: return self.n_buttons
        elif kind == self.ENTRY: return self.n_entries
        elif kind == self.SCALE: return self.n_scales
        elif kind in [self.CB, self.CHECKBOX]: return self.n_cbs
        elif kind in [self.RB, self.RADIOBUTTON]: return self.n_rbs
        elif kind in [self.LB, self.LISTBOX]: return self.n_lbs
        elif kind == self.SPIN: return self.n_spins
        elif kind == self.OPTION: return self.n_options
        elif kind == self.TEXTAREA: return self.n_textAreas
        elif kind == self.LINK: return self.n_links
        elif kind == self.METER: return self.n_meters
        elif kind == self.IMAGE: return self.n_images
        elif kind == self.PIECHART: return self.n_pieCharts

        elif kind == self.LABELFRAME: return self.n_labelFrames
        elif kind == self.TABBEDFRAME: return self.n_tabbedFrames
        elif kind == self.PANEDWINDOW: return self.n_panedFrames
        elif kind == self.SCROLLPANE: return self.n_scrollPanes
        elif kind == self.PAGEDWINDOW: return self.n_pagedWindows
        elif kind == self.TOGGLEFRAME: return self.n_toggleFrames

        else: raise Exception ("Unknown widget type: " + str(kind))

    def configureAllWidgets(self, kind, option, value):
        items = list(self.__getItems(kind))
        self.configureWidgets(kind, items, option, value)

    def configureWidgets(self, kind, names, option, value ):
        if not isinstance(names, list): self.configureWidget(kind, names, option, value)
        else:
            for widg in names:
                self.configureWidget(kind, widg, option, value)

    def getWidget(self, kind, name):
        # get the list of items for this type, and validate the widget is in the list
        items = self.__getItems(kind)
        return self.__verifyItem(items, name, False)

    def configureWidget(self, kind, name, option, value, key=None, deprecated=False):
        # warn about deprecated functions
        if deprecated:
            self.warn("Deprecated config function ("+option+") used for: "
                        +self.WIDGETS[kind]+"->"+name+" use "+deprecated+" instead")
        if kind in [self.RB, self.LB, self.CB]:
            self.warn("Deprecated config function ("+option+") used for: "
                        +self.WIDGETS[kind]+"->"+name+" use "+self.WIDGETS[kind/10]+" instead")
        # get the list of items for this type, and validate the widgetis in the list
        items = self.__getItems(kind)
        self.__verifyItem(items, name)

        if kind in [self.RB, self.RADIOBUTTON]: items = items[name]
        else: items = [items[name]]

        # loop through each item, and try to reconfigure it
        # this will often faile - widgets have varied config options
        for item in items:
            try:
                if option == 'background':
                    if kind==self.METER:
                        item.setBg(value)
                    elif kind==self.TABBEDFRAME:
                        item.setBg(value)
                    else:
                        self.__setWidgetBg(item, value)
                elif option == 'foreground':
                    if kind==self.ENTRY:
                        if item.hasDefault: item.oldFg=value
                        else:
                            item.config(foreground=value)
                            item.oldFg=value
                    elif kind==self.METER:
                              item.setFg(value)
                    else:
                        item.config(foreground=value)
                elif option == 'disabledforeground': item.config( disabledforeground=value )
                elif option == 'width':
                    if kind==self.METER: item.setWidth(value)
                    else: item.config( width=value )
                elif option == 'height':
                    if kind==self.METER: item.setHeight(value)
                    else: item.config( height=value )
                elif option == 'state': item.config( state=value )
                elif option == 'relief': item.config( relief=value )
                elif option == 'align':
                    if kind==self.ENTRY:
                        if value == W or value == LEFT: value = LEFT
                        elif value == E or value == RIGHT: value = RIGHT
                        item.config( justify=value )
                    else:
                        item.config( anchor=value )
                elif option == 'anchor': item.config( anchor=value )
                elif option == 'cursor': item.config( cursor=value )
                elif option == 'tooltip': self.__addTooltip(item, value)
                elif option == "focus": item.focus_set()
                elif option == 'over':
                    if not isinstance(value, list): value=[value]
                    if len(value) == 1: value.append(None)
                    if len(value) != 2:
                        raise Exception("Invalid arguments, set<widget>OverFunction requires 1 ot 2 functions to be passed in.")
                    if kind==self.LABEL:
                        if value[0] is not None: item.bind("<Enter>",self.__makeFunc(value[0], name, True), add="+")
                        if value[1] is not None: item.bind("<Leave>",self.__makeFunc(value[1], name, True), add="+")
                        #item.bind("<B1-Motion>",self.__makeFunc(value[0], name, True), add="+")
                elif option == 'drag':
                    if not isinstance(value, list): value=[value]
                    if len(value) == 1: value.append(None)
                    if len(value) != 2:
                        raise Exception("Invalid arguments, set<widget>DragFunction requires 1 ot 2 functions to be passed in.")
                    if kind==self.LABEL:
                        if platform() == "Darwin":
                            item.config(cursor="pointinghand")
                        elif platform() in [ "win32", "Windows"]:
                            item.config(cursor="hand2")

                        def getLabel(f):
                            # loop through all labels
                            for key, value in self.n_labels.items():
                                if self.__isMouseInWidget(value):
                                    f(key)
                                    return

                        if value[0] is not None: item.bind("<ButtonPress-1>", self.__makeFunc(value[0], name, True) , add="+")
                        if value[1] is not None: item.bind("<ButtonRelease-1>", self.__makeFunc(getLabel, value[1], True) , add="+")
                elif option == 'command':
                    # this will discard the scale value, as default function can't handle it
                    if kind==self.SCALE:
                        item.config( command=self.__makeFunc(value,name, True) )
                    elif kind==self.OPTION:
                        # need to trace the variable??
                        item.var.trace('w',  self.__makeFunc(value,name, True))
                    elif kind==self.ENTRY:
                        if key is None: key =name
                        item.bind('<Return>', self.__makeFunc(value, key, True))
                    elif kind==self.BUTTON:
                        item.config(command=self.__makeFunc(value, name))
                        item.bind('<Return>', self.__makeFunc(value, name, True))
                    # make labels clickable, add a cursor, and change the look
                    elif kind==self.LABEL or kind==self.IMAGE:
                        if platform() == "Darwin":
                            item.config(cursor="pointinghand")
                        elif platform() in [ "win32", "Windows"]:
                            item.config(cursor="hand2")

                        item.bind("<Button-1>",self.__makeFunc(value, name, True), add="+")
                        # these look good, but break when dialogs take focus
                        #up = item.cget("relief").lower()
                        #down="sunken"
                        # make it look like it's pressed
                        #item.bind("<Button-1>",lambda e: item.config(relief=down), add="+")
                        #item.bind("<ButtonRelease-1>",lambda e: item.config(relief=up))
                    else:
                        item.config( command=self.__makeFunc(value,name) )
                elif option == 'sticky':
                    info = {}
                    # need to reposition the widget in its grid
                    if self.__widgetHasContainer(kind, item):
                        # pack uses LEFT & RIGHT & BOTH
                        info["side"] = value
                        if value.lower() == "both":
                            info["expand"] = 1
                            info["side"] = "right"
                        else: info["expand"] = 0
                    else:
                        # grid uses E+W
                        if value.lower() == "left": side = W
                        elif value.lower() == "right": side = E
                        elif value.lower() == "both": side = W+E
                        else: side = value.upper()
                        info["sticky"] = side
                    self.__repackWidget(item, info)
                elif option == 'padding':
                    item.config(padx=value[0], pady=value[0])
            except TclError as e:
                self.warn("Error configuring " + name + ": " + str(e))

    # dynamic way to create the configuration functions
    def __buildConfigFuncs(self):
        # loop through all the available widgets
        # and make all the below functons for each one
        for k, v in self.WIDGETS.items():
              exec("def set"+v+"Bg(self, name, val): self.configureWidgets("+str(k)+", name, 'background', val)")
              exec("gui.set"+v+"Bg=set" +v+ "Bg")
              exec("def set"+v+"Fg(self, name, val): self.configureWidgets("+str(k)+", name, 'foreground', val)")
              exec("gui.set"+v+"Fg=set" +v+ "Fg")
              exec("def set"+v+"DisabledFg(self, name, val): self.configureWidgets("+str(k)+", name, 'disabledforeground', val)")
              exec("gui.set"+v+"DisabledFg=set" +v+ "DisabledFg")
              exec("def set"+v+"Width(self, name, val): self.configureWidgets("+str(k)+", name, 'width', val)")
              exec("gui.set"+v+"Width=set" +v+ "Width")
              exec("def set"+v+"Height(self, name, val): self.configureWidgets("+str(k)+", name, 'height', val)")
              exec("gui.set"+v+"Height=set" +v+ "Height")
              exec("def set"+v+"State(self, name, val): self.configureWidgets("+str(k)+", name, 'state', val)")
              exec("gui.set"+v+"State=set" +v+ "State")
              exec("def set"+v+"Padding(self, name, x, y): self.configureWidgets("+str(k)+", name, 'padding', [x, y])")
              exec("gui.set"+v+"Padding=set" +v+ "Padding")

              # might not all be necessary, could make exclusion list
              exec("def set"+v+"Relief(self, name, val): self.configureWidget("+str(k)+", name, 'relief', val)")
              exec("gui.set"+v+"Relief=set" +v+ "Relief")
              exec("def set"+v+"Align(self, name, val): self.configureWidget("+str(k)+", name, 'align', val)")
              exec("gui.set"+v+"Align=set" +v+ "Align")
              exec("def set"+v+"Anchor(self, name, val): self.configureWidget("+str(k)+", name, 'anchor', val)")
              exec("gui.set"+v+"Anchor=set" +v+ "Anchor")
              exec("def set"+v+"Tooltip(self, name, val): self.configureWidget("+str(k)+", name, 'tooltip', val)")
              exec("gui.set"+v+"Tooltip=set" +v+ "Tooltip")
              exec("def set"+v+"Function(self, name, val, key=None): self.configureWidget("+str(k)+", name, 'command', val, key)")
              exec("gui.set"+v+"Function=set" +v+ "Function")
              exec("def set"+v+"DragFunction(self, name, val): self.configureWidget("+str(k)+", name, 'drag', val)")
              exec("gui.set"+v+"DragFunction=set" +v+ "DragFunction")
              exec("def set"+v+"OverFunction(self, name, val): self.configureWidget("+str(k)+", name, 'over', val)")
              exec("gui.set"+v+"OverFunction=set" +v+ "OverFunction")
# deprecated, but left in for backwards compatability
              exec("def set"+v+"Command(self, name, val, key=None): self.configureWidget("+str(k)+", name, 'command', val, key, deprecated='Function')")
              exec("gui.set"+v+"Command=set" +v+ "Command")
              exec("def set"+v+"Func(self, name, val, key=None): self.configureWidget("+str(k)+", name, 'command', val, key, deprecated='Function')")
              exec("gui.set"+v+"Func=set" +v+ "Func")
# end deprecated
              # http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/cursors.html
              exec("def set"+v+"Cursor(self, name, val): self.configureWidget("+str(k)+", name, 'cursor', val)")
              exec("gui.set"+v+"Cursor=set" +v+ "Cursor")
              exec("def set"+v+"Focus(self, name): self.configureWidget("+str(k)+", name, 'focus', None)")
              exec("gui.set"+v+"Focus=set" +v+ "Focus")

              # change the stickyness
              exec("def set"+v+"Sticky(self, name, pos): self.configureWidget("+str(k)+", name, 'sticky', pos)")
              exec("gui.set"+v+"Sticky=set" +v+ "Sticky")

              # functions to manage widgets
              exec("def show"+v+"(self, name): self.showWidget("+str(k)+", name)")
              exec("gui.show"+v+"=show" +v )
              exec("def hide"+v+"(self, name): self.hideWidget("+str(k)+", name)")
              exec("gui.hide"+v+"=hide" +v )
              exec("def remove"+v+"(self, name): self.removeWidget("+str(k)+", name)")
              exec("gui.remove"+v+"=remove" +v )

              # convenience functions for enable/disable
              # might not all be necessary, could make exclusion list
              exec("def enable"+v+"(self, name): self.configureWidget("+str(k)+", name, 'state', 'normal')")
              exec("gui.enable"+v+"=enable"+v)
              exec("def disable"+v+"(self, name): self.configureWidget("+str(k)+", name, 'state', 'disabled')")
              exec("gui.disable"+v+"=disable"+v)

              # group functions
              exec("def set"+v+"Widths(self, names, val): self.configureWidgets("+str(k)+", names, 'width', val)")
              exec("gui.set"+v+"Widths=set" +v+ "Widths")
              exec("def setAll"+v+"Widths(self, val): self.configureAllWidgets("+str(k)+", 'width', val)")
              exec("gui.setAll"+v+"Widths=setAll" +v+ "Widths")

              exec("def set"+v+"Heights(self, names, val): self.configureWidgets("+str(k)+", names, 'height', val)")
              exec("gui.set"+v+"Heights=set" +v+ "Heights")
              exec("def setAll"+v+"Heights(self, val): self.configureAllWidgets("+str(k)+", 'height', val)")
              exec("gui.setAll"+v+"Heights=setAll" +v+ "Heights")

              exec("def get"+v+"Widget(self, name): return self.getWidget("+str(k)+", name)")
              exec("gui.get"+v+"Widget=get" +v+ "Widget")

#####################################
## FUNCTION to hide/show/remove widgets
#####################################
    def __widgetHasContainer(self, kind, item):
        if kind in [self.SCALE, self.ENTRY, self.SPIN, self.OPTION, self.LABEL] and item.inContainer: return True
        else: return False

    def hideWidget(self, kind, name):
        # get the dictionary of items, and find the item in it
        items = self.__getItems(kind)
        item = self.__verifyItem(items, name)

        if self.__widgetHasContainer(kind, item):
              widget = item.master
              self.n_frameLabs[name].hidden = True
        else:
              if kind in [self.RB, self.RADIOBUTTON]:
                    for rb in item:
                          if rb.text == name:
                                widget = rb
              widget = item

        if "in" in widget.grid_info():
              widget.grid_remove()
#                  self.__updateLabelBoxes(name)

    def showWidget(self, kind, name):
        # get the dictionary of items, and find the item in it
        items = self.__getItems(kind)
        item = self.__verifyItem(items, name)

        if self.__widgetHasContainer(kind, item):
              widget = item.master
              self.n_frameLabs[name].hidden = False
        else: widget = item

        # only show the widget, if it's not already showing
        if "in" not in widget.grid_info():
              widget.grid()
#                  self.__updateLabelBoxes(name)

    def removeWidget(self, kind, name):
        # get the dictionary of items, and find the item in it
        items = self.__getItems(kind)
        item = self.__verifyItem(items, name)

        # if it's a flasher, remove it
        if item in self.n_flashLabs:
            self.n_flashLabs.remove(item)
            if len(self.n_flashLabs) == 0: self.doFlash = False

        if self.__widgetHasContainer(kind, item):
              # destroy the parent
              parent = item.master
              parent.grid_forget()
              parent.destroy()
              # remove frame, label & widget from lists
              self.n_labels.pop(name)
              self.n_frameLabs.pop(name)
              self.n_frames.remove(parent)
        else:
              item.grid_forget()
              item.destroy()

        # finally remove it from the dictionary
        items.pop(name)

    def removeAllWidgets(self):
        for child in self.containerStack[0]['container'].winfo_children():
              child.destroy()
        self.__configBg(self.containerStack[0]['container'])
        self.__initArrays()
        self.setGeom(None)

#####################################
## FUNCTION for managing commands
#####################################
    # funcion to wrap up lambda
    # if the thing calling this generates parameters - then set discard=True
    def __makeFunc(self, funcName, param, discard=False):
        if discard: return lambda *args: funcName(param)
        else: return lambda: funcName(param)

    def __checkFunc(self, names, funcs):
        singleFunc = None
        if funcs is None: return None
        elif callable(funcs) : singleFunc = funcs
        elif len(names) != len(funcs): raise Exception("List sizes don't match")
        return singleFunc

#####################################
## FUNCTION to position a widget
#####################################
    # checks if the item already exists
    def __verifyItem(self, items, item, newItem=False):
        if not newItem and item not in items: raise ItemLookupError("Invalid key: "+ item + " does not exist")
        elif not newItem and item in items: return items[item]
        elif newItem and item in items: raise ItemLookupError("Duplicate key: '"+item+"' already exists")

    def getRow(self):
        return self.containerStack[-1]['emptyRow']

    def getNextRow(self):
        temp = self.containerStack[-1]['emptyRow']
        self.containerStack[-1]['emptyRow'] = temp + 1
        return temp

    def __repackWidget(self, widget, params):
        if widget.winfo_manager() == "grid":
              ginfo = widget.grid_info()
              ginfo.update(params)
              widget.grid(ginfo)
        elif widget.winfo_manager() == "pack":
              pinfo = widget.pack_info()
              pinfo.update(params)
              widget.pack(pinfo)
        else:
              raise Exception("Unknown geometry manager: " + widget.winfo_manager())

    # convenience function to set RCS, referencing the current container's settings
    def __getRCS(self, row, column, colspan, rowspan):
        if row is None: row=self.getNextRow()
        else: self.containerStack[-1]['emptyRow'] = row + 1

        if column >= self.containerStack[-1]['colCount']: self.containerStack[-1]['colCount'] = column + 1
        #if column == 0 and colspan == 0 and self.containerStack[-1]['colCount'] > 1:
        #      colspan = self.containerStack[-1]['colCount']

        return row, column, colspan, rowspan

    # convenience method to set a widget's bg
    def __setWidgetBg(self, widget, bg):

        # POTENTIAL ISSUES
        # spinBox - highlightBackground
        # cbs/rbs - activebackground
        # grids - background

        darwinBorders = ["Text", "Button", "Entry"]#, "OptionMenu"]
        noBg = ["Spinbox", "Scale", "ListBox", "SplitMeter", "Meter", "DualMeter"]

        widgType = widget.__class__.__name__
        isDarwin = platform() == "Darwin"

        # Mac specific colours
        if isDarwin and widgType in darwinBorders:
                widget.config(highlightbackground=bg)
#                if widgType == "OptionMenu": widget.config(background=bg)

        # widget with label, in frame
        elif widgType == "LabelBox":
            widget.theLabel["bg"]=bg
            widgType = widget.theWidget.__class__.__name__ 
            if isDarwin and  widgType in darwinBorders:
                widget.theWidget.config(highlightbackground=bg)
            if widgType == "OptionMenu": widget.theWidget.config(background=bg)

        # group of buttons or labels
        elif widgType == "WidgetBox":
            widget["bg"]=bg
            if isDarwin:
                for widg in widget.theWidgets:
                    widgType = widg.__class__.__name__
                    if widgType == "Button": widg.config(highlightbackground=bg)
                    elif widgType == "Label": widg.config(background=bg)

        elif widgType == "PagedWindow":
            widget.setBg(bg)

        # any other widgets
        elif widgType not in noBg:
            widget["bg"]=bg

    def __getContainerBg(self):
        return self.__getContainer()["bg"]

    # two important things here:
    # grid - sticky: position of widget in its space (side or fill)
    # row/columns configure - weight: how to grow with GUI
    def __positionWidget(self, widget, row, column=0, colspan=0, rowspan=0, sticky=W+E):
        # allow item to be added to container
        container = self.__getContainer()
        self.__setWidgetBg(widget, self.__getContainerBg())

        # alpha paned window placement
        if self.containerStack[-1]['type'] ==self.C_PANEDWINDOW:
            container.add(widget)
            self.containerStack[-1]['widgets']=True
            return

        # else, add to grid
        row, column, colspan, rowspan = self.__getRCS(row, column, colspan, rowspan)

        # build a dictionary for the named params
        iX = self.containerStack[-1]['ipadx']
        iY = self.containerStack[-1]['ipady']
        cX = self.containerStack[-1]['padx']
        cY = self.containerStack[-1]['pady']
        params = {"row":row, "column":column, "ipadx":iX, "ipady":iY, "padx":cX, "pady":cY}

        # if we have a column span, apply it
        if colspan != 0 : params["columnspan"] = colspan
        # if we have a rowspan, apply it
        if rowspan != 0 : params["rowspan"] = rowspan

        # 1) if param has sticky, use that
        # 2) if container has sticky - overrirde
        # 3) else, none
        if self.containerStack[-1]["sticky"] is not None: params["sticky"] = self.containerStack[-1]["sticky"]
        elif sticky is not None: params["sticky"] = sticky
        else: pass

#        if rowspan != 0 : params["sticky"] = N+S+E+W;

        # expand that dictionary out as we pass it as a value
        widget.grid (**params)
        self.containerStack[-1]['widgets']=True
        # if we're in a PANEDWINDOW - we need to set parent...
        if self.containerStack[-1]['type'] ==self.C_PANEDFRAME:
            self.containerStack[-2]['widgets']=True

        # configure the row/column to expand equally
        if self.containerStack[-1]['expand'] in ["ALL", "COLUMN"]: Grid.columnconfigure(container, column, weight=1)
        else: Grid.columnconfigure(container, column, weight=0)
        if self.containerStack[-1]['expand'] in ["ALL", "ROW"]: Grid.rowconfigure(container, row, weight=1)
        else: Grid.rowconfigure(container, row, weight=0)

#        self.containerStack[-1]['container'].columnconfigure(0, weight=1)
#        self.containerStack[-1]['container'].rowconfigure(0, weight=1)

#####################################
## FUNCTION to manage containers
#####################################
    # adds the container to the container stack - makes this the current working container
    def __addContainer(self, cType, container, row, col, sticky=None):
        self.containerStack.append (
            {'type':cType, 'container':container,'emptyRow':row, 'colCount':col, 'sticky':sticky,
            'padx':0, 'pady':0, 'ipadx':0, 'ipady':0, 'expand':"ALL", 'widgets':False, 'stopFunction':None}
        )

    # returns the current working container
    def __getContainer(self):
        container=self.containerStack[-1]['container']
        if self.containerStack[-1]['type']==self.C_SCROLLPANE:
            return container.interior
        elif self.containerStack[-1]['type']==self.C_PAGEDWINDOW:
            return container.getPage()
        elif self.containerStack[-1]['type']==self.C_TOGGLEFRAME:
            return container.getContainer()
        else:
            return container

    # if possible, removes the current container
    def __removeContainer(self):
        if len(self.containerStack) == 1:
            raise Exception("Can't remove container, already in root window.")
        elif not self.containerStack[-1]['widgets']:
            raise Exception("Put something in the container, before removing it.")
        else:
            return self.containerStack.pop()

    # functions to start the various containers
    def startContainer(self, fType, title, row=None, column=0, colspan=0, rowspan=0, sticky=None):
        if fType == self.C_LABELFRAME:
            # first, make a LabelFrame, and position it correctly
            self.__verifyItem(self.n_labelFrames, title, True)
            container = LabelFrame(self.containerStack[-1]['container'], text=title)
            container.isContainer = True
            container.config(background=self.__getContainerBg(), font=self.labelFrameFont, relief="groove")
            self.__positionWidget(container, row, column, colspan, rowspan, "nsew")
            self.n_labelFrames[title] = container

            # now, add to top of stack
            self.__addContainer(self.C_LABELFRAME, container, 0, 1, sticky)
        elif fType == self.C_TABBEDFRAME:
            self.__verifyItem(self.n_tabbedFrames, title, True)
            tabbedFrame = TabbedFrame(self.containerStack[-1]['container'], bg=self.__getContainerBg())
            tabbedFrame.isContainer = True
            self.__positionWidget(tabbedFrame, row, column, colspan, rowspan, sticky=sticky)
            self.n_tabbedFrames[title] = tabbedFrame

            # now, add to top of stack
            self.__addContainer(self.C_TABBEDFRAME, tabbedFrame, 0, 1, sticky)
        elif fType == self.C_TAB:
            # add to top of stack
            self.containerStack[-1]['widgets']=True
            self.__addContainer(self.C_TAB, self.containerStack[-1]['container'].addTab(title), 0, 1, sticky)
        elif fType == self.C_PANEDWINDOW:
            # if we previously put a frame for widgets
            # remove it
            if self.containerStack[-1]['type'] == self.C_PANEDFRAME:
                self.stopContainer()

            # now, add the new pane
            self.__verifyItem(self.n_panedWindows, title, True)
            pane = PanedWindow(self.containerStack[-1]['container'], showhandle=True, sashrelief="groove", bg=self.__getContainerBg())
            pane.isContainer = True
            self.__positionWidget(pane, row, column, colspan, rowspan, sticky=sticky)
            self.n_panedWindows[title] = pane

            # now, add to top of stack
            self.__addContainer(self.C_PANEDWINDOW, pane, 0, 1, sticky)

            # now, add a frame to the pane
            self.startContainer(self.C_PANEDFRAME, title)
        elif fType == self.C_PANEDFRAME:
            # create a frame, and add it to the pane
            frame = Frame(self.containerStack[-1]['container'], bg=self.__getContainerBg())
            frame.isContainer = True
            self.containerStack[-1]['container'].add(frame)
            self.n_panedFrames[title] = frame

            # now, add to top of stack
            self.__addContainer(self.C_PANEDFRAME, frame, 0, 1, sticky)
        elif fType == self.C_SCROLLPANE:
            scrollPane = ScrollPane(self.containerStack[-1]['container'], bg=self.__getContainerBg(), width=100,height=100)
            scrollPane.isContainer = True
#                self.containerStack[-1]['container'].add(scrollPane)
            self.__positionWidget(scrollPane, row, column, colspan, rowspan, sticky=sticky)
            self.n_scrollPanes[title] = scrollPane

            # now, add to top of stack
            self.__addContainer(self.C_SCROLLPANE, scrollPane, 0, 1, sticky)
        elif fType == self.C_TOGGLEFRAME:
            toggleFrame = ToggleFrame(self.containerStack[-1]['container'], title=title, bg=self.__getContainerBg())
            toggleFrame.setFont(self.toggleFrameFont)
            toggleFrame.isContainer = True
            self.__positionWidget(toggleFrame, row, column, colspan, rowspan, sticky=sticky)
            self.__addContainer(self.C_TOGGLEFRAME, toggleFrame, 0, 1, "nw")
            self.n_toggleFrames[title] = toggleFrame
        elif fType == self.C_PAGEDWINDOW:
            # create the paged window
            pagedWindow = PagedWindow(self.containerStack[-1]['container'], title=title, bg=self.__getContainerBg(), width=200, height=400)
            # bind events
            self.topLevel.bind("<Left>", pagedWindow.showPrev)
            self.topLevel.bind("<Control-Left>", pagedWindow.showFirst)
            self.topLevel.bind("<Right>", pagedWindow.showNext)
            self.topLevel.bind("<Control-Right>", pagedWindow.showLast)
            # register it as a container
            pagedWindow.isContainer = True
            self.__positionWidget(pagedWindow, row, column, colspan, rowspan, sticky=sticky)
            self.__addContainer(self.C_PAGEDWINDOW, pagedWindow, 0, 1, "nw")
            self.n_pagedWindows[title] = pagedWindow
        elif fType == self.C_PAGE:
            page = self.containerStack[-1]['container'].addPage()
            page.isContainer = True
            self.__addContainer(self.C_PAGE, page, 0, 1, sticky)
            self.containerStack[-1]['expand']="None"
        else:
            raise Exception("Unknown container: " + fType)

    def startTabbedFrame(self, title, row=None, column=0, colspan=0, rowspan=0, sticky="NSEW"):
        self.startContainer(self.C_TABBEDFRAME, title, row, column, colspan, rowspan, sticky)

    def setTabbedFrameTabExpand(self, title, expand=True):
        nb = self.__verifyItem(self.n_tabbedFrames, title)
        nb.expandTabs(expand)

    def setTabbedFrameSelectedTab(self, title, tab):
        nb = self.__verifyItem(self.n_tabbedFrames, title)
        nb.changeTab(tab)

    def startTab(self, title):
        # auto close the previous TAB - keep it?
        if self.containerStack[-1]['type'] == self.C_TAB:
              self.warn("You didn't STOP the previous TAB")
              self.stopContainer()
        elif self.containerStack[-1]['type'] != self.C_TABBEDFRAME:
              raise Exception("Can't add a Tab to the current container: ", self.containerStack[-1]['type'])
        self.startContainer(self.C_TAB, title)

    def startPanedWindow(self, title, row=None, column=0, colspan=0, rowspan=0, sticky="NSEW"):
        self.startContainer(self.C_PANEDWINDOW, title, row, column, colspan, rowspan, sticky)

    def startSubWindow(self, name, title=None):
        self.__verifyItem(self.n_subWindows, name, True)
        if title == None: title=name
        top = SubWindow()
        top.title(title)
        top.protocol("WM_DELETE_WINDOW", self.__makeFunc(self.destroySubWindow, name))
        top.withdraw()
        top.win = self
        self.n_subWindows[name] = top

        # now, add to top of stack
        self.__addContainer(self.C_SUBWINDOW, top, 0, 1, "")

    # sticky is alignment inside frame
    # frame will be added as other widgets
    def startLabelFrame(self, title, row=None, column=0, colspan=0, rowspan=0, sticky=W):
        self.startContainer(self.C_LABELFRAME, title, row, column, colspan, rowspan, sticky)

    ###### TOGGLE FRAMES #######
    def startToggleFrame(self, title, row=None, column=0, colspan=0, rowspan=0):
        self.startContainer(self.C_TOGGLEFRAME, title, row, column, colspan, rowspan, sticky="new")

    def stopToggleFrame(self):
        if self.containerStack[-1]['type'] != self.C_TOGGLEFRAME:
            raise Exception("Can't stop a TOGGLEFRAME, currently in:", self.containerStack[-1]['type'])
        self.containerStack[-1]['container'].stop()
        self.stopContainer()

    def toggleToggleFrame(self, title):
        toggle = self.__verifyItem(self.n_toggleFrames, title)
        toggle.toggle()

    def disableToggleFrame(self, title, disabled=True):
        toggle = self.__verifyItem(self.n_toggleFrames, title)
        toggle.disable(disabled)

    def getToggleFrameState(self, title):
        toggle = self.__verifyItem(self.n_toggleFrames, title)
        return toggle.isShowing()

    ###### PAGED WINDOWS #######
    def startPagedWindow(self, title, row=None, column=0, colspan=0, rowspan=0):
        self.startContainer(self.C_PAGEDWINDOW, title, row, column, colspan, rowspan, sticky="nsew")

    def setPagedWindowPage(self, title, page):
        pager = self.__verifyItem(self.n_pagedWindows, title)
        pager.showPage(page)

    def setPagedWindowButtonsTop(self, title, top=True):
        pager = self.__verifyItem(self.n_pagedWindows, title)
        pager.setNavPositionTop(top)

    def setPagedWindowButtons(self, title, buttons):
        pager = self.__verifyItem(self.n_pagedWindows, title)
        if not isinstance(buttons, list) or len(buttons) != 2:
            raise Exception("You must provide a list of two strings fot setPagedWinowButtons()")
        pager.setPrevButton(buttons[0])
        pager.setNextButton(buttons[1])

    def setPagedWindowFunction(self, title, func):
        pager = self.__verifyItem(self.n_pagedWindows, title)
        command = self.__makeFunc(func, title)
        pager.registerPageChangeEvent(command)

    def getPagedWindowPageNumber(self, title):
        pager = self.__verifyItem(self.n_pagedWindows, title)
        return pager.getPageNumber()

    def showPagedWindowPageNumber(self, title, show=True):
        pager = self.__verifyItem(self.n_pagedWindows, title)
        pager.showLabel(show)

    def showPagedWindowTitle(self, title, show=True):
        pager = self.__verifyItem(self.n_pagedWindows, title)
        pager.showTitle(show)

    def setPagedWindowTitle(self, title, pageTitle):
        pager = self.__verifyItem(self.n_pagedWindows, title)
        pager.setTitle(pageTitle)

    def startPage(self, row=None, column=0, colspan=0, rowspan=0, sticky="nw"):
        if self.containerStack[-1]['type'] == self.C_PAGE:
            self.warn("You didn't STOP the previous PAGE")
            self.stopPage()
        elif self.containerStack[-1]['type'] != self.C_PAGEDWINDOW:
            raise Exception("Can't start a PAGE, currently in:", self.containerStack[-1]['type'])

        self.containerStack[-1]['widgets']=True
        self.startContainer(self.C_PAGE, None, row, column, colspan, rowspan, sticky="nw")

    def stopPage(self):
        if self.containerStack[-1]['type'] == self.C_PAGE:
            self.stopContainer()
        else:
            raise Exception("Can't stop PAGE, currently in:", self.containerStack[-1]['type'])
        self.containerStack[-1]['container'].stopPage()

    def stopPagedWindow(self):
        if self.containerStack[-1]['type'] == self.C_PAGE:
            self.warn("You didn't STOP the previous PAGE")
            self.containerStack[-1]['container'].stopPage()
            self.stopContainer()
        if self.containerStack[-1]['type'] != self.C_PAGEDWINDOW:
            raise Exception("Can't stop a PAGEDWINDOW, currently in:", self.containerStack[-1]['type'])
        self.stopContainer()

    ###### PAGED WINDOWS #######

    def startScrollPane(self, title, row=None, column=0, colspan=0, rowspan=0, sticky="NSEW"):
        self.startContainer(self.C_SCROLLPANE, title, row, column, colspan, rowspan, sticky)

    # functions to stop the various containers
    def stopContainer(self): self.__removeContainer()

    def stopSubWindow(self):
        if self.containerStack[-1]['type'] == self.C_SUBWINDOW:
              self.stopContainer()
        else:
              raise Exception("Can't stop a SUBWINDOW, currently in:", self.containerStack[-1]['type'])

    def stopTabbedFrame(self):
        # auto close the existing TAB - keep it?
        if self.containerStack[-1]['type'] == self.C_TAB:
              self.warn("You didn't STOP the previous TAB")
              self.stopContainer()
        self.stopContainer()

    def stopTab(self):
        if self.containerStack[-1]['type'] != self.C_TAB:
              raise Exception("Can't stop a TAB, currently in:", self.containerStack[-1]['type'])
        self.stopContainer()

    def stopLabelFrame(self):
        if self.containerStack[-1]['type'] != self.C_LABELFRAME:
              raise Exception("Can't stop a LABELFRAME, currently in:", self.containerStack[-1]['type'])
        self.stopContainer()

    def stopPanedWindow(self):
        if self.containerStack[-1]['type'] == self.C_PANEDFRAME:
              self.stopContainer()
        if self.containerStack[-1]['type'] != self.C_PANEDWINDOW:
              raise Exception("Can't stop a PANEDWINDOW, currently in:", self.containerStack[-1]['type'])
        self.stopContainer()

    def stopScrollPane(self):
        if self.containerStack[-1]['type'] != self.C_SCROLLPANE:
              raise Exception("Can't stop a SCROLLPANE, currently in:", self.containerStack[-1]['type'])
        self.stopContainer()

    def stopAllPanedWindows(self):
        while True:
              try: self.stopPanedWindow()
              except: break

    # functions to show/hide/destroy SubWindows
    def showSubWindow(self, title):
        tl = self.__verifyItem(self.n_subWindows, title)
        tl.deiconify()
        tl.config(takefocus=True)

    def setSubWindowLocation(self, title, x, y):
        tl = self.__verifyItem(self.n_subWindows, title)
        tl.geometry("+%d+%d" % (x, y))

    def hideSubWindow(self, title):
        self.__verifyItem(self.n_subWindows, title).withdraw()

    def destroySubWindow(self, title):
        topLevel = self.__verifyItem(self.n_subWindows, title)
        theFunc = topLevel.stopFunction
        if theFunc is None or theFunc():
            # stop any sounds, ignore error when not on Windows
            topLevel.destroy()
            del self.n_subWindows[title]

    # make a PanedWindow align vertically
    def setPanedWindowVertical(self, window):
        pane = self.__verifyItem(self.n_panedWindows, window )
        pane.config(orient=VERTICAL)

    # function to set position of title for label frame
    def setLabelFrameAnchor(self, title, anchor):
        frame = self.__verifyItem(self.n_labelFrames, title)
        frame.config(labelanchor=anchor)

    # functions to change colours of TabbedFrames
    def setTabbedFrameTabBg(self, tabbedFrame, tab, bg):
        myFrame = self.__verifyItem(self.n_tabbedFrames, tabbedFrame)
        myFrame.setTabBg(tab, bg)

    def setTabbedFrameTab(self, tabbedFrame, tab):
        myFrame = self.__verifyItem(self.n_tabbedFrames, tabbedFrame)
        myFrame.changeTab(tab)

    def setTabbedFrameFg(self, tabbedFrame, active, inactive):
        myFrame = self.__verifyItem(self.n_tabbedFrames, tabbedFrame)
        myFrame.setFg(active, inactive)

    def setTabbedFrameBg(self, tabbedFrame, active, inactive):
        myFrame = self.__verifyItem(self.n_tabbedFrames, tabbedFrame)
        myFrame.setBg(active, inactive)

#####################################
## warn when bad functions called...
#####################################
    def __getattr__(self,name):
        def handlerFunction(*args,**kwargs):
              self.warn("Unknown function:"+name+" "+str(args)+" "+str(kwargs))
        return handlerFunction

    def __setattr__(self, name, value):
        if self.built == True and not hasattr(self, name): # would this create a new attribute?
              raise AttributeError("Creating new attributes is not allowed!")
        super(gui, self).__setattr__(name, value)

#####################################
## FUNCTION to add labels before a widget
#####################################
    # this will build a frame, with a label on the left hand side
    def __getLabelBox(self, title):
        self.__verifyItem(self.n_labels, title, True)

        # first, make a frame
        frame = LabelBox(self.__getContainer())
        frame.config( background=self.__getContainerBg() )
        self.n_frames.append(frame)

        # if this is a big label, update the others to match...
        if len(title) > self.labWidth:
              self.labWidth = len(title)
              #loop through other labels and resize
              for na in self.n_frameLabs:
#                        self.n_frameLabs[na].config(width=self.labWidth)
                    pass

        # next make the label
        lab = Label(frame)
        frame.theLabel = lab
        lab.hidden = False
        lab.inContainer = True
        lab.config( anchor=W,text=title, justify=LEFT, font=self.labelFont, background=self.__getContainerBg() )
#            lab.config( width=self.labWidth)
        self.n_labels[title]=lab
        self.n_frameLabs[title]=lab

        # now put the label in the frame
        lab.pack(side=LEFT, fill=Y)
        #lab.grid ( row=0, column=0, sticky=W )
        #Grid.columnconfigure(frame, 0, weight=1)
        #Grid.rowconfigure(frame, 0, weight=1)

        return frame

    # this is where we add the widget to the frame built above
    def __packLabelBox(self, frame, widget):
        widget.pack(side=LEFT, fill=BOTH, expand=True)
        widget.inContainer = True
        frame.theWidget=widget
        #widget.grid ( row=0, column=1, sticky=W+E )
        #Grid.columnconfigure(frame, 1, weight=1)
        #Grid.rowconfigure(frame, 0, weight=1)

    # function to resize labels, if they are hidden or shown
    def __updateLabelBoxes(self, title):
        if len(title) >= self.labWidth:
              self.labWidth = 0
              #loop through other labels and resize
              for na in self.n_frameLabs:
                    size = len ( self.n_frameLabs[na].cget("text") )
                    if not self.n_frameLabs[na].hidden and size > self.labWidth: self.labWidth = size
              for na in self.n_frameLabs:
                    self.n_frameLabs[na].config(width=self.labWidth)

#####################################
## FUNCTION for check boxes
#####################################
    def addCheckBox(self, title, row=None, column=0, colspan=0, rowspan=0):
        self.__verifyItem(self.n_cbs, title, True)
        var=IntVar(self.topLevel)
        cb = Checkbutton(self.__getContainer())
        cb.config(text=title, variable=var, font=self.cbFont, background=self.__getContainerBg(), activebackground=self.__getContainerBg())
        cb.config(anchor=W)
        cb.bind("<Button-1>", self.__grabFocus)
        self.n_cbs[title]=cb
        self.n_boxVars[title]=var
        self.__positionWidget(cb, row, column, colspan, rowspan, EW)

    def getCheckBox(self, title):
        bVar = self.__verifyItem(self.n_boxVars, title)
        if bVar.get() == 1: return True
        else: return False

    def setCheckBox(self, title, ticked=True):
        cb = self.__verifyItem(self.n_cbs, title)
        if ticked: cb.select()
        else: cb.deselect()

#####################################
## FUNCTION for scales
#####################################

    def __buildScale(self, title, frame):
        self.__verifyItem(self.n_scales, title, True)
        scale = Scale(frame)
        scale.config(repeatinterval=10,digits=1,orient=HORIZONTAL, showvalue=False, highlightthickness=1)
        self.n_scales[title] = scale
        scale.bind("<Button-1>", self.__grabFocus)
        return scale

    def addScale(self, title, row=None, column=0, colspan=0, rowspan=0):
        scale = self.__buildScale(title, self.__getContainer())
        self.__positionWidget(scale, row, column, colspan, rowspan)

    def addLabelScale(self, title, row=None, column=0, colspan=0, rowspan=0):
        frame = self.__getLabelBox(title)
        scale = self.__buildScale(title, frame)
        self.__packLabelBox(frame, scale)
        self.__positionWidget(frame, row, column, colspan, rowspan)

    def getScale(self, title):
        sc = self.__verifyItem(self.n_scales, title)
        return sc.get()

    def setScale(self, title, pos):
        sc = self.__verifyItem(self.n_scales, title)
        sc.set(pos)

    def setScaleWidth(self, title, width):
        sc = self.__verifyItem(self.n_scales, title)
        sc.config(width=width)

    def setScaleLength(self, title, length):
        sc = self.__verifyItem(self.n_scales, title)
        sc.config(sliderlength=length)

    # this will make the scale show interval numbers
    # set to 0 to remove
    def showScaleIntervals(self, title, intervals):
        sc = self.__verifyItem(self.n_scales, title)
        sc.config(tickinterval=intervals)

    # this will make the scale show its value
    def showScaleValue(self, title, show=True):
        sc = self.__verifyItem(self.n_scales, title)
        sc.config(showvalue=show)

    # change the orientation (Hor or Vert)
    def orientScaleHor(self, title, hor=True):
        self.warn(".orientScaleHor() is deprecated. Please use .setScaleHorizontal() or .setScaleVertical()")
        sc = self.__verifyItem(self.n_scales, title)
        if hor: sc.config(orient=HORIZONTAL)
        else: sc.config(orient=VERTICAL)

    def setScaleVertical(self, title):
        sc = self.__verifyItem(self.n_scales, title)
        sc.config(orient=VERTICAL)

    def setScaleHorizontal(self, title):
        sc = self.__verifyItem(self.n_scales, title)
        sc.config(orient=HORIZONTAL)

    def setScaleRange(self, title, start, end, curr=None):
        if curr is None: curr=start
        sc = self.__verifyItem(self.n_scales, title)
        sc.config(from_=start, to=end)
        self.setScale(title, curr)

#####################################
## FUNCTION for simple grids - RETHINK
#####################################
    # first row is used as a header
# ADD ROWSPAN HERE WHEN FIXIBG...
    def addGrid(self, title, data, row=None, column=0, colspan=0, rowspan=0, action=None, addRow=False):
        self.__verifyItem(self.n_grids, title, True)
        frame = self.__makeGrid(title, data, action, addRow)
        self.__positionWidget(frame, row, column, colspan, rowspan, N+E+S+W)

    def updateGrid(self, title, data, addRow=None):
        frame = self.__verifyItem(self.n_grids, title)
        params = frame.grid_info()
        action = frame.action
        if addRow is None: addRow = frame.addRow
        entries = frame.entries
        for e in frame.entries:
              del self.n_entries[e.myTitle]

        del ( self.n_grids[title] )
        frame.grid_forget()
        frame.destroy()

        self.addGrid(title, data, int(params["row"]), int(params["column"]), int(params["columnspan"]), action, addRow)

    def __refreshGrids(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        for name in self.n_grids:
            can = self.n_grids[name].c1
            can.configure(scrollregion=can.bbox("all"))
            #can.itemconfig(_id, height=frame.c1.height, width=frame.c1.width)

    def __gridCellEnter(self, event):
        cell = event.widget
        cell.config(background=self.gdHBg)

    def __gridCellLeave(self, event):
        cell = event.widget
        if cell.selected: cell.config(background=self.gdSBg)
        else: cell.config(background=self.gdBg)

    def __gridCellClick(self, event):
        cell = event.widget
        if cell.selected:
            cell.selected = False
            cell.config(background=self.gdBg)
        else:
            cell.selected = True
            cell.config(background=self.gdSBg)

    # function to scroll the canvas/scrollbars
    # gets the requested grid
    # and checks the event.delta to determine where to scroll
    # https://www.daniweb.com/programming/software-development/code/217059/using-the-mouse-wheel-with-tkinter-python
    def __scrollGrid(self, event, title):
        if platform() in [ "win32", "Windows", "Darwin"]:
              if platform() in [ "win32", "Windows"]:
                  val = event.delta/120
              else:
                  val = event.delta

              val = val * -1

              if event.delta in [1,-1]:
                  self.n_grids[title].c1.yview_scroll(val, "units")
              elif event.delta in [2,-2]:
                  self.n_grids[title].c1.xview_scroll(val, "units")

        elif platform() == "Linux":
                if event.num == 4:
                    self.n_grids[title].c1.yview_scroll(-1*2, "units")
                elif event.num == 5:
                    self.n_grids[title].c1.yview_scroll(2, "units")

    def setGridGeom(self, title, width=200, height=200):
        grid = self.__verifyItem(self.n_grids, title)
        grid.configure(width=width, height=height)

    def getGridEntries(self, title):
        return [e.var.get() for e in self.__verifyItem(self.n_grids, title).entries ]

    def setGridBackground(self, title, colour=None):
        grid = self.__verifyItem(self.n_grids, title)
        if colour == None: colour = self.gdC
        self.gdC = colour
        grid.c1.configure(background=self.gdC, highlightcolor=self.gdC, highlightbackground=self.gdC)

    # note - if use grid layout, can use AutoScrollBar
    # However, couldn't get canvas to expand in frame using grid
    def __makeGrid(self, title, data, action=None, addRow=False):
        frame = Frame(self.__getContainer())
        frame.configure( background=self.__getContainerBg() )
        self.n_grids[title] = frame
        frame.action = action
        frame.addRow = addRow
        frame.entries = []      # store them in the frame object for access, later

        frame.c1 = Canvas(frame, borderwidth=0, highlightthickness=2)

        if platform() == "Linux":
            frame.c1.bind_all("<4>", lambda event, arg=title: self.__scrollGrid(event, arg))
            frame.c1.bind_all("<5>", lambda event, arg=title: self.__scrollGrid(event, arg))
        else:
            # Windows and MacOS
            frame.c1.bind_all("<MouseWheel>", lambda event, arg=title: self.__scrollGrid(event, arg))

        self.setGridBackground(title)

        vsb = Scrollbar(frame, orient="vertical", command=frame.c1.yview)
        frame.c1.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        #vsb.grid(row=0, column=1, sticky=N+S)

        hsb = Scrollbar(frame, orient="horizontal", command=frame.c1.xview)
        frame.c1.configure(xscrollcommand=hsb.set)
        hsb.pack(side="bottom", fill="x")
        #hsb.grid(row=1, column=0, sticky=E+W)

        frame.c1.pack(side="left", fill="both", expand=True)
        #frame.c1.grid(row=0, column=0, sticky=N+S+E+W)

        #frame.c1.grid_rowconfigure(0, weight=1)
        #frame.c1.grid_columnconfigure(0, weight=1)

        gridFrame = Frame(frame.c1)
        gridFrame.configure( background=self.__getContainerBg() )
        frame.c1.create_window((4,4), window=gridFrame, anchor="nw", tags="gridFrame")
        gridFrame.bind("<Configure>", self.__refreshGrids)

        # find the longest row...
        maxSize = 0
        for rowNum in range(len(data)):
              if len(data[rowNum]) > maxSize: maxSize = len(data[rowNum])

        # loop through each row
        for rowNum in range(len(data)):
              vals = []
              # then the cells in that row
              for cellNum in range(maxSize):
                    # get a name and val ("" if no val)
                    name = "c" + str(rowNum) + "-" + str(cellNum)
                    if cellNum >= len(data[rowNum]) : val = ""
                    else: val = data[rowNum][cellNum]
                    vals.append(val)

                    lab = Label(gridFrame)
                    lab.selected = False
                    if rowNum == 0: lab.configure( relief=RIDGE,text=val, font=self.ghFont, background=self.ghBg )
                    else:
                          lab.configure( relief=RIDGE,text=val, font=self.gdFont, background=self.gdBg )
                          lab.bind("<Enter>", self.__gridCellEnter)
                          lab.bind("<Leave>", self.__gridCellLeave)
                          lab.bind("<Button-1>", self.__gridCellClick)

                    lab.grid ( row=rowNum, column=cellNum, sticky=N+E+S+W )
                    Grid.columnconfigure(gridFrame, cellNum, weight=1)
              Grid.rowconfigure(gridFrame, rowNum, weight=1)

              # add some buttons for each row
              if action is not None:
                    widg = Label(gridFrame)
                    widg.configure( relief=RIDGE )
                    if rowNum == 0:
                          widg.configure( text="Action", font=self.ghFont, background=self.ghBg )
                    else:
                          but = Button(widg)
                          but.configure( text="Press", command=self.__makeFunc(action, vals),font=self.buttonFont )
                          but.grid ( row=0,column=0, sticky=N+E+S+W )
                    widg.grid ( row=rowNum, column=cellNum+1, sticky=N+E+S+W )
        # add a row of entry boxes...
        if addRow==True:
              for cellNum in range(maxSize):
                    name = "GR"+str(cellNum)
                    #widg = Label(gridFrame)
                    #widg.configure( relief=RIDGE )
                    #entry = self.__buildEntry(name, widg)
                    widg = self.__buildEntry(name, gridFrame)
                    frame.entries.append(widg)
                    #entry.grid ( row=0,column=0, sticky=N+E+S+W )
                    widg.grid ( row=len(data), column=cellNum, sticky=N+E+S+W )
              widg = Label(gridFrame)
              widg.configure( relief=RIDGE )
              but = Button(widg)
              but.configure( text="Press", command=self.__makeFunc(action, "newRow"),font=self.buttonFont )
              but.grid ( row=0,column=0, sticky=N+E+S+W )
              widg.grid ( row=len(data), column=maxSize, sticky=N+E+S+W )

        return frame

#####################################
## FUNCTION for optionMenus
#####################################
    def __buildOptionBox(self, frame, title, options, kind="normal"):
        self.__verifyItem(self.n_options, title, True)

        # create a string var to hold selected item
        var=StringVar(self.topLevel)
        self.n_optionVars[title]=var

        maxSize, options = self.__configOptionBox(title, options, kind)

        if len(options) > 0 and kind == "normal":
            option = OptionMenu(frame,var,*options)
            var.set(options[0])
            option.kind="normal"
        elif kind == "ticks":
            ## http://stackoverflow.com/questions/29019760/how-to-create-a-combobox-that-includes-checkbox-for-each-item
            option = OptionMenu(frame,variable=var,value="")
            # delete the empty value we just added
            option['menu'].delete(0, 'end')
            var.set(title)
            vals = []
            for o in options:
                vals.append(BooleanVar())
                option['menu'].add_checkbutton(label=o, onvalue=1, offvalue=False, variable=vals[-1])
            self.n_optionVars[title]=vals
            option.kind="ticks"
        else:
            option = OptionMenu(frame,var,[])
            option.kind="normal"

        option.config(justify=LEFT, font=self.optionFont, background=self.__getContainerBg(), highlightthickness=1, width=maxSize, takefocus=1)
        option.bind("<Button-1>", self.__grabFocus)
        # compare on windows & mac
        #option.config(highlightthickness=12, bd=0, highlightbackground=self.__getContainerBg())
        option.var = var
        option.maxSize = maxSize
        option.inContainer = False
        option.options = options

        # configure the drop-down too
        dropDown = option.nametowidget(option.menuname)
        dropDown.configure(font=self.optionFont)
#            dropDown.configure(background=self.__getContainerBg())

#        if platform() == "Darwin":
#              option.config(highlightbackground=self.__getContainerBg())

        option.bind("<Tab>", self.__focusNextWindow)
        option.bind("<Shift-Tab>", self.__focusLastWindow)

        self.__disableOptionBoxSeparators(option)

        # add to array list
        self.n_options[title]=option
        return option

    def addOptionBox(self, title, options, row=None, column=0, colspan=0, rowspan=0):
        option = self.__buildOptionBox(self.__getContainer(), title, options)
        self.__positionWidget(option, row, column, colspan, rowspan)

    # under development
    def addTickOptionBox(self, title, options, row=None, column=0, colspan=0, rowspan=0):
        tick = self.__buildOptionBox(self.__getContainer(), title, options, "ticks")
        self.__positionWidget(tick, row, column, colspan, rowspan)

    def addLabelTickOptionBox(self, title, options, row=None, column=0, colspan=0, rowspan=0):
        frame = self.__getLabelBox(title)
        tick = self.__buildOptionBox(frame, title, options, "ticks")
        self.__packLabelBox(frame, tick)
        self.__positionWidget(frame, row, column, colspan, rowspan)

    def addLabelOptionBox(self, title, options, row=None, column=0, colspan=0, rowspan=0):
        frame = self.__getLabelBox(title)
        option = self.__buildOptionBox(frame, title, options)
        self.__packLabelBox(frame, option)
        self.__positionWidget(frame, row, column, colspan, rowspan)

    def getOptionBox(self, title):
        self.__verifyItem(self.n_optionVars, title)
        val=self.n_optionVars[title]

        if type(val) == list:
            ## get list of values ##
            menu = self.n_options[title]["menu"]
            last = menu.index("end")
            items = []
            for index in range(last+1):
                items.append(menu.entrycget(index, "label"))
            ########################
            vals={}
            for pos, v in enumerate(val):
                if v.get(): vals[items[pos]] = True
                else: vals[items[pos]] = False
            return vals
        else:
            val = val.get().strip()
            # set to None if it's a divider
            if val.startswith("-") or len(val) == 0: val = None
            return val

    def __disableOptionBoxSeparators(self, box):
        # disable any separators
        for pos, item in enumerate(box.options):
            if item.startswith("-"):
                box["menu"].entryconfigure(pos, state="disabled")


    def __configOptionBox(self, title, options, kind):
        # deal with a dict_keys object - messy!!!!
        if not isinstance(options, list): options = list(options)

        options = [str(i) for i in options]
        # create a title if necessary
        found = False
        for pos, item in enumerate(options):
            if item == "":
                if not found:
                    options[pos] = "- options -"
                    found = True
                else:
                    del options[pos]

        # get the longest string length
        try: maxSize = len(str(max(options, key=len)))
        except:
            try: maxSize = len(str(max(options)))
            except: maxSize = 0

        if kind == "ticks":
            if len(title) > maxSize:
                maxSize = len(title)

        return maxSize, options

    # http://www.prasannatech.net/2009/06/tkinter-optionmenu-changing-choices.html
    def changeOptionBox(self, title, options, index=None):
        self.__verifyItem(self.n_optionVars, title)

        # get the relevant items
        box = self.n_options[title]
        if box.kind == "ticks":
            self.warn("Unable to change TickOptionBoxes")
            return
        var = self.n_optionVars[title]

        maxSize, options = self.__configOptionBox(title, options, "normal")

        # warn if new options bigger
        if maxSize > box.maxSize:
            self.warn("The new options are longer then the old ones. " + str(maxSize) + ">"+str(box.maxSize))

        # delete the current options
        box['menu'].delete(0, 'end')
        var.set(" ")
        box.options = options

        # add the new items
        for option in options:
              box["menu"].add_command(label=option, command=lambda temp = option: box.setvar(box.cget("textvariable"), value = temp))

        # disable any separators
        self.__disableOptionBoxSeparators(box)

        # select the specified option
        self.setOptionBox(title, index)

    # select the option at the specified position
    def setOptionBox(self, title, index):
        self.__verifyItem(self.n_optionVars, title)
        box = self.n_options[title]
        if box.kind == "ticks":
            self.warn("Unable to set TickOptionBoxes")
            return
        count = len(box.options)
        if index is None: index = 0
        if count > 0:
            if not isinstance(index, int):
                try: index = box.options.index(index)
                except:
                    self.warn("Inavlid selection option: " + str(index))
                    return

            if index < 0 or index > count-1:
                self.warn("Invalid selection index: " + str(index) + ". Should be between 0 and " + str(count-1) + ".")
            else:
                if not box['menu'].invoke(index):
                    self.warn("Invalid selection index: " + str(index) + " is a disabled index.")
        else:
            self.warn("No items to select from: " + title)

#####################################
## FUNCTION to add spin boxes
#####################################
    def __buildSpinBox(self, frame, title, vals):
        self.__verifyItem(self.n_spins, title, True)
        if type(vals) not in [list, tuple]:
              raise Exception("Can't create SpinBox " + title + ". Invalid values: " + str(vals))
        vals=list(vals)
        vals.reverse()
        vals=tuple(vals)

        spin = Spinbox(frame)
        spin.inContainer = False
        spin.config(font=self.entryFont, highlightthickness=0)

# adds bg colour under spinners
#        if platform() == "Darwin":
#              spin.config(highlightbackground=self.__getContainerBg())

        spin.bind("<Tab>", self.__focusNextWindow)
        spin.bind("<Shift-Tab>", self.__focusLastWindow)

        spin.config(values=vals)
        # prevent invalid entries
        if self.validateSpinBox == None:
              self.validateSpinBox = (self.containerStack[0]['container'].register(self.__validateSpinBox),'%P', '%W')

        spin.config(validate='all', validatecommand=self.validateSpinBox)

        self.n_spins[title] = spin
        return  spin


    def __addSpinBox(self, title, values,row=None, column=0, colspan=0, rowspan=0):
        spin = self.__buildSpinBox(self.__getContainer(), title, values)
        self.__positionWidget(spin, row, column, colspan, rowspan)
        self.setSpinBoxPos(title, 0)

    def addSpinBox(self, title, values, row=None, column=0, colspan=0, rowspan=0):
        self.__addSpinBox(title, values, row, column, colspan, rowspan)

    def addLabelSpinBox(self, title, values, row=None, column=0, colspan=0, rowspan=0):
        frame = self.__getLabelBox(title)
        spin = self.__buildSpinBox(frame, title, values)
        self.__packLabelBox(frame, spin)
        self.__positionWidget(frame, row, column, colspan, rowspan)
        self.setSpinBoxPos(title, 0)

    def addSpinBoxRange(self, title, fromVal, toVal, row=None, column=0, colspan=0, rowspan=0):
        vals = list(range(fromVal, toVal+1))
        self.__addSpinBox(title, vals, row, column, colspan, rowspan)

    def addLabelSpinBoxRange(self, title, fromVal, toVal, row=None, column=0, colspan=0, rowspan=0):
        vals = list(range(fromVal, toVal+1))
        self.addLabelSpinBox(title, vals, row, column, colspan, rowspan)

    def getSpinBox(self, title):
        spin = self.__verifyItem(self.n_spins, title)
        return spin.get()

    # validates that an item in the named spinbox starts with the user_input
    def __validateSpinBox(self, user_input, widget_name):
        spin = self.containerStack[0]['container'].nametowidget(widget_name)

        vals = spin.cget("values")#.split()
        vals=self.__getSpinBoxValsAsList(vals)
        for i in vals:
              if i.startswith(user_input): return True

        self.containerStack[0]['container'].bell()
        return False

    # expects a valid spin box widget, and a valid value
    def __setSpinBoxVal(self, spin, val):
        var = StringVar(self.topLevel)
        var.set(val)
        spin.config(textvariable=var)

    # is it going to be a hash or list??
    def __getSpinBoxValsAsList(self, vals):
        if "{" in vals:
            vals=vals[1:-1]
            vals=vals.split("} {")
        else:
            vals=vals.split()
        return vals

    def setSpinBox(self, title, value):
        spin = self.__verifyItem(self.n_spins, title)
        vals = spin.cget("values")#.split()
        vals = self.__getSpinBoxValsAsList(vals)
        val = str(value)
        if val not in vals:
              raise Exception("Invalid value: "+ val + ". Not in SpinBox: "+title+"=" + str(vals)) from None
        self.__setSpinBoxVal(spin, val)

    def setSpinBoxPos(self, title, pos):
        spin = self.__verifyItem(self.n_spins, title)
        vals = spin.cget("values")#.split()
        vals = self.__getSpinBoxValsAsList(vals)
        pos=int(pos)
        if pos <  0 or pos >= len(vals):
              raise Exception("Invalid position: "+ str(pos) + ". No position in SpinBox: "+title+"=" + str(vals)) from None
        pos = len(vals)-1 - pos
        val = vals[pos]
        self.__setSpinBoxVal(spin, val)

#####################################
## FUNCTION to add images
#####################################
    # looks up label containing image
    def __animateImage(self, title):
        lab = self.__verifyItem(self.n_images, title)
        if not lab.image.animating: return
        try:
              if lab.image.cached:
                    pic =lab.image.pics[lab.image.anim_pos]
              else:
                    pic = PhotoImage(file=lab.image.path, format="gif - {}".format(lab.image.anim_pos))
                    lab.image.pics.append(pic)
              lab.image.anim_pos += 1
              lab.config(image=pic)
              self.topLevel.after(lab.image.anim_speed, self.__animateImage, title)
        except:
              lab.image.anim_pos=0
              lab.image.cached=True
              self.__animateImage(title)

    def __preloadAnimatedImage(self, img):
        if img.cached: return
        try:
            pic = PhotoImage(file=img.path, format="gif - {}".format(img.anim_pos))
            img.pics.append(pic)
            img.anim_pos += 1
            self.topLevel.after(0, self.__preloadAnimatedImage, img)
        # when all frames have been processed
        except TclError:
              img.anim_pos=0
              img.cached=True

    def __configAnimatedImage(self, img):
        img.isAnimated=True
        img.pics=[]
        img.cached=False
        img.anim_pos=0
        img.anim_speed=150
        img.animating=True

    # simple way to check if image is animated
    def __checkIsAnimated(self, name):
        if imghdr.what(name) == "gif":
            try:
                PhotoImage(file=name, format="gif - 1")
                return True
            except: pass
        return False

    def setAnimationSpeed(self, name, speed):
        img = self.__verifyItem(self.n_images, name).image
        img.anim_speed=speed

    def stopAnimation(self, name):
        img = self.__verifyItem(self.n_images, name).image
        img.animating=False

    def startAnimation(self, name):
        img = self.__verifyItem(self.n_images, name).image
        if not img.animating:
              img.animating=True
              self.topLevel.after(img.anim_speed, self.__animateImage, name)

    def addAnimatedImage(self, name, imageFile, row=None, column=0, colspan=0, rowspan=0):
        self.warn("addAnimatedImage() is now deprecated - use addImage()")
        self.addImage(name, imageFile, row, column, colspan, rowspan)

    # function to set an alternative image, when a mouse goes over
    def setImageMouseOver(self, title, overImg):
        lab = self.__verifyItem(self.n_images, title)
        leaveImg=lab.image.path
        lab.bind("<Leave>", lambda e: self.setImage(title, leaveImg))
        lab.bind("<Enter>", lambda e: self.setImage(title, overImg))

    # function to set an image location
    def setImageLocation(self, location):
        if os.path.isdir(location):
            self.userImages = location
        else:
            raise Exception("Invalid image location: " + location)

    # function to remove image objects form cache
    def clearImageCache(self):
        self.n_imageCache = {}

    # internal function to check/build image object
    def __getImage(self, imagePath, cache=True):
        if imagePath is None: return None
        if self.userImages is not None:
            imagePath = os.path.join(self.userImages,imagePath)

        if cache and imagePath in self.n_imageCache and self.n_imageCache[imagePath] is not None:
              photo=self.n_imageCache[imagePath]
        elif os.path.isfile(imagePath):
              if os.access(imagePath, os.R_OK):
                    imgType = imghdr.what(imagePath)
                    if not imagePath.lower().endswith(imgType) and not (imgType=="jpeg" and imagePath.lower().endswith("jpg")):
                          # the image has been saved with the wrong extension
                          raise Exception("Invalid image extension: " + imagePath + " should be a ." + imgType)
                    elif imagePath.lower().endswith('.gif'):
                          photo=PhotoImage(file=imagePath)
                    elif imagePath.lower().endswith('.ppm') or imagePath.lower().endswith('.pgm'):
                          photo=PhotoImage(file=imagePath)
                    elif imagePath.lower().endswith('jpg') or imagePath.lower().endswith('jpeg'):
                          self.warn("Image processing for .JPGs is slow. .GIF is the recommended format")
                          photo=self.convertJpgToBmp(imagePath)
                    elif imagePath.lower().endswith('.png'):
                          self.warn("Image processing for .PNGs is slow. .GIF is the recommended format")
                          # known issue here, some PNGs lack IDAT chunks
                          png = PngImageTk(imagePath)
                          png.convert()
                          photo=png.image
                    else:
                          raise Exception("Invalid image type: "+ imagePath) from None
              else:
                    raise Exception("Can't read image: "+ imagePath) from None
        else:
              raise Exception("Image "+imagePath+" does not exist") from None

        photo.path=imagePath

        # sort out if it's an animated images
        if self.__checkIsAnimated(imagePath):
            self.__configAnimatedImage(photo)
            self.__preloadAnimatedImage(photo)
        else:
            photo.isAnimated=False
            photo.animating=False
            if cache: self.n_imageCache[imagePath]=photo

        return photo

    # replace the current image, with a new one
    def setImage(self, name, imageFile):
        label = self.__verifyItem(self.n_images, name)
        # only set the image if it's different
        if label.image.path == imageFile: return

        label.image.animating=False
        image = self.__getImage(imageFile)

        label.config(image=image)
        label.config(anchor=CENTER, font=self.labelFont, background=self.__getContainerBg())
        label.image = image # keep a reference!

        if image.isAnimated:
                self.topLevel.after(image.anim_speed, self.__animateImage, name)

        # removed - keep the label the same size, and crop images
        #h = image.height()
        #w = image.width()
        #label.config(height=h, width=w)
        self.topLevel.update_idletasks()

    # must be GIF or PNG
    def addImage(self, name, imageFile, row=None, column=0, colspan=0, rowspan=0):
        #image = re.escape(image)
        self.__verifyItem(self.n_images, name, True)
        img = self.__getImage(imageFile)

        label = Label(self.__getContainer())
        label.config(anchor=CENTER, font=self.labelFont, background=self.__getContainerBg())
        label.config(image=img)
        label.image = img # keep a reference!

        if img is not None:
              h = img.height()
              w = img.width()
              label.config(height=h, width=w)

        self.n_images[name] = label
        self.__positionWidget(label, row, column, colspan, rowspan)
        if img.isAnimated:
                self.topLevel.after(img.anim_speed, self.__animateImage, name)

    def setImageSize(self, name, width, height):
        img = self.__verifyItem(self.n_images, name)
        img.config(height=height, width=width)

#      def rotateImage(self, name, image):
#            img = self.__verifyItem(self.n_images, name)

    #if +ve then grow, else shrink...
    def zoomImage(self, name, x, y=''):
        img = self.__verifyItem(self.n_images, name)
        if x <= 0: self.shrinkImage(name, x*-1, y*-1)
        else: self.growImage(name, x, y)

    #get every nth pixel (must be an integer)
    # 0 will return an empty image, 1 will return the image, 2 will be 1/2 the size ...
    def shrinkImage(self, name, x, y=''):
        img = self.__verifyItem(self.n_images, name)
        image = img.image.subsample(x,y)

        img.config(image=image)
        img.config(anchor=CENTER, font=self.labelFont, background=self.__getContainerBg())
        img.modImage = image # keep a reference!
        img.config(width=image.width(), height=image.height())

    #get every nth pixel (must be an integer)
    # 0 won't work, 1 will return the original size
    def growImage(self, name, x,y=''):
        label = self.__verifyItem(self.n_images, name)
        image = label.image.zoom(x,y)

        label.config(image=image)
        label.config(anchor=CENTER, font=self.labelFont, background=self.__getContainerBg())
        label.modImage = image # keep a reference!
        label.config(width=image.width(), height=image.height())

    def convertJpgToBmp(self, image):
        # read the image into an array of bytes
        with open(image, 'rb') as inFile:
              import array
              buf = array.array("B",inFile.read())

        # init the translator, and decode the array of bytes
        nanojpeg.njInit()
        nanojpeg.njDecode(buf, len(buf))

        # determine a file name & type
        if nanojpeg.njIsColor():
              fileName = image.split('.jpg', 1)[0] + '.ppm'
              param = 6
        else:
              fileName = image.split('.jpg', 1)[0] + '.pgm'
              fileName = "test3.pgm"
              param = 5

        # create a string, starting with the header
        val = "P%d\n%d %d\n255\n" % (param, nanojpeg.njGetWidth(), nanojpeg.njGetHeight())
        # append the bytes, converted to chars
        val += ''.join(map(chr,nanojpeg.njGetImage()))

        # release any stuff
        nanojpeg.njDone()

        photo = PhotoImage(data=val)
        return photo

        # write the chars to a new file, if python3 we need to encode them first
#            with open(fileName, "wb") as outFile:
#                  if sys.version_info[0] == 2: outFile.write(val)
#                  else: outFile.write(val.encode('ISO-8859-1'))
#
#            return fileName

    # function to set a background image
    # make sure this is done before everything else, otherwise it will cover other widgets
    def setBgImage(self, image):
        image = self.__getImage(image, False) # make sure it's not cached
        #self.containerStack[0]['container'].config(image=image) # window as a label doesn't work...
        self.bgLabel.config(image=image)
        self.containerStack[0]['container'].image = image # keep a reference!

    def removeBgImage(self):
        self.bgLabel.config(image=None)
        #self.containerStack[0]['container'].config(image=None) # window as a label doesn't work...
        self.containerStack[0]['container'].image = None # remove the reference - shouldn't be cached

    def resizeBgImage(self):
        if self.containerStack[0]['container'].image == None: return
        else:
              pass

#####################################
## FUNCTION to play sounds
#####################################
    # function to set a sound location
    def setSoundLocation(self, location):
        if os.path.isdir(location):
            self.userSounds = location
        else:
            raise Exception("Invalid sound location: " + location)

    # internal function to manage sound availability
    def __soundWrap(self, sound, isFile=False, repeat=False, wait=False):
        if platform() in ["win32", "Windows"]:
              if self.userSounds is not None:
                    sound = os.path.join(self.userSounds,sound)

              if isFile:
                    if False== os.path.isfile(sound): raise Exception("Can't find sound: "+ sound)
                    if not sound.lower().endswith('.wav'): raise Exception("Invalid sound format: "+ sound)
                    kind = winsound.SND_FILENAME | winsound.SND_ASYNC
              else:
                    if sound is None:
                          kind = winsound.SND_FILENAME
                    else:
                          kind = winsound.SND_ALIAS
                          if not wait: kind = kind | winsound.SND_ASYNC

              if repeat: kind = kind | winsound.SND_LOOP

              winsound.PlaySound(sound, kind)
        else:
              # sound not available at this time
              raise Exception("Sound not supported on this platform: " + platform() )

    def playSound(self, sound, wait=False):
        self.__soundWrap(sound, True, False, wait)

    def stopSound(self):
        self.__soundWrap(None)

    def loopSound(self, sound):
        self.__soundWrap(sound, True, True)

    def soundError(self):
        self.__soundWrap("SystemHand")
    def soundWarning(self):
        self.__soundWrap("SystemAsterisk")

    def playNote(self, note, duration=200):
        if platform() in ["win32", "Windows"]:
              try:
                    if isinstance(note, str): freq=self.NOTES[note.lower()]
                    else: freq=note
              except KeyError:
                    raise Exception("Error: cannot play note - "+ note)
              try:
                    if isinstance(duration, str): length=self.DURATIONS[duration.upper()]
                    else: length=duration
              except KeyError:
                    raise Exception("Error: cannot play duration - " + duration)

              try:
                    winsound.Beep(freq, length)
              except RuntimeError:
                    raise Exception("Sound not available on this platform: " + platform() )
        else:
              # sound not available at this time
              raise Exception("Sound not supported on this platform: " + platform() )

#####################################
## FUNCTION for radio buttons
#####################################
    def addRadioButton(self, title, name, row=None, column=0, colspan=0, rowspan=0):
        var = None
        newRb = False
        if (title in self.n_rbVars):
              var = self.n_rbVars[title]
              vals = self.n_rbVals[title]
              if name in vals: raise Exception("Invalid radio button: "+ name+ " already exists" )
              else: vals.append(name)
        else:
              var = StringVar(self.topLevel)
              vals = [name]
              self.n_rbVars[title]=var
              self.n_rbVals[title]=vals
              newRb = True
        rb = Radiobutton(self.__getContainer())
        rb.config(text=name, variable=var, value=name, background=self.__getContainerBg(), activebackground=self.__getContainerBg(), font=self.rbFont, indicatoron=1)
        rb.config(anchor=W)
        rb.bind("<Button-1>", self.__grabFocus)
        if (title in self.n_rbs): self.n_rbs[title].append(rb)
        else: self.n_rbs[title]=[rb]
        #rb.bind("<Tab>", self.__focusNextWindow)
        #rb.bind("<Shift-Tab>", self.__focusLastWindow)
        if newRb: rb.select()
        self.__positionWidget(rb, row, column, colspan, rowspan, EW)

    def getRadioButton(self, title):
        var = self.__verifyItem(self.n_rbVars, title)
        return var.get()

    def setRadioButton(self, title, value):
        vals = self.__verifyItem(self.n_rbVals, title)
        if value not in vals: raise Exception("Invalid radio button: '"+ value+ "' doesn't exist" )
        var = self.n_rbVars[title]
        var.set(value)

    def setRadioTick(self, title, tick=True):
        radios = self.__verifyItem(self.n_rbs, title)
        for rb in radios:
              if tick: rb.config(indicatoron=1)
              else: rb.config(indicatoron=0)

#####################################
## FUNCTION for list box
#####################################
    def addListBox(self, name, values=None, row=None, column=0, colspan=0, rowspan=0):
        self.__verifyItem(self.n_lbs, name, True)
        frame = ListBox(self.__getContainer())
        vscrollbar = AutoScrollbar(frame)
        hscrollbar = AutoScrollbar(frame, orient=HORIZONTAL)

        lb = Listbox(frame, yscrollcommand = vscrollbar.set, xscrollcommand=hscrollbar.set )

        vscrollbar.grid(row=0, column=1, sticky=N+S)
        hscrollbar.grid(row=1, column=0, sticky=E+W)

        lb.grid(row=0, column=0, sticky=N+S+E+W)

        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        vscrollbar.config( command = lb.yview )
        hscrollbar.config( command = lb.xview )

        lb.config( font=self.lbFont )
        self.n_lbs[name] = lb

        if values is not None:
              for name in values:
                    lb.insert(END, name)

        self.__positionWidget(frame, row, column, colspan, rowspan)

    # set how many rows to display
    def setListBoxRows(self, name, rows):
        lb = self.__verifyItem(self.n_lbs, name)
        lb.config(height=rows)

    # make the list single/multi select
    # default is single
    def setListBoxMulti(self, title, multi=True):
        lb = self.__verifyItem(self.n_lbs, title)
        if multi: lb.config(selectmode=EXTENDED)
        else: lb.config(selectmode=BROWSE)

    # make the list single/multi select
    # default is single
    def setListBoxSingle(self, title, single=True):
        self.setListSingle(title, single)

    def setListSingle(self, title, single=True):
        self.setListBoxMulti(title, not single)

    # select the specified item in the list
    def selectListItem(self, title, item):
        lb = self.__verifyItem(self.n_lbs, title)
        items = lb.get(0, END)
        if len(items) > 0:
              for pos in range(len(items)):
                    if items[pos] == item:
                        self.selectListItemPos(title, pos)
                        break

    def selectListItemPos(self, title, pos):
        lb = self.__verifyItem(self.n_lbs, title)
        sel=lb.curselection()
        lb.selection_clear(0,END)
        # show & select this item
        if pos>=0:
            lb.see(pos)
            lb.activate(pos)
            lb.selection_set(pos)

    # replace the list items in the list box
    def updateListItems(self, title, items):
        self.clearListBox(title)
        self.addListItems(title, items)

    # add the items to the specified list box
    def addListItems(self, title, items):
        for i in items:
              self.addListItem(title, i)

    # add the item to the end of the list box
    def addListItem(self, title, item):
        lb = self.__verifyItem(self.n_lbs, title)
        # add it at the end
        lb.insert(END, item)

        # clear any selection
        items = lb.curselection()
        if len(items) > 0: lb.selection_clear(items)

        # show & select the newly added item
        self.selectListItemPos(title, lb.size()-1)

    # returns a list containing 0 or more elements
    # all that are in the selected range
    def getListItems(self, title):
        lb = self.__verifyItem(self.n_lbs, title)
        items = lb.curselection()
        values = []
        for loop in range(len(items)):
            values.append ( lb.get(items[loop]) )
        return values

    def getListItemsPos(self, title):
        lb = self.__verifyItem(self.n_lbs, title)
        items = lb.curselection()
        return items

    def removeListItemAtPos(self, title, pos):
        lb = self.__verifyItem(self.n_lbs, title)
        items = lb.get(0, END)
        if pos >= len(items):
            raise Exception("Invalid position: " + str(pos))
        lb.delete(pos)

        # show & select this item
        if pos >= lb.size(): pos-=1
        self.selectListItemPos(title, pos)

    # remove a specific item from the listBox
    # will only remove the first item that matches the String
    def removeListItem(self, title, item):
        lb = self.__verifyItem(self.n_lbs, title)
        items = lb.get(0, END)
        lastPos=0
        for pos, val in enumerate(items):
              if val == item:
                    lb.delete(pos)
                    lastPos=pos
        # show & select this item
        # show & select this item
        if pos >= lb.size(): pos-=1
        self.selectListItemPos(title, pos)

    def clearListBox(self, title):
        lb = self.__verifyItem(self.n_lbs, title)
        lb.delete(0, END) # clear

#####################################
## FUNCTION for buttons
#####################################
    def __buildButton(self, title, func, frame, name = None):
        if name is None: name = title
        self.__verifyItem(self.n_buttons, title, True)
        but = Button(frame)

        but.config( text=name, font=self.buttonFont )

        if func is not None:
              command = self.__makeFunc(func, title)
              bindCommand = self.__makeFunc(func, title, True)

              but.config( command=command )
              but.bind('<Return>', bindCommand)

        if platform() == "Darwin":
            but.config(highlightbackground=self.__getContainerBg())
        #but.bind("<Tab>", self.__focusNextWindow)
        #but.bind("<Shift-Tab>", self.__focusLastWindow)
        self.n_buttons[name]=but

        return but

    def addNamedButton(self, name, title, func, row=None, column=0, colspan=0, rowspan=0):
        but = self.__buildButton(title, func, self.__getContainer(), name)
        self.__positionWidget(but, row, column, colspan, rowspan, None)

    def addButton(self, title, func, row=None, column=0, colspan=0, rowspan=0):
        but = self.__buildButton(title, func, self.__getContainer())
        self.__positionWidget(but, row, column, colspan, rowspan, None)

    def setButton(self, name, text):
        but = self.__verifyItem(self.n_buttons, name)
        but.config(text=text)

    def setButtonImage(self, name, imgFile):
        but = self.__verifyItem(self.n_buttons, name)
        image = self.__getImage( imgFile )
        but.config(image=image, compound=TOP, text="", justify=LEFT) # works on Mac & Windows :)
        #but.config(image=image, compound=None, text="") # works on Windows, not Mac

        but.image = image

    # adds a set of buttons, in the row, spannning specified columns
    # pass in a list of names & a list of functions (or a single function to use for all)
    def addButtons(self, names, funcs, row=None, column=0, colspan=0, rowspan=0):

        if not isinstance(names, list):
              raise Exception("Invalid button: " + names + ". It must be a list of buttons.")

        singleFunc = self.__checkFunc(names, funcs)

        frame = WidgetBox(self.__getContainer())
        frame.config( background=self.__getContainerBg() )

        # make them into a 2D array, if not already
        if not isinstance(names[0], list):
              names = [names]
              # won't be used if single func
              if funcs is not None: funcs = [funcs]

        for bRow in range(len(names)):
              for i in range(len(names[bRow])):
                    t = names[bRow][i]
                    if funcs is None: tempFunc = None
                    elif singleFunc is None:tempFunc = funcs[bRow][i]
                    else: tempFunc = singleFunc
                    but = self.__buildButton(t, tempFunc, frame)

                    but.grid ( row=bRow, column=i )
                    Grid.columnconfigure(frame, i, weight=1)
                    Grid.rowconfigure(frame, bRow, weight=1)
                    frame.theWidgets.append(but)

        self.__positionWidget(frame, row, column, colspan, rowspan)
        self.n_frames.append(frame)

#####################################
## FUNCTIONS for links
#####################################
    def __buildLink(self, title):
        link = Link(self.__getContainer())
        link.config(text=title, font=self.linkFont, background=self.__getContainerBg())
        self.n_links[title]=link
        return link

    # launches a browser to the specified page
    def addWebLink(self, title, page, row=None, column=0, colspan=0, rowspan=0):
        link = self.__buildLink(title)
        link.registerWebpage(page)
        self.__positionWidget(link, row, column, colspan, rowspan)

    # executes the specified function
    def addLink(self, title, func, row=None, column=0, colspan=0, rowspan=0):
        link = self.__buildLink(title)
        myF = self.__makeFunc(func, title, True)
        link.registerCallback(myF)
        self.__positionWidget(link, row, column, colspan, rowspan)

#####################################
## FUNCTIONS for grips
#####################################
    # adds a simple grip, used to drag the window around
    def addGrip(self, row=None, column=0, colspan=0, rowspan=0):
        grip = Grip(self.__getContainer())
        self.__positionWidget(grip, row, column, colspan, rowspan)
        self.__addTooltip(grip, "Drag here to move")

#####################################
## FUNCTIONS for labels
#####################################
    def __flash(self):
        if self.doFlash:
              for lab in self.n_flashLabs:
                    bg = lab.cget("background")
                    fg = lab.cget("foreground")
                    lab.config(background=fg, foreground=bg)
        self.topLevel.after(250, self.__flash)

    def addFlashLabel(self, title, text=None, row=None, column=0, colspan=0, rowspan=0):
        self.addLabel(title, text, row, column, colspan, rowspan)
        self.n_flashLabs.append(self.n_labels[title])
        self.doFlash = True

    def addLabel(self, title, text=None, row=None, column=0, colspan=0, rowspan=0):
        self.__verifyItem(self.n_labels, title, True)
        container = self.__getContainer()
        lab = Label(container)

        lab.inContainer=False
        if text is not None: lab.config ( text=text )
        lab.config( justify=LEFT, font=self.labelFont, background=self.__getContainerBg() )
        self.n_labels[title]=lab

        self.__positionWidget(lab, row, column, colspan, rowspan)

    def addEmptyLabel(self, title, row=None, column=0, colspan=0, rowspan=0):
        self.addLabel(title, None, row, column, colspan, rowspan)

    # adds a set of labels, in the row, spannning specified columns
    def addLabels(self, names, row=None, colspan=0, rowspan=0):
        frame = WidgetBox(self.__getContainer())
        frame.config( background=self.__getContainerBg() )
        for i in range(len(names)):
              self.__verifyItem(self.n_labels, names[i], True)
              lab = Label(frame)
              lab.config( text=names[i], font=self.labelFont, justify=LEFT, background=self.__getContainerBg() )
              lab.inContainer=False

              self.n_labels[names[i]]=lab
              lab.grid ( row=0, column=i )
              Grid.columnconfigure(frame, i, weight=1)
              Grid.rowconfigure(frame, 0, weight=1)
              frame.theWidgets.append(lab)

        self.__positionWidget(frame, row, 0, colspan, rowspan)
        self.n_frames.append(frame)

    def setLabel(self, name, text):
        lab = self.__verifyItem(self.n_labels, name)
        lab.config(text=text)

    def getLabel(self, name):
        lab = self.__verifyItem(self.n_labels, name)
        return lab.cget("text")

    def clearLabel(self, name):
        self.setLabel(name, "")

#####################################
## FUNCTIONS to add Text Area
#####################################
    def __buildTextArea(self, title, frame, scrollable=False):
        self.__verifyItem(self.n_textAreas, title, True)
        if scrollable: text = scrolledtext.ScrolledText(frame)
        else: text = Text(frame)
        text.config(font=self.taFont, width=20, height=10)

        if platform() == "Darwin":
            text.config(highlightbackground=self.__getContainerBg())
        text.bind("<Tab>", self.__focusNextWindow)
        text.bind("<Shift-Tab>", self.__focusLastWindow)

        text.bind('<Button-2>',self.__rightClick)
        text.bind('<Button-3>',self.__rightClick)

        self.n_textAreas[title]=text
        self.logTextArea(title)
        return text

    def addTextArea(self, title, row=None, column=0, colspan=0, rowspan=0):
        text = self.__buildTextArea(title, self.__getContainer())
        self.__positionWidget(text, row, column, colspan, rowspan, N+E+S+W)

    def addScrolledTextArea(self, title, row=None, column=0, colspan=0, rowspan=0):
        text = self.__buildTextArea(title, self.__getContainer(), True)
        self.__positionWidget(text, row, column, colspan, rowspan, N+E+S+W)

    def getTextArea(self, title):
        self.__verifyItem(self.n_textAreas, title)
        text = self.n_textAreas[title].get('1.0', END+'-1c')
        return text

    def setTextArea(self, title, text):
        self.__verifyItem(self.n_textAreas, title)
        self.n_textAreas[title].insert('1.0',text)

    # functions to try to monitor text areas
    def clearTextArea(self, title):
        self.__verifyItem(self.n_textAreas, title)
        self.n_textAreas[title].delete('1.0',END)

    def logTextArea(self, title):
        newHash = self.__getTextAreaHash(title)
        self.n_taHashes[title] = newHash

    def textAreaChanged(self, title):
        newHash = self.__getTextAreaHash(title)
        return newHash != self.n_taHashes[title]

    def __getTextAreaHash(self, title):
        self.__verifyItem(self.n_textAreas, title)
        text = self.getTextArea(title)
        md5 = hashlib.md5(str.encode(text)).digest()
        return md5

#####################################
## FUNCTIONS to add Tree Widgets
#####################################
    def addTree(self, title, data, row=None, column=0, colspan=0, rowspan=0):
        self.__verifyItem(self.n_trees, title, True)
        frame=ScrollPane(self.__getContainer(), relief=RAISED,
                        borderwidth=2, bg="white", highlightthickness=0, takefocus=1)
        self.__positionWidget(frame, row, column, colspan, rowspan, "NSEW")

        xmlDoc=parseString(data)
        item=ajTreeData(xmlDoc.documentElement)
        node=ajTreeNode(frame.getPane(), None, item)
        self.n_trees[title]=node
        # update() & expand() called in go() function

    def setTreeEditable(self, title, value=True):
        tree = self.__verifyItem(self.n_trees, title)
        tree.item.setCanEdit(value)

    def setTreeBg(self, title, colour):
        tree = self.__verifyItem(self.n_trees, title)
        tree.setBgColour(colour)

    def setTreeFg(self, title, colour):
        tree = self.__verifyItem(self.n_trees, title)
        tree.setFgColour(colour)

    def setTreeHighlightBg(self, title, colour):
        tree = self.__verifyItem(self.n_trees, title)
        tree.setBgHColour(colour)

    def setTreeHighlightFg(self, title, colour):
        tree = self.__verifyItem(self.n_trees, title)
        tree.setFgHColour(colour)

    def setTreeDoubleClickFunction(self, title, func):
        if func is not None:
              tree = self.__verifyItem(self.n_trees, title)
              command = self.__makeFunc(func, title)
              tree.item.registerDblClick(command)

    def setTreeEditFunction(self, title, func):
        if func is not None:
            tree = self.__verifyItem(self.n_trees, title)
            command = self.__makeFunc(func, title)
            tree.registerEditEvent(command)

    # get whole tree as XML
    def getTreeXML(self, title):
        tree = self.__verifyItem(self.n_trees, title)
        return tree.item.node.toxml()

    # get selected node as a string
    def getTreeSelected(self, title):
        tree = self.__verifyItem(self.n_trees, title)
        return tree.getSelectedText()

    # get selected node (and children) as XML
    def getTreeSelectedXML(self, title):
        tree = self.__verifyItem(self.n_trees, title)
        item = tree.getSelected()
        if item is not None:
            return item.node.toxml()
        else:
            return None

#####################################
## FUNCTIONS to add Message Box
#####################################
    def addMessage(self, title, text, row=None, column=0, colspan=0, rowspan=0):
        if (title in self.n_messages): raise Exception("Invalid name:", title, "already exists")
        mess = Message(self.__getContainer())
        mess.config(font=self.messageFont)
        mess.config( justify=LEFT, background=self.__getContainerBg() )
        if text is not None: mess.config(text=text)
        if platform() == "Darwin":
            mess.config(highlightbackground=self.__getContainerBg())
        self.n_messages[title]=mess

        self.__positionWidget(mess, row, column, colspan, rowspan)
#            mess.bind("<Configure>", lambda e: mess.config(width=e.width-10))

    def addEmptyMessage(self, title, row=None, column=0, colspan=0, rowspan=0):
        self.addMessage(title, None, row, column, colspan, rowspan)

    def setMessage(self, title, text):
        if (title not in self.n_messages): raise Exception("Invalid message:", title)
        self.n_messages[title].config(text=text)

    def clearMessage(self, title ):
        if (title not in self.n_messages): raise Exception("Invalid message:", title)
        self.n_messages[title].config(text="")

#####################################
## FUNCTIONS for entry boxes
#####################################
    def __buildEntry(self, title, frame, secret=False):
        self.__verifyItem(self.n_entries, title, True)
        var=StringVar(self.topLevel)
        ent = Entry(frame)
        ent.var = var
        ent.inContainer = False
        ent.hasDefault = False
        ent.myTitle=title
        ent.isNumeric=False
        ent.config(textvariable=var, font=self.entryFont)
        if secret: ent.config(show="*")
        if platform() == "Darwin":
            ent.config(highlightbackground=self.__getContainerBg())
        ent.bind("<Tab>", self.__focusNextWindow)
        ent.bind("<Shift-Tab>", self.__focusLastWindow)

        ent.bind('<Button-2>',self.__rightClick)
        ent.bind('<Button-3>',self.__rightClick)
        self.n_entries[title]=ent
        self.n_entryVars[title]=var
        return ent

    def addEntry(self, title, row=None, column=0, colspan=0, rowspan=0, secret=False):
        ent = self.__buildEntry(title, self.__getContainer(), secret)
        self.__positionWidget(ent, row, column, colspan, rowspan)

    def __validateNumericEntry(self, action, index, value_if_allowed, prior_value, text, validation_type, trigger_type, widget_name):
        if action == "1":
            if text in '0123456789.-+':
                try:
                    float(value_if_allowed)
                    return True
                except ValueError:
                    self.containerStack[0]['container'].bell()
                    return False
            else:
                    self.containerStack[0]['container'].bell()
                    return False
        else:
            return True

    def addNumericEntry(self, title, row=None, column=0, colspan=0, rowspan=0, secret=False):
        ent = self.__buildEntry(title, self.__getContainer(), secret)
        self.__positionWidget(ent, row, column, colspan, rowspan)

        if self.validateNumeric == None:
              self.validateNumeric = (self.containerStack[0]['container'].register(self.__validateNumericEntry), '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')

        ent.isNumeric=True
        ent.config(validate='key', validatecommand=self.validateNumeric)
        self.setEntryTooltip(title, "Numeric data only.")

    def addLabelNumericEntry(self, title, row=None, column=0, colspan=0, rowspan=0, secret=False):
      self. addNumericLabelEntry(title, row, column, colspan, rowspan, secret)

    def addNumericLabelEntry(self, title, row=None, column=0, colspan=0, rowspan=0, secret=False):
        frame = self.__getLabelBox(title)
        ent = self.__buildEntry(title, frame, secret)
        self.__packLabelBox(frame, ent)
        self.__positionWidget(frame, row, column, colspan, rowspan)

        if self.validateNumeric == None:
              self.validateNumeric = (self.containerStack[0]['container'].register(self.__validateNumericEntry), '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')

        ent.isNumeric=True
        ent.config(validate='key', validatecommand=self.validateNumeric)
        self.setEntryTooltip(title, "Numeric data only.")

    def addSecretEntry(self, title, row=None, column=0, colspan=0, rowspan=0):
        self.addEntry(title, row, column, colspan, rowspan, True)

    def addLabelEntry(self, title, row=None, column=0, colspan=0, rowspan=0, secret=False):
        frame = self.__getLabelBox(title)
        ent = self.__buildEntry(title, frame, secret)
        self.__packLabelBox(frame, ent)
        self.__positionWidget(frame, row, column, colspan, rowspan)

    def addLabelSecretEntry(self, title, row=None, column=0, colspan=0, rowspan=0):
        self.addSecretLabelEntry(title, row, column, colspan, rowspan)

    def addSecretLabelEntry(self, title, row=None, column=0, colspan=0, rowspan=0):
        self.addLabelEntry(title, row, column, colspan, rowspan, True)

    def getEntry(self, name):
        self.__verifyItem(self.n_entryVars, name)
        entry = self.__verifyItem(self.n_entries, name)
        if entry.hasDefault:
              return ""
        else:
              val = self.n_entryVars[name].get()
              if entry.isNumeric:
                    if len(val) == 0: return 0
                    else: return float(val)
              else: return val

    def setEntry(self, name, text):
        self.__verifyItem(self.n_entryVars, name)
        self.n_entryVars[name].set(text)

    def __updateEntryDefault(self, name):
        self.__verifyItem(self.n_entryVars, name)
        entry = self.__verifyItem(self.n_entries, name)
        current = self.n_entryVars[name].get()

        if entry.hasDefault: #True when never clicked
              self.n_entryVars[name].set("")
              entry.hasDefault = False
              entry.config(justify=entry.oldJustify, foreground=entry.oldFg)
        elif current == "": #empty if they didn't type??
              self.n_entryVars[name].set(entry.default)
              entry.config(justify='center', foreground='grey')
              entry.hasDefault = True

    def setEntryDefault(self, name, text="default"):
        entry = self.__verifyItem(self.n_entries, name)
        self.__verifyItem(self.n_entryVars, name)
        self.n_entryVars[name].set(text)
        entry.default = text
        entry.hasDefault = True
        entry.oldJustify=entry.cget('justify')
        entry.oldFg=entry.cget('foreground')
        entry.config(justify='center', foreground='grey')
        command = self.__makeFunc(self.__updateEntryDefault, name, True)
        entry.bind("<FocusIn>", command)
        entry.bind("<FocusOut>", command)

    def clearEntry(self, name):
        self.__verifyItem(self.n_entryVars, name)
        self.n_entryVars[name].set("")
        self.setFocus(name)

    def clearAllEntries(self):
        for entry in self.n_entryVars:
              self.n_entryVars[entry].set("")

    def setFocus(self, name):
        self.__verifyItem(self.n_entries, name)
        self.n_entries[name].focus_set()

    def __lookupValue(self, myDict, val):
        for name in myDict:
            if type(myDict[name]) == type([]):  # array of cbs
                for rb in myDict[name]:
                    if rb == val:
                        return name
            else:
                if myDict[name] == val:
                    return name
        return None

    def __getWidgetName(self, widg):
        name = widg.__class__.__name__
        if name.lower() == "tk": return self.__getTopLevel().title()
        elif name == "Listbox": return self.__lookupValue(self.n_lbs, widg)
        elif name == "Button":
            # merge together Buttons & Toolbar Buttons
            z = self.n_buttons.copy()
            z.update(self.n_tbButts)
            return self.__lookupValue(z, widg)
        elif name == "Entry": return self.__lookupValue(self.n_entries, widg)
        elif name == "Scale": return self.__lookupValue(self.n_scales, widg)
        elif name == "Checkbutton": return self.__lookupValue(self.n_cbs, widg)
        elif name == "Radiobutton": return self.__lookupValue(self.n_rbs, widg)
        elif name == "Spinbox": return self.__lookupValue(self.n_spins, widg)
        elif name == "OptionMenu": return self.__lookupValue(self.n_options, widg)
        elif name == "Text": return self.__lookupValue(self.n_textAreas, widg)
        elif name == "Link": return self.__lookupValue(self.n_links, widg)
        else:
              raise Exception("Unknown widget type: " + name)

    def getFocus(self):
        widg = self.topLevel.focus_get()
        return self.__getWidgetName(widg)

#####################################
## FUNCTIONS for progress bars (meters)
#####################################
    ##############
    # DUAL METERS
    ##############
    def addDualMeter(self, name, row=None, column=0, colspan=0, rowspan=0):
        self.__verifyItem(self.n_meters, name, True)
        meter = DualMeter(self.__getContainer(), font=self.meterFont)
        self.n_meters[name] = meter
        self.__positionWidget(meter, row, column, colspan, rowspan)

    # update the value of the specified meter
    # note: expects a value between -100 & 100
    def setDualMeter(self, name, value=0.0, text=None):
        item = self.__verifyItem(self.n_meters, name)
        value = value/100
        item.set(value, text)

    def getDualMeter(self, name):
        item = self.__verifyItem(self.n_meters, name)
        return item.get()

    def setDualMeterFill(self, name, colours):
        item = self.__verifyItem(self.n_meters, name)
        item.setFill(colours)

    ##############
    # SPLIT METERS
    ##############
    def addSplitMeter(self, name, row=None, column=0, colspan=0, rowspan=0):
        self.__verifyItem(self.n_meters, name, True)
        meter = SplitMeter(self.__getContainer(), font=self.meterFont)
        self.n_meters[name] = meter
        self.__positionWidget(meter, row, column, colspan, rowspan)

    # update the value of the specified meter
    # note: expects a value between -100 & 100
    def setSplitMeter(self, name, value=0.0, text=None):
        item = self.__verifyItem(self.n_meters, name)
        value = value/100
        item.set(value, text)

    def getSplitMeter(self, name):
        item = self.__verifyItem(self.n_meters, name)
        return item.get()

    def setSplitMeterFill(self, name, colours):
        item = self.__verifyItem(self.n_meters, name)
        item.setFill(colours)

    ########
    # METERS
    ########
    def addMeter(self, name, row=None, column=0, colspan=0, rowspan=0):
        self.__verifyItem(self.n_meters, name, True)
        meter = Meter(self.__getContainer(), font=self.meterFont)
        self.n_meters[name] = meter
        self.__positionWidget(meter, row, column, colspan, rowspan)

    # update the value of the specified meter
    # note: expects a value between 0 & 100
    def setMeter(self, name, value=0.0, text=None):
        item = self.__verifyItem(self.n_meters, name)
        value = value/100
        item.set(value, text)

    def getMeter(self, name):
        item = self.__verifyItem(self.n_meters, name)
        return item.get()

    def setMeterFill(self, name, colour):
        item = self.__verifyItem(self.n_meters, name)
        item.setFill(colour)

#####################################
## FUNCTIONS for seperators
#####################################
    def addSeparator(self, row=None, column=0, colspan=0, rowspan=0, colour=None):
        sep = Separator(self.__getContainer())
        if colour is not None: sep.setLineFg(colour)
        self.n_separators.append(sep)
        self.__positionWidget(sep, row, column, colspan, rowspan)

#####################################
## FUNCTIONS for pie charts
#####################################
    def addPieChart(self, name, fracs, size=100, row=None, column=0, colspan=0, rowspan=0):
        self.__verifyItem(self.n_pieCharts, name, True)
        pie = PieChart(self.__getContainer(), fracs, size, self.__getContainerBg() )
        self.n_pieCharts[name] = pie
        self.__positionWidget(pie, row, column, colspan, rowspan, sticky=None)

    def setPieChart(self, title, name, value):
        pie = self.__verifyItem(self.n_pieCharts, title)
        pie.setValue(name, value)

#####################################
## FUNCTIONS for tool bar
#####################################
    # adds a list of buttons along the top - like a tool bar...
    def addToolbar(self, names, funcs):
        if not self.hasTb: self.hasTb = True

        image = None
        singleFunc = self.__checkFunc(names, funcs)
        if not isinstance(names, list): names = [names]

        for i in range(len(names)):
              t = names[i]
              if (t in self.n_tbButts): raise Exception("Invalid toolbar name: "+ t+ " already exists")

              imgFile = os.path.join(self.icon_path,"default",t.lower() + ".png")
              try: image = self.__getImage( imgFile )
              except Exception as e: image = None

              but = Button(self.tb)
              self.n_tbButts[t] = but

              if singleFunc is not None:
                    u = self.__makeFunc(singleFunc, t)
              else:
                    u = self.__makeFunc(funcs[i], t)

              but.config( text=t, command=u, relief=FLAT, font=self.tbFont )
              if image is not None:
                    but.image = image
                    but.config(image=image, compound=TOP, text="", justify=LEFT) # works on Mac & Windows :)
              but.pack (side=LEFT, padx=2, pady=2)
              self.__addTooltip(but, t)

    def setToolbarImage(self, name, imgFile):
        if (name not in self.n_tbButts): raise Exception("Unknown toolbar name: " + name)
        image = self.__getImage( imgFile )
        self.n_tbButts[name].config(image=image)
        self.n_tbButts[name].image = image

    # functions to hide & show the toolbar
    def hideToolbar(self):
        if self.hasTb: self.tb.pack_forget()
    def showToolbar(self):
        if self.hasTb: self.tb.pack(before=self.containerStack[0]['container'], side=TOP, fill=X) 

#####################################
## FUNCTIONS for menu bar
#####################################
    def addMenuList(self, menuName, names, funcs, tearable=False):
        self.__initMenu()
        menu = Menu(self.menuBar, tearoff=tearable)

        # deal with a dict_keys object - messy!!!!
        if not isinstance(names, list): names = list(names)

        # append some Nones, if it's a list and contains separators
        if funcs is not None:
            if not callable(funcs):
                seps = names.count("-")
                for i in range(seps): funcs.append(None)
            singleFunc = self.__checkFunc(names, funcs)

        # add menu items
        for t in names:
              if t == "-":
                    menu.add_separator()
              else:
                    if funcs is None:
                        menu.add_command(label=t)
                    else:
                        if singleFunc is not None:
                                u = self.__makeFunc(singleFunc, t)
                        else:
                                u = self.__makeFunc(funcs.pop(0), t)

                        menu.add_command(label=t, command=u )

        self.menuBar.add_cascade(label=menuName,menu=menu)
        self.n_menus[menuName]=menu

    def __initMenu(self):
        # create a menu bar - only shows if populated
        if not self.hasMenu:
            self.hasMenu = True
            self.menuBar = Menu(self.topLevel)

            appmenu = Menu(self.menuBar, name='apple')
            self.menuBar.add_cascade(menu=appmenu)
            self.n_menus["appmenu"]=appmenu


    # add a single entry for a menu
    def addMenu(self, name, func):
        if platform() == "Darwin":
            self.warn("Unable to make topLevel menus (" + name + ") on Mac")
        else:
            self.__initMenu()
            u = self.__makeFunc(func, name, True)
            self.menuBar.add_command(label=name, command=u)

    # add a parent menu, for menu items
    def createMenu(self, title, tearable=False):
        self.__verifyItem(self.n_menus, title, True)
        self.__initMenu()
        menu = Menu(self.menuBar, tearoff=tearable)
        self.menuBar.add_cascade(label=title,menu=menu)
        self.n_menus[title]=menu

    def disableMenuItem(self, title, item):
        menu = self.__verifyItem(self.n_menus, title)
        menu.entryconfigure(item, state=DISABLED)

    def enableMenuItem(self, title, item):
        menu = self.__verifyItem(self.n_menus, title)
        menu.entryconfigure(item, state=NORMAL)

    # add items to the named menu
    def addMenuItem(self, title, item, func=None, kind=None, shortcut=None):
        menu = self.__verifyItem(self.n_menus, title)
        var = None

        if shortcut is not None:
            if platform() == "Darwin":
                shortcut="Command-"+shortcut.lower()
            elif platform() in [ "win32", "Windows"]:
                shortcut=shortcut.upper()

        if item == "-" or kind=="separator":
              menu.add_separator()
        # creates a var rb+item
        # uses func for the title of this radiobutotn
        elif kind == "rb":
              varName = "rb"+item
              newRb=False
              if (varName in self.n_menuVars):
                    var = self.n_menuVars[varName]
              else:
                    newRb=True
                    var = StringVar(self.topLevel)
                    self.n_menuVars[varName]=var
              menu.add_radiobutton(label=func, variable=var, value=func, accelerator=shortcut)
              if newRb: self.setMenuRadioButton(title, item, func)
        # creates a var cb+item
        elif kind == "cb":
              varName = "cb"+item
              self.__verifyItem(self.n_menuVars, varName, True)
              var = StringVar(self.topLevel)
              self.n_menuVars[varName]=var
              menu.add_checkbutton(label=item, variable=var, onvalue=1, offvalue=0, accelerator=shortcut)
        elif kind == "sub":
            self.__verifyItem(self.n_menus, item, True)
            subMenu = Menu(menu)
            self.n_menus[item]=subMenu
            menu.add_cascade(menu=subMenu, label=item, accelerator=shortcut)
        else:
              if func is not None:
                    u = self.__makeFunc(func, item, True)
                    menu.add_command(label=item, command=u, accelerator=shortcut)
                    shortcut = "<"+shortcut+">"
                    self.topLevel.bind(shortcut, u)
              else:
                    menu.add_command(label=item, accelerator=shortcut)

    def __getMenu(self, menu, title, kind):
        title=kind+title
        var = self.__verifyItem(self.n_menuVars, title)
        if kind=="rb":
              return var.get()
        elif kind=="cb":
              if var.get() == "1": return True
              else: return False

    def getMenuCheckBox(self, menu, title):
        return self.__getMenu(menu, title, "cb")

    def getMenuRadioButton(self, menu, title):
        return self.__getMenu(menu, title, "rb")

    #################
    # wrappers for other menu types

    def addMenuSeparator(self, menu):
        self.addMenuItem(menu, "-")

    def addMenuCheckBox(self, menu, name):
        self.addMenuItem(menu, name, kind="cb")

    def addMenuRadioButton(self, menu, name, value):
        self.addMenuItem(menu, name, value, kind="rb")

    #################
    # wrappers for setters

    def __setMenu(self, menu, title, value, kind):
        title=kind+title
        var = self.__verifyItem(self.n_menuVars, title)
        if kind=="rb":
              var.set(value)
        elif kind=="cb":
              if var.get() == "1": var.set("0")
              else: var.set("1")

    def setMenuCheckBox(self, menu, name):
        self.__setMenu(menu, name, None, "cb")

    def setMenuRadioButton(self, menu, name, value):
        self.__setMenu(menu, name, value, "rb")

    #################
    # wrappers for platform specific menus

    # enables the preferences item in the app menu
    def addMenuPreferences(self, func):
        self.__initMenu()
        u = self.__makeFunc(func, "preferences")
        self.topLevel.createcommand('tk::mac::ShowPreferences', u)

    def addMenuHelp(self, func):
        self.__initMenu()
        helpMenu = Menu(self.menuBar, name='help')
        self.menuBar.add_cascade(menu=helpMenu, label='Help')
        u = self.__makeFunc(func, "help")
        self.topLevel.createcommand('tk::mac::ShowHelp', u)
        self.n_menus["help"]=helpMenu

    # Shows a Window menu
    def addMenuWindow(self):
        self.__initMenu()
        windowMenu = Menu(self.menuBar, name='window')
        self.menuBar.add_cascade(menu=windowMenu, label='Window')
        self.n_menus["window"]=windowMenu

#####################################
## FUNCTIONS for status bar
#####################################
    # TO DO - make multi fielded
    def addStatus(self, header="", fields=1, side=None):
        self.hasStatus = True
        self.header=header
        self.statusFrame = Frame(self.appWindow)
        self.statusFrame.config( bd=1, relief=SUNKEN)
        self.statusFrame.pack(side=BOTTOM, fill=X, anchor=S)

        self.status=[]
        for i in range(fields):
            self.status.append(Label(self.statusFrame))
            self.status[i].config( bd=1, relief=SUNKEN, anchor=W, font=self.statusFont, width=10)
            self.__addTooltip(self.status[i], "Status bar")

            if side=="LEFT": self.status[i].pack(side=LEFT)
            elif side=="RIGHT": self.status[i].pack(side=RIGHT)
            else: self.status[i].pack(side=LEFT, expand=1, fill=BOTH)

    def setStatus(self, text, field=0):
        if self.hasStatus:
            if field is None:
                for status in self.status:
                    status.config(text=self.__getFormatStatus(text))
            elif field >=0 and field < len(self.status):
                self.status[field].config(text=self.__getFormatStatus(text))
            else:
                raise Exception("Invalid status field: " + str(field) + ". Must be between 0 and " + str(len(self.status)-1))

    def setStatusBg(self, colour, field=None):
        if self.hasStatus:
            if field is None:
                for status in self.status:
                    status.config(background=colour)
            elif field >=0 and field < len(self.status):
                self.status[field].config(background=colour)
            else:
                raise Exception("Invalid status field: " + str(field) + ". Must be between 0 and " + str(len(self.status)-1))

    def setStatusFg(self, colour, field=None):
        if self.hasStatus:
            if field is None:
                for status in self.status:
                    status.config(foreground=colour)
            elif field >=0 and field < len(self.status):
                self.status[field].config(foreground=colour)
            else:
                raise Exception("Invalid status field: " + str(field) + ". Must be between 0 and " + str(len(self.status)-1))

    def setStatusWidth(self, width, field=None):
        if self.hasStatus:
            if field is None:
                for status in self.status:
                    status.config(width=width)
            elif field >=0 and field < len(self.status):
                self.status[field].config(width=width)
            else:
                raise Exception("Invalid status field: " + str(field) + ". Must be between 0 and " + str(len(self.status)-1))

    def clearStatus(self, field=None):
        if self.hasStatus:
            if field is None:
                for status in self.status:
                    status.config(text=self.__getFormatStatus(""))
            elif field >=0 and field < len(self.status):
                self.status[field].config(text=self.__getFormatStatus(""))
            else:
                raise Exception("Invalid status field: " + str(field) + ". Must be between 0 and " + str(len(self.status)-1))

    # formats the string shown in the status bar
    def __getFormatStatus(self, text):
        text = str(text)
        if len(text) == 0: return ""
        elif len (self.header) == 0:
              return text
        else:
              return self.header + ": " + text
#####################################
## TOOLTIPS
#####################################
    def __addTooltip(self, item, text):
        tip = ToolTip(item, delay=500, follow_mouse=1, text=text)

#####################################
## FUNCTIONS to show pop-up dialogs
#####################################
    def infoBox(self, title, message):
        self.topLevel.update_idletasks()
        messagebox.showinfo(title, message)
        self.__bringToFront()

    def errorBox(self, title, message):
        self.topLevel.update_idletasks()
        messagebox.showerror(title, message)
        self.__bringToFront()

    def warningBox(self, title, message):
        self.topLevel.update_idletasks()
        messagebox.showwarning(title, message)
        self.__bringToFront()

    def yesNoBox(self, title, message):
        self.topLevel.update_idletasks()
        return messagebox.askyesno(title, message)

    def questionBox(self, title, message):
        self.topLevel.update_idletasks()
        return messagebox.askquestion(title, message)

    def okBox(self, title, message):
        self.topLevel.update_idletasks()
        return messagebox.askokcancel(title, message)

    def retryBox(self, title, message):
        self.topLevel.update_idletasks()
        return messagebox.askretrycancel(title, message)

    def openBox(self, title=None, fileName=None, dirName=None, fileExt=".txt", fileTypes=None, asFile=False):
        self.topLevel.update_idletasks()
        if fileTypes is None: fileTypes = [('all files', '.*'), ('text files', '.txt')]
        # define options for opening
        options = {}
        options['defaultextension'] = fileExt
        options['filetypes'] = fileTypes
        options['initialdir'] = dirName
        options['initialfile'] = fileName
        options['title'] = title

        if asFile: return filedialog.askopenfile(mode="r", **options)
        # will return "" if cancelled
        else:return filedialog.askopenfilename(**options)

    def saveBox(self, title=None, fileName=None, dirName=None, fileExt=".txt", fileTypes=None, asFile=False):
        self.topLevel.update_idletasks()
        if fileTypes is None: fileTypes = [('all files', '.*'), ('text files', '.txt')]
        # define options for opening
        options = {}
        options['defaultextension'] = fileExt
        options['filetypes'] = fileTypes
        options['initialdir'] = dirName
        options['initialfile'] = fileName
        options['title'] = title

        if asFile: return filedialog.asksaveasfile(mode='w', **options)
        # will return "" if cancelled
        else: return filedialog.asksaveasfilename(**options)

    def directoryBox(self, title=None, dirName=None):
        self.topLevel.update_idletasks()
        options = {}
        options['initialdir'] = dirName
        options['title'] = title
        options['mustexist'] = False
        file =  filedialog.askdirectory(**options)
        if file == "": return None
        else: return file

    def colourBox(self, colour='#ff0000'):
        self.topLevel.update_idletasks()
        col = colorchooser.askcolor(colour)
        if col[1] is None: return None
        else: return col[1]

    def textBox(self, title, question):
        self.topLevel.update_idletasks()
        return TextDialog(self.topLevel, title, question).result

    def numberBox(self, title, question): self.numBox(title, question)
    def numBox(self, title, question):
        self.topLevel.update_idletasks()
        return NumDialog(self.topLevel, title, question).result

#####################################
## ProgressBar Class
## from: http://tkinter.unpythonic.net/wiki/ProgressMeter
#####################################
class Meter(Frame):
    def __init__(self, master, width=100, height=20, bg='white', fillColour='orchid1', value=0.0, text=None, font=None, textColour='black', *args, **kw):
        Frame.__init__(self, master, bg=bg, width=width, height=height, *args, **kw)
        self._value = value
        self.config(relief='ridge', bd=3)

#            self._canv = Canvas(self, bg=self['bg'], height=self['height'], highlightthickness=0, relief='flat', bd=0)
        self._canv = Canvas(self, bg=self['bg'], width=self['width'], height=self['height'], highlightthickness=0, relief='flat', bd=0)
        self._canv.pack(fill='both', expand=1)
        self._rect = self._canv.create_rectangle(0, 0, 0, self._canv.winfo_reqheight(), fill=fillColour, width=0)
        self._text = self._canv.create_text(self._canv.winfo_reqwidth()/2, self._canv.winfo_reqheight()/2, text='', fill=textColour)
        if font: self._canv.itemconfigure(self._text, font=font)

        self.set(value, text)
        self.bind('<Configure>', self._update_coords)

    def setFill(self, col):
        self._canv.itemconfigure(self._rect, fill=col)

    def setFg(self, col):
        self._canv.itemconfigure(self._text, fill=col)

    def setBg(self, col):
        self._canv.config(bg=col)

    def setWidth(self, width):
        self._canv.config(width=width)

    def setHeight(self, height):
        self._canv.config(height=height)

    def _update_coords(self, event):
        '''Updates the position of the text and rectangle inside the canvas when the size of the widget gets changed.'''
        self._setCanvas()

    def _setCanvas(self):
        # looks like we have to call update_idletasks() twice to make sure
        # to get the results we expect
        self._canv.update_idletasks()
        self._canv.coords(self._text, self._canv.winfo_width()/2, self._canv.winfo_height()/2)
        self._canv.coords(self._rect, 0, 0, self._canv.winfo_width()*self._value, self._canv.winfo_height())
        self._canv.update_idletasks()

    def get(self): return self._value, self._canv.itemcget(self._text, 'text')

    def set(self, value=0.0, text=None):
        #make the value failsafe:
        if value < 0.0: value = 0.0
        elif value > 1.0: value = 1.0
        self._value = value

        #if no text is specified use the default percentage string:
        if text == None: text = str(int(round(100 * value))) + ' %'

        self._canv.coords(self._rect, 0, 0, self._canv.winfo_width()*value, self._canv.winfo_height())
        self._canv.itemconfigure(self._text, text=text)
        self._canv.update_idletasks()

#####################################
## SplitMeter Class extends the Meter above
## Used to allow bi-directional metering, starting from a mid point
## Two colours should be provided - left & right fill
## A gradient fill will be applied to the Meter
#####################################
class SplitMeter(Meter):
    def __init__(self, master, width=100, height=20, bg='white', leftfillColour='red',
              rightfillColour='blue', value=0.0, text=None, font=None, textColour='white', *args, **kw):

        Frame.__init__(self, master, bg=bg, width=width, height=height, *args, **kw)

        self._value = value
        self.config(relief='ridge', bd=3)

        self._leftFill=leftfillColour
        self._rightFill=rightfillColour
        self._midFill=textColour

        self._canv = Canvas(self, bg=self['bg'], width=self['width'], height=self['height'], highlightthickness=0, relief='flat', bd=0)
        self._canv.pack(fill='both', expand=1)

        self.bind('<Configure>', self._update_coords)

    def _update_coords(self, event):
        '''Updates the position of the text and rectangle inside the canvas when the size of the widget gets changed.'''
        self._setCanvas()

    def setFill(self, cols):
        self._leftFill = cols[0]
        self._rightFill = cols[1]
        self._setCanvas()

    def setFg(self, col):
        self._midFill=col
        self._setCanvas()

    def _setCanvas(self):
        self._canv.update_idletasks()
        self.drawLines()
        self._canv.update_idletasks()

    def drawLines(self):
        '''Draw a gradient'''
        # http://stackoverflow.com/questions/26178869/is-it-possible-to-apply-gradient-colours-to-bg-of-tkinter-python-widgets

        self._canv.delete("gradient")
        self._canv.delete("midline")

        # get range to draw lines
        width=self._canv.winfo_width()
        height = self._canv.winfo_height()
        start=width/2
        fin=start+(start*self._value)

        # determine start & end colour
        if self._value == 0: col = self._midFill
        elif self._value < 0: col = self._leftFill
        else: col = self._rightFill
        (r1,g1,b1) = self.tint(col,-30000)
        (r2,g2,b2) = self.tint(col,30000)

        # determine a direction & range
        if self._value<0:
              direction=-1
              limit=int(start-fin)
        else:
              direction=1
              limit=int(fin-start)

        # if no lines to draw, end it here - with a midline
        if limit==0:
              self._canv.create_line(start, 0, start, height, fill=self._midFill, tags=("midline",))
              return

        # work out the ratios
        r_ratio = float(r2-r1) / limit
        g_ratio = float(g2-g1) / limit
        b_ratio = float(b2-b1) / limit

        # loop through the range of lines, in the right direction
        modder = 0
        for i in range(int(start),int(fin),direction):
              nr = int(r1 + (r_ratio * modder))
              ng = int(g1 + (g_ratio * modder))
              nb = int(b1 + (b_ratio * modder))

              colour = "#%4.4x%4.4x%4.4x" % (nr,ng,nb)
              self._canv.create_line(i,0,i,height, tags=("gradient",), fill=colour)
              modder += 1

        self._canv.lower("gradient")
        self._canv.create_line(start, 0, start, height, fill=self._midFill, tags=("midline",))

    def tint(self, col, brightness_offset=1):
        ''' dim or brighten the specified colour by the specified offset '''
        # http://chase-seibert.github.io/blog/2011/07/29/python-calculate-lighterdarker-rgb-colors.html
        rgb_hex = self._canv.winfo_rgb(col)
        new_rgb_int = [hex_value + brightness_offset for hex_value in rgb_hex]
        new_rgb_int = [min([65535, max([0, i])]) for i in new_rgb_int] # make sure new values are between 0 and 65535
        return new_rgb_int

    def set(self, value=0.0, text=None):
        #make the value failsafe:
        if value < -1: value = -1.0
        elif value > 1.0: value = 1.0
        self._value = value
        self._setCanvas()

class DualMeter(SplitMeter):
    def __init__(self, master, width=100, height=20, bg='white', leftfillColour='pink',
              rightfillColour='green', value=0.5, text=None, font=None, textColour='white', *args, **kw):

        Frame.__init__(self, master, bg=bg, width=width, height=height, *args, **kw)

        self._value = value
        self.config(relief='ridge', bd=3)

        self._leftFill=leftfillColour
        self._rightFill=rightfillColour
        self._midFill=textColour

        self._canv = Canvas(self, bg=self['bg'], width=self['width'], height=self['height'], highlightthickness=0, relief='flat', bd=0)
        width = self._canv.winfo_width()
        mid = width * self._value
        self._r_rect = self._canv.create_rectangle(0, 0, width, self._canv.winfo_reqheight(), fill=self._rightFill, width=0)
        self._l_rect = self._canv.create_rectangle(0, 0, mid, self._canv.winfo_reqheight(), fill=self._leftFill, width=0)
        self._canv.pack(fill='both', expand=1)

        self.bind('<Configure>', self._update_coords)

    def set(self, value=0.0, text=None):
        #make the value failsafe:
        if value < 0.0: value = 0.0
        elif value > 1.0: value = 1.0
        self._value = value
        self._setCanvas()


    def drawLines(self):
        width = self._canv.winfo_width()
        mid = width * self._value
        self._canv.coords(self._l_rect, 0, 0, mid, self._canv.winfo_height())
        self._canv.coords(self._r_rect, 0, 0, width, self._canv.winfo_height())


#################################
## TabbedFrame Class
#################################
class TabbedFrame(Frame):
    def __init__(self, master, bg, fill=False, *args, **kwargs):
        Frame.__init__(self, master, bg=bg)
        self.tabs=Frame(self,bg=bg)
        self.paneBg=bg
        self.panes=Frame(self,relief=SUNKEN,bd=2,bg=self.paneBg,**kwargs)
        self.fill=fill
        self.tabList=[]

        if self.fill:
            self.tabs.grid(row=0, sticky=W+E)
        else:
            self.tabs.grid(row=0, sticky=W)

        Grid.columnconfigure(self, 0, weight=1)
        self.panes.grid(row=1,sticky="NESW")
        Grid.rowconfigure(self, 1, weight=1)

        self.activeFg="blue"
        self.inactiveFg="black"
        self.activeBg="white"
        self.inactiveBg="grey"

        self.tabVars = {}
        self.selectedTab = None
        self.highlightedTab = None

    def expandTabs(self, fill=True):
        self.fill = fill
        self.tabs.grid_forget()
        if self.fill:
            self.tabs.grid(row=0, sticky=W+E)
        else:
            self.tabs.grid(row=0, sticky=W)

        for tab in self.tabList:
            tab.pack_forget()
            if self.fill:
                tab.pack(side=LEFT,ipady=4,ipadx=4, expand=True, fill=BOTH)
            else:
                tab.pack(side=LEFT,ipady=4,ipadx=4)

    def addTab(self, text, **kwargs):
        # log the first tab as the selected tab
        if self.selectedTab is None: self.selectedTab=text
        if self.highlightedTab is None: self.highlightedTab=text

        # create the tab, bind events, pack it in
        tab=Label(self.tabs,text=text,relief=RIDGE,cursor="hand2",takefocus=1,**kwargs)
        self.tabList.append(tab)

        tab.bind("<Button-1>", lambda *args:self.changeTab(text))
        tab.bind("<Return>", lambda *args:self.changeTab(text))
        tab.bind("<space>", lambda *args:self.changeTab(text))
        tab.bind("<FocusIn>", lambda *args:self.__focusIn(text))
        tab.bind("<FocusOut>", lambda *args:self.__focusOut(text))
        if self.fill:
            tab.pack(side=LEFT,ipady=4,ipadx=4, expand=True, fill=BOTH)
        else:
            tab.pack(side=LEFT,ipady=4,ipadx=4)

        # create the pane
        pane=Frame(self.panes,bg=self.paneBg)
        pane.grid(sticky="nsew", row=0, column=0)
        self.panes.grid_columnconfigure(0, weight=1)
        self.panes.grid_rowconfigure(0, weight=1)

        self.tabVars[text]=[tab, pane]
        self.__colourTabs(self.selectedTab)

        return pane

    def __focusIn(self, tabName):
        self.highlightedTab = tabName
        self.__colourTabs(False)

    def __focusOut(self, tabName):
        self.tabVars[tabName][0]['fg']='black'

    def changeTab(self, tabName):
        if tabName not in self.tabVars.keys():
            raise Exception("Invalid tab name: " + tabName)
        self.tabVars[tabName][0].focus_set()
        self.highlightedTab = tabName
        if tabName != self.selectedTab:
              self.selectedTab=tabName
              self.__colourTabs()

    def __colourTabs(self, swap=True):
        # clear all tabs & remove if necessary
        for key in list(self.tabVars.keys()):
              self.tabVars[key][0]['bg']=self.inactiveBg
              self.tabVars[key][0]['fg']=self.inactiveFg
              if swap: self.tabVars[key][1].grid_remove()

        # now decorate the active tab
        self.tabVars[self.selectedTab][0]['bg']=self.activeBg
        self.tabVars[self.highlightedTab][0]['fg']=self.activeFg
        # and grid it if necessary
        if swap: self.tabVars[self.selectedTab][1].grid()

    def setBg(self, bg):
        self.paneBg=bg
        for key in list(self.tabVars.keys()):
            self.tabVars[key][1]['bg']=bg

    def setTabBg(self, tab, bg):
        self.tabVars[tab][1].config(bg=bg)

    def setFg(self, activeFg, inactiveFg):
        self.activeFg = activeFg
        self.inactiveFg = inactiveFg
        self.__colourTabs(False)

    def setBg(self, activeBg, inactiveBg):
        self.activeBg = activeBg
        self.inactiveBg = inactiveBg
        self.__colourTabs(False)

#####################################
## Drag Grip Label Class
#####################################
class Grip(Label):
    def __init__(self, *args, **kwargs):
        Label.__init__(self, bitmap="gray25", *args, **kwargs)
        self.config(cursor="fleur")
        self.bind("<ButtonPress-1>", self.StartMove)
        self.bind("<ButtonRelease-1>", self.StopMove)
        self.bind("<B1-Motion>", self.OnMotion)

    def StartMove(self, event):
        self.x = event.x
        self.y = event.y

    def StopMove(self, event):
        self.x = None
        self.y = None

    def OnMotion(self, event):
        parent = self.winfo_toplevel()
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = parent.winfo_x() + deltax
        y = parent.winfo_y() + deltay

        parent.geometry("+%s+%s" % (x, y))

#####################################
## Hyperlink Class
#####################################
class Link(Label):
    def __init__(self, *args, **kwargs):
        Label.__init__(self, *args, **kwargs)
        self.config(fg="blue", takefocus=1, highlightthickness=1)
        self.page=""

        if platform() == "Darwin":
              self.config(cursor="pointinghand")
        elif platform() in [ "win32", "Windows"]:
              self.config(cursor="hand2")

    def registerCallback(self, callback):
        self.bind("<Button-1>", callback)
        self.bind("<Return>", callback)
        self.bind("<space>", callback)

    def launchBrowser(self, event):
        webbrowser.open_new(r""+self.page)
        #webbrowser.open_new_tab(self.page)

    def registerWebpage(self, page):
        if not page.startswith("http"):
              raise InvalidURLError("Invalid URL: " + page + " (it should begin as http://)")

        self.page = page
        self.bind("<Button-1>", self.launchBrowser)
        self.bind("<Return>", self.launchBrowser)
        self.bind("<space>", self.launchBrowser)

#####################################
## Simple Separator
#####################################
class Separator(Frame):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
        self.line = Frame(self)
        self.line.config(relief="ridge", height=2, width=100, borderwidth=1)
        self.line.pack(padx=5, pady=5, fill="x")

    def setLineFg(self, colour):
        self.line.config(bg=colour)

#####################################
## Pie Chart Class
#####################################
class PieChart(Canvas):
    # constant for available colours
    COLOURS=[ "#023fa5", "#7d87b9", "#bec1d4", "#d6bcc0", "#bb7784", "#8e063b",
              "#4a6fe3", "#8595e1", "#b5bbe3", "#e6afb9", "#e07b91", "#d33f6a",
              "#11c638", "#8dd593", "#c6dec7", "#ead3c6", "#f0b98d", "#ef9708",
              "#0fcfc0", "#9cded6", "#d5eae7", "#f3e1eb", "#f6c4e1", "#f79cd4"]

    def __init__(self, container, fracs, size, bg):
        Canvas.__init__(self,container, width=size, height=size, bd=0, highlightthickness=0, bg=bg)
        self.fracs=fracs
        self.size=size
        self._drawPie()

    def _drawPie(self):
        pos = 0
        col = 0
        for key, val in self.fracs.items():
            sliceId="slice"+str(col)
            coord=self.size*.05,self.size*.05,self.size*.95,self.size*.95
            arc=self.create_arc(coord,
                              fill=self.COLOURS[col%len(self.COLOURS)],
                              start=self.frac(pos), extent=self.frac(val), activedash=(3,5),
                              activeoutline="grey", activewidth=3, tag=(sliceId,), width=1)

            # generate a tooltip
            frac = int(val/sum(self.fracs.values())*100)
            tip = key + ": " + str(val) + " (" + str(frac) + "%)"
            tt=ToolTip(self,tip,delay=500, follow_mouse=1, specId=sliceId) 

            pos += val
            col+=1

    def frac(self, curr):
        return 360. * curr / sum(self.fracs.values())

    def setValue(self, name, value):
        if value == 0 and name in self.fracs:
            del self.fracs[name]
        else:
            self.fracs[name]=value

        self._drawPie()

#####################################
## Tree Widget Class
## https://www.safaribooksonline.com/library/view/python-cookbook-2nd/0596007973/ch11s11.html
## idlelib -> TreeWidget.py
## modify minidom - https://wiki.python.org/moin/MiniDom
#####################################
class ajTreeNode(TreeNode):
    def __init__(self, canvas, parent, item):

        TreeNode.__init__(self, canvas, parent, item)

        self.bgColour = None
        self.fgColour = None
        self.bgHColour = None
        self.fgHColour = None
        self.editEvent = None

        if self.parent:
            self.bgColour = self.parent.bgColour
            self.fgColour = self.parent.fgColour
            self.bgHColour = self.parent.bgHColour
            self.fgHColour = self.parent.fgHColour
            self.editEvent = self.parent.editEvent

    def registerEditEvent(self, func):
        self.editEvent = func
        for c in self.children:
            c.registerEditEvent(func)

    def setBgColour(self, colour):
        self.canvas.config(background=colour)
        self.bgColour = colour
        self.__doUpdateColour()

    def setFgColour(self, colour):
        self.fgColour = colour
        self.__doUpdateColour()

    def setBgHColour(self, colour):
        self.bgHColour = colour
        self.__doUpdateColour()

    def setFgHColour(self, colour):
        self.fgHColour = colour
        self.__doUpdateColour()

    def __doUpdateColour(self):
        self.__updateColours(self.bgColour, self.bgHColour, self.fgColour, self.fgHColour)
        self.update()

    def __updateColours(self, bgCol, bgHCol, fgCol, fgHCol):
        self.bgColour = bgCol
        self.fgColour = fgCol
        self.bgHColour = bgHCol
        self.fgHColour = fgHCol
        for c in self.children:
            c.__updateColours(bgCol, bgHCol, fgCol, fgHCol)

    # override parent function, so that we can change the label's background colour
    def drawtext(self):
        super().drawtext()
        self.colourLabels()

    # override parent function, so that we can generate an event on finish editing
    def edit_finish(self, event=None):
        super().edit_finish(event)
        self.editEvent()

    def colourLabels(self):
        try:
            if not self.selected:
                self.label.config(background=self.bgColour, fg=self.fgColour)
            else:
                self.label.config(background=self.bgHColour, fg=self.fgHColour)
        except:
            pass

    def getSelectedText(self):
        item = self.getSelected()
        if item is not None:
            return item.GetText()
        else:
            return None

    def getSelected(self):
        if self.selected:
            return self.item
        else:
            for c in self.children:
                val = c.getSelected()
                if val is not None: return val
            return None

# implementation of container for XML data
# functions implemented as specified in skeleton
class ajTreeData(TreeItem):
    def __init__(self, node):
        self.node = node
        self.dblClickFunc = None
        self.canEdit = True

## REQUIRED FUNCTIONS

    # called whenever the tree expands
    def GetText(self):
        node = self.node
        if node.nodeType == node.ELEMENT_NODE:
              return node.nodeName
        elif node.nodeType == node.TEXT_NODE:
              return node.nodeValue

    def IsEditable(self):
        return self.canEdit and not self.node.hasChildNodes()

    def SetText(self, text):
        self.node.replaceWholeText(text)

    def IsExpandable(self):
        return self.node.hasChildNodes()

    def GetIconName(self):
        if not self.IsExpandable():
            return "python" # change to file icon

    def GetSubList(self):
        children = self.node.childNodes
        prelist = [ajTreeData(node) for node in children]
        itemList = [item for item in prelist if item.GetText().strip()]
        for item in itemList:
            item.registerDblClick(self.dblClickFunc)
            item.canEdit=self.canEdit
        return itemList

    def OnDoubleClick(self):
        if self.IsEditable():
            # TO DO: start editing this node...
            pass
        if self.dblClickFunc is not None:
            self.dblClickFunc()

## EXTRA FUNCTIONS

    # TODO: can only set before calling go()
    def setCanEdit(self, value=True):
        self.canEdit = value

    # TODO: can only set before calling go()
    def registerDblClick(self, func):
        self.dblClickFunc = func

    # not used - for DEBUG
    def getSelected(self, spaces=1):
        if spaces==1: print(self.node.tagName)
        for c in self.node.childNodes:
            if c.__class__.__name__ == "Element":
                print(" "*spaces, ">>",c.tagName)
                node = ajTreeData(c)
                node.getSelected(spaces+2)
            elif c.__class__.__name__ == "Text":
                val=c.data.strip()
                if len(val)>0: print(" "*spaces, ">>>>",val)

#####################################
## errors
#####################################
class ItemLookupError(LookupError):
    '''raise this when there's a lookup error for my app'''
    pass

class InvalidURLError(ValueError):
    '''raise this when there's a lookup error for my app'''
    pass



#####################################
## ToggleFrame - collapsable frame
## http://stackoverflow.com/questions/13141259/expandable-and-contracting-frame-in-tkinter
#####################################
class ToggleFrame(Frame):
    def __init__(self, parent, title="", *args, **options):
        Frame.__init__(self, parent, *args, **options)

        self.config(relief="raised", borderwidth=2, padx=5, pady=5)
        self.showing=True

        self.titleFrame = Frame(self)
        self.titleFrame.config(bg="DarkGray")

        self.titleLabel = Label(self.titleFrame, text=title)
        self.titleLabel.config(font="-weight bold")

        self.toggleButton = Button(self.titleFrame, width=2, text='-', command=self.toggle)

        self.subFrame = Frame(self, relief="sunken", borderwidth=2)

        self.setBg("DarkGray")

        self.grid_columnconfigure(0, weight=1)
        self.titleFrame.grid(row=0, column=0, sticky=EW)
        self.titleFrame.grid_columnconfigure(0, weight=1)
        self.titleLabel.grid(row=0, column=0)
        self.toggleButton.grid(row=0, column=1)
        self.subFrame.grid(row=1, column=0, sticky=EW)

    def setFont(self, font):
        self.titleLabel.config(font=font)
        self.toggleButton.config(font=font)

    def toggle(self):
        if not self.showing:
            self.subFrame.grid()
            self.toggleButton.configure(text='-')
        else:
            self.subFrame.grid_remove()
            self.toggleButton.configure(text='+')
        self.showing = not self.showing

    def getContainer(self):
        return self.subFrame

    def setBg(self, colour):
        self.config(bg=colour)
        self.titleFrame.config(bg=colour)
        self.titleLabel.config(bg=colour)
        self.subFrame.config(bg=colour)
        if platform() == "Darwin": self.toggleButton.config(highlightbackground=colour)

    def stop(self):
        self.update_idletasks()
        self.titleFrame.config(width=self.winfo_reqwidth())
        self.toggle()

    def isShowing(self):
        return self.showing

    def disable(self, disable=True):
        if disable:
            if self.showing:
                self.toggle()
            self.toggleButton.config(state="disabled")
        else:
            self.toggleButton.config(state="normal")

#####################################
## Paged Window
#####################################
class PagedWindow(Frame):
    def __init__(self, parent, title=None, **opts):
        # call the super constructor
        Frame.__init__(self, parent, **opts)
        self.config(width=300, height=400)

        # globals to hold list of frames(pages) and current page
        self.currentPage = -1
        self.frames=[]
        self.shouldShowLabel = True
        self.shouldShowTitle = True
        self.title=title
        self.navPos = 1
        self.maxX=0
        self.maxY=0
        self.pageChangeEvent = None

        # create the 3 components, including a default container frame
        self.titleLabel = Label(self)
        self.prevButton = Button(self, text="PREVIOUS", command=self.showPrev, state="disabled", width=10)
        self.nextButton = Button(self, text="NEXT", command=self.showNext, state="disabled", width=10)
        self.prevButton.bind("<Control-Button-1>", self.showFirst)
        self.nextButton.bind("<Control-Button-1>", self.showLast)
        self.posLabel = Label(self, width=8)

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        # grid the navigation components
        self.prevButton.grid(row=self.navPos+1, column=0, sticky=N+S+W, padx=5, pady=(0,5))
        self.posLabel.grid(row=self.navPos+1, column=1, sticky=N+S+E+W, padx=5, pady=(0,5))
        self.nextButton.grid(row=self.navPos+1, column=2, sticky=N+S+E, padx=5, pady=(0,5))

        # show the title
        if self.title is not None and self.shouldShowTitle:
            self.titleLabel.config(text=self.title, font="-weight bold")
            self.titleLabel.grid(row=0, column=0, columnspan=3, sticky=N+W+E)

        # show the label
        self.__setLabel()

    def setBg(self, colour):
        self.config(bg=colour)
        if platform() == "Darwin":
            self.prevButton.config(highlightbackground=colour)
            self.nextButton.config(highlightbackground=colour)
        self.posLabel.config(bg=colour)
        self.titleLabel.config(bg=colour)

    def setFg(self, colour):
        self.poslabel.config(fg=colour)
        self.titleLabel.config(fg=colour)

    # functions to change the labels of the two buttons
    def setPrevButton(self, title): self.prevButton.config(text=title)
    def setNextButton(self, title): self.nextButton.config(text=title)

    def setNavPositionTop(self, top=True):
        oldNavPos = self.navPos
        pady=(0,5)
        if top: self.navPos = 0
        else: self.navPos = 1
        if oldNavPos != self.navPos:
            if self.navPos == 0:
                self.grid_rowconfigure(1, weight=0)
                self.grid_rowconfigure(2, weight=1)
                pady=(5,0)
            else:
                self.grid_rowconfigure(1, weight=1)
                self.grid_rowconfigure(2, weight=0)
            # grid the navigation components
            self.frames[self.currentPage].grid_remove()
            self.prevButton.grid_remove()
            self.posLabel.grid_remove()
            self.nextButton.grid_remove()

            self.frames[self.currentPage].grid(row=int(not self.navPos)+1, column=0, columnspan=3, sticky=N+S+E+W, padx=5, pady=5)
            self.prevButton.grid(row=self.navPos+1, column=0, sticky=S+W, padx=5, pady=pady)
            self.posLabel.grid(row=self.navPos+1, column=1, sticky=S+E+W, padx=5, pady=pady)
            self.nextButton.grid(row=self.navPos+1, column=2, sticky=S+E, padx=5, pady=pady)

    def showLabel(self, val=True):
        self.shouldShowLabel = val
        self.__setLabel()

    def setTitle(self, title):
        self.title = title
        self.showTitle()

    def showTitle(self, val=True):
        self.shouldShowTitle = val
        if self.title is not None and self.shouldShowTitle:
            self.titleLabel.config(text=self.title, font="-weight bold")
            self.titleLabel.grid(row=0, column=0, columnspan=3, sticky=N+W+E)
        else:
            self.titleLabel.grid_remove()

    # function to update the contents of the label
    def __setLabel(self):
        if self.shouldShowLabel:
            self.posLabel.config(text=str(self.currentPage+1) + "/" + str(len(self.frames)))
        else:
            self.posLabel.config(text="")

    # get the current frame being shown - for adding widgets
    def getPage(self): return self.frames[self.currentPage]

    # get current page number
    def getPageNumber(self): return self.currentPage+1

    # register a funciton to call when the page changes
    def registerPageChangeEvent(self, event):
        self.pageChangeEvent = event

    # adds a new page, making it visible
    def addPage(self):
        # if we're showing a page, remove it
        if self.currentPage >= 0:
            self.__updateMaxSize()
            self.frames[self.currentPage].grid_forget()

        # add a new page
        self.frames.append(Page(self))
        self.frames[-1].grid(row=int(not self.navPos)+1, column=0, columnspan=3, sticky=N+S+E+W, padx=5, pady=5)

        self.currentPage = len(self.frames)-1

        # update the buttons & labels
        if self.currentPage > 0: self.prevButton.config(state="normal")
        self.__setLabel()
        return self.frames[-1]

    def stopPage(self):
        self.__updateMaxSize()
        self.showPage(1)

    def __updateMaxSize(self):
        self.frames[self.currentPage].update_idletasks()
        x = self.frames[self.currentPage].winfo_reqwidth()
        y = self.frames[self.currentPage].winfo_reqheight()
        if x > self.maxX: self.maxX = x
        if y > self.maxY: self.maxY = y

    # function to display the specified page
    # will re-grid, and disable/enable buttons
    # also updates label
    def showPage(self, page):
        if page < 1 or page > len(self.frames):
            raise Exception("Invalid page number: " + str(page) + ". Must be between 1 and " + str(len(self.frames)))

        self.frames[self.currentPage].grid_forget()
        self.currentPage = page - 1
        self.frames[self.currentPage].grid_propagate(False)
        self.frames[self.currentPage].grid(row=int(not self.navPos)+1, column=0, columnspan=3, sticky=N+S+E+W, padx=5, pady=5)
        self.frames[self.currentPage].grid_columnconfigure(0, weight=1)
        self.frames[self.currentPage].config(width=self.maxX, height=self.maxY)
        self.__setLabel()

        # update the buttons
        if self.currentPage == 0:
            self.prevButton.config(state="disabled")
            self.nextButton.config(state="normal")
        elif self.currentPage == len(self.frames)-1:
            self.prevButton.config(state="normal")
            self.nextButton.config(state="disabled")
        else:
            self.prevButton.config(state="normal")
            self.nextButton.config(state="normal")

    def showFirst(self, event=None):
        if self.currentPage == 0:
            self.bell()
        else:
            self.showPage(1)
            if self.pageChangeEvent is not None: self.pageChangeEvent()

    def showLast(self, event=None):
        if self.currentPage == len(self.frames)-1:
            self.bell()
        else:
            self.showPage(len(self.frames))
            if self.pageChangeEvent is not None: self.pageChangeEvent()

    def showPrev(self, event=None):
        if self.currentPage > 0:
            self.showPage(self.currentPage)
            if self.pageChangeEvent is not None: self.pageChangeEvent()
        else:
            self.bell()

    def showNext(self, event=None):
        if self.currentPage < len(self.frames)-1:
            self.showPage(self.currentPage + 2)
            if self.pageChangeEvent is not None: self.pageChangeEvent()
        else:
            self.bell()

class Page(Frame):
    def __init__(self, parent, **opts):
        Frame.__init__(self, parent)
        self.config(relief=RIDGE, borderwidth=2)

#####################################
## Named classes for containing groups
#####################################
class LabelBox(Frame):
    def __init__(self, parent, **opts):
        Frame.__init__(self, parent)
        self.theLabel=None
        self.theWidget=None

class WidgetBox(Frame):
    def __init__(self, parent, **opts):
        Frame.__init__(self, parent)
        self.theWidgets=[]

class ListBox(Frame):
    def __init__(self, parent, **opts):
        Frame.__init__(self, parent)

#####################################
## scrollable frame...
# http://effbot.org/zone/tkinter-autoscrollbar.htm
#####################################
class AutoScrollbar(Scrollbar):
    def __init__(self, parent, **opts):
        Scrollbar.__init__(self, parent, **opts)

    # a scrollbar that hides itself if it's not needed
    # only works if you use the grid geometry manager
    def set(self, lo, hi):
        if float(lo) <= 0.0 and float(hi) >= 1.0:
            # grid_remove is currently missing from Tkinter!
            self.tk.call("grid", "remove", self)
        else:
            self.grid()
        Scrollbar.set(self, lo, hi)
    def pack(self, **kw):
        raise Exception("cannot use pack with this widget")
    def place(self, **kw):
        raise Exception("cannot use place with this widget")

#######################
## Frame with uilt in scrollbars and canvas for placing stuff on
## http://effbot.org/zone/tkinter-autoscrollbar.htm
## Modified with help from idlelib TreeWidget.py
#######################
class ScrollPane(Frame):
    def __init__(self, parent, **opts):
      Frame.__init__(self, parent)

      # make the ScrollPane expandable
      self.grid_rowconfigure(0, weight=1)
      self.grid_columnconfigure(0, weight=1)

      if 'yscrollincrement' not in opts: opts['yscrollincrement'] = 17
      opts['height']=100

      vscrollbar = Scrollbar(self)
      hscrollbar = Scrollbar(self, orient=HORIZONTAL)
      opts['yscrollcommand']=vscrollbar.set
      opts['xscrollcommand']=hscrollbar.set

      self.canvas = Canvas(self,**opts)

      vscrollbar.grid(row=0, column=1, sticky=N+S+E)
      hscrollbar.grid(row=1, column=0, sticky=E+W+S)
      self.canvas.grid(row=0, column=0, sticky=N+S+E+W)

      vscrollbar.config(command=self.canvas.yview)
      hscrollbar.config(command=self.canvas.xview)

      self.canvas.bind("<Key-Prior>", self.page_up)
      self.canvas.bind("<Key-Next>", self.page_down)
      self.canvas.bind("<Key-Up>", self.unit_up)
      self.canvas.bind("<Key-Down>", self.unit_down)
      self.canvas.bind("<Alt-Key-2>", self.zoom_height)
      self.canvas.focus_set()

      self.canvas.bind("<Enter>", self.__mouseEnter)
      self.canvas.bind("<Leave>", self.__mouseLeave)
      self.b_ids = []

      self.interior = interior = Frame(self.canvas)
      self.interior_id = self.canvas.create_window(0,0,window=interior, anchor=NW)

      # removed - was cropping label's width
      #self.canvas.bind('<Configure>', self.__configureCanvas)
      self.interior.bind('<Configure>', self.__configureInterior)

    # track changes to the canvas and frame width and sync them,
    # also updating the scrollbar
    # http://www.scriptscoop2.com/t/35d742299f35/python-tkinter-scrollbar-for-frame.html
    def __configureInterior(self, event):
      # update the scrollbars to match the size of the inner frame
      size = (self.interior.winfo_reqwidth(), self.interior.winfo_reqheight())
      self.canvas.config(scrollregion="0 0 %s %s" % size)
      if self.interior.winfo_reqwidth() != self.canvas.winfo_width():
        # update the canvas's width to fit the inner frame
        self.canvas.config(width=self.interior.winfo_reqwidth())

    def __configureCanvas(self, event):
      if self.interior.winfo_reqwidth() != self.canvas.winfo_width():
        # update the inner frame's width to fill the canvas
        self.canvas.itemconfigure(self.interior_id, width=self.canvas.winfo_width())
        pass

    # unbind any saved bind ids
    def __unbindIds(self):
      if len(self.b_ids) == 0: return

      if platform() == "Linux":
        self.canvas.unbind("<4>", self.b_ids[0])
        self.canvas.unbind("<5>", self.b_ids[1])
      else: # Windows and MacOS
        self.canvas.unbind("<MouseWheel>", self.b_ids[0])

      self.b_ids=[]

    # bind mouse scroll to this widget only when mouse is over
    def __mouseEnter(self, event):
      self.__unbindIds()
      if platform() == "Linux":
        self.b_ids.append(self.canvas.bind_all("<4>", self.__mouseScroll))
        self.b_ids.append(self.canvas.bind_all("<5>", self.__mouseScroll))
      else: # Windows and MacOS
        self.b_ids.append(self.canvas.bind_all("<MouseWheel>", self.__mouseScroll))

    # remove mouse scroll binding, when mouse leaves
    def __mouseLeave(self, event):
      self.__unbindIds()

    # https://www.daniweb.com/programming/software-development/code/217059/using-the-mouse-wheel-with-tkinter-python
    def __mouseScroll(self, event):
      timer=round(time.time(),1)

      # get the mouse scroll direciton value
      newDelta = event.delta

      # if windows - make it the same as other platforms
      if platform() in [ "win32", "Windows"]:
        newDelta = (newDelta/120) * -1

      # scrolled before
      if hasattr(self, 'lastScrollTime'):

        # too soon to scroll
        if self.lastScrollTime == timer:
            if newDelta in [1,-1,2,-2]: self.times.append(newDelta)
            self.speed += 1

        # time to scroll
        else:
            # get the delta
            try: delta=max(set(self.times), key=self.times.count)
            except: delta=self.oldDelta

            # windows/mac osx scroll event
            if platform() in [ "win32", "Windows", "Darwin"]:
                if platform() in [ "win32", "Windows"]:
                    val = delta * -1
                    if delta < 0: val = val * -1
                    if delta < 0: self.speed = self.speed * -1
                else:
                    val = (self.times.count(delta))
                    if delta > 0: val = val * -1
                    if delta > 0: self.speed = self.speed * -1

                if delta in [1,-1]: self.canvas.yview_scroll(self.speed, "units")
                elif delta in [2,-2]: self.canvas.xview_scroll(self.speed, "units")
                else: pass

            # linux scroll event
            elif platform() == "Linux":
                if event.num == 4:
                    self.canvas.yview_scroll(-1*2, "units")
                elif event.num == 5:
                    self.canvas.yview_scroll(2, "units")
            # unknown platform scroll event
            else:
                pass

            # finally, set some stuff
            self.times=[]
            self.oldDelta=delta
            if newDelta in [1,-1,2,-2]: self.times.append(newDelta)
            self.lastScrollTime = timer
            self.speed=1

      # no lastScrollTime set
      else:
        self.times=[]
        if newDelta in [1,-1,2,-2]: self.times.append(newDelta)
        self.lastScrollTime = timer
        self.speed=1

    def getPane(self):
      return self.canvas

    def page_up(self, event):
      self.canvas.yview_scroll(-1, "page")
      return "break"
    def page_down(self, event):
      self.canvas.yview_scroll(1, "page")
      return "break"
    def unit_up(self, event):
      self.canvas.yview_scroll(-1, "unit")
      return "break"
    def unit_down(self, event):
      self.canvas.yview_scroll(1, "unit")
      return "break"
    def zoom_height(self, event):
      ZoomHeight.zoom_height(self.master)
      return "break"

#################################
## Additional Dialog Classes
#################################
# the main dialog class to be extended
class Dialog(Toplevel):
    def __init__(self, parent, title = None):
      Toplevel.__init__(self, parent)
      self.transient(parent)

      if title: self.title(title)
      self.parent = parent
      self.result = None

      # create a frame to hold the contents
      body = Frame(self)
      self.initial_focus = self.body(body)
      body.pack(padx=5, pady=5)

      # create the buttons
      self.buttonbox()

      self.grab_set()
      if not self.initial_focus: self.initial_focus = self

      self.protocol("WM_DELETE_WINDOW", self.cancel)
      self.geometry("+%d+%d" % (parent.winfo_rootx()+50,
                              parent.winfo_rooty()+50))

      self.initial_focus.focus_set()
      self.wait_window(self)

    # override to create the contents of the dialog
    # should return the widget to give focus to
    def body(self, master):
      pass

    # add standard buttons
    # override if you don't want the standard buttons
    def buttonbox(self):
      box = Frame(self)

      w = Button(box, text="OK", width=10, command=self.ok, default=ACTIVE)
      w.pack(side=LEFT, padx=5, pady=5)
      w = Button(box, text="Cancel", width=10, command=self.cancel)
      w.pack(side=LEFT, padx=5, pady=5)

      self.bind("<Return>", self.ok)
      self.bind("<Escape>", self.cancel)

      box.pack()

    # called when ok button pressed
    def ok(self, event=None):
      # only continue of validate() returns True
      if not self.validate():
        self.initial_focus.focus_set() # put focus back
        return

      self.withdraw()
      self.update_idletasks()

      # call the validate function before calling the cancel function
      self.apply()
      self.cancel()

    # called when cancel button pressed
    def cancel(self, event=None):
      self.parent.focus_set() # give focus back to the parent
      self.destroy()

    # override this to cancel closing the form
    def validate(self):
      return True

    # override this to do something before closing
    def apply(self):
      pass

# a base class for a simple data capture dialog
class SimpleEntryDialog(Dialog):
    def __init__(self, parent, title, question):
      self.error = False
      self.question = question
      super(SimpleEntryDialog, self).__init__(parent, title)

    def clearError(self, e):
      if self.error:
        self.error = False
        self.l1.config(text="")

    def setError(self, message):
      self.error = True
      self.l1.config(text=message)

    # a label for the question, an entry for the answer
    # a label for an error message
    def body(self, master):
      Label(master, text=self.question).grid(row=0)
      self.e1 = Entry(master)
      self.l1 = Label(master, fg="red")
      self.e1.grid(row=1)
      self.l1.grid(row=2)
      self.e1.bind("<Key>", self.clearError)
      return self.e1

# captures a string - must not be empty
class TextDialog(SimpleEntryDialog):
    def __init__(self, parent, title, question):
      super(TextDialog, self).__init__(parent, title, question)

    def validate(self):
      res = self.e1.get()
      if len(res.strip()) == 0:
        self.setError("Invalid text.")
        return False
      else:
        self.result = res
        return True

# captures a number - must be a valid float
class NumDialog(SimpleEntryDialog):
    def __init__(self, parent, title, question):
      super(NumDialog, self).__init__(parent, title, question)

    def validate(self):
      res = self.e1.get()
      try:
        self.result = float(res) if '.' in res else int(res)
        return True
      except ValueError:
        self.setError("Invalid number.")
        return False

#####################################
## Toplevel Stuff
#####################################
class SubWindow(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.escapeBindId = None # used to exit fullscreen
        self.stopFunction = None # used to stop

    def __getattr__(self,name):
        def handlerFunction(*args,**kwargs):
              print("Unknown function:", name,args,kwargs)
        return handlerFunction

#####################################
## MAIN - for testing
#####################################
if __name__ == "__main__":
    print("This is a library class and cannot be executed.")
    sys.exit()
