# Package Imports
import subprocess
import os
from os import listdir
from os.path import isfile, join
from zipfile import ZipFile
import json

# Files Imports
import InOut


def extracts(targetDirectory):

    reportsDirectory = targetDirectory + "Reports/"
    extractDirectory = targetDirectory + "Extract/"
    failed_reports = []

    print(reportsDirectory)

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
        # Need to create a PowerShell script
        powershell_script = f'''
            Get-Content "{extractDirectory + file}" -Raw -Encoding unicode |
            Out-File -FilePath "{jsonDirectory + file}.json" -Encoding utf8
        '''

    # Powershell
    subprocess.run(["powershell", "-Command", powershell_script])

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
        
            filtered_data = dataset.get("partitInOutns")[0].get("source").get("expressInOutn")[1]
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
    targetDirectory = os.getcwd() + "/"

    # Step 1: Verify Folders
    folders = ['Extract', 'JsonConverted', 'Output']

    for folder in folders:
        InOut.existsFolder(targetDirectory, folder)

    # Step 2: Unzip Report
    #extracts(targetDirectory)

    # Step 3: Convert to Json
    #JsonConverted(targetDirectory)

    # Step 4: Report find Dataset
    #elements = ["Sprint", "Issues", "Dog"]
    #finder(targetDirectory, elements)
