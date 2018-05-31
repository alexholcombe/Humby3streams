from __future__ import print_function
from psychopy import event, sound, logging
from psychopy import visual, event, sound, tools
import numpy as np
import string, random
from math import floor
from copy import deepcopy

def calcRespYandBoundingBox(possibleResps, horizVert, i):
    spacingCtrToCtr = 2.0 / len(possibleResps)
    charHeight = spacingCtrToCtr
    #coordinate will be interpreted as y if horizVert, x otherwise
    startCoordinate = 1-charHeight/2 #top , to bottom
    if horizVert==0:
        startCoordinate*= -1 #left to right
    increment = i*spacingCtrToCtr
    if horizVert==1:
        increment*=- 1 #go down from top
    coordinate = startCoordinate + increment
    boxWidth = spacingCtrToCtr #0.1
    boxHeight = spacingCtrToCtr
    return coordinate, boxWidth, boxHeight

def drawRespOption(myWin,bgColor,constantCoord,horizVert,color,drawBoundingBox,relativeSize,possibleResps,i):
        #constantCoord is x if horizVert=1 (vertical), y if horizontal
        #relativeSize multiplied by standard size to get desired size
        coord, w, h = calcRespYandBoundingBox( possibleResps, horizVert, i )
        x = constantCoord if horizVert else coord
        y = coord if horizVert else constantCoord
        if relativeSize != 1: #erase bounding box so erase old letter before drawing new differently-sized letter 
            #print('drawing to erase')
            boundingBox = visual.Rect(myWin,width=w,height=h, pos=(x,y), fillColor=bgColor, lineColor=None, units='norm' ,autoLog=False) 
            boundingBox.draw()
        option = visual.TextStim(myWin, font = 'sloan',colorSpace='rgb',color=color,alignHoriz='center', alignVert='center',
                                                                    height=h*relativeSize,units='norm',autoLog=False)
        option.setText(possibleResps[i])
        option.pos = (x, y)
        option.draw()
        if drawBoundingBox:
            boundingBox = visual.Rect(myWin,width=w,height=h, pos=(x,y))
            boundingBox.draw()
        
def drawArray(myWin,bgColor,possibleResps,horizVert,constCoord,lightness,drawBoundingBox):
    '''Draw possibleResps in position x with RGB lightness    
     constCoord is x if horizVert=1 (vertical), y if horizontal
    '''
    #print("lightness in drawArray=",lightness," x=",x)
    #Draw it vertically, from top to bottom
    for i in xrange(len(possibleResps)):
        drawRespOption(myWin,bgColor,constCoord,horizVert,(lightness,lightness,lightness),drawBoundingBox,1,possibleResps,i)

def drawResponseArrays(myWin,bgColor,horizVert,xOffset,possibleResps,numLineupsToDraw,leftCentralRight):
    '''If numLineupsToDraw=2, draw array on both sides, with one side dimmed. If 3, also draw one in center
    If leftRightCentral=0, collect response from left side, and draw other side dim. If =1, from right side. 2= central array.
    possibleResps is usually an array of all the letters to populate the array with.
    xOffset is offset of center of response array relative to center of screen, in norm units
    '''
    numResps = len(possibleResps)
    dimRGB = -.3
    drawBoundingBox = False #to debug to visualise response regions, make True
    lightnessLCR = [bgColor,bgColor,bgColor] #lightness on left, central, right.
    if numLineupsToDraw >= 2:
        lightnessLCR[0] = dimRGB
        lightnessLCR[2] = dimRGB
    if numLineupsToDraw == 3:
        lightnessLCR[1] = dimRGB

    lightnessLCR[leftCentralRight] = 1 #Make the one being probed now bright
    
    if numLineupsToDraw == 1:
        lightness = 1
        if leftCentralRight == 0:
            x = -xOffset
        elif leftCentralRight == 2:
            x = xOffset
        elif leftCentralRight==1:
            x = 0
        drawArray(myWin,bgColor,possibleResps,horizVert, x, lightness,drawBoundingBox)
        
    if numLineupsToDraw>1: #draw two or three
        drawArray(myWin,bgColor,possibleResps,horizVert, xOffset*-1, lightnessLCR[0],drawBoundingBox) #left
        drawArray(myWin,bgColor,possibleResps,horizVert, xOffset, lightnessLCR[2],drawBoundingBox) #right
        if numLineupsToDraw>2:
            drawArray(myWin,bgColor,possibleResps,horizVert, 0, lightnessLCR[1],drawBoundingBox) #central

