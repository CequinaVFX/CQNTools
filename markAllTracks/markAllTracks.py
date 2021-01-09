##############################################################################
#
# Mark all tracks (Adapted from www.isaacspiegel.com)
# Version: 1.0.0
# Latest update: December 09 2020
#
# To report bugs or suggestions lucianocequinel@gmail.com
# or linkedin.com/in/cequinel
#
##############################################################################

import nuke


def get_Properties():

	try:

		this_node = nuke.selectedNode()

		if this_node.Class() not in ('Tracker4'):
			nuke.message('Select a Tracker!')
			return

	except:
		nuke.message('Select a Tracker!')
		return

	z = nuke.Panel('Mark all tracks...')

	z.addBooleanCheckBox('Translate', 'True')
	z.addBooleanCheckBox('Rotate', 'True')
	z.addBooleanCheckBox('Scale', 'True')

	result = z.show()

	if result == 0:
		return

	else:
		t_knob_value = z.value('Translate')
		r_knob_value = z.value('Rotate')
		s_knob_value = z.value('Scale')

		tracker_checkboxes(this_node, t_knob_value, r_knob_value, s_knob_value)




def tracker_checkboxes(this_node, t_knob_value, r_knob_value, s_knob_value):

	knob = this_node['tracks']
	num_columns = 31
	col_translate = 6
	col_rotate = 7
	col_scale = 8
	count = 0
	trackers_knob_value = 'All'

	# Put toScript in list:
	trackers = []
	script = this_node['tracks'].toScript()
	trackers.append(script)  # add to list

	# Get number of tracks from list:
	for item in trackers:
		total_tracks = item.count('track ')

	# Check ALL boxes:
	# Math = (True (1) or False (0), 31 columns * track number (0 to infinity)
	# + Translate (6), Rotate (7), or Scale (8))
	if total_tracks >= 1:

		if trackers_knob_value == 'All':

			while count <= int(total_tracks)-1:

				if all([t_knob_value, r_knob_value, s_knob_value]):
					knob.setValue(True, num_columns * count + col_translate)
					knob.setValue(True, num_columns * count + col_rotate)
					knob.setValue(True, num_columns * count + col_scale)

				elif not any([t_knob_value, r_knob_value, s_knob_value]):
					knob.setValue(False, num_columns * count + col_translate)
					knob.setValue(False, num_columns * count + col_rotate)
					knob.setValue(False, num_columns * count + col_scale)


				if t_knob_value is True:
					knob.setValue(True, num_columns * count + col_translate)

				elif t_knob_value is False:
					knob.setValue(False, num_columns * count + col_translate)


				if r_knob_value is True:
					knob.setValue(True, num_columns * count + col_rotate)

				elif r_knob_value is False:
					knob.setValue(False, num_columns * count + col_rotate)


				if s_knob_value is True:
					knob.setValue(True, num_columns * count + col_scale)

				elif s_knob_value is False:
					knob.setValue(False, num_columns * count + col_scale)
				
				count += 1



#Add a menu and assign a shortcut
Toolbar = nuke.menu('Nodes')
cqnTools = Toolbar.addMenu('Tools', 'Modify.png')
cqnTools.addCommand('Mark all tracks', 'markAllTracks.get_Properties()', 'Alt+Shift+C', icon = 'Tracker.png' )