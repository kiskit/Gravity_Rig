import bpy

from . makerig import make_gravity_rig
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
    return ob
    # make empties @ each vertex
    # make bone wherever there is a connection
    # make bone parenting
    # make bone constraints
    # amt = bpy.data.armatures.new("vBones")
    # rig = bpy.data.objects.new('vRig', amt)
    # bpy.context.collection.objects.link(rig)
    # bpy.context.view_layer.objects.active = rig
    # bpy.context.view_layer.update()

    # for v in vertex_list:
    #     empty = bpy.data.objects.new("empty", None)
    #     bpy.context.scene.collection.objects.link( empty )
    #     empty.location = v
    # bpy.ops.object.editmode_toggle()
    # #bones_list = []
    # for i in range(0, len(edges_list)):
    #     bone = amt.edit_bones.new(str(i + 1))
    #     bone.head = vertex_list[edges_list[i][0]]
    #     bone.tail = vertex_list[edges_list[i][1]]
    # #    bones_list[i] = bone
    # for i in range(0, len(bones_list)):
    
    
    #     None
    # bpy.ops.object.editmode_toggle()
        
class SelectReferenceObject(bpy.types.Operator):
    bl_idname = "gravityrig.selectreference"
    bl_label= "Gravity Rig Select Reference"
    bl_description = "Select Reference Object"
    # global attempt
    reference_object=None

    def execute(self, context):
        print("selecting ref object")
        SelectReferenceObject.reference_object = bpy.context.view_layer.objects.active
        print("selected ref object", SelectReferenceObject.reference_object)
        print("Active", bpy.context.view_layer.objects.active)
        o = create_custom_mesh("target", (2, 2, 0))
        bpy.context.view_layer.objects.active = o
        # print("Active", bpy.context.view_layer.objects.active)
        bpy.ops.object.select_all(action='DESELECT')
        # o = bpy.data.objects["target"]
        bpy.data.objects["target"].select_set(True)
        # o.select_set(True)
        # print("Target", o)
        # print("Active", bpy.context.view_layer.objects.active)
        # bpy.context.view_layer.objects.active = o
        # bpy.ops.object.transform_apply(location = True, scale = True, rotation = True)
        return{'FINISHED'}



class MakeRig(bpy.types.Operator):
    bl_idname = "gravityrig.generaterig"
    bl_label= "Gravity Rig Generate Rig"
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

