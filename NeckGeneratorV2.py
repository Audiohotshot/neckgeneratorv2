
# Audiohotshot Neck Generator
# This plugin is under Common Creative License
# December 2021
# highest string, thinnest, bottom, first string = high E
# lowest string, thickest, top, last string = lowest E

import adsk.core, adsk.fusion, adsk.cam, traceback
import math

# Global list to keep all event handlers in scope.
# This is only needed with Python.
handlers = []

def drawNeckScale(scaleLowString):
    # DRAWING STARTS HERE
    # Get the root component of the active design.
    app = adsk.core.Application.get()
    design = app.activeProduct
    rootComp = design.rootComponent        
    # Create a new sketch on the xy plane.
    sketches = rootComp.sketches;                                           
    xyPlane = rootComp.xYConstructionPlane
    sketch = sketches.add(xyPlane)
    sketch.name = 'Scale' 
    lines = sketch.sketchCurves.sketchLines;
        
    #draw center construction line
    x1 = (0 ) / 2
    y1 = 0
    x2 = (scaleLowString )
    y2 = 0
    line1 = lines.addByTwoPoints(adsk.core.Point3D.create(x1, y1, 0), adsk.core.Point3D.create(x2, y2, 0))    
    line1.isConstruction = True

def drawNeckScaleFanned( scaleLowString , scaleHighString, neutralPoint, eeNutDistance, eeTremDistance):
    # DRAWING STARTS HERE
    # Get the root component of the active design.
    app = adsk.core.Application.get()
    design = app.activeProduct
    rootComp = design.rootComponent        
    # Create a new sketch on the xy plane.
    sketches = rootComp.sketches;                                           
    xyPlane = rootComp.xYConstructionPlane
    sketch = sketches.add(xyPlane)
    sketch.name = 'Scale' 
    lines = sketch.sketchCurves.sketchLines
    
    #calculate Neutral point on each scale
    scaleLowXNeutralPositionToNut = scaleLowString - (scaleLowString / 2 ** ( neutralPoint /12) )   # (800-(800/2**(5/12))=200
    scaleLowXNeutralPositionToTrem = scaleLowString - scaleLowXNeutralPositionToNut                 # 800 - 200 = 600
    scaleHighXNeutralPositionToNut = scaleHighString - (scaleHighString / 2 ** ( neutralPoint /12) )# 150
    scaleHighXNeutralPositionToTrem = scaleHighString - scaleHighXNeutralPositionToNut              # 600 - 150 = 450
    #calculate x distance between low and high scale
    xOffsetNut =  scaleLowXNeutralPositionToNut - scaleHighXNeutralPositionToNut                    # 200 - 150 = 50
    xOffsetTrem = scaleLowXNeutralPositionToTrem - scaleHighXNeutralPositionToTrem                  # 600 - 450 = 150
    #calculate center length
    scaleCenter = ((scaleHighString + scaleLowString ) /2)                                          # (600+800)/2 = 700
    scaleCenterNeutralposition = scaleCenter - (scaleCenter / 2 ** ( neutralPoint /12) )
    #draw Neutralposition on ScaleCenter
    circles = sketch.sketchCurves.sketchCircles
    circles.addByCenterRadius(adsk.core.Point3D.create( scaleCenterNeutralposition, 0, 0), 0.2)

    # calculate eeNut Y-position of start of scale, based on lenght of 1/2 eeNutDistance to top and bottom string
    #y position of 1/2 angled eeNutDistance =>> pythagoras (sqrt(a^2+b^2)) >> a2+b2=c2 -> b2= c2-a2
    a = ( xOffsetNut / 2 ) 
    c = ( eeNutDistance / 2 ) 
    yOffsetNut = math.sqrt( (c ** 2) - (a ** 2) ) 
    #calculate eeTrem Y position
    a = ( xOffsetTrem / 2 ) 
    c = ( eeTremDistance / 2 ) 
    yOffsetTrem = math.sqrt( (c ** 2) - (a ** 2) ) 

    #draw Highest String as construction line
    x1 = ( xOffsetNut / 2 )
    y1 = yOffsetNut
    x2 = (scaleHighString + (xOffsetNut / 2 ) )
    y2 = yOffsetTrem
    line1 = lines.addByTwoPoints(adsk.core.Point3D.create(x1, y1, 0), adsk.core.Point3D.create(x2, y2, 0))    
    line1.isConstruction = True

    #draw Lowest String as construction line
    x1 = - ( xOffsetNut / 2 )
    y1 = - yOffsetNut
    x2 = ( scaleLowString - (xOffsetNut / 2 ) )
    y2 = - yOffsetTrem
    line1 = lines.addByTwoPoints(adsk.core.Point3D.create(x1, y1, 0), adsk.core.Point3D.create(x2, y2, 0))    
    line1.isConstruction = True

    #draw centerScale as construction line
    x1 = 0
    y1 = 0
    x2 = scaleCenter
    y2 = 0
    line1 = lines.addByTwoPoints(adsk.core.Point3D.create(x1, y1, 0), adsk.core.Point3D.create(x2, y2, 0))    
    line1.isConstruction = True

