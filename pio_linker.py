"""
	platform.py - updates cpp links in local Core and UnityTests folders
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

Import("env")
from py_scripts.cpp_linker import copyCPPFiles

def build(source, target, env):
	copyCPPFiles()

env.AddPreAction("buildprog", build)
#env.AddPostAction("buildprog", build)