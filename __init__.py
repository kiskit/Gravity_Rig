# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name" : "GravityRig",
    "author" : "Nicolas Bellardie",
    "description" : "",
    "blender" : (2, 80, 0),
    "version" : (0, 0, 1),
    "location" : "",
    "warning" : "",
    "category" : "Generic"
}

import bpy

from . panel import Gravity_Rig_Panel
from . operator import SelectReferenceObject, RemoveEverything, MakeRig
from . preferences import GravityRigPreferences

classes = (MakeRig, SelectReferenceObject, Gravity_Rig_Panel, GravityRigPreferences, RemoveEverything)
register, unregister = bpy.utils.register_classes_factory(classes)