def drawOutlineFretboard(scaleLowString, nutWidth, fretno , tremWidth, fretboardEnd):
    # DRAWING STARTS HERE
    # Get the root component of the active design.
    app = adsk.core.Application.get()
    design = app.activeProduct
    rootComp = design.rootComponent        
    # Create a new sketch on the xy plane.
    sketches = rootComp.sketches;                                           
    xyPlane = rootComp.xYConstructionPlane
    sketch = sketches.add(xyPlane)
    sketch.name = 'Outline Fretboard' 
    lines = sketch.sketchCurves.sketchLines;

    # draw outline fretboard high and low
    #lowest string side (lowE)
    x1 = 0
    y1 = -(nutWidth / 2 )
    x2 = scaleLowString 
    y2 = - ( tremWidth /2)  
    lines.addByTwoPoints(adsk.core.Point3D.create(x1, y1, 0) , adsk.core.Point3D.create(x2, y2, 0))
    #highest string side (highE)
    x1 = 0
    y1 = (nutWidth / 2 )
    x2 = scaleLowString 
    y2 = ( tremWidth / 2)
    lines.addByTwoPoints(adsk.core.Point3D.create(x1, y1, 0) , adsk.core.Point3D.create(x2, y2, 0))

    #draw fret 0
    x1 = 0
    y1 = -(nutWidth / 2 )
    x2 = 0
    y2 = (nutWidth / 2 )
    lines.addByTwoPoints(adsk.core.Point3D.create(x1, y1, 0) , adsk.core.Point3D.create(x2, y2, 0))

    #draw last extra fretboard at end of fretboard to hold last fret
    x1 = ( scaleLowString - (scaleLowString / 2 ** ((fretno-1)/12)) + fretboardEnd )
    a = ( scaleLowString - (scaleLowString / 2 ** ((fretno-1)/12)) + fretboardEnd )
    c = ( tremWidth / 2) 
    y1 = - ( ( ( ( c - (nutWidth/2 ) ) * a ) / scaleLowString ) + (nutWidth/2) ) 
    x2 = scaleLowString - (scaleLowString / 2 ** ((fretno-1)/12) ) + fretboardEnd
    y2 = ( ( ( ( c - (nutWidth/2 ) ) * a ) / scaleLowString ) + (nutWidth/2) )
    lines.addByTwoPoints(adsk.core.Point3D.create(x1, y1, 0) , adsk.core.Point3D.create(x2, y2, 0))  

    #draw trem e-e
    x1 = scaleLowString
    y1 = - ( tremWidth / 2 )
    x2 = scaleLowString 
    y2 = ( tremWidth /2 )  
    lines.addByTwoPoints(adsk.core.Point3D.create(x1, y1, 0) , adsk.core.Point3D.create(x2, y2, 0))

