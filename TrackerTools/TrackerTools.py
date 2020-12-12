##############################################################################
#                                                                            #
# Tracker Tools      			                                             #
# V 1.0                                                                      #
# Release September 02 2020                                                  #
#                                                                            #
# Created by Luciano Cequinel (vimeo.com/cequinavfx)                         #
# to report bugs or suggestions lucianocequinel@gmail.com                    #
#                                                                            #
##############################################################################


'''

Just write
import TrackerTools
on menu.py
and copy TrackerTools.py to .nuke folder

See ref_menu.py as reference.

'''

import nuke, operator


#Color Nodes
cyan = "00FFFFFF"
magenta = "FF00FFFF"


def Tk2Roto_Linked():
	#Get Input
	node = nuke.selectedNode()

	if node.Class() not in ('Tracker4'):
	    nuke.message('Unsupported node type. Selected Node must be a Tracker')    
	else:
		#Get Values from Tracker
		t = str(node.name() + '.translate')
		r = str(node.name() + '.rotate')
		s = str(node.name() + '.scale')
		c = str(node.name() + '.center')
		ref = str(node.name() + '.reference_frame')

		#Create Roto Node linked by Expression
		newRoto = nuke.createNode('Roto')
		newRoto.setName('Roto_Linked_to_' + node.name() + '_')
		newRoto['translate'].setExpression(t)
		newRoto['rotate'].setExpression(r)
		newRoto['scale'].setExpression(s)
		newRoto['center'].setExpression(c)
		newRoto.setInput(0, None)
		newRoto['tile_color'].setValue( int(cyan, 16) )
		newRoto['gl_color'].setValue( int(cyan, 16) )
		newRoto["xpos"].setValue(node["xpos"].getValue()+50)
		newRoto["ypos"].setValue(node["ypos"].getValue()+50)
		tab = nuke.Tab_Knob('Tracker Info')
		newRoto.addKnob(tab)
		tk = nuke.Int_Knob('reff',"Reference Frame")
		newRoto.addKnob(tk)
		newRoto['reff'].setExpression(ref)
		newRoto['label'].setValue('Reference Frame: [value knob.reff]')
		#newRoto.hideControlPanel()


def Tk2Roto_Baked():
	#Get Input
	node = nuke.selectedNode()

	#Get Frame Range
	fRange = nuke.FrameRange('%s-%s' % (nuke.root().firstFrame(), nuke.root().lastFrame()))

	if node.Class() not in ('Tracker4'):
		nuke.message('Unsupported node type. Selected Node must be a Tracker')    
	else:
		#Change Transform to Match Move just to get the right infos
		orgTransform = str(node['transform'].getValue())
		node['transform'].setValue('match-move')

		newRoto = nuke.createNode('Roto')
		newRoto.setName('Roto_From_' + node.name() + '_')
		newRoto['translate'].setAnimated()
		newRoto['rotate'].setAnimated()
		newRoto['scale'].setAnimated()
		newRoto['center'].setAnimated()

		task = nuke.ProgressTask( 'Creating Roto' )
		task.setMessage( 'Creating: ' + newRoto.name() )      
		for n in fRange:
			task.setProgress( int( float(n)/fRange.last() * 100 ) )

			#Get Translate
			newRoto.knob( 'translate').setValueAt( node.knob( 'translate' ).getValueAt(n)[0] , n, 0)
			newRoto.knob( 'translate').setValueAt( node.knob( 'translate' ).getValueAt(n)[1] , n, 1)
			#Get Rotate
			newRoto.knob( 'rotate').setValueAt( node.knob( 'rotate' ).getValueAt(n) , n)
			#Get Scale
			newRoto.knob( 'scale').setValueAt( node.knob( 'scale' ).getValueAt(n) , n)
			#Get Center
			newRoto.knob( 'center').setValueAt( node.knob( 'center' ).getValueAt(n)[0] , n, 0)
			newRoto.knob( 'center').setValueAt( node.knob( 'center' ).getValueAt(n)[1] , n, 1)
			# Cosmetics 
			newRoto.setInput(0, None)
			newRoto['tile_color'].setValue( int(cyan, 16) )
			newRoto['gl_color'].setValue( int(cyan, 16) )
			newRoto["xpos"].setValue(node["xpos"].getValue()+50)
			newRoto["ypos"].setValue(node["ypos"].getValue()+50)

		ref = node['reference_frame'].getValue()
		newRoto['label'].setValue('Reference Frame: %s' %(ref))


		#Change back to Original Transform
		node['transform'].setValue(orgTransform)



def Tk2Transform_Linked():
	#Get Input
	node = nuke.selectedNode()

	if node.Class() not in ('Tracker4'):
		nuke.message('Unsupported node type. Selected Node must be a Tracker')    
	else:
		#Get Values from Tracker
		t = str(node.name() + '.translate')
		r = str(node.name() + '.rotate')
		s = str(node.name() + '.scale')
		c = str(node.name() + '.center')
		ref = str(node.name() + '.reference_frame')

		#Create Transform Node linked by Expression
		newTransform = nuke.createNode('Transform')
		newTransform.setName('Transform_Linked_to_' + node.name() + '_')
		newTransform['translate'].setExpression(t)
		newTransform['rotate'].setExpression(r)
		newTransform['scale'].setExpression(s)
		newTransform['center'].setExpression(c)
		newTransform.setInput(0, None)
		newTransform['tile_color'].setValue( int(magenta, 16) )
		newTransform['gl_color'].setValue( int(magenta, 16) )
		newTransform["xpos"].setValue(node["xpos"].getValue()+150)
		newTransform["ypos"].setValue(node["ypos"].getValue()+50)
		tab = nuke.Tab_Knob('Tracker Info')
		newTransform.addKnob(tab)
		tk = nuke.Int_Knob('reff',"Reference Frame")
		newTransform.addKnob(tk)
		newTransform['reff'].setExpression(ref)
		newTransform['label'].setValue('Reference Frame: [value knob.reff]')
		newTransform.hideControlPanel()



def Tk2Transform_Baked():
	#Get Input
	node = nuke.selectedNode()

	#Get Frame Range
	fRange = nuke.FrameRange('%s-%s' % (nuke.root().firstFrame(), nuke.root().lastFrame()))

	if node.Class() not in ('Tracker4'):
		nuke.message('Unsupported node type. Selected Node must be a Tracker')    
	else:
		#Change Transform to Match Move just to get the right infos
		orgTransform = str(node['transform'].getValue())
		node['transform'].setValue('match-move')

		newTransform = nuke.createNode('Transform')
		newTransform.setName('Transform_From_' + node.name() + '_')
		newTransform['translate'].setAnimated()
		newTransform['rotate'].setAnimated()
		newTransform['scale'].setAnimated()
		newTransform['center'].setAnimated()

		task = nuke.ProgressTask( 'Creating Roto' )
		task.setMessage( 'Creating: ' + newTransform.name() )      
		for n in fRange:
			task.setProgress( int( float(n)/fRange.last() * 100 ) )

			#Get Translate
			newTransform.knob( 'translate').setValueAt( node.knob( 'translate' ).getValueAt(n)[0] , n, 0)
			newTransform.knob( 'translate').setValueAt( node.knob( 'translate' ).getValueAt(n)[1] , n, 1)
			#Get Rotate
			newTransform.knob( 'rotate').setValueAt( node.knob( 'rotate' ).getValueAt(n) , n)
			#Get Scale
			newTransform.knob( 'scale').setValueAt( node.knob( 'scale' ).getValueAt(n) , n)
			#Get Center
			newTransform.knob( 'center').setValueAt( node.knob( 'center' ).getValueAt(n)[0] , n, 0)
			newTransform.knob( 'center').setValueAt( node.knob( 'center' ).getValueAt(n)[1] , n, 1)
			# Cosmetics 
			newTransform.setInput(0, None)
			newTransform['tile_color'].setValue( int(magenta, 16) )
			newTransform['gl_color'].setValue( int(magenta, 16) )
			newTransform["xpos"].setValue(node["xpos"].getValue()+50)
			newTransform["ypos"].setValue(node["ypos"].getValue()+50)


		ref = node['reference_frame'].getValue()
		newTransform['label'].setValue('Reference Frame: %s' %(ref))

		#Change back to Original Transform
		node['transform'].setValue(orgTransform)




def hex_color_to_rgb(red, green, blue):
	return int('%02x%02x%02x%02x' % (red*255,green*255,blue*255,255),16)



def StabFromMocha():

	node = nuke.selectedNode()

	curFrame = nuke.frame()

	if node.Class() not in ('CornerPin2D'):
		nuke.message('Unsupported node type. Selected Node must be a CornerPin2D')
	else:
		fRange = nuke.FrameRange('%s-%s' % (nuke.root().firstFrame(), nuke.root().lastFrame()))

		#Stabilize Node
		newStab = nuke.createNode('CornerPin2D')
		newStab.setName('Stab_Baked_From_' + node.name() + '_')
		newStab.setInput(0, None)

		tab = nuke.Tab_Knob('Reference Frame')
		newStab.addKnob(tab)
		fh = nuke.Int_Knob('hold',"Hold at")
		newStab.addKnob(fh)
		newStab['hold'].setValue(curFrame)

		newStab['tile_color'].setValue( int(magenta, 16) )
		newStab['gl_color'].setValue( int(magenta, 16) )
		newStab['label'].setValue('Stabilize \n Ref Frame: [value knob.hold]')
		newStab["xpos"].setValue(node["xpos"].getValue()+150)
		newStab["ypos"].setValue(node["ypos"].getValue()+150)
		newStab.hideControlPanel()

		newStab['to1'].setAnimated()
		newStab['to2'].setAnimated()
		newStab['to3'].setAnimated()
		newStab['to4'].setAnimated()

		newStab['from1'].setAnimated()
		newStab['from2'].setAnimated()
		newStab['from3'].setAnimated()
		newStab['from4'].setAnimated()

		newStab['to1'].setExpression('curve(knob.hold)')
		newStab['to2'].setExpression('curve(knob.hold)')
		newStab['to3'].setExpression('curve(knob.hold)')
		newStab['to4'].setExpression('curve(knob.hold)')

		#Match Move Node
		newMMove = nuke.createNode('CornerPin2D')
		newMMove.setName('MatchMove_From_' + node.name() + '_')
		newMMove['invert'].setValue('True')

		newMMove['to1'].setExpression(newStab.name() + '.to1')
		newMMove['to2'].setExpression(newStab.name() + '.to2')
		newMMove['to3'].setExpression(newStab.name() + '.to3')
		newMMove['to4'].setExpression(newStab.name() + '.to4')

		newMMove['from1'].setAnimated()
		newMMove['from2'].setAnimated()
		newMMove['from3'].setAnimated()
		newMMove['from4'].setAnimated()

		newMMove.setInput(0, newStab)

		newMMove['tile_color'].setValue( int(magenta, 16) )
		newMMove['gl_color'].setValue( int(magenta, 16) )
		newMMove['label'].setValue('MatchMove')
		newMMove["xpos"].setValue(node["xpos"].getValue()+150)
		newMMove["ypos"].setValue(node["ypos"].getValue()+300)
		newMMove.hideControlPanel()


		#Copy animations
		task = nuke.ProgressTask( 'Creating Stab Kit' )
		task.setMessage( 'Creating: ' + newMMove.name() )      
		for n in fRange:
			task.setProgress( int( float(n)/fRange.last() * 100 ) )

			#Stabilize Node
			newStab.knob( 'to1').setValueAt( node.knob( 'to1' ).getValueAt(n)[0] , n, 0)
			newStab.knob( 'to1').setValueAt( node.knob( 'to1' ).getValueAt(n)[1] , n, 1)

			newStab.knob( 'to2').setValueAt( node.knob( 'to2' ).getValueAt(n)[0] , n, 0)
			newStab.knob( 'to2').setValueAt( node.knob( 'to2' ).getValueAt(n)[1] , n, 1)

			newStab.knob( 'to3').setValueAt( node.knob( 'to3' ).getValueAt(n)[0] , n, 0)
			newStab.knob( 'to3').setValueAt( node.knob( 'to3' ).getValueAt(n)[1] , n, 1)

			newStab.knob( 'to4').setValueAt( node.knob( 'to4' ).getValueAt(n)[0] , n, 0)
			newStab.knob( 'to4').setValueAt( node.knob( 'to4' ).getValueAt(n)[1] , n, 1)   

			newStab.knob( 'from1').setValueAt( node.knob( 'to1' ).getValueAt(n)[0] , n, 0)
			newStab.knob( 'from1').setValueAt( node.knob( 'to1' ).getValueAt(n)[1] , n, 1)

			newStab.knob( 'from2').setValueAt( node.knob( 'to2' ).getValueAt(n)[0] , n, 0)
			newStab.knob( 'from2').setValueAt( node.knob( 'to2' ).getValueAt(n)[1] , n, 1)

			newStab.knob( 'from3').setValueAt( node.knob( 'to3' ).getValueAt(n)[0] , n, 0)
			newStab.knob( 'from3').setValueAt( node.knob( 'to3' ).getValueAt(n)[1] , n, 1)

			newStab.knob( 'from4').setValueAt( node.knob( 'to4' ).getValueAt(n)[0] , n, 0)
			newStab.knob( 'from4').setValueAt( node.knob( 'to4' ).getValueAt(n)[1] , n, 1)

			#Match Move Node
			newMMove.knob( 'from1').setValueAt( node.knob( 'to1' ).getValueAt(n)[0] , n, 0)
			newMMove.knob( 'from1').setValueAt( node.knob( 'to1' ).getValueAt(n)[1] , n, 1)

			newMMove.knob( 'from2').setValueAt( node.knob( 'to2' ).getValueAt(n)[0] , n, 0)
			newMMove.knob( 'from2').setValueAt( node.knob( 'to2' ).getValueAt(n)[1] , n, 1)

			newMMove.knob( 'from3').setValueAt( node.knob( 'to3' ).getValueAt(n)[0] , n, 0)
			newMMove.knob( 'from3').setValueAt( node.knob( 'to3' ).getValueAt(n)[1] , n, 1)

			newMMove.knob( 'from4').setValueAt( node.knob( 'to4' ).getValueAt(n)[0] , n, 0)
			newMMove.knob( 'from4').setValueAt( node.knob( 'to4' ).getValueAt(n)[1] , n, 1)



		#Create Backdrop
		newStab['selected'].setValue('True')
		newMMove['selected'].setValue('True')

		selNodes = nuke.selectedNodes()

		positions = [(i.xpos(), i.ypos()) for i in selNodes]
		xPos = sorted(positions, key = operator.itemgetter(0))
		yPos = sorted(positions, key = operator.itemgetter(1))
		xMinMaxPos = (xPos[0][0], xPos[-1:][0][0])
		yMinMaxPos = (yPos[0][1], yPos[-1:][0][1])
		bdColor = hex_color_to_rgb(0.5,0.2,0.2)
		nuke.nodes.BackdropNode(xpos = xMinMaxPos[0]-100, bdwidth = xMinMaxPos[1]-xMinMaxPos[0]+300, ypos = yMinMaxPos[0]-100, bdheight = yMinMaxPos[1]-yMinMaxPos[0]+200, label = '<center>Stab & Paint', note_font_size = 42, tile_color = bdColor)



#Add a menu and assign a shortcut
toolbar = nuke.menu('Nodes')
cqnTools = toolbar.addMenu('CQNTools', 'Modify.png')
cqnTools.addCommand('Tracker Linked to Roto', 'TrackerTools.Tk2Roto_Linked()', icon='Tracker.png')
cqnTools.addCommand('Tracker Baked to Roto', 'TrackerTools.Tk2Roto_Baked()', 'F2', icon='Tracker.png')
cqnTools.addCommand('Tracker Linked to Transform', 'TrackerTools.Tk2Transform_Linked()', icon='Tracker.png')
cqnTools.addCommand('Tracker Baked to Transform', 'TrackerTools.Tk2Transform_Baked()', 'F3', icon='Tracker.png')
cqnTools.addCommand('Stab kit from Mocha', 'TrackerTools.StabFromMocha()', 'alt+c', icon='Tracker.png')