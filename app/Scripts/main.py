# Package Imports
# import subprocess, sys
import os
from zipfile import ZipFile
import json

# Files Imports
import InOut


def extracts(targetDirectory):

    reportsDirectory = targetDirectory + "Reports/"
    extractDirectory = targetDirectory + "Extract/"
    failed_reports = []

    files = InOut.allFiles(reportsDirectory)

    for file in files:
        filename = file.split('.')[0]

        try:
            with ZipFile(reportsDirectory + file, 'r') as zObject:  
                zObject.extract("DataModelSchema", path=f"{extractDirectory}") 
            zObject.close()

            os.rename(extractDirectory + "DataModelSchema", extractDirectory + f"{filename}")

        except KeyError:
            failed_reports.append(file)
    
    if len(failed_reports) > 0:
        fileFullPath = targetDirectory + "Output/" + "results_bad.txt"

        # Clear Text File
        InOut.clearTextFile(fileFullPath)

        # Save to Text File
        InOut.saveResults(fileFullPath, failed_reports)

    return


def JsonConverted(targetDirectory):

    extractDirectory = targetDirectory + "Extract/"
    jsonDirectory = targetDirectory + "JsonConverted/"

    files = InOut.allFiles(extractDirectory)

    for file in files:

        with open(extractDirectory + file, 'rb') as extractFile:
            content = extractFile.read()

        with open(jsonDirectory + file + ".json", 'wb') as convertFile:
            convertFile.write(content)

    return


def finder(targetDirectory, elementToFind):

    # Read Json
    results = []

    jsonDirectory = targetDirectory + "JsonConverted/"
    files = InOut.allFiles(jsonDirectory)

    for file in files:
        with open(f"{jsonDirectory + file}", "rb") as f:
            data = json.load(f)
    
        for dataset in data.get("model").get("tables"):
        
            filtered_data = dataset.get("partitions")[0].get("source").get("expression")[1]
            res = [ele for ele in elementToFind if(ele in filtered_data)]
            
            if res:
                results.append([f"Element: {res}", f"Report: {file}"])
                break
    
    if len(results) > 0:
        fileFullPath = targetDirectory + "Output/" + "results.txt"

        # Clear Text File
        InOut.clearTextFile(fileFullPath)

        # Save to Text File
        InOut.saveResults(fileFullPath, results)

    return


if __name__ == "__main__":

    # Working Directory
    targetDirectory = os.getcwd() + "/app/"

    if "DatasetFinder" not in targetDirectory:
        #Because of no docker
        targetDirectory = "/app/"

    # Step 1: Verify Folders
    folders = ['Extract', 'JsonConverted', 'Output']

    for folder in folders:
        InOut.existsFolder(targetDirectory + "data/", folder)

    # Step 2: Unzip Report
    extracts(targetDirectory + "data/")
    
    # Step 3: Convert to Json
    JsonConverted(targetDirectory + "data/")
    
    # Step 4: Report find Dataset
    elements = ["Sprint", "Issues", "Dog"]
    finder(targetDirectory + "data/", elements)
    
