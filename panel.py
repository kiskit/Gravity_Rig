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
        row = layout.row()
        row.operator("gravityrig.selectreference", text="Select Reference Object")
        row = layout.row()
        row.prop(prefs, 'min_value')
        row = layout.row()
        row.prop(prefs, 'falloff')
        row = layout.row()
        row.operator("gravityrig.generaterig", text="Generate Rig")



        # layout.separator()
        # menu = layout.menu(text="mymenu", icon='NONE')
        # for i in self.get_user_preferences(bpy.context).addons:
        #     print(i) 
        # prefs = bpy.context.preferences.addons["GravityRig"].preferences

        # column = layout.column()
        # column.prop(prefs, 'falloff')
        # row = layout.row()
        # row.prop(prefs, 'min_value')
        # row = layout.row()
        # scene = context.scene
        # row.operator("gravityrig.selectreference", text="Select Reference Object")