def checkForOKclick(mousePos,respZone):
    OK = False
    if respZone.contains(mousePos):
            OK = True
    return OK

def convertXYtoNormUnits(XY,currUnits,win):
    if currUnits == 'norm':
        return XY
    else:
        widthPix = win.size[0]
        heightPix = win.size[1]
        if currUnits == 'pix':
            xNorm = XY[0]/ (widthPix/2)
            yNorm = XY[1]/ (heightPix/2)
        elif currUnits== 'deg':
            xPix = tools.monitorunittools.deg2pix(XY[0], win.monitor, correctFlat=False)
            yPix = tools.monitorunittools.deg2pix(XY[1], win.monitor, correctFlat=False)
            xNorm = xPix / (widthPix/2)
            yNorm = yPix / (heightPix/2)
            #print("Converted ",XY," from ",currUnits," units first to pixels: ",xPix,yPix," then to norm: ",xNorm,yNorm)
    return xNorm, yNorm

def collectOneLineupResponse(myWin,bgColor,myMouse,numLineupsToDraw,horizVert,leftCentralRight,OKtextStim,OKrespZone,possibleResps,xOffset,clickSound,badClickSound):
   if leftCentralRight == 0: #left
        constCoord = -1*xOffset
   elif leftCentralRight == 1: #central
        constCoord = 0
        if not horizVert: #horizontal
            OKrespZone.pos += [-.0,-.6]
            OKtextStim.pos+= [-.0,-.6]
   elif leftCentralRight == 2: #right
        constCoord = xOffset
   sideIndicatorCoord = .6*constCoord  #.77
   if leftCentralRight==1: #central
       sideIndicatorCoord = -.2
       if random.randint(0, 1): #randomly pick which side, to avoid introducing any left/right bias
        sideIndicatorCoord *= -1 
   myMouse.clickReset()
   sideIndicator = visual.Rect(myWin, width=.14, height=.04, fillColor=(1,1,1), fillColorSpace='rgb', lineColor=None, units='norm', autoLog=False)

   sideIndicator.setPos( [sideIndicatorCoord, 0] )
   chosenLtr = visual.TextStim(myWin, font = 'sloan',colorSpace='rgb',color=(1,1,1),alignHoriz='center', alignVert='center',height=.4,units='norm',autoLog=False)
   if horizVert: #vertical array
    chosenLtrPos = [sideIndicatorCoord,0]
    chosenLtr.setPos( chosenLtrPos )  #big drawing of chosen letter, offset from lineup
   else: #horizontal array
    sideIndicatorCoord = -.3
    chosenLtrPos = [0,sideIndicatorCoord]
    chosenLtr.setPos( chosenLtrPos )  #big drawing of chosen letter, offset from lineup
   
   whichResp = -1
   state = 'waitingForFirstClick' 
   #waitingForClick means OK is on the screen, so can either click a lineup item, or click OK
   #'finished' exit this lineup, choice has been made
   expStop = False
   while state != 'finished' and not expStop:
        #draw everything corresponding to this state
        drawResponseArrays(myWin,bgColor,horizVert,xOffset,possibleResps,numLineupsToDraw,leftCentralRight = leftCentralRight)
        if state == 'waitingForClick':
            #draw selected one in green, and bigly
            selectedColor = (-1,1,-1) #green
            buttonThis = np.where(pressed)[0] #assume only one button can be recorded as pressed
            if buttonThis == 0:
                selectedColor = (1,1,-1) #yellow for low confidence,
            drawRespOption(myWin,bgColor,constCoord,horizVert,selectedColor,False,1.5,possibleResps,whichResp)
            chosenLtr.setText(possibleResps[whichResp])
            chosenLtr.setColor( selectedColor )
            chosenLtr.draw()
            #draw respZone and big OK at same place as big offset letter
            OKrespZone.setPos( chosenLtrPos )
            OKrespZone.draw()
            OKtextStim.setPos( chosenLtrPos )
            OKtextStim.draw()
        else:
            pass
            #if leftCentralRight != 1:
            #    sideIndicator.draw()
            
        myWin.flip()
        #poll keyboard and mouse

        #Used to use pressed,times = myMouse.getPressed(getTime=True) because it's supposed to return all presses since last call to clickReset. But, doesn't seem to work. So, now block
        #If getTime=True (False by default) then getPressed will return all buttons that have been pressed since the last call to mouse.clickReset as well as their time stamps:
        pressed,times = myMouse.getPressed(getTime=True)
        while not any(pressed): #wait until pressed
            pressed = myMouse.getPressed() 
        mousePos = myMouse.getPos()
        mousePos = convertXYtoNormUnits(mousePos,myWin.units,myWin)
        #Check what was clicked, if anything
        OK = False
        if any(pressed):
            if state == 'waitingForClick':
                OK = checkForOKclick(mousePos,OKrespZone)
                #print('OK=', OK)
                if OK:
                    state = 'finished'
            if not OK: #didn't click OK. Check whether clicked near response array item
                topmostCoord, topmostW, topmostH =  calcRespYandBoundingBox( possibleResps, horizVert, 0) #determine bounds of adjacent option
                topmostX = constCoord if horizVert else topmostCoord
                topmostY = topmostCoord if horizVert else constCoord
                btmmostCoord, btmmostW, btmmostH =  calcRespYandBoundingBox(possibleResps,horizVert, len(possibleResps)-1)
                btmmostX = constCoord if horizVert else btmmostCoord
                btmmostY = btmmostCoord if horizVert else constCoord
                w = topmostW
                h = topmostH
                if horizVert:
                    horizBounds = [ constCoord-w/2, constCoord+w/2 ]
                    vertBounds = [btmmostY - h/2, topmostY + h/2]
                else: #horizontal
                    horizBounds = [topmostX-w/2, btmmostX+w/2,]  #top letter in vertical is first in horizontal
                    vertBounds =  [constCoord-h/2, constCoord+w/2 ]
                #print("horizBounds=",horizBounds," vertBounds=",vertBounds, " constCoord=", constCoord)
                xValid = horizBounds[0] <= mousePos[0] <= horizBounds[1]  #clicked in a valid x-position
                yValid = vertBounds[0] <= mousePos[1] <= vertBounds[1]  #clicked in a valid y-position
                if xValid and yValid:
                        clickSound.play()
                        relToBtm = mousePos[1] - vertBounds[0] #mouse coordinates go up from -1 to +1
                        relToLeft = mousePos[0] - horizBounds[0]
                        if horizVert: #vertical
                            whichResp = int (relToBtm / h)
                            #change from relToBtm to relative to top
                            whichResp = len(possibleResps) - 1- whichResp 
                        else: #horizontal
                            whichResp = int(relToLeft / w)
                            #print("whichResp from left hopefully = ",whichResp, " corresponding to ", possibleResps[whichResp])
                        #print("whichResp from top = ",whichResp, "xOffsetThis=",xOffsetThis, " About to redraw and draw one item in red")
                        lastValidClickButtons = deepcopy(pressed) #record which buttons pressed. Have to make copy, otherwise will change when pressd changes later
                        #print('lastValidClickButtons=',lastValidClickButtons)
                        state = 'waitingForClick' 
                else: 
                    badClickSound.play()
            for key in event.getKeys(): #only checking keyboard if mouse was clicked, hoping to improve performance
                key = key.upper()
                if key in ['ESCAPE']:
                    expStop = True
                    #noResponseYet = False
   response = possibleResps[whichResp]
   
   #Determine which button was pressed
   whichPressed = np.where(lastValidClickButtons)[0]
   if len(whichPressed)>1:
        print("Thought it was impossible to have pressed both buttons")
        print('whichPressed=',whichPressed)
   else:
        button = whichPressed[0]
   
   #print('Returning with response=',response,'button=',button,' expStop=',expStop)
   return response, button, expStop
        
