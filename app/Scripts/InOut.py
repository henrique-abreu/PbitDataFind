# Package Imports
import os
from os import listdir
from os.path import isfile, join
from pymongo.mongo_client import MongoClient
from pymongo.errors import ConnectionFailure


def check_mongodb_connection():

    # Check if mongodb is running
    for serverName in ("localhost", "mongodb"):
        try:
            client = MongoClient(f'mongodb://{serverName}:27017/', username='admin', password='admin')

            # Use a command to check the server status
            server_info = client.admin.command('serverStatus')

            return client
        
        except ConnectionFailure:
            continue
    
    return None


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
    if os.path.exists(fileFullPath):
        # File exists, clear its contents by opening in write mode and closing
        open(f'{fileFullPath}', 'w').close()
    else:
        # File doesn't exist, create an empty file
        with open(fileFullPath, 'w') as file:
            pass 
    return


def saveResults(fileFullpath, results):

    with open(f'{fileFullpath}', 'w') as file:
        file.write(str(results))
    
    return


def saveResultsMongo(client, collection, data):
    
    # Create Database and Collection
    db = client["Results"] 
    coll = db[f"{collection}"] 

    # Insert Document
    coll.insert_one(data)
    
    # Close Connection
    client.close()
    
    return


def elementToFind(filefullpath):

    with open(filefullpath, 'r') as file:
        data = file.read()
        elements_list = data.split(',')
        elements = [string.strip() for string in elements_list]

    elements_list.clear()

    return elements