def drawOutlineFretboardFanned( scaleLowString, scaleHighString, neutralPoint, eeNutDistance, eeTremDistance, nutWidth, fretno, tremWidth, fretboardEnd):
    # DRAWING STARTS HERE
    # Get the root component of the active design.
    app = adsk.core.Application.get()
    design = app.activeProduct
    rootComp = design.rootComponent        
    # Create a new sketch on the xy plane.
    sketches = rootComp.sketches;                                           
    xyPlane = rootComp.xYConstructionPlane
    sketch = sketches.add(xyPlane)
    sketch.name = 'Outline Fretboard' 
    lines = sketch.sketchCurves.sketchLines

    #calculate Neutral point on each scale
    diffEENutandNut = (nutWidth - eeNutDistance) / 2
    scaleLowStringAndNut = scaleLowString + diffEENutandNut
    scaleHighStringAndNut = scaleHighString + ( (nutWidth - eeNutDistance) )
    scaleLowXNeutralPositionToNut = scaleLowString - (scaleLowString / 2 ** ( neutralPoint /12) )   # (800-(800/2**(5/12))=200
    scaleLowXNeutralPositionToTrem = scaleLowString - scaleLowXNeutralPositionToNut                 # 800 - 200 = 600
    scaleHighXNeutralPositionToNut = scaleHighString - (scaleHighString / 2 ** ( neutralPoint /12) )# 150
    scaleHighXNeutralPositionToTrem = scaleHighString - scaleHighXNeutralPositionToNut              # 600 - 150 = 450
    #calculate x distance between low and high scale
    xOffsetNut =  scaleLowXNeutralPositionToNut - scaleHighXNeutralPositionToNut                    # 200 - 150 = 50
    xOffsetTrem = scaleLowXNeutralPositionToTrem - scaleHighXNeutralPositionToTrem                  # 600 - 450 = 150
    #calculate center length
    #scaleCenter = ((scaleHighString + scaleLowString ) /2)                                          # (600+800)/2 = 700

    # calculate eeNut Y-position of start of scale, based on length of 1/2 eeNutDistance to top and bottom string
    #y position of 1/2 angled eeNutDistance =>> pythagoras (sqrt(a^2+b^2)) >> a2+b2=c2 -> b2= c2-a2
    a = ( xOffsetNut / 2 )
    c = ( nutWidth / 2 ) 
    yOffsetNut = math.sqrt( (c ** 2) - (a ** 2) ) 
    #calculate eeTrem Y position
    a = ( xOffsetTrem / 2 ) 
    c = ( tremWidth / 2 ) 
    yOffsetTrem = math.sqrt( (c ** 2) - (a ** 2) ) 

    # draw outline fretboard high and low
    #lowest string side (lowE)
    x1 = - ( xOffsetNut / 2 ) - (diffEENutandNut / 3) #????
    y1 = - yOffsetNut
    x2 = ( scaleLowString - ( xOffsetNut / 2 ) )
    y2 = - yOffsetTrem
    lines.addByTwoPoints(adsk.core.Point3D.create(x1, y1, 0) , adsk.core.Point3D.create(x2, y2, 0))
    #highest string side (highE)
    x1 = ( xOffsetNut / 2 )
    y1 = yOffsetNut
    x2 = (scaleHighString + (xOffsetNut / 2 ) )
    y2 = yOffsetTrem
    lines.addByTwoPoints(adsk.core.Point3D.create(x1, y1, 0) , adsk.core.Point3D.create(x2, y2, 0))

    #draw fret 0
    x1 = 0
    y1 = -(nutWidth / 2 )
    x2 = 0
    y2 = (nutWidth / 2 )
    #lines.addByTwoPoints(adsk.core.Point3D.create(x1, y1, 0) , adsk.core.Point3D.create(x2, y2, 0))

    #draw last extra fretboard at end of fretboard to hold last fret
    x1 = ( scaleLowString - (scaleLowString / 2 ** ((fretno-1)/12)) + fretboardEnd )
    a = ( scaleLowString - (scaleLowString / 2 ** ((fretno-1)/12)) + fretboardEnd )
    c = ( tremWidth / 2) 
    y1 = - ( ( ( ( c - (nutWidth/2 ) ) * a ) / scaleLowString ) + (nutWidth/2) ) 
    x2 = scaleLowString - (scaleLowString / 2 ** ((fretno-1)/12) ) + fretboardEnd
    y2 = ( ( ( ( c - (nutWidth/2 ) ) * a ) / scaleLowString ) + (nutWidth/2) )
    #lines.addByTwoPoints(adsk.core.Point3D.create(x1, y1, 0) , adsk.core.Point3D.create(x2, y2, 0))  

    #draw trem e-e
    x1 = scaleLowString
    y1 = - ( tremWidth / 2 )
    x2 = scaleLowString 
    y2 = ( tremWidth /2 )  
    #lines.addByTwoPoints(adsk.core.Point3D.create(x1, y1, 0) , adsk.core.Point3D.create(x2, y2, 0))

