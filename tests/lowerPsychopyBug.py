import psychopy.info
from psychopy import monitors, visual, event, data, logging, core, sound, gui
monitorname = 'testmonitor'
waitBlank = False
mon = monitors.Monitor(monitorname,width=30, distance=57)#relying on  monitorwidth cm (39 for Mitsubishi to do deg calculations) and gamma info in calibratn
mon.setSizePix( (1024,768) )
units='deg' #'cm'
bgColor = [-.7,-.7,-.7] # [-1,-1,-1]
allowGUI = False
waitBlank = True
scrn = 0
fullscr=True
def openMyStimWindow(): #make it a function because have to do it several times, want to be sure is identical each time
    myWin = visual.Window(monitor=mon,size=(1024,768),allowGUI=allowGUI,units=units,color=bgColor,colorSpace='rgb',fullscr=fullscr,screen=scrn,waitBlanking=waitBlank,
                   winType='pyglet' ) #pygame doesn't work, don't know why. Works in textLocationTest.py
    return myWin
myWin = openMyStimWindow()


runInfo = psychopy.info.RunTimeInfo(
            # if you specify author and version here, it overrides the automatic detection of __author__ and __version__ in your script
            #author='<your name goes here, plus whatever you like, e.g., your lab or contact info>',
            #version="<your experiment version info>",
            win=myWin,    ## a psychopy.visual.Window() instance; None = default temp window used; False = no win, no win.flips()
            refreshTest='grating', ## None, True, or 'grating' (eye-candy to avoid a blank screen)
            verbose=True, ## True means report on everything 
            userProcsDetailed=True  ## if verbose and userProcsDetailed, return (command, process-ID) of the user's processes
            )
print(runInfo)