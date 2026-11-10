bl_info = {
    "name": "Viewport Mode Toggle",
    "author": "Pature",
    "version": (1, 0, 0),
    "blender": (3, 0, 0),
    "location": "3D Viewport > Sidebar (N) > Toggle",
    "description": "One-click toggle between a clean flat/white viewport setup and your original settings",
    "category": "3D View",
}

import bpy

# ---------------------------------------------------------------------------
# Settings to change: (where, property name, new value)
# where = "shading" -> space.shading, "overlay" -> space.overlay
# Properties that don't exist in your Blender version are skipped safely.
# ---------------------------------------------------------------------------
SETTINGS = [
    # Viewport shading
    ("shading", "wireframe_color_type", 'THEME'),
    ("shading", "light", 'FLAT'),
    ("shading", "color_type", 'OBJECT'),
    ("shading", "background_type", 'VIEWPORT'),      # "Custom"
    ("shading", "background_color", (1.0, 1.0, 1.0)),
    ("shading", "show_xray", False),
    ("shading", "show_shadows", False),
    ("shading", "show_cavity", False),

    # Viewport overlays
    ("overlay", "show_floor", False),
    ("overlay", "show_axis_x", False),
    ("overlay", "show_axis_y", False),
    ("overlay", "show_axis_z", False),
    ("overlay", "show_cursor", False),
    ("overlay", "show_stats", False),
    ("overlay", "show_text", False),                 # General info text
    ("overlay", "show_fps", False),                  # Performance (name may vary by version)
    ("overlay", "show_extras", False),
    ("overlay", "show_bones", False),
    ("overlay", "show_relationship_lines", False),
    ("overlay", "show_object_origins", False),
    ("overlay", "show_outline_selected", False),
    ("overlay", "show_wireframes", True),
    ("overlay", "wireframe_threshold", 1.0),
    ("overlay", "wireframe_opacity", 0.825),
    ("overlay", "show_face_orientation", False),
]

# Saved original states, keyed by the 3D viewport's pointer.
# Lives in memory only (cleared when Blender restarts or the addon is reloaded).
_saved_states = {}


def _get_target(space, where):
    return space.shading if where == "shading" else space.overlay


def _to_storable(value):
    # Colors/vectors must be copied, otherwise they'd update live.
    # Enum values are strings, so they must be kept as-is (tuple("STUDIO") would split it into letters).
    if isinstance(value, (str, bool, int, float)):
        return value
    try:
        return tuple(value)
    except TypeError:
        return value


def _is_active(space):
    return space.as_pointer() in _saved_states


def _apply(space):
    snapshot = []
    for where, prop, new_value in SETTINGS:
        target = _get_target(space, where)
        if not hasattr(target, prop):
            continue
        try:
            snapshot.append((where, prop, _to_storable(getattr(target, prop))))
            setattr(target, prop, new_value)
        except Exception as e:
            print(f"[Viewport Toggle] Could not set {where}.{prop}: {e}")
    _saved_states[space.as_pointer()] = snapshot


def _restore(space):
    snapshot = _saved_states.pop(space.as_pointer(), [])
    # Restore in reverse so dependent settings (e.g. background type vs color) settle correctly
    for where, prop, old_value in reversed(snapshot):
        target = _get_target(space, where)
        try:
            setattr(target, prop, old_value)
        except Exception as e:
            print(f"[Viewport Toggle] Could not restore {where}.{prop}: {e}")


class VIEW3D_OT_toggle_viewport_mode(bpy.types.Operator):
    bl_idname = "view3d.toggle_viewport_mode"
    bl_label = "Toggle Viewport Mode"
    bl_description = "Switch between the clean viewport setup and your original settings"

    @classmethod
    def poll(cls, context):
        return context.space_data is not None and context.space_data.type == 'VIEW_3D'

    def execute(self, context):
        space = context.space_data
        if _is_active(space):
            _restore(space)
            self.report({'INFO'}, "Viewport restored to original settings")
        else:
            _apply(space)
            self.report({'INFO'}, "Clean viewport mode enabled")
        return {'FINISHED'}


class VIEW3D_PT_viewport_mode_toggle(bpy.types.Panel):
    bl_label = "Viewport Mode"
    bl_idname = "VIEW3D_PT_viewport_mode_toggle"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Toggle"

    def draw(self, context):
        layout = self.layout
        active = _is_active(context.space_data)
        layout.operator(
            VIEW3D_OT_toggle_viewport_mode.bl_idname,
            text="Restore Original" if active else "Enable Clean Mode",
            icon='LOOP_BACK' if active else 'SHADING_WIRE',
            depress=active,
        )


classes = (
    VIEW3D_OT_toggle_viewport_mode,
    VIEW3D_PT_viewport_mode_toggle,
)

addon_keymaps = []


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    # Optional shortcut: Shift+Alt+Z in the 3D viewport (change or remove if you like)
    wm = bpy.context.window_manager
    if wm.keyconfigs.addon:
        km = wm.keyconfigs.addon.keymaps.new(name="3D View", space_type='VIEW_3D')
        kmi = km.keymap_items.new(
            VIEW3D_OT_toggle_viewport_mode.bl_idname, 'Z', 'PRESS', shift=True, alt=True
        )
        addon_keymaps.append((km, kmi))


def unregister():
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    _saved_states.clear()


if __name__ == "__main__":
    register()
