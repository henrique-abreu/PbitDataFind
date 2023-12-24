# Package Imports
import os
from os import listdir
from os.path import isfile, join


def existsFolder(targetDirectory, subfolder):

    desiredFolder = targetDirectory + subfolder
    exists = os.path.exists(desiredFolder)
    
    if exists is False:
        os.mkdir(desiredFolder)

    else:
        files = os.listdir(desiredFolder)

        if len(files) > 0:
            for file in files:
                file_path = os.path.join(desiredFolder, file)
                os.remove(file_path)

    return


def allFiles(targetDirectory):
    new_list = []

    files = [f for f in listdir(targetDirectory) if isfile(join(targetDirectory, f))]

    for file in files:
        if file != ".gitkeep":
            new_list.append(file)
    
    return new_list


def clearTextFile(fileFullPath):
    return open(f'{fileFullPath}', 'w').close()


def saveResults(fileFullpath, results):

    with open(f'{fileFullpath}', 'w') as file:
        for item in results:
            # write each item on a new line
            file.write("%s\n" % item)
    
    return


def elementToFind():

    with open('elements.txt', 'r') as file:
        data = file.read()
        elements = data.split(',')

    return elements
