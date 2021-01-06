##############################################################################
#                                                                            #
# superAutoCrop                                                              #
# V 1.5                                                                      #
# Release January 06 2021                                                    #
#                                                                            #
# Did as a thankful gift to my mentor and friend Emerson Bonadias.           #
#                                                                            #
# Created by Luciano Cequinel (vimeo.com/cequinavfx)                         #
# to report bugs or suggestions lucianocequinel@gmail.com                    #
#                                                                            #
##############################################################################


'''

Just write
import superAutoCrop
on menu.py
and copy superAutoCrop.py to .nuke folder

See the ref_menu.py as a reference


'''

import nuke


def superAutoCrop():

    selNode = nuke.selectedNodes()
    nkRoot = nuke.root()

    if len(selNode) == 1:

        selNode = nuke.selectedNode()

        # Get Frame Range
        frame_range = nuke.FrameRange(nuke.getInput('Inform the Frame Range to bake', '%s-%s' % (nuke.root().firstFrame(), nuke.root().lastFrame())))

        frame_range = str(frame_range)

        first_frame = frame_range.split('-')[0]
        last_frame = frame_range.split('-')[1]


        # Get Width & Height
        wNode = selNode.width()
        hNode = selNode.height()


        # Create a CurveTool
        cTool = nuke.nodes.CurveTool()
        cTool.setInput(0, selNode)
        cTool['operation'].setValue('Auto Crop')
        cTool['channels'].setValue('alpha')
        cTool['resetROI'].setValue('True')
        cTool.knob("ROI").setValue( [ 0, 0 , selNode.width() , selNode.height() ] )
        cTool.setInput(0, selNode)


        #Execute CurveTool
        nuke.execute(cTool, int(first_frame), int(last_frame))


        # Create New Crop with data from CurveTool
        nCrop = nuke.nodes.Crop()
        nCrop.knob("box").copyAnimations(cTool.knob("autocropdata").animations())
        nCrop['label'].setValue('AutoCrop from %s' %(selNode.name()))
        nCrop.setInput(0, selNode)
        nCrop.knob('tile_color').setValue(01050)
        nCrop.knob('note_font').setValue('Verdana bold')


        # Create new Tab and Knobs to control the bounding box
        tab = nuke.Tab_Knob('Size Control')
        nCrop.addKnob(tab)
        
        gS = nuke.Double_Knob('genSize',"Proportional Size")
        gS.setRange(0,300)
        nCrop.addKnob(gS)

        div = nuke.Text_Knob("divider","")
        nCrop.addKnob(div)

        lS = nuke.Double_Knob('lSize',"Left")
        lS.setRange(-50,50)
        nCrop.addKnob(lS)

        rS = nuke.Double_Knob('rSize',"Right")
        rS.setRange(-50,50)
        nCrop.addKnob(rS)

        tS = nuke.Double_Knob('tSize',"Top")
        tS.setRange(-50,50)
        nCrop.addKnob(tS)
        
        bS = nuke.Double_Knob('bSize',"Bottom")
        bS.setRange(-50,50)
        nCrop.addKnob(bS)

        c = nuke.Text_Knob('c0', '')
        nCrop.addKnob(c)

        c = nuke.Text_Knob('c1', '', '<font color = "#EF4E3D">Version 1.5')
        nCrop.addKnob(c)

        c = nuke.Text_Knob('c2', '', '<font color = "#EF4E3D">Created by Luciano Cequinel')
        nCrop.addKnob(c)

        c = nuke.Text_Knob('c3', '', '<font color = "#EF4E3D">Check for updates <a href=\"https://www.github.com/CequinaVFX"><font color=#EF4E3D><b>here</a>')
        nCrop.addKnob(c)


        # Set expressions to knobs

        nCrop['genSize'].setValue(30)

        nCrop.knob('box').setExpression('(curve) + ((knob.lSize) + (knob.genSize) *-1)', 0)
        nCrop.knob('box').setExpression('(curve) + ((knob.bSize) + (knob.genSize) *-1)', 1)
        nCrop.knob('box').setExpression('(curve) + (knob.rSize) + (knob.genSize)', 2)
        nCrop.knob('box').setExpression('(curve) + (knob.tSize) + (knob.genSize)', 3)



        # Delete CurveTool
        nuke.delete(cTool)


    else:
        nuke.message('Select one node, please!')




#Add a menu and assign a shortcut
toolbar = nuke.menu('Nodes')
cqnTools = toolbar.addMenu('CQNTools', icon='Modify.png')
cqnTools.addCommand('superAutoCrop', 'superAutoCrop.superAutoCrop()', '[', icon='AutoCrop.png')