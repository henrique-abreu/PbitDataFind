import os

targetDirectory = os.getcwd() + "/"

if "jira" not in targetDirectory:
    targetDirectory = "/jira/"

print(targetDirectory)
