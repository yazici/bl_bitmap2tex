bl_info = {
    "name": "Bitmap2Tex",
    "author": "ywaby",
    "version": (0, 0, 1),
    "blender": (2, 78),
    "description": "generate texture from bitmap",
    "warning": "",
    "wiki_url": "http://github.com/bl_bitmap2tex"
                "Scripts/Add_Mesh/Planes_from_Images",
    "tracker_url": "http://github.com",
    "support": "TESTING",
    "category": "Texture"
}
import bpy
import addon_utils
from . import bitmap2tex
from bpy.app.handlers import persistent

@persistent
def load_handler(arg):
    if not addon_utils.check("bitmap2tex")[1]:
        bpy.app.handlers.load_post.remove(load_handler)
        bpy.ops.wm.addon_enable(module="bitmap2tex")

def register():
    bpy.utils.register_module(__name__)
    bpy.app.handlers.load_post.append(load_handler)
    
def unregister():
    bpy.utils.unregister_module(__name__)
    

if __name__ == "__main__":
    register()


