import os

import sys

from cx_Freeze import (
	setup,
	Executable
)


build_exe_options = {
	'packages': [
		'os',
		'sys',
		'PIL',
		'time',
		'random',
		'fstring',
		'argparse',
		'collections'
	],
	'excludes': [
		'tkinter'
	],
	'optimize': 2,
	'include_msvcr': True
}

setup(
	name='pim27',
	version='0.1.2',
	description='App for some stuff with images',
	options={
		'build_exe': build_exe_options
	},
	executables=[
		Executable(
			script='main.py',
			base='Console',
			targetName='pim27.exe',
			icon='aqua.ico'
		)
	]
)
