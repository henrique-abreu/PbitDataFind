# WITH pbi-tools INSTALLED and added to Environment Variables

# File import
from app.Scripts import InOut

# Dependencies
from subprocess import Popen, PIPE
import os
import shutil


# Change rootFolder as needed
rootFolder = os.getcwd()
rootFolder = rootFolder.replace("\\", "/") + "/"

needed_folders = ["failed", "success"]

for folder in needed_folders:
    if not os.path.exists(f"{rootFolder}/{folder}"):
        os.makedirs(f"{rootFolder}/{folder}")


files = InOut.allFiles(rootFolder)
new_files = []

if len(files) > 0:
    for file in files:
        if ".pbix" in file:
            new_files.append(file)

    files.clear()

for file in new_files:

    filename, extension = file.split(".")

    # Extract From pbix
    step = Popen(["pbi-tools", "extract", f"{rootFolder + file}"])
    step.communicate()

    # Convert to pbit
    step = Popen(["pbi-tools", "compile", f"{rootFolder + filename}", "-outPath", f"{rootFolder}/success/{filename}.pbit", "-format", "PBIT", "-overwrite", "True"], 
                 stdout=PIPE, stderr=PIPE)
    
    output, error = step.communicate()

    # Check if error happened
    if "Exception" in str(output):
        shutil.move(f"{rootFolder + file}", f"{rootFolder}/failed/{file}")
        os.remove(f"{rootFolder}/success/{filename}.pbit")

    # Remove folder
    shutil.rmtree(f"{rootFolder + filename}", ignore_errors=True)
