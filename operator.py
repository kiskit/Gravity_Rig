import bpy

from . makerig import make_gravity_rig, cleanup_previous_rigs
def create_custom_mesh (name, location):
    vertex_list=[
        (-1, 0, 0), #0
        (0, 0, 0), #1
        (1, 1, 0), #2
        (1, 2, 0), #3
        (2, 1, 0), #4
        (2, 2, 0), #5
        (1, -1, 0), #6
    #    (3, 3, 0), #7
    #    (3, 4, 0) #8
        ]
    edges_list = [
        (0, 1),
        (1, 2),
        (2, 3),
        (2, 4),
        (4, 5),
        (1, 6),
    #    (7, 8)
    ]

    mesh = bpy.data.meshes.new(name)  # add the new mesh
    ob = bpy.data.objects.new(mesh.name,mesh)
    col = bpy.data.collections.get("Collection")
    col.objects.link(ob)
    bpy.context.view_layer.objects.active = ob
    
    mesh.from_pydata(vertex_list, edges_list, [])
    ob.location = location
    # ob.transform_apply(location = True, scale = True, rotation = True)
    bpy.data.objects[ob.name].select_set(True)
    return ob
        
class SelectReferenceObject(bpy.types.Operator):
    bl_idname = "gravityrig.selectreference"
    bl_label= "Gravity Rig Select Reference"
    bl_description = "Select Reference Object"
    # global attempt
    reference_object=None

    def execute(self, context):
        SelectReferenceObject.reference_object = bpy.context.view_layer.objects.active
        context.preferences.addons["GravityRig"].preferences.reference_object_name = SelectReferenceObject.reference_object.name
        # o = create_custom_mesh("target", (2, 2, 0))
        return{'FINISHED'}



class MakeRig(bpy.types.Operator):
    bl_idname = "gravityrig.generaterig"
    bl_label= "Gravity Rig"
    bl_description = "Generate Rig Object"
    def execute(self, context):
        if (SelectReferenceObject.reference_object == None):
            return {'CANCELLED'}
        target_object = context.view_layer.objects.active
        if (target_object == None):
            return {'CANCELLED'}
        print("generating rig")
        prefs = context.preferences.addons["GravityRig"].preferences
        print("min value", prefs.min_value)
        make_gravity_rig(SelectReferenceObject.reference_object, target_object, prefs.min_value, context)
        return{'FINISHED'}

class RemoveEverything(bpy.types.Operator):
    bl_idname = "gravityrig.removeeverything"
    bl_label= "Remove Gravity Rig"
    bl_description = "Remove the objects created by gravity rig"
    def execute(self, context):
        target_object = context.view_layer.objects.active
        cleanup_previous_rigs(target_object)
        return{'FINISHED'}
    