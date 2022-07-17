bl_info = {
    "name": "Multi-camera Recordnig",
    "author": "Akshay B Bistagond",
    "version": (1, 0),
    "blender": (2, 80, 0),
#    "location": "View3D > Add > Mesh > ",
    "description": "Sets up and records animation from multiple cameras",
    "warning": "",
    "doc_url": "",
    "category": "Render",
}

import bpy
import os
from math import pi
from bpy.props import BoolProperty

cameras = [
    {
        "location":(-6.35,4.545,5),
        "rotation":(62.1,0,234),
        "scale":(1,1,1),
        "name":"cam_Left",
        "suffix":"_Left"
    },
    {
        "location":(6.9,6,4.4),
        "rotation":(67.5,0,133),
        "scale":(1,1,1),
        "name":"cam_Right",
        "suffix":"_Right"
    },
    {
        "location":(0,-8,3.5),
        "rotation":(72,0,1.54),
        "scale":(1,1,1),
        "name":"cam_Front",
        "suffix":"_Front"
    },
    {
        "location":(-5.8,-8.3,6.6),
        "rotation":(58.6,0,-40),
        "scale":(1,1,1),
        "name":"cam_Back",
        "suffix":"_Back"
    },
    {
        "location":(7.35,-6.9,5),
        "rotation":(63.6,0,46.7),
        "scale":(1,1,1),
        "name":"cam_Low", 
        "suffix":"_Low"
    }
]

#renderPath = os.path.dirname(bpy.data.filepath)
renderPath = "//"
renderPath = os.path.join(renderPath, "Results/Endres")
print(renderPath)


def get_scene():
    return bpy.context.scene

def setup_env():
    scn = get_scene()
    coll = bpy.data.collections.new("SimulVid")
    scn.collection.children.link(coll)
    for cam in cameras:
        tcam = bpy.data.cameras.new(cam['name'])
        tcam_obj = bpy.data.objects.new(cam['name'], tcam)
        tcam_obj.location = cam['location']
        tcam_obj.rotation_euler =  tuple(map(lambda x: pi*x/180 ,cam['rotation'] ))
        coll.objects.link(tcam_obj)
        scn.camera = tcam_obj
        
        

def destroy_setup():
    for x in bpy.data.collections['SimulVid'].objects.items():
        bpy.data.objects.remove(x[1])
    bpy.data.collections.remove(bpy.data.collections['SimulVid'])
    

def clear_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    for x in bpy.data.cameras.items():
        bpy.data.cameras.remove(x[1])
    for x in bpy.data.collections.items():
        bpy.data.collections.remove(x[1])
    
        
        
def record_all_cam():
    scn = get_scene()
    scn.render.use_multiview = True
    scn.render.views_format = 'MULTIVIEW'
    
    front_view = scn.render.views.new("front")
    back_view = scn.render.views.new("back")
    low_view = scn.render.views.new("low")
    
    scn.render.views["left"].camera_suffix = cameras[0]['suffix']
    scn.render.views["right"].camera_suffix = cameras[1]['suffix']
    scn.render.views["front"].camera_suffix = cameras[2]['suffix']
    scn.render.views["back"].camera_suffix = cameras[3]['suffix']
    scn.render.views["low"].camera_suffix = cameras[4]['suffix']
    
    scn.render.filepath = renderPath
    scn.render.image_settings.file_format = "FFMPEG"
#    scn.render.image_settings.file_format = "PNG"
    scn.eevee.taa_render_samples = 2
    bpy.ops.render.render(animation=True)
    
    scn.render.views.remove(front_view)
    scn.render.views.remove(back_view)
    scn.render.views.remove(low_view)
    scn.render.use_multiview = False

#clear_scene()    


def setup_scene(context):
    setup_env()
    
def remove_setup(context):
    destroy_setup()

def record_scene(context):
    record_all_cam()
    

class SetupOperator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.setup_operator"
    bl_label = "Setup Cameras"

    def execute(self, context):
        setup_scene(context)
        context.scene.setupDone = not context.scene.setupDone
        return {'FINISHED'}


def menu_func_setup(self, context):
    self.layout.operator(SetupOperator.bl_idname, text=SetupOperator.bl_label)
    
class DestroyOperator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.destroy_operator"
    bl_label = "Remove Setup"

    def execute(self, context):
        remove_setup(context)
        context.scene.setupDone = not context.scene.setupDone
        return {'FINISHED'}


def menu_func_destroy(self, context):
    self.layout.operator(DestroyOperator.bl_idname, text=DestroyOperator.bl_label)
    
class RecordOperator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.record_operator"
    bl_label = "Record Animation"

    def execute(self, context):
        record_scene(context)
        return {'FINISHED'}


def menu_func_rec(self, context):
    self.layout.operator(RecordOperator.bl_idname, text=RecordOperator.bl_label)


class LayoutDemoPanel(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_label = "MultiCam Recording"
    bl_idname = "SCENE_PT_layout"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"

    def draw(self, context):
        layout = self.layout

        scene = context.scene
            
        
        layout.label(text="Setup Cameras:")
        row = layout.row()
        row.scale_y = 1.5
        row.enabled = not context.scene.setupDone
        row.operator("object.setup_operator")
        
        layout.label(text="Remove Setup:")
        row = layout.row()
        row.scale_y = 1.5
        row.enabled = context.scene.setupDone
        row.operator("object.destroy_operator")
        
        
        layout.label(text="Recording Window:")

        row = layout.row()
        row.prop(scene, "frame_start")
        row.prop(scene, "frame_end")

        layout.label(text="Output Path:")

        row = layout.row()
        row.prop(scene, "conf_path")

        
        layout.label(text="Record Animation:")
        row = layout.row()
        row.scale_y = 1.5
        row.enabled = context.scene.setupDone
        row.operator("object.record_operator")


def register():
    bpy.types.Scene.setupDone = BoolProperty(name='setupDone', default = False)
    bpy.utils.register_class(SetupOperator)
    bpy.types.VIEW3D_MT_object.append(menu_func_setup)
    bpy.utils.register_class(RecordOperator)
    bpy.types.VIEW3D_MT_object.append(menu_func_rec)
    bpy.utils.register_class(DestroyOperator)
    bpy.types.VIEW3D_MT_object.append(menu_func_destroy)
    bpy.utils.register_class(LayoutDemoPanel)


def unregister():
    del bpy.types.Scene.setupDone
    bpy.utils.unregister_class(SetupOperator)
    bpy.types.VIEW3D_MT_object.remove(menu_func_setup)
    bpy.utils.unregister_class(RecordOperator)
    bpy.types.VIEW3D_MT_object.remove(menu_func_rec)
    bpy.utils.unregister_class(DestroyOperator)
    bpy.types.VIEW3D_MT_object.remove(menu_func_destroy)
    bpy.utils.unregister_class(LayoutDemoPanel)


if __name__ == "__main__":
    register()
