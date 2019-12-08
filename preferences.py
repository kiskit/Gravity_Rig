import bpy
from bpy.props import (
    StringProperty,
    EnumProperty,
)

# from .utils.addon_updator import AddonUpdatorManager
# from .utils.bl_class_registry import BlClassRegistry
# from .utils import compatibility as compat


# @BlClassRegistry()
# @compat.make_annotations
class GravityRigPreferences(bpy.types.AddonPreferences):
    bl_idname = "GravityRig"
    # falloff = bpy.props.EnumProperty(
    #     name='Falloff',
    #     items=[('LINEAR', 'Linear', "Linear falloff"),
    #            ('QUADRATIC', 'Quadratic', 'Quadratic falloff'),
    #            ],
    #     default='LINEAR',
    # )
    
    reference_object_name = bpy.props.StringProperty(
        name="Reference Object"
    )
    min_value = bpy.props.FloatProperty(
        name='Min Value',
        default=0.1,
        min=0.0,
        max=1.0,
        step=0.1,
    )

    # color = bpy.props.FloatVectorProperty(
    #     name='Color',
    #     default=(1.0, 1.0, 1.0),
    #     min=0.0,
    #     max=1.0,
    #     subtype='COLOR_GAMMA',
    #     size=3
    # )
    # color_shadow = bpy.props.FloatVectorProperty(
    #     name='Shadow Color',
    #     default=(0.0, 0.0, 0.0, 0.0),
    #     min=0.0,
    #     max=1.0,
    #     subtype='COLOR_GAMMA',
    #     size=4
    # )
    # font_size = bpy.props.IntProperty(
    #     name='Font Size',
    #     default=compat.get_user_preferences(bpy.context).ui_styles[0].widget.points,
    #     min=6,
    #     max=48
    # )
    # origin = bpy.props.EnumProperty(
    #     name='Origin',
    #     items=[('REGION', 'Region', "Region.type is 'WINDOW'"),
    #            ('AREA', 'Area', ''),
    #            ('WINDOW', 'Window', '')],
    #     default='REGION',
    # )
    # offset = bpy.props.IntVectorProperty(
    #     name='Offset',
    #     default=(20, 80),
    #     size=2,
    # )
    # display_time = bpy.props.FloatProperty(
    #     name='Display Time',
    #     default=3.0,
    #     min=0.5,
    #     max=10.0,
    #     step=10,
    #     subtype='TIME'
    # )
    # show_last_operator = bpy.props.BoolProperty(
    #     name='Show Last Operator',
    #     default=False,
    # )

    # # for UI
    # category = EnumProperty(
    #     name="Category",
    #     description="Preferences Category",
    #     items=[
    #         ('CONFIG', "Configuration", "Configuration about this add-on"),
    #         ('UPDATE', "Update", "Update this add-on"),
    #     ],
    #     default='CONFIG'
    # )

    # # for add-on updater
    # updater_branch_to_update = EnumProperty(
    #     name="branch",
    #     description="Target branch to update add-on",
    #     items=get_update_candidate_branches
    # )
