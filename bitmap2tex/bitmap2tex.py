import os
import bpy
from bpy_extras import image_utils


class InitProject(bpy.types.Operator):
    """Init Bitmap2Tex project"""
    bl_label = 'Init Project'
    bl_idname = 'bitmap2tex.init_project'

    def execute(self, context):
        bitmap2tex_path = os.path.dirname(__file__)
        bitmap2tex_startup = os.path.join(
            bitmap2tex_path, "./bitmap2tex_startup.blend")
        bpy.ops.wm.read_homefile(filepath=bitmap2tex_startup, load_ui=True)
        # enable addon
        return {'FINISHED'}


class EditStartup(bpy.types.Operator):
    """Edit Bitmap2Tex startup file"""
    bl_label = 'Edit Startup'
    bl_idname = 'bitmap2tex.edit_startup'

    def execute(self, context):
        bitmap2tex_path = os.path.dirname(__file__)
        bitmap2tex_startup = os.path.join(
            bitmap2tex_path, "./bitmap2tex_startup.blend")
        bpy.ops.wm.open_mainfile(filepath=bitmap2tex_startup, load_ui=True)
        # enable addon
        return {'FINISHED'}


class TexGen(bpy.types.Operator):
    """Texture Generate"""
    bl_label = "Texture generate"
    bl_idname = "bitmap2tex.tex_gen"
    image_type = {
        'PNG': "png",
        'JPEG': "jpeg",
        'TIFF': "tiff"
    }
    tex_name_map = {
        "AO": "ao",
        "Bump": "bump",
        "Albedo": "alb",
        "Normal": "nor",
        "Displacement": "disp",
        "Roughness": "rou"
    }

    def execute(self, context):
        if bpy.data.filepath == "":            
            self.report({'INFO'}, "save file first!")
            return {"FINISHED"}
        # render
        bpy.ops.render.render()
        # rename and get tex_output_files
        comp_nodes = context.scene.node_tree.nodes
        bitmap_image = comp_nodes.get("Bitmap").image
        if not bitmap_image:
            self.report({'INFO'}, "Bitmap node'image is null")
            return {"FINISHED"}
        bitmap_name = bitmap_image.name
        tex_output_node = comp_nodes.get("Bitmap2Tex Output")
        self.tex_output_files = {}  # {name, path}
        base_path = bpy.path.abspath(tex_output_node.base_path)
        for slot in tex_output_node.file_slots:
            file_format = TexGen.image_type.get(slot.format.file_format)
            tex_name = TexGen.tex_name_map.get(slot.path)
            tex_path = f"{base_path}/{slot.path}{bpy.context.scene.frame_current:0>4d}.{file_format}"
            if tex_name is not None:    # rename
                tex_real_path = f"{base_path}/{bitmap_name}_{tex_name}.{file_format}"
                os.rename(tex_path, tex_real_path)
                tex_path = tex_real_path
            self.tex_output_files[slot.path] = tex_path
        # load image in Inage Editor
        # self.tex_output_image = {}  # {name, image}
        self.tex_output_image = {node_name: image_utils.load_image(tex_path, tex_path, check_existing=True, force_reload=True)
                                 for node_name, tex_path in self.tex_output_files.items()}
        # load image in material
        prev_mat = bpy.data.materials["bitmap2tex_preview"]
        mat_nodes = prev_mat.node_tree.nodes
        image_nodes = [node for node in mat_nodes
                       if node.type == "TEX_IMAGE" and self.tex_output_image.get(node.label)]
        for node in image_nodes:
            node.image = self.tex_output_image[node.label]
        return {"FINISHED"}


class GenNormal(bpy.types.Operator):
    """Bake Normal"""
    bl_label = "Bake normal"
    bl_idname = "bitmap2tex.bake_nor"

    def execute(self, context):
        prev_mat = bpy.data.materials["bitmap2tex_preview"]
        mat_nodes = prev_mat.node_tree.nodes
        mat_nodes.active = mat_nodes["Normal"]
        bpy.ops.object.bake(type='NORMAL',use_selected_to_active=False)
        # bpy.ops.object.bake(type='NORMAL', filepath="/home/ywaby/Documents/myproject/blender/scripts/tex_gen/test.png", width=2048, height=512, save_mode='EXTERNAL', use_automatic_name=True, uv_layer="")                 
        return {"FINISHED"}

class Bitmap2Tex_Tools(bpy.types.Panel):
    bl_space_type = 'NODE_EDITOR'
    bl_label = "Bitmap 2 Tex"
    bl_category = 'bitmap2tex'
    bl_region_type = 'TOOLS'
    bl_idname = 'bitmap2tex.tools'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        layout.operator(InitProject.bl_idname, icon="BLENDER")
        layout.operator(TexGen.bl_idname, icon="TEXTURE")
        layout.operator(GenNormal.bl_idname, icon="TEXTURE")        
        layout.operator(EditStartup.bl_idname, icon="BLENDER")
