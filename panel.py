import bpy


class Gravity_Rig_Panel(bpy.types.Panel):
    bl_idname = "Gravity_Rig_Panel"
    bl_label= "Gravity Rig"
    bl_category = "Gravity Rig"
    bl_space_type = "VIEW_3D"
    bl_order = 0
    bl_region_type = "UI"


    reference_object_name = None
    def draw(self, context):
        layout = self.layout
        prefs = bpy.context.preferences.addons["GravityRig"].preferences
        box = layout.box()
        row = box.row()
        row.operator("gravityrig.selectreference", text="Select Reference Object")
        box = box.box()
        if (Gravity_Rig_Panel.reference_object_name != None):
            box.label(text=Gravity_Rig_Panel.reference_object_name)
        else:
             box.label(text='Please select a reference object')
        # row.prop(prefs, 'reference_object_name')
        
        row = layout.row()
        row.prop(prefs, 'min_value')

        row = layout.row()
        row.operator("gravityrig.cleanuprig", text="Remove Rig")

        row = layout.row()
        row.operator("gravityrig.generaterig", text="(Re)generate Rig")
        
