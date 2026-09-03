import PyInstaller.__main__
import os
import customtkinter

ctk_path = os.path.dirname(customtkinter.__file__)

PyInstaller.__main__.run([
    'app_gui.py',
    '--onefile',
    '--noconsole',
    '--name=PC_Diagnostic_Rapport',
    f'--add-data={ctk_path}:customtkinter/'
])
