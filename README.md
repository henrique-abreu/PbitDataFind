# Pbit Dataset Finder

## Table of contents:

## Description:
The goal of this project was to find in which PowerBi reports (with the extension **Pbit**), certain words would appear. The words correspond to the Dataset that is desired to be found simbolizing that a certain dataset is being used by the report in question. This could have been much simplified, but the goal was to use implementing something and learn in the process :stuck_out_tongue:, with something that was originally tasked to do, in this case using docker and mongodb.

**Note:** The conversion from Pbix to Pbit needs to be done manually unfortunately.

---

### How it works:

The python main.py file, follows the following logic:

- Extraction from the "Reports" folder, the file called "DataModel" that is present in any report and stores it in the "Extract" folder
- It then converts that same file into a valid json and stores it in the "JsonConverted" Folder 
- After that, it tries to insert into a collection on MongoDB, in case the connection is live, otherwise it will store the results in the "Output" folder.

The last step was to be able to run the python code without the need of MongoDB since it's not really a requirement. Nonetheless, the pymongo would still need to be ran from the command line, in order to install it and make it work.

From the root directory of the project:

```
pip install -r ./app/Scripts/requirements.txt 
```

**Files Structure:**
```
C:.
│   .gitignore
│   DatasetFinder.code-workspace
│   docker.yaml
│   Dockerfile
│   instructions.txt
│   README.md
│
└───app
    │   requirements.txt
    │
    ├───data
    │   ├───Extract
    │   │
    │   ├───JsonConverted
    │   │
    │   ├───Output
    │   └───Reports
    │           .gitkeep
    │
    └───Scripts
        │   elements.txt
        │   InOut.py
        │   main.py
        │
        └───__pycache__
                InOut.cpython-311.pyc
                InOut.cpython-312.pyc
```
                