def drawFrets(scaleLowString, nutWidth, fretno , tremWidth):
    # DRAWING STARTS HERE
    # Get the root component of the active design.
    app = adsk.core.Application.get()
    design = app.activeProduct
    rootComp = design.rootComponent        
    # Create a new sketch on the xy plane.
    sketches = rootComp.sketches;                                           
    xyPlane = rootComp.xYConstructionPlane
    sketch = sketches.add(xyPlane)
    sketch.name = 'Fretlines' 
    lines = sketch.sketchCurves.sketchLines;
    
    # draw individual frets
    n = 1
    while True:
        #draw fretlines 
        x1 = ( scaleLowString - (scaleLowString / 2 ** (n/12) ) )
        a = ( scaleLowString - (scaleLowString / 2 ** (n/12)) )
        c = ( tremWidth / 2) 
        y1 = - ( ( ( ( c - (nutWidth/2 ) ) * a ) / scaleLowString ) + (nutWidth/2) )
        x2 = ( scaleLowString - (scaleLowString / 2 ** (n/12) ) )
        y2 = ( ( ( ( c - (nutWidth/2 ) ) * a ) / scaleLowString ) + (nutWidth/2) )
        lines.addByTwoPoints(adsk.core.Point3D.create(x1, y1, 0), adsk.core.Point3D.create(x2, y2, 0))        
        #counter        
        n = n + 1 
        if n == fretno:
            break

def drawDots (scaleLowString, nutWidth, fretno, radius):
    # DRAWING STARTS HERE
    # Get the root component of the active design.
    app = adsk.core.Application.get()
    design = app.activeProduct
    rootComp = design.rootComponent        
    # Create a new sketch on the xy plane.
    sketches = rootComp.sketches;                                           
    xyPlane = rootComp.xYConstructionPlane
    sketch = sketches.add(xyPlane)
    sketch.name = 'Inlay Dots' 
    #lines = sketch.sketchCurves.sketchLines;
    
    #draw dots 
    a = [0,0,1,0,1,0,1,0,1,0,0, 2,0,0,1,0,1,0,1,0,1,0,0, 2,0,0,1,0,1,0,1,0,1,0,0,2]
    n = 0
    while True:
        if n != 0:
            s = a[n-1]
            #calculate centre dot
            x1 = scaleLowString - (scaleLowString / 2 ** ((n-0.5)/12))
            y1 = 0
            if s == 1:
                #draw dot
                circles = sketch.sketchCurves.sketchCircles
                circles.addByCenterRadius(adsk.core.Point3D.create(x1, y1, 0), radius)
            if s == 2:
                #calculate x position dots
                x1 = scaleLowString - (scaleLowString / 2 ** ((n-0.5)/12)) 
                #calculate y position dots
                y1 = (0 - nutWidth / 2) + (nutWidth *  (1/3))
                y2 = (0 - nutWidth / 2) + (nutWidth * (2/3))  
                #draw dots
                circles = sketch.sketchCurves.sketchCircles
                circles.addByCenterRadius(adsk.core.Point3D.create(x1, y1, 0), radius)
                circles.addByCenterRadius(adsk.core.Point3D.create(x1, y2, 0), radius)  
        n = n + 1 
        if n == fretno:
            break

