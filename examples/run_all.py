import os
import subprocess

# Folder where this script is located
folder = os.path.dirname(os.path.abspath(__file__))

for archive in os.listdir(folder):
    if archive.endswith(".py") and archive != os.path.basename(__file__):
        route = os.path.join(folder, archive)
        subprocess.run(["python", route])