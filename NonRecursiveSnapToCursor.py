bl_info = {
    "name": "Snap to cursor but keep children world transformation",
    "blender": (3, 1, 0),
    "category": "Object",
    "author": "Maxime CHAMBEFORT (elmajime)",
    "version": (1, 0),
    "location": "View3D > Object",
    "support": "COMMUNITY",
    "category": "Snap Object",
}


import bpy

class NonRecursiveSnapToCursor(bpy.types.Operator):
    """Non recursive snap to cursor"""
    bl_idname = "object.non_recursive_snap_to_cursor"
    bl_label = "Snap to cursor non recursive"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        current_node = bpy.context.selected_objects[0]

        global_trsfs = {}

        for child in current_node.children:
            global_trsfs[child] = child.matrix_world.copy()
            
        bpy.ops.view3d.snap_selected_to_cursor(use_offset=False)
        
        for node, trsf in global_trsfs.items():
            node.matrix_world = trsf
        
        return {'FINISHED'}
    
    
def menu_func(self, context):
    self.layout.operator(NonRecursiveSnapToCursor.bl_idname)

def register():
    bpy.utils.register_class(NonRecursiveSnapToCursor)
    bpy.types.VIEW3D_MT_object.append(menu_func)

def unregister():
    bpy.utils.unregister_class(NonRecursiveSnapToCursor)

if __name__ == "__main__":
    register()