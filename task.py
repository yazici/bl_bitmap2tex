import zipfile
import os
import shutil
import glob
from pytk import BaseNode

project_path = os.path.dirname(__file__)
addon_path = os.path.expandvars('$HOME/.config/blender/2.79/scripts/addons')


class package(BaseNode):
    """package prject to release file (zip)"""

    def action(self):
        srcs = glob.glob("./bitmap2tex/**/*.py", recursive=True)
        srcs.append("./bitmap2tex/bitmap2tex_startup.blend")
        with zipfile.ZipFile('bitmap2tex.zip', 'w', zipfile.ZIP_DEFLATED) as tzip:
            for src in srcs:
                tzip.write(src)
            tzip.close()
        if not os.path.exists("./dist"):
            os.mkdir("./dist")
        shutil.move("bitmap2tex.zip", "dist/bitmap2tex.zip")


class link(BaseNode):
    """link project to blender addon path(need sudo)"""

    def action(self):
        src = os.path.join(project_path, "./bitmap2tex")
        link = os.path.abspath(src)
        target = os.path.join(addon_path, "./bitmap2tex")
        if os.path.exists(target):
            os.rmdir(target)
        os.symlink(link, target)
