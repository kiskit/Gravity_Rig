import bpy


class Gravity_Rig_Panel(bpy.types.Panel):
    bl_idname = "Gravity_Rig_Panel"
    bl_label= "Gravity Rig"
    bl_category = "Gravity Rig"
    bl_space_type = "VIEW_3D"
    bl_order = 0
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout
        prefs = bpy.context.preferences.addons["GravityRig"].preferences
        box = layout.box()
        row = box.row()
        row.operator("gravityrig.selectreference", text="Select Reference Object")
        row = box.row()
        row.prop(prefs, 'reference_object_name')
        
        row = layout.row()
        row.prop(prefs, 'min_value')
        # row = layout.row()
        # row.prop(prefs, 'falloff')
        row = layout.row()
        row.operator("gravityrig.generaterig", text="(Re)generate Rig")
        row = layout.row()
        row.operator("gravityrig.removeeverything", text="Remove Rig")

