"""
	cpp_linker.py - updates cpp links in local Core and UnityTests folders
	Copyright (C) 2025 Camren Chraplak

	This program is free software: you can redistribute it and/or modify
	it under the terms of the GNU General Public License as published by
	the Free Software Foundation, either version 3 of the License, or
	(at your option) any later version.

	This program is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU General Public License for more details.

	You should have received a copy of the GNU General Public License
	along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import os

folder: str = ".vscode" # folder to change
fileNames: list[str] = ["c_cpp_properties.json"] # files to change
debug: bool = False # whether to print debug statements to console
mainRun: bool = False # whether main is called here or somewhere else

def printDebug(value: str):
	"""
	Prints to console only if debugging is enabled\n
	:param value	value to print
	"""

	global debug
	if debug:
		print(value)

def printError(value: str, exitScript = True):
	"""
	Prints to console any errors\n
	:param value		value to print
	:param exitScript	whether to exit program or not
	"""

	print("[Err]: " + value)
	if exitScript:
		exit(-1)

def copyProp(newDir: str) -> None:
	"""
	Copies C++ configuration files to new directory\n
	:param newDir	directory of files to change
	"""

	def replaceFiles(dir: str, fileName: str) -> None:
		"""
		Replaces one file in directory
		
		:param dir			directory of files to change\n
		:param fileName		file name to copy
		"""

		global folder

		# prints paths
		controllerPath: str = folder + "/" + fileName
		sourcePath: str = dir + fileName
		printDebug("\tfilename: " + fileName)
		printDebug("\t\tController Path: " + controllerPath)
		printDebug("\t\tSource Path: " + sourcePath)

		# configures files
		if os.path.exists(sourcePath):
			try:
				os.remove(sourcePath)
			except (NotADirectoryError, FileNotFoundError):
				printError("'" + sourcePath + "' isn't a directory")

		try:
			newFile = open(sourcePath, "w")
		except OSError:
			printError("Failed to write " + sourcePath)
		
		try:
			oldFile = open(controllerPath, "r")
		except:
			printError("Failed to read " + controllerPath)
		
		try:
			lines = oldFile.readlines()

			# writes old file to new file
			for line in lines:
				newFile.write(line)
			newFile.close()
		except (BlockingIOError, OSError, ValueError):
			printError("Failed to read lines for " + controllerPath)

	global fileNames, folder

	printDebug("Path: " + newDir)

	indeces = [False] * len(fileNames)

	# looks at source directory files
	for dirs in os.listdir(newDir):

		if dirs.endswith(folder):

			# looks at .vscode files
			folderPath = newDir + "/" + folder
			for files in os.listdir(folderPath):

				# looks at all files that need to be replaced
				index = 0
				for nFiles in fileNames:
					if files == nFiles:
						replaceFiles(folderPath + "/", nFiles)
						indeces[index] = True
					index += 1
	
	# looks if old file doesn't exist
	index = 0
	for indexVal in indeces:
		if indexVal == False:
			folderPath = newDir + "/" + folder
			replaceFiles(folderPath + "/", fileNames[index])
		index += 1
	
	printDebug("")

def copyCPPFiles():
	"""
	Copies cpp config files from Controller to local Core and UnityTests
	"""

	global debug, fileNames, folder, mainRun

	# links 'linker_sources' based on standalone or PlatformIO usage
	if mainRun:
		import linker_sources as lnk
	else:
		import py_scripts.linker_sources as lnk

	# sets debug status
	try:
		lnk.debug
		debug = lnk.debug
	except (NameError, AttributeError):
		print("")
		printError("debug not found, setting False", False)
	
	# prints all files to copy from Controller
	printDebug("\nAll controller paths:")
	for paths in fileNames:
		controllerPath: str = folder + "/" + paths
		printDebug("\t" + controllerPath)
	printDebug("")

	# tries to modify Core directory
	try:
		lnk.coreDir
		copyProp(lnk.coreDir)
	except (NameError, AttributeError):
		printError("coreDir not found", False)

	# tries to modify UnityTests directory
	try:
		lnk.testDir
		copyProp(lnk.testDir)
	except (NameError, AttributeError):
		printError("testDir not found", False)
	
	print("")

if __name__ == '__main__':

	mainRun = True
	copyCPPFiles()