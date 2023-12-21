# Package Imports
import subprocess
import os
from os import listdir
from os.path import isfile, join
from zipfile import ZipFile
import json


def allFiles(targetDirectory):
    new_list = []

    files = [f for f in listdir(targetDirectory) if isfile(join(targetDirectory, f))]

    for file in files:
        if file != ".gitkeep":
            new_list.append(file)
    
    return new_list


def extracts(targetDirectory):

    reportsDirectory = targetDirectory + "Reports/"
    extractDirectory = targetDirectory + "Extract/"
    failed_reports = []

    print(reportsDirectory)

    files = allFiles(reportsDirectory)

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
        clearTextFile(fileFullPath)

        # Save to Text File
        saveResults(fileFullPath, failed_reports)

    return


def JsonConverted(targetDirectory):

    extractDirectory = targetDirectory + "Extract/"
    jsonDirectory = targetDirectory + "JsonConverted/"
    files = allFiles(extractDirectory)

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
    files = allFiles(jsonDirectory)

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
        clearTextFile(fileFullPath)

        # Save to Text File
        saveResults(fileFullPath, results)

    return


def clearTextFile(fileFullPath):
    return open(f'{fileFullPath}', 'w').close()


def saveResults(fileFullpath, results):

    with open(f'{fileFullpath}', 'w') as file:
        for item in results:
            # write each item on a new line
            file.write("%s\n" % item)
    
    return