def doLineup(myWin,bgColor,myMouse,clickSound,badClickSound,possibleResps,numLineups,whichLineupEachResp,autopilot):
    #whichLineupEachResp: 0 is left side, 1 is central, 2 is right
    
    expStop = False
    passThisTrial = False
    responsesAutopilot = []
    responses = []
    buttons = []
    #First collect one, then dim that one and collect the other
    xOffset = 0.7
    
    numDone = 0
    while numDone < numLineups:
        if autopilot: #I haven't bothered to make autopilot display the response screen
            responsesAutopilot.append('Z')
        else:
            #Draw arrays again, with some (if more than one) dim, to collect the other response
            leftCentralRight_this = whichLineupEachResp[numDone]
            okZoneX = 0
            if leftCentralRight_this == 1:
                okZoneX = -.25 #Can't have it in center because then will occlude the lineup
            OKrespZone = visual.GratingStim(myWin, tex="sin", mask="gauss", texRes=64, units='norm', size=[.25, .25], pos=(okZoneX,0), sf=[0, 0], name='OKrespZone')
            OKtextStim = visual.TextStim(myWin, font = 'sloan',pos=(okZoneX, 0),colorSpace='rgb',color=(-1,-1,-1),alignHoriz='center', alignVert='center',height=.13,units='norm',autoLog=False)
            OKtextStim.setText('OK')
            horizVert = 0 #horizontal
            if numLineups > 1:
                horizVert = 1
            whichResp0, whichButtonResp0, expStop = \
                    collectOneLineupResponse(myWin,bgColor,myMouse,numLineups,horizVert,leftCentralRight_this,OKtextStim,OKrespZone,possibleResps, xOffset, clickSound, badClickSound)
            responses.append(whichResp0)
            buttons.append(whichButtonResp0)
        numDone += 1 
    
    return expStop,passThisTrial,responses,buttons,responsesAutopilot

