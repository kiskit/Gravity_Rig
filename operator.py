import bpy

from . makerig import make_gravity_rig



def create_custom_mesh(objname, px, py, pz):
    
    # Define arrays for holding data    
    myvertices = []
    myfaces = []
    myedges = []
    # Create all Vertices

    # vertex 0
    mypoint = [(0.0, -1.0, 0.0)]
    myvertices.extend(mypoint)

    # vertex 1
    mypoint = [(1.0, -1.0, 0.0)]
    myvertices.extend(mypoint)
    myegde=[{0,1}]
    myedges.extend(myegde)
    # vertex 2
    mypoint = [(-1.0, 1.0, 0.0)]
    myvertices.extend(mypoint)
    myegde=[{1,2}]
    myedges.extend(myegde)
    
    # vertex 3
    mypoint = [(1.0, 1.0, 0.0)]
    myvertices.extend(mypoint)
    myegde=[{2,3}]
    myedges.extend(myegde)
    

    # -------------------------------------
    # Create all Faces
    # -------------------------------------
    #myface = [(0, 1, 3, 2)]
    #myfaces.extend(myface)


    mymesh = bpy.data.meshes.new(objname)

    myobject = bpy.data.objects.new(objname, mymesh)
    bpy.context.collection.objects.link(myobject)
    #bpy.context.scene.objects.link(myobject)

    # Generate mesh data
    mymesh.from_pydata(myvertices, myedges, [])
    # Calculate the edges
    mymesh.update(calc_edges=True)

    # Set Location
    myobject.location.x = px
    myobject.location.y = py
    myobject.location.z = pz
    
    return myobject



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
        o = create_custom_mesh("target", 0, 3, 0)
        bpy.context.view_layer.objects.active = o
        print("Active", bpy.context.view_layer.objects.active)
        o = bpy.data.objects["target"]
        bpy.data.objects["target"].select_set(True)
        print("Target", o)
        print("Active", bpy.context.view_layer.objects.active)
        bpy.context.view_layer.objects.active = o
        bpy.ops.object.transform_apply(location = True, scale = True, rotation = True)
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
        make_gravity_rig(SelectReferenceObject.reference_object, target_object, context)
        return{'FINISHED'}