def drawStrings(scaleLowString, eeNutDistance, eeTremDistance, stringsNo ):
    # DRAWING STARTS HERE
    # Get the root component of the active design.
    app = adsk.core.Application.get()
    design = app.activeProduct
    rootComp = design.rootComponent        
    # Create a new sketch on the xy plane.
    sketches = rootComp.sketches;                                           
    xyPlane = rootComp.xYConstructionPlane
    sketch = sketches.add(xyPlane)
    sketch.name = 'Strings' 
    lines = sketch.sketchCurves.sketchLines;

    # draw string 
    x1 = 0
    x2 = scaleLowString 
    
    n = 0
    while True:
        startNutHeigth = eeNutDistance / 2
        factorNut = eeNutDistance / (stringsNo - 1)
        y1 = startNutHeigth - (n * factorNut)

        startTremHeight = eeTremDistance /2
        factorTrem = eeTremDistance / (stringsNo - 1)
        y2 = startTremHeight - (n * factorTrem)
        lines.addByTwoPoints(adsk.core.Point3D.create(x1, y1, 0) , adsk.core.Point3D.create(x2, y2, 0))
    
        n = n + 1 
        if n == stringsNo:
            break
       
def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        
        # Get the CommandDefinitions collection.
        cmdDefs = ui.commandDefinitions
       
        # Create a button command definition.
        buttonSample = cmdDefs.addButtonDefinition('MyButtonDefIdPython', 
                                                   'Neck Generator', 
                                                   'Sample button tooltip',
                                                   './Resources')
        
        # Connect to the command created event.
        sampleCommandCreated = SampleCommandCreatedEventHandler()
        buttonSample.commandCreated.add(sampleCommandCreated)
        handlers.append(sampleCommandCreated)

        # Get the ADD-INS panel in the model workspace. 
        addInsPanel = ui.allToolbarPanels.itemById('SolidCreatePanel')
        
        # Add the button to the bottom of the panel.
        addInsPanel.controls.addCommand(buttonSample)
        if context['IsApplicationStartup'] == False:    
            ui.messageBox('The "Neck Generator" command has been added\nto the CREATE panel')
            
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
        
def stop(context):
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        
        # Clean up the UI.
        cmdDef = ui.commandDefinitions.itemById('MyButtonDefIdPython')
        if cmdDef:
            cmdDef.deleteMe()
            
        addinsPanel = ui.allToolbarPanels.itemById('SolidCreatePanel')
        cntrl = addinsPanel.controls.itemById('MyButtonDefIdPython')
        if cntrl:
            cntrl.deleteMe()
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))	