def setupSoundsForResponse():
    fileName = '406__tictacshutup__click-1-d.wav'
    try:
        clickSound=sound.Sound(fileName)
    except:
        print('Could not load the desired click sound file, instead using manually created inferior click')
        try:
            clickSound=sound.Sound('D',octave=3, sampleRate=22050, secs=0.015, bits=8)
        except:
            clickSound = None
            print('Could not create a click sound for typing feedback')
    try:
        badKeySound = sound.Sound('A',octave=5, sampleRate=22050, secs=0.08, bits=8)
    except:
        badKeySound = None
        print('Could not create an invalid key sound for typing feedback')
        
    return clickSound, badKeySound

if __name__=='__main__':  #Running this file directly, must want to test functions in this file
    from psychopy import monitors
    monitorname = 'testmonitor'
    mon = monitors.Monitor(monitorname,width=40.5, distance=57)
    windowUnits = 'deg' #purely to make sure lineup array still works when windowUnits are something different from norm units
    bgColor = [-.7,-.7,-.7] 
    myWin = visual.Window(monitor=mon,colorSpace='rgb',color=bgColor,units=windowUnits)
    #myWin = visual.Window(monitor=mon,size=(widthPix,heightPix),allowGUI=allowGUI,units=units,color=bgColor,colorSpace='rgb',fullscr=fullscr,screen=scrn,waitBlanking=waitBlank) #Holcombe lab monitor

    logging.console.setLevel(logging.WARNING)
    autopilot = False
    clickSound, badClickSound = setupSoundsForResponse()
    alphabet = list(string.ascii_uppercase)
    possibleResps = alphabet
    possibleResps.remove('C'); possibleResps.remove('W') #per Goodbourn & Holcombe, including backwards-ltrs experiments
    myWin.flip()
    passThisTrial = False
    myMouse = event.Mouse()

    testHorizontalLineup = False
    if testHorizontalLineup:
        #Do horizontal lineups
        responseDebug=False; responses = list(); responsesAutopilot = list();
        expStop = False
        numLineups = 1
        leftCentralRight = 2 #central
        expStop,passThisTrial,responses,buttons,responsesAutopilot = \
                    doLineup(myWin, bgColor, myMouse, clickSound, badClickSound, possibleResps, numLineups, leftCentralRight, autopilot)
        print('autopilot=',autopilot, ' responsesAutopilot =', responsesAutopilot)
        print('expStop=',expStop,' passThisTrial=',passThisTrial,' responses=',responses)
    
    testVertical2Lineup = False
    if testVertical2Lineup:
        #Do vertical 2-lineup case
        responseDebug=False; responses = list(); responsesAutopilot = list();
        expStop = False
        numLineups = 2
        leftCentralRightFirst = 2
        expStop,passThisTrial,responses,buttons,responsesAutopilot = \
                    doLineup(myWin, bgColor,myMouse, clickSound, badClickSound, possibleResps, numLineups, leftCentralRightFirst, autopilot)
        print('autopilot=',autopilot, ' responsesAutopilot =', responsesAutopilot)
        print('expStop=',expStop,' passThisTrial=',passThisTrial,' responses=',responses)
    
    #Do vertical 3-lineup case
    responseDebug=False; responses = list(); responsesAutopilot = list();
    expStop = False
    numLineups = 3
    whichLineupEachResp = [2,1,0]
    expStop,passThisTrial,responses,buttons,responsesAutopilot = \
                doLineup(myWin, bgColor,myMouse, clickSound, badClickSound, possibleResps, numLineups, whichLineupEachResp, autopilot)
    
    print('autopilot=',autopilot, 'responses=',responses)
    print('expStop=',expStop,' passThisTrial=',passThisTrial,' responses=',responses, ' responsesAutopilot =', responsesAutopilot)
    print('Finished') 