# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

import os

import bpy

# check if custom preview icons available
try:
	import bpy.utils.previews
except:
	print("MCprep: No custom icons in this blender instance")
	pass

# -----------------------------------------------------------------------------
# ADDON GLOBAL VARIABLES AND INITIAL SETTINGS
# -----------------------------------------------------------------------------

def init():

	# -----------------------------------------------
	# Verbose, use as conf.v
	# Used to print out extra information, set false with distribution
	# -----------------------------------------------
	global dev
	dev = True

	global v
	v = True # $VERBOSE, UI setting

	global vv
	vv = dev # $VERYVERBOSE


	# -----------------------------------------------
	# To display smart warnings and fixes
	# -----------------------------------------------

	global mcprep_warnings
	mcprep_warnings = []
	# examples: is your scene scaled at /10 for mineways?


	# -----------------------------------------------
	# JSON attributes
	# -----------------------------------------------

	# shouldn't load here, just globalize any json data?

	global data
	# import json

	global json_data # mcprep_data.json
	json_data = None # later will load addon information etc

	# if existing json_data_update exists, overwrite it
	global json_path
	json_path = os.path.join(
		os.path.dirname(__file__),
		"MCprep_resources",
		"mcprep_data.json")
	json_path_update = os.path.join(
		os.path.dirname(__file__),
		"MCprep_resources",
		"mcprep_data_update.json")

	# if new update file found from install, replace old one with new
	if os.path.isfile(json_path_update):
		if os.path.isfile(json_path) is True:
			os.remove(json_path)
		os.rename(json_path_update, json_path)

	# lazy load json, ie only load it when needed (util function defined)

	# -----------------------------------------------
	# For preview icons
	# -----------------------------------------------

	global use_icons
	use_icons = True
	global preview_collections
	preview_collections = {}


	# -----------------------------------------------
	# For initializing the custom icons
	# -----------------------------------------------
	icons_init()


	# -----------------------------------------------
	# For cross-addon lists
	# -----------------------------------------------
	global skin_list
	skin_list = [] # each is: [ basename, path ]

	global rig_categories
	rig_categories = [] # simple list of directory names


# -----------------------------------------------------------------------------
# ICONS INIT
# -----------------------------------------------------------------------------


def icons_init():
	# start with custom icons
	# put into a try statement in case older blender version!
	global preview_collections
	global v

	collection_sets = ["main", "skins", "mobs", "blocks", "items"]

	try:
		for iconset in collection_sets:
			preview_collections[iconset] = bpy.utils.previews.new()

		script_path = bpy.path.abspath(os.path.dirname(__file__))
		icons_dir = os.path.join(script_path,'icons')
		preview_collections["main"].load(
			"crafting_icon",
			os.path.join(icons_dir, "crafting_icon.png"),
			'IMAGE')
		preview_collections["main"].load(
			"grass_icon",
			os.path.join(icons_dir, "grass_icon.png"),
			'IMAGE')
		preview_collections["main"].load(
			"spawner_icon",
			os.path.join(icons_dir, "spawner_icon.png"),
			'IMAGE')
		preview_collections["main"].load(
			"sword_icon",
			os.path.join(icons_dir, "sword_icon.png"),
			'IMAGE')
	except Exception as e:
		log("Old verison of blender, no custom icons available")
		log("\t"+str(e))
		global use_icons
		use_icons = False
		for iconset in collection_sets:
			preview_collections[iconset] = ""


def log(statement, vv_only=False):
	"""General purpose simple logging function."""
	global v
	global vv
	if vv_only:
		if vv:
			print(statement)
	elif v:
		print(statement)


# -----------------------------------------------------------------------------
# GLOBAL REGISTRATOR INIT
# -----------------------------------------------------------------------------


def register():
	init()


def unregister():
	global preview_collections
	if use_icons:
		for pcoll in preview_collections.values():
			try:
				bpy.utils.previews.remove(pcoll)
			except:
				log('Issue clearing preview set '+str(pcoll))
	preview_collections.clear()

	global json_data
	json_data = None  # actively clearing out json data for next open
