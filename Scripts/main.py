# Package Imports
import subprocess
import os
from os import listdir
from os.path import isfile, join
from zipfile import ZipFile
import json

# Files Imports
import io


def extracts(targetDirectory):

    reportsDirectory = targetDirectory + "Reports/"
    extractDirectory = targetDirectory + "Extract/"
    failed_reports = []

    print(reportsDirectory)

    files = io.allFiles(reportsDirectory)

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
        io.clearTextFile(fileFullPath)

        # Save to Text File
        io.saveResults(fileFullPath, failed_reports)

    return


def JsonConverted(targetDirectory):

    extractDirectory = targetDirectory + "Extract/"
    jsonDirectory = targetDirectory + "JsonConverted/"
    files = io.allFiles(extractDirectory)

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
    files = io.allFiles(jsonDirectory)

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
        io.clearTextFile(fileFullPath)

        # Save to Text File
        io.saveResults(fileFullPath, results)

    return


if __name__ == "__main__":

    # Working Directory
    targetDirectory = os.getcwd() + "/"

    # Step 1: Verify Folders


    # Step 2: Unzip Report
    extracts(targetDirectory)

    # Step 3: Convert to Json
    JsonConverted(targetDirectory)

    # Step 4: Report find Dataset
    elements = ["Sprint", "Issues", "Dog"]
    finder(targetDirectory, elements)


'''
elementToFind = ["A575", "A575_and_KONP_id", "A575_and_KONP_land", "A575_id", "EKBE", "EKBE_id", "EKBE_land", "EKES", "EKES_hist", "EKES_id", 
                     "EKES_land", "EKET", "EKET_id", "EKET_land", "EKKN", "EKKN_id", "EKKN_land", "EKKO", "EKKO_id", "EKKO_land", "EKPO", "EKPO_id", 
                     "EKPO_land", "HAOV_DATE", "KONP", "KONP_id", "LFA1", "LFA1_id", "LFA1_land", "MAKT", "MAKT_land", "MARA", "MARA_id", "MARA_land", 
                     "MVKE", "MVKE_id", "MVKE_land", "OrderFirstCommitDates", "T023T", "T023T_land", "T134T", "T134T_land", "TPTMT", "TPTMT_land", 
                     "TSPAT", "TSPAT_land", "VBAK", "VBAK_id", "VBAK_land", "VBAP", "VBAP_id", "VBAP_land", "ZCSAB", "ZCSAB_land", "ZCTO_TECHHIST", 
                     "ZCTO_TECHHIST_id", "ZCTO_TECHHIST_Land", "ZCTOWEBALIGHT", "ZCTOWEBALIGHT_land", "ZCVAS", "ZCVAS_land", "ZKTP_PRDB", 
                     "ZKTP_PRDB_land", "ZMG_FAMILIET", "ZMG_FAMILIET_land", "ZMG_MODELLT", "ZMG_MODELLT_land", "ZMG_PRAESKATEGT", "ZMG_PRAESKATEGT_land", 
                     "ZMG_SUBKATEGT", "ZMG_SUBKATEGT_land", "ZMTKONFTYP_T", "ZMTKONFTYP_T_land", "ZVLIEF", "ZVLIEF_id", "ZVLIEF_INBOUND", "ZVLIEF_INBOUND_id", 
                     "ZVLIEF_INBOUND_land", "ZVLIEF_land", "ZVMHIER", "ZVMHIER_id", "ZVMHIER_land", "ZVSCARD", "ZVSCARD_id", "ZVSCARD_land", 
                     "PDS_SAPP84CentralPricing", "PDS_SAPP84ProductBOM", "PDS_SAPP84System", "PDS_SAPP84TC", "PDS_SFDCProduct", "PDS_MaterialByQuote", 
           "vwFixSupplyPurchaseOrders", "vwFixSupplyPurchaseOrdersStatusHistory", "vwFixSupplyReschedules", "vwFixSupplyReschedules_ZCTO_TECHHIST", 
           "vwMaterialByQuote", "vwPDS_MaterialByQuote", "vwPDS_SAPP84CentralPricing", "vwPDS_SAPP84ProductBOM", "vwPDS_SAPP84System", "vwPDS_SAPP84TC", 
           "vwPDS_SFDCProduct", "vwSalesforceVolumes"]

'''