# Event handler for the inputChanged event.
class SampleCommandInputChangedHandler(adsk.core.InputChangedEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        try:
            app = adsk.core.Application.get()
            ui  = app.userInterface            
            eventArgs = adsk.core.InputChangedEventArgs.cast(args)
            
            # Check the value of the check box.
            changedInput = eventArgs.input
            if changedInput.id == 'fanned':
                inputs = eventArgs.firingEvent.sender.commandInputs
                targetInput = inputs.itemById('scaleHighString')
                targetInput2 = inputs.itemById('neutralPoint')
           
                # Change the visibility of the scale value input.
                if changedInput.value == False:
                    targetInput.isVisible = False
                    targetInput2.isVisible = False
                else:
                    targetInput.isVisible = True
                    targetInput2.isVisible = True
    
            # Check the value of the check box.
            if changedInput.id == 'chkDots':
                inputs = eventArgs.firingEvent.sender.commandInputs
                targetInput = inputs.itemById('dotSize')
                # Change the visibility of the scale value input.
                if changedInput.value == False:
                    targetInput.isVisible = False
                else:
                    targetInput.isVisible = True
            
            # Check the value of the check box.
            if changedInput.id == 'chkStrings':
                inputs = eventArgs.firingEvent.sender.commandInputs
                targetInput = inputs.itemById('stringsNo')
                # Change the visibility of the scale value input.
                if changedInput.value == False:
                    targetInput.isVisible = False
                else:
                    targetInput.isVisible = True
                    
        except:
            if ui:
                ui.messageBox(('Input changed event failed: {}').format(traceback.format_exc()))  

# Event handler for the execute event.
class SampleCommandExecuteHandler(adsk.core.CommandEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):                
        # Code to react to the event.
        app = adsk.core.Application.get()
        ui  = app.userInterface
        #ui.messageBox('In command execute event handler.')                          
        try:
            command = args.firingEvent.sender
            ui.messageBox(('command: {} executed successfully').format(command.parentCommandDefinition.id))
        except:
            if ui:
                ui.messageBox(('command executed failed: {}').format(traceback.format_exc()))
                
# Event handler for the commandCreated event.
class SampleCommandCreatedEventHandler(adsk.core.CommandCreatedEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        try:        
            eventArgs = adsk.core.CommandCreatedEventArgs.cast(args)
            app = adsk.core.Application.get()
            ui  = app.userInterface     
            # Get the commandS
            cmd = eventArgs.command 
            
            # Get the CommandInputs collection to create new command inputs.            
            inputs = cmd.commandInputs
    
            # Create a check box to get if it should be fanned  or not. UNDER CONSTRUCTION
            # inputs.addBoolValueInput('fanned', 'Fanned Frets', True, '', False) 

            # Create the value input to get the scale. 
            inputs.addValueInput('scaleLowString', 'Scale', 'mm', adsk.core.ValueInput.createByReal(70))
                                                   
            # Create the value input to get the lower scale. 
            scaleHighString = inputs.addValueInput('scaleHighString', 'Scale High', 'mm', adsk.core.ValueInput.createByReal(65))
            scaleHighString.isVisible = False
                                               
            # Create the value input to get the centre fret of the fanned scale. 
            neutralPoint = inputs.addValueInput('neutralPoint', 'Neutral point', '', adsk.core.ValueInput.createByReal(5)) 
            neutralPoint.isVisible = False                                          
                                                
            # Create the value input to get the amount of frets. 
            inputs.addValueInput('fretsNo', 'Number of frets', '', adsk.core.ValueInput.createByReal(24))   
            #fretsNo = inputs.addIntegerSliderCommandInput('fretsno', 'Number of frets', 1, 36)
            
            # Create a check box to get if it should string dots or not.
            inputs.addBoolValueInput('chkStrings', 'Draw strings', True, '', False) 
            
            # Create the value input to get the numnber of strings (6 for guitar)
            stringsno = inputs.addValueInput('stringsNo', 'No. of strings', '', adsk.core.ValueInput.createByReal(6)) 
            stringsno.isVisible = False  

            # Create the value input to get the width of the board. 
            inputs.addValueInput('nutWidth', 'Nut width', 'mm', adsk.core.ValueInput.createByReal(4.4))

            # Create the value input to get the E-E distance. 
            inputs.addValueInput('eeNutDistance', 'E-E Nut width', 'mm', adsk.core.ValueInput.createByReal(4.0)) #3.4  
            
            # Create the value input to get the width of the tremolo E-E distance. 
            inputs.addValueInput('eeTremDistance', 'E-E Trem width', 'mm', adsk.core.ValueInput.createByReal(5.0)) #5.3

            # Create the value input to get the width of the tremolo E-E distance. 
            inputs.addValueInput('fretboardEnd', 'Last fret end', 'mm', adsk.core.ValueInput.createByReal(0.5)) 

            # Create a check box to get if it should draw dots or not.
            inputs.addBoolValueInput('chkDots', 'Draw dots', True, '', False)  
    
            # Create the value input to get the dotsize
            dotsize = inputs.addValueInput('dotSize', 'Dots size', 'mm', adsk.core.ValueInput.createByReal(0.4))
            dotsize.isVisible = False  
                                        
            #errMessage = inputs.addTextBoxCommandInput('errMessage', '', '', 2, True)
            errMessage = inputs.addTextBoxCommandInput('errmessage', 'Text Box 1', '', 2, True)
            errMessage.isFullWidth = True                                    
            
            # Connect to the execute event.
            onExecute = SampleCommandExecuteHandler()
            cmd.execute.add(onExecute)
            handlers.append(onExecute)
    
            # Connect to the inputChanged event.
            onInputChanged = SampleCommandInputChangedHandler()
            cmd.inputChanged.add(onInputChanged)
            handlers.append(onInputChanged)
    
            # execute preview
            onExecutePreview = SampleCommandExecutePreviewHandler()
            cmd.executePreview.add(onExecutePreview)
            handlers.append(onExecutePreview)
            
            # execute validation
            onValidateInputs = SampleCommandValidateInputsHandler()
            cmd.validateInputs.add(onValidateInputs)
            handlers.append(onValidateInputs)
        except:
            if ui:
                ui.messageBox('Failed CreatedEventHandler:\n{}'.format(traceback.format_exc()))	

# Event handler for the validateInputs event.
class SampleCommandValidateInputsHandler(adsk.core.ValidateInputsEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        try:
            app = adsk.core.Application.get()
            ui  = app.userInterface     
            
            eventArgs = adsk.core.ValidateInputsEventArgs.cast(args)
            inputs = eventArgs.firingEvent.sender.commandInputs
            
            # Verify that the scale is greater than 0.1.
            inputarg = inputs.itemById('fretsNo').value
            if inputarg < 1:
                eventArgs.areInputsValid = False
                return
            else:
                inputarg = inputs.itemById('neutralPoint').value
                if inputarg < 1:
                    eventArgs.areInputsValid = False
                    return
                else:
                    eventArgs.areInputsValid = True
                
        except:
            if ui:
                ui.messageBox('Failed ValidateInputsHandler:\n{}'.format(traceback.format_exc()))
                
# Event handler for the executePreview event.
class SampleCommandExecutePreviewHandler(adsk.core.CommandEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        try:
            app = adsk.core.Application.get()
            ui  = app.userInterface     
                    
            eventArgs = adsk.core.CommandEventArgs.cast(args)
            
            # Collect all input
            # Get the command
            cmd = eventArgs.command
    
            # Get the CommandInputs collection to create new command inputs.            
            inputs = cmd.commandInputs
                    
           
            scaleLowString = inputs.itemById('scaleLowString').value        
            scaleHighString = inputs.itemById('scaleHighString').value
            neutralPoint = inputs.itemById('neutralPoint').value
            fretno = inputs.itemById('fretsNo').value + 1
            nutWidth = inputs.itemById('nutWidth').value
            eeNutDistance = inputs.itemById('eeNutDistance').value
            eeTremDistance = inputs.itemById('eeTremDistance').value
            tremWidth = eeTremDistance + (nutWidth - eeNutDistance )
            fretboardEnd = (inputs.itemById('fretboardEnd').value)
            chkdots = inputs.itemById('chkDots').value
            radius = inputs.itemById('dotSize').value / 2
            stringsNo = inputs.itemById('stringsNo').value 
            chkstrings = inputs.itemById('chkStrings').value 
            #fanned = inputs.itemById('fanned').value UNDER CONSTRUCTION
            fanned = False
            
            # THE ACTUAL DRAWING IS INITIATED HERE
            if fanned == False:  
                drawNeckScale( scaleLowString )
                drawOutlineFretboard(scaleLowString, nutWidth, fretno, tremWidth, fretboardEnd)
                drawFrets(scaleLowString, nutWidth, fretno, tremWidth)
            else:
                drawNeckScaleFanned( scaleLowString , scaleHighString, neutralPoint, eeNutDistance, eeTremDistance)
                drawOutlineFretboardFanned( scaleLowString, scaleHighString, neutralPoint, eeNutDistance, eeTremDistance, nutWidth, fretno, tremWidth, fretboardEnd)
            
            if chkdots == True: 
                drawDots (scaleLowString, nutWidth, fretno, radius)
            if chkstrings == True: 
                drawStrings(scaleLowString, eeNutDistance, eeTremDistance, stringsNo )     
            
            # Set the isValidResult property to use these results at the final result.
            # This will result in the execute event not being fired.
            eventArgs.isValidResult = True

        except:
            if ui:
                ui.messageBox('Failed ValidateInputsHandler:\n{}'.format(traceback.format_exc()))





#cos alfa = (a/c) =  math.degrees(math.acos(0))
    #angle = math.acos( a / c )

    #show calculated number in textcommands
    #app = adsk.core.Application.get()
    #ui  = app.userInterface
    #ui.palettes.itemById('TextCommands').writeText("Textje van mij")
    