##############################################################################
#                                                                            #
# Breakdown Frame Exporter                                                   #
# V 1.0.0                                                                    #
# Release August 01 2020                                                     #
#                                                                            #
# Created by Luciano Cequinel (vimeo.com/cequinavfx)                         #
# to report bugs or suggestions lucianocequinel@gmail.com                    #
#                                                                            #
##############################################################################



'''
To improve
- position of dot
- name of write node, to prevent error message
- to create a section to config some stuffs, like file extension, channels, premult

'''


'''

Just write
import FrameBreakdown
on menu.py
and copy FrameBreakdown.py to .nuke folder

'''


import nuke
import os


def FrameBreakdown():

    selNode = nuke.selectedNodes()

    if len (selNode) == 1:

        selNode = nuke.selectedNode()

        #Get current frame
        curFrame = (nuke.frame())

        folderName = 'bkdown_' + str(curFrame)# + '/'

        #Get current script folder and create a folder called 'frames'
        saveDir = ('/'.join(nuke.root().name().split("/")[0:-1])+'/')

        path, dirs, files = next(os.walk(saveDir))

        if folderName not in dirs:
            saveDir = saveDir + folderName
            os.mkdir(saveDir)
            path, dirs, files = next(os.walk(saveDir))
            file_count = len(files) + 1
        else:
            saveDir = saveDir + folderName
            path, dirs, files = next(os.walk(saveDir))
            file_count = len(files) + 1

        #Create a filename to save
        saveDir = ('%s/%03d_frame_%s_%s.exr' %(saveDir, file_count, curFrame, selNode.name()))
 
        #Get original state of Proxy Mode in Project Settings
        origProxyMode = nuke.root().proxy()
        #Set Proxy Mode to Off for render purpose
        nuke.root()['proxy'].setValue(False)

        #Create a Write node
        nWrite = nuke.createNode('Write')
        nWrite['name'].setValue('WriteFrame')
        nWrite['channels'].setValue('rgba')
        nWrite['file'].setValue (saveDir)
        nWrite['file_type'].setValue ('exr')
        nWrite['create_directories'].setValue(True)

        #Create Dot do mark were you render a frame
        nDot = nuke.createNode('Dot')
        nDot['label'].setValue(folderName)
        nDot['tile_color'].setValue(35)
        nDot['note_font_size'].setValue(10)
        nDot['note_font_color'].setValue(15)
        nDot.setInput(0, selNode)
        nDot.hideControlPanel()

        nWrite.setInput(0, selNode)
        nWrite.hideControlPanel()

        #Execute and Delete the Write Node
        nuke.execute(nWrite, curFrame, curFrame)
        nuke.delete(nWrite)

        #Set Proxy Mode to Original state
        nuke.root()['proxy'].setValue(origProxyMode)
    else:
        nuke.message('Select just one node, dude')


#Add a menu and assign a shortcut
toolbar = nuke.menu('Nodes')
cqnTools = toolbar.addMenu('CequinaTools', 'cqnTools.png')
cqnTools.addCommand('Frame Breakdown', 'FrameBreakdown.FrameBreakdown()', 'F12', icon='Write.png